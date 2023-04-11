import openSocket from 'socket.io-client';

const socket = openSocket("https://onlinechesspybackend-filipposcaramuzza1999.b4a.run/", {transports: ['websocket']})
//const socket = openSocket("http://localhost:8080")

export default socket;
