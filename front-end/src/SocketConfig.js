import openSocket from 'socket.io-client';

//const socket = openSocket("https://fs-chess-backend.herokuapp.com", {transports:['websocket']});
const socket = openSocket("http://192.168.1.86:4000", {transports:['websocket']});

export default socket;
