from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit, join_room, leave_room

app = Flask(__name__)
CORS(app)

# Initialize Flask-SocketIO
socketio = SocketIO(app, cors_allowed_origins="*")

# Dictionary to map user emails to their socket IDs and names
users = {}

private_rooms = {}

# Route to handle user connection
@app.route("/api/connect", methods=["POST"])
def connect_user():
    user_data = request.get_json()
    user_name = user_data.get("name", "Anonymous")
    user_email = user_data.get("email")  # Get the email from the frontend

    # Add user to the dictionary with their email as the key
    if user_email not in users:
        users[user_email] = {
            "name": user_name,
            "socket_id": None,
        }  # Initialize socket_id as None

    # Emit the updated users list with emails to all connected clients
    socketio.emit(
        "update_users",
        [
            {"name": user_info["name"], "email": user_email}
            for user_email, user_info in users.items()
        ],
    )

    return jsonify(
        {
            "status": "User connected",
            "users": [
                {"name": user_info["name"], "email": user_email}
                for user_email, user_info in users.items()
            ],
        }
    )


# WebSocket event to handle user joining their own room (identified by their email)
@socketio.on("join")
def on_join(data):
    user_email = data["email"]  # Use email to identify the user
    if user_email in users:
        users[user_email]["socket_id"] = request.sid  # Set the socket ID for the user
        join_room(user_email)  # Join the room based on the email
        print(
            f"{users[user_email]['name']} has joined their room with socket ID: {request.sid}"
        )
    else:
        print(f"User with email {user_email} not found.")


# WebSocket event to handle personal message delivery
@socketio.on("send_personal_message")
def handle_personal_message(data):
    recipient_email = data["recipient_email"]
    sender_name = data["sender_name"]
    message = data["message"]

    # Check if sender's email exists in users
    if data["sender_email"] in users:
        sender_socket_id = users[data["sender_email"]][
            "socket_id"
        ]  # Get sender's socket ID

        # Check if recipient is online and get their socket ID
        recipient_socket_id = users.get(recipient_email, {}).get("socket_id")

        print(
            f"Trying to send message to {recipient_email}."
        )  # Debug: message recipient info
        print(
            f"Recipient socket ID: {recipient_socket_id}"
        )  # Debug: check recipient's socket ID

        if recipient_socket_id:
            # Send the message to the recipient's room (identified by email)
            emit(
                "receive_message",
                {
                    "sender": sender_name,
                    "recipient": recipient_email,
                    "message": message,
                },
                room=recipient_email,
            )
            print(f"Message sent from {sender_name} to {recipient_email}")
        else:
            print(f"Recipient {recipient_email} not found or not connected.")
    else:
        print(f"Sender {data['sender_email']} not connected.")


@socketio.on("join_private_room")
def on_join_private_room(data):
    user_email = data["email"]
    recipient_email = data["recipientEmail"]
    room_name = f"{min(user_email, recipient_email)}_{max(user_email, recipient_email)}"

    join_room(room_name)
    private_rooms[user_email] = room_name
    print(f"{user_email} joined private room: {room_name}")


@socketio.on("leave_private_room")
def on_leave_private_room(data):
    user_email = data["email"]
    recipient_email = data["recipientEmail"]
    room_name = f"{min(user_email, recipient_email)}_{max(user_email, recipient_email)}"

    leave_room(room_name)
    if user_email in private_rooms:
        del private_rooms[user_email]
    print(f"{user_email} left private room: {room_name}")


@socketio.on("send_private_message")
def handle_private_message(data):
    sender = data["sender"]
    recipient = data["recipient"]
    room_name = f"{min(sender, recipient)}_{max(sender, recipient)}"

    emit("private_message", data, room=room_name)
    print(f"Private message sent in room: {room_name}")


# WebSocket event to handle user disconnecting
@socketio.on("disconnect")
def on_disconnect():
    # Remove user from the room and handle cleanup
    for user_email, user_info in list(users.items()):
        if request.sid == user_info.get("socket_id"):
            leave_room(user_email)
            del users[user_email]
            print(f"User {user_info['name']} has disconnected.")
            break


if __name__ == "__main__":
    socketio.run(app, debug=True, host="0.0.0.0", port=8080)

