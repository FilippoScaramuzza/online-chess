import openSocket from 'socket.io-client';

const socket = openSocket("https://fs-chess-backend.herokuapp.com", {transports:['websocket']});
//const socket = openSocket("http://localhost:4000", {transports:['websocket']});

export default socket;
