import socket
import threading
from googletrans import Translator
import tkinter as tk
from tkinter import scrolledtext, ttk
from ttkthemes import ThemedTk

# Initialize the translator
translator = Translator()

# Supported languages dictionary
languages = {
    'en': 'English', 'hi': 'Hindi', 'es': 'Spanish', 'fr': 'French',
    'de': 'German', 'zh-cn': 'Chinese (Simplified)', 'ar': 'Arabic', 'ja': 'Japanese'
}

# Track users and their language preferences
user_data = {}
clients = {}
user_count = 0

# Function to update the GUI log
def update_log(text):
    log_display.configure(state='normal')
    log_display.insert(tk.END, text + "\n")
    log_display.configure(state='disabled')
    log_display.see(tk.END)

# Function to handle communication between users
def handle_client(client_socket, user_id):
    update_log(f"{user_id} connected.")
    
    if user_id not in user_data:
        client_socket.send("Enter your spoken language code: ".encode('utf-8'))
        src_lang = client_socket.recv(1024).decode('utf-8').strip().lower()
        if src_lang not in languages:
            src_lang = 'en'  # Default to English if invalid
        user_data[user_id] = {'src_lang': src_lang}

    src_lang = user_data[user_id]['src_lang']
    clients[user_id] = client_socket

    while True:
        try:
            msg = client_socket.recv(1024).decode('utf-8')
            if not msg:
                break
            
            update_log(f"{user_id} ({src_lang}) sent: {msg}")

            for other_user_id, other_client_socket in clients.items():
                if other_user_id != user_id:
                    other_src_lang = user_data[other_user_id]['src_lang']
                    try:
                        translated_text = translator.translate(msg, src=src_lang, dest=other_src_lang).text
                        update_log(f"Translated to {other_src_lang}: {translated_text}")
                        response = f"{user_id} ({src_lang}) sent: {msg} | Translated to {other_src_lang}: {translated_text}"
                        other_client_socket.send(response.encode('utf-8'))
                    except Exception as e:
                        error_msg = f"Error in translation: {str(e)}"
                        other_client_socket.send(error_msg.encode('utf-8'))

        except ConnectionResetError:
            break

    update_log(f"{user_id} disconnected.")
    del clients[user_id]
    client_socket.close()

def start_server():
    global user_count
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 5000))
    server.listen(5)
    update_log("Server listening on port 5000")

    while True:
        client_socket, addr = server.accept()
        user_count += 1
        user_id = f"user{user_count}"
        client_handler = threading.Thread(target=handle_client, args=(client_socket, user_id))
        client_handler.start()

# GUI setup
root = ThemedTk(theme="equilux")  # Use a dark theme
root.title("Text-translation")
root.geometry("800x600")

style = ttk.Style()
style.configure("TFrame", background="#2e2e2e")
style.configure("TButton", padding=10, relief="flat", background="#4a7abc", foreground="white")
style.configure("TLabel", background="#2e2e2e", foreground="#ffffff", font=("Helvetica", 12))

main_frame = ttk.Frame(root, padding="20 20 20 20", style="TFrame")
main_frame.pack(fill=tk.BOTH, expand=True)

title_label = ttk.Label(main_frame, text="Text-translation Server Log", font=("Helvetica", 16, "bold"), style="TLabel")
title_label.pack(pady=(0, 20))

log_frame = ttk.Frame(main_frame, style="TFrame")
log_frame.pack(fill=tk.BOTH, expand=True)

log_display = scrolledtext.ScrolledText(log_frame, width=80, height=20, font=("Consolas", 10), 
                                        background="#1e1e1e", foreground="#ffffff", insertbackground="#ffffff")
log_display.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

status_label = ttk.Label(main_frame, text="Server Status: Running", style="TLabel")
status_label.pack(pady=(20, 0))

start_thread = threading.Thread(target=start_server)
start_thread.daemon = True
start_thread.start()

root.mainloop()