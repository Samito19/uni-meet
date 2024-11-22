const config = {
	iceServers: [
		{ urls: "stun:stun.l.google.com:19302" },
		{ urls: "stun:stun.l.google.com:5349" },
		{ urls: "stun:stun1.l.google.com:3478" },
	]
}

const constraints = {
	audio: true,
	video: true,
}

/* Type used to facilitate a perfect negotiation pattern as seen on MDN docs
 * https://developer.mozilla.org/en-US/docs/Web/API/WebRTC_API/Perfect_negotiation*/
const PeerType = Object.freeze({
	POLITE: 0,
	IMPOLITE: 1,
});

const webSocketConn = new WebSocket("ws://localhost:8765");
const pc = new RTCPeerConnection(config);

const localVideo = document.getElementById("localVideo")
const remoteVideo = document.getElementById("remoteVideo")

/* This function allows us to request the user for Camera and Microphone permissions, 
 * and once obtained are they're added as track to the PeerConnection */
async function start() {
	try {
		const stream = await navigator.mediaDevices.getUserMedia(constraints);

		for (const track of stream.getTracks()) {
			pc.addTrack(track, stream);
		}
		localVideo.srcObject = stream;
	} catch (err) {
		console.error("Error at start(): ", err);
	}
}

start();

/* Handle connection open state, this is where the application lets the server know that it wants to get into the matchmaking.*/
webSocketConn.onopen = () => {
	webSocketConn.send("Just connected!");
}

/* Handle incoming messages */
webSocketConn.onmessage = (event) => {
	console.log(event.data);
}

/* Handle inbound video and audio tracks from the other peers */
pc.ontrack = ({ track, streams }) => {
	track.onmute = () => {
		if (remoteVideo.srcObject) {
			return;
		}
		remoteVideo.srcObject = streams[0];
	}
}


