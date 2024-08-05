import os
import eventlet
eventlet.monkey_patch()

from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
from flask_socketio import SocketIO, send, emit
from werkzeug.utils import secure_filename
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'
socketio = SocketIO(app)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mov', 'avi'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

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

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    if 'file' not in request.files:
        return redirect(url_for('chat'))
    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('chat'))
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        data['messages'].append({'user': username, 'file': filename, 'type': 'file'})
        with open('data.json', 'w') as f:
            json.dump(data, f)
        send({'user': username, 'file': filename, 'type': 'file'}, broadcast=True)
    return redirect(url_for('chat'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@socketio.on('message')
def handle_message(msg):
    username = session['username']
    data['messages'].append({'user': username, 'text': msg, 'type': 'text'})
    with open('data.json', 'w') as f:
        json.dump(data, f)
    send({'user': username, 'text': msg, 'type': 'text'}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)
