from flask import Flask, render_template, request  
from flask_socketio import SocketIO, send, join_room, leave_room, emit
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)

# In-memory storage
messages = []
users = {}

@app.route('/')
def index():
  return render_template('index.html', messages=messages)

@socketio.on('connect')
def handle_connect():
  users[request.sid] = 'Anônimo'
  send(f"Um usuário entrou no chat.", broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
  username = users.pop(request.sid, 'Anônimo')
  send(f"{username} saiu do chat.", broadcast=True)

@socketio.on('message')
def handle_message(msg):
  timestamp = datetime.now().strftime('%H:%M')
  message = {'username': users.get(request.sid, 'Anônimo'), 'text': msg, 'timestamp': timestamp}
  messages.append(message)
  send(message, broadcast=True)

@socketio.on('set_username')
def set_username(username):
  users[request.sid] = username
  send(f"{username} entrou no chat.", broadcast=True)

if __name__ == '__main__':
  socketio.run(app, debug=True)
