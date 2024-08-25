import tkinter as tk
from tkinter import messagebox
import subprocess

# To run the server
def run_server():
    try:
        subprocess.Popen(['python3', 'text_translation-s.py'])
    except Exception as e:
        messagebox.showerror("Error", f"Failed to start server: {e}")

# To run the client
def run_client():
    try:
        subprocess.Popen(['python3', 'text_translation-c.py'])
    except Exception as e:
        messagebox.showerror("Error", f"Failed to start client: {e}")

# To exit the application
def exit_app():
    root.quit()

# Create the main window
root = tk.Tk()
root.title("Text-Translation")

# Set a fixed window size
root.geometry("300x200")
root.resizable(False, False)

# Styling: modern and minimal
root.configure(bg="#2c3e50")
button_style = {
    "bg": "#34495e",
    "fg": "#ecf0f1",
    "font": ("Helvetica", 12),
    "relief": "flat",
    "activebackground": "#1abc9c"
}

# Title label
title_label = tk.Label(root, text="Translation Tool", bg="#2c3e50", fg="#ecf0f1", font=("Helvetica", 14, "bold"))
title_label.pack(pady=20)

# Create and place buttons
btn_run_server = tk.Button(root, text="Run Server", command=run_server, **button_style, width=20, height=2)
btn_run_server.pack(pady=5)

btn_run_client = tk.Button(root, text="Run Client", command=run_client, **button_style, width=20, height=2)
btn_run_client.pack(pady=5)

btn_exit = tk.Button(root, text="Exit", command=exit_app, **button_style, width=20, height=2)
btn_exit.pack(pady=20)

# Run the tkinter main loop
root.mainloop()
