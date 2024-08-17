import socket
import threading
from googletrans import Translator

# Initialize the translator
translator = Translator()

# Supported languages dictionary
languages = {
    'en': 'English',
    'hi': 'Hindi',
    'es': 'Spanish',
    'fr': 'French',
    'de': 'German',
    'zh-cn': 'Chinese (Simplified)',
    'ar': 'Arabic',
    'ja': 'Japanese'
}

# Track users and their language preferences
user_data = {}
clients = {}
user_count = 0

# Function to handle communication between users
def handle_client(client_socket, user_id):
    print(f"{user_id} connected.")
    
    # Prompt for source language preferences (spoken language)
    if user_id not in user_data:
        client_socket.send("Enter your spoken language code (e.g., 'hi' for Hindi): ".encode('utf-8'))
        src_lang = client_socket.recv(1024).decode('utf-8').strip().lower()
        if src_lang not in languages:
            src_lang = 'en'  # Default to English if invalid
        user_data[user_id] = {'src_lang': src_lang}

    # Store the user's spoken language
    src_lang = user_data[user_id]['src_lang']

    # Add the client to the clients list
    clients[user_id] = client_socket

    # Handle messages and send translations between users
    while True:
        try:
            msg = client_socket.recv(1024).decode('utf-8')
            if not msg:
                break
            
            print(f"Received message from {user_id}: {msg}")

            # Forward the translated message to the other users
            for other_user_id, other_client_socket in clients.items():
                if other_user_id != user_id:
                    other_src_lang = user_data[other_user_id]['src_lang']
                    try:
                        translated_text = translator.translate(msg, src=src_lang, dest=other_src_lang).text
                        response = f"{user_id} (translated to {languages[other_src_lang]}): {translated_text}"
                        print(f"Server log: {response}")  # Show translated message on the server
                        other_client_socket.send(response.encode('utf-8'))
                    except Exception as e:
                        error_msg = f"Error in translation: {str(e)}"
                        other_client_socket.send(error_msg.encode('utf-8'))

        except ConnectionResetError:
            break

    # Clean up when the client disconnects
    print(f"{user_id} disconnected.")
    del clients[user_id]
    client_socket.close()

# Set up the server
def start_server():
    global user_count
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 5000))  # Bind to all available interfaces at port 5000
    server.listen(5)  # Listen for up to 5 connections
    print("Server listening on port 5000")

    while True:
        client_socket, addr = server.accept()
        user_count += 1
        user_id = f"user{user_count}"
        client_handler = threading.Thread(target=handle_client, args=(client_socket, user_id))
        client_handler.start()

if __name__ == "__main__":
    start_server()
