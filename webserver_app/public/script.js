
// Window 1 (Peer A) creates an offer and sends it to the signaling server.
// Window 2 (Peer B) receives the offer from the signaling server, sets it as the remote description, and creates an answer.
// Window 2 sends the answer back to the signaling server.
// Window 1 receives the answer and sets it as the remote description.
// Both peers exchange ICE candidates until a direct connection is established
const socket = io();

const servers = {
    iceServers: [
        { urls: 'stun:stun.l.google.com:19302' },
    ]
};

// Create a new RTCPeerConnection
const peerConnection = new RTCPeerConnection(servers);

// Get local media (video and audio)
navigator.mediaDevices.getUserMedia({ video: true, audio: true })
    .then((stream) => {
        document.querySelector('video').srcObject = stream;

        // Add the local stream tracks to the peer connection
        stream.getTracks().forEach(track => peerConnection.addTrack(track, stream));

        // When we have a new ICE candidate, send it to the other peer
        peerConnection.onicecandidate = (event) => {
            if (event.candidate) {
                socket.emit('candidate', event.candidate);
            }
        };

        // When we receive a remote stream, display it in the remote video element
        peerConnection.ontrack = (event) => {
            const [remoteStream] = event.streams;
            document.querySelector('video#remoteVideo').srcObject = remoteStream;
        };

        // Check if this is Peer A or Peer B
        socket.emit('check-role');

        // Create an offer if this is Peer A
        socket.on('role', (role) => {
            if (role === 'peerA') {
                peerConnection.createOffer()
                    .then(offer => {
                        console.log("Creating offer: ", offer);
                        peerConnection.setLocalDescription(offer);
                        socket.emit('offer', offer);
                    });
            }
        });

        // Handle receiving an offer (Peer B)
        socket.on('offer', (offer) => {
            peerConnection.setRemoteDescription(new RTCSessionDescription(offer))
                .then(() => peerConnection.createAnswer())
                .then((answer) => {
                    console.log("Creating answer: ", answer);
                    peerConnection.setLocalDescription(answer);
                    socket.emit('answer', answer);
                });
        });

        // Handle receiving an answer (Peer A)
        socket.on('answer', (answer) => {
            console.log("Received answer: ", answer);
            peerConnection.setRemoteDescription(new RTCSessionDescription(answer));
        });

        // Handle receiving ICE candidates
        socket.on('candidate', (candidate) => {
            peerConnection.addIceCandidate(new RTCIceCandidate(candidate));
        });

    })
    .catch(error => console.error('Error accessing media devices.', error));
