const socket = io();

const servers = {
    iceServers: [
        { urls: 'stun:stun.l.google.com:19302' },
    ]
};


navigator.mediaDevices.getUserMedia({ video: true, audio: true })
    .then((stream) => {
        document.querySelector('video').srcObject = stream;
        
        // Add the stream to the RTCPeerConnection
        const peerConnection = new RTCPeerConnection(servers);

        // Add local stream to connection
        stream.getTracks().forEach(track => peerConnection.addTrack(track, stream));

        // Create offer
        peerConnection.createOffer()
            .then(offer => {
                peerConnection.setLocalDescription(offer);
                socket.emit('offer', offer);
            });

        // Handle answer
        socket.on('answer', (answer) => {
            peerConnection.setRemoteDescription(new RTCSessionDescription(answer));
        });

        // Handle ICE candidates
        peerConnection.onicecandidate = (event) => {
            if (event.candidate) {
                socket.emit('candidate', event.candidate);
            }
        };

        socket.on('candidate', (candidate) => {
            peerConnection.addIceCandidate(new RTCIceCandidate(candidate));
        });

        // Receiving remote stream
        peerConnection.ontrack = (event) => {
            const [remoteStream] = event.streams;
            document.querySelector('video#remoteVideo').srcObject = remoteStream;
        };

    })
    .catch(error => console.error('Error accessing media devices.', error));
