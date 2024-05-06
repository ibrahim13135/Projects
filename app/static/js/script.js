const socket = io(); // Establish a Socket.IO connection
const messageInput = document.getElementById('message');
const sendButton = document.getElementById('send');
const messagesContainer = document.getElementById('messages');

// Handle sending a message
sendButton.addEventListener('click', () => {
    const message = messageInput.value.trim();
    if (message !== '') {
        socket.emit('newMessage', message);
        messageInput.value = '';
    }
});

// Listen for new messages from the server
socket.on('newMessage', (message) => {
    const messageHTML = `<li>${message.username}: ${message.message}</li>`;
    messagesContainer.innerHTML += messageHTML;
});
