const express = require('express');
const http = require('http');
const { Server } = require('socket.io');

// Initialize the Express app
const app = express();

// Serve static files (optional, if you have any front-end files to serve)
app.use(express.static('public'));

// Create an HTTP server
const server = http.createServer(app);

// Attach Socket.io to the server
const io = new Server(server);

io.on('connection', (socket) => {
    console.log('a user connected');

    // Handle offer, answer, and candidate events
    socket.on('offer', (offer) => {
        socket.broadcast.emit('offer', offer);
    });

    socket.on('answer', (answer) => {
        socket.broadcast.emit('answer', answer);
    });

    socket.on('candidate', (candidate) => {
        socket.broadcast.emit('candidate', candidate);
    });

    socket.on('disconnect', () => {
        console.log('user disconnected');
    });
});

// Start the server
const PORT = process.env.PORT || 3000;
server.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
