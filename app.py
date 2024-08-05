from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, send, emit
import json
import eventlet

app = Flask(__name__)
app.secret_key = 'your_secret_key'
socketio = SocketIO(app)

# Kullanıcı verileri
users = {
    "Mustafa": "12345",
    "Helin": "12345"
}

# Mesajlar ve kullanıcı ayarları
data = {
    "messages": [],
    "settings": {
        "Mustafa": {},
        "Helin": {}
    }
}

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('chat'))
    return render_template('index.html')

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    return render_template('chat.html', messages=data['messages'], username=username)

@app.route('/settings', methods=['POST'])
def settings():
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    settings = request.form.to_dict()
    data['settings'][username] = settings
    with open('data.json', 'w') as f:
        json.dump(data, f)
    return redirect(url_for('chat'))

@socketio.on('message')
def handle_message(msg):
    username = session['username']
    data['messages'].append({'user': username, 'text': msg})
    with open('data.json', 'w') as f:
        json.dump(data, f)
    send({'user': username, 'text': msg}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)
