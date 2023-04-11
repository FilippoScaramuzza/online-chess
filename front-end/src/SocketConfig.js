import openSocket from 'socket.io-client';

const socket = openSocket("https://onlinechess-py-backend.onrender.com", {transports: ['websocket']})
//const socket = openSocket("http://localhost:8080")

export default socket;
