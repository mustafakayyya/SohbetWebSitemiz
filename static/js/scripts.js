document.addEventListener('DOMContentLoaded', function () {
    var socket = io();

    document.getElementById('messageForm').addEventListener('submit', function (e) {
        e.preventDefault();
        var messageInput = document.getElementById('message');
        socket.send(messageInput.value);
        messageInput.value = '';
    });

    socket.on('message', function (msg) {
        var messagesDiv = document.getElementById('messages');
        var messageElement = document.createElement('div');
        messageElement.className = 'message ' + (msg.user === "{{ username }}" ? 'own-message' : 'other-message');
        messageElement.innerHTML = '<strong>' + msg.user + ':</strong> ' + msg.text;
        messagesDiv.appendChild(messageElement);
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    });

    const themeSelect = document.getElementById('theme');
    themeSelect.addEventListener('change', function () {
        document.body.className = themeSelect.value;
    });
});
