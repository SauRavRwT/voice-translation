from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import uuid

app = Flask(__name__)
CORS(app)

# Initialize Flask-SocketIO
socketio = SocketIO(app, cors_allowed_origins="*")

# Dictionary to map user UUIDs to their data
users = {}

# Route to handle user connection
@app.route('/api/connect', methods=['POST'])
def connect_user():
    user_id = str(uuid.uuid4())
    user_data = request.get_json()
    user_name = user_data.get('name', 'Anonymous')

    # Add the user to the dictionary
    users[user_id] = {"id": user_id, "name": user_name}

    # Emit the updated users list to all connected clients
    socketio.emit('update_users', list(users.values()))

    return jsonify({"status": "User connected", "users": list(users.values())})

# WebSocket event to handle personal message delivery
@socketio.on('send_personal_message')
def handle_personal_message(data):
    recipient_id = data['recipient_id']
    message = data['message']
    sender_id = data['sender_id']

    # Broadcast the message to the specific recipient
    emit('receive_message', {'sender': sender_id, 'recipient': recipient_id, 'message': message}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True, host="0.0.0.0", port=8080)