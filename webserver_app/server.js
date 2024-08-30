const express = require('express');
const http = require('http');
const socketIo = require('socket.io');

const app = express();
const server = http.createServer(app);
const io = socketIo(server);

let peerAConnected = false;

app.use(express.static('public'));

io.on('connection', (socket) => {
    console.log('A user connected:', socket.id);

    // Determine the role of the connecting peer (Peer A or Peer B)
    socket.on('check-role', () => {
        if (!peerAConnected) {
            peerAConnected = true;
            socket.emit('role', 'peerA');
        } else {
            socket.emit('role', 'peerB');
        }
    });

    // Handle the offer from Peer A
    socket.on('offer', (offer) => {
        socket.broadcast.emit('offer', offer);
    });

    // Handle the answer from Peer B
    socket.on('answer', (answer) => {
        socket.broadcast.emit('answer', answer);
    });

    // Handle ICE candidates
    socket.on('candidate', (candidate) => {
        socket.broadcast.emit('candidate', candidate);
    });

    socket.on('disconnect', () => {
        console.log('User disconnected:', socket.id);
        peerAConnected = false; // Reset for simplicity
    });
});

server.listen(3000, () => {
    console.log('Server is running on port 3000');
});
