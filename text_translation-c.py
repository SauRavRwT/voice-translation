import socket

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 5000))  # Connect to the server at localhost and port 5000

    print("Connected to the translation server.")
    
    preferred_langs_set = False

    while True:
        # Set spoken language if not already set
        if not preferred_langs_set:
            src_lang_prompt = client.recv(1024).decode('utf-8')
            src_lang = input(src_lang_prompt).strip().lower()
            client.send(src_lang.encode('utf-8'))
            preferred_langs_set = True

        # Ask user for the text to send to the chat
        text = input("Enter the message: ")

        # Send the message to the server
        client.send(text.encode('utf-8'))
        
        # Receive and print translated responses from the server
        response = client.recv(1024).decode('utf-8')
        print(response)

if __name__ == "__main__":
    start_client()
