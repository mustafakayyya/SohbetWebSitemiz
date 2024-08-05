from flask import Flask, render_template, request, redirect, url_for, session
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'

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
    if request.method == 'POST':
        message = request.form['message']
        data['messages'].append({'user': username, 'text': message})
        with open('data.json', 'w') as f:
            json.dump(data, f)
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

if __name__ == '__main__':
    app.run(debug=True)
