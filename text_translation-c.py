import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, ttk
from ttkthemes import ThemedTk

# Function to handle receiving messages from the server
def receive_messages(client_socket, display_area):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            display_area.configure(state='normal')
            display_area.insert(tk.END, message + "\n")
            display_area.configure(state='disabled')
            display_area.yview(tk.END)
        except ConnectionResetError:
            break

# Function to send messages to the server
def send_message(event=None):
    message = input_field.get()
    if message:
        input_field.delete(0, tk.END)
        client_socket.send(message.encode('utf-8'))

def start_client():
    global client_socket, input_field
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 5000))

    root = ThemedTk(theme="equilux")  # Use a dark theme
    root.title("Text-Translation")
    root.geometry("550x600")

    style = ttk.Style()
    style.configure("TFrame", background="#2e2e2e")
    style.configure("TButton", padding=10, relief="flat", background="#4a7abc", foreground="white")
    style.configure("TEntry", padding=10, fieldbackground="#1e1e1e", foreground="white")

    main_frame = ttk.Frame(root, padding="20 20 20 20", style="TFrame")
    main_frame.pack(fill=tk.BOTH, expand=True)

    title_label = ttk.Label(main_frame, text="Client Side", font=("Helvetica", 16, "bold"), style="TLabel")
    title_label.pack(pady=(0, 20))

    display_area = scrolledtext.ScrolledText(main_frame, width=60, height=20, font=("Consolas", 10), 
                                             background="#1e1e1e", foreground="#ffffff", insertbackground="#ffffff")
    display_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    input_frame = ttk.Frame(main_frame, style="TFrame")
    input_frame.pack(fill=tk.X, pady=(20, 0))

    input_field = ttk.Entry(input_frame, width=40, style="TEntry")
    input_field.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 10))

    send_button = ttk.Button(input_frame, text="Send", command=send_message, style="TButton")
    send_button.pack(side=tk.RIGHT)

    # Bind the Enter key to send messages
    root.bind('<Return>', send_message)

    # Thread to handle receiving messages
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket, display_area))
    receive_thread.daemon = True
    receive_thread.start()

    # Make the window responsive
    for i in range(3):
        root.grid_columnconfigure(i, weight=1)
    for i in range(3):
        root.grid_rowconfigure(i, weight=1)

    root.mainloop()

if __name__ == "__main__":
    start_client()