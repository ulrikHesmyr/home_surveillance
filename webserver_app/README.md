# WebRTC:
Three main APIs:
- Mediastream: Captures video and audio streams
- RTCPeerConnection: Establishes a connection and transfers the media stream
- RTCDataChannel: Transfers arbitrary data

# Infrastructure:
- Frontend:
    - React with typescript
- Backend: 
    - Signalling server for initial connection handshake. This can be built using Node.js and socket.io

## Signalling server
Is responsible for exchanging metadata (like SDP (Session description protocol), ICE candidates)

### Session description protocol
Negotiates between endpoints for exchanging metadata. Uses a set of properties and parameters to be exhanged containing media types, network metrics and other associated properties. This set is called session profile.
