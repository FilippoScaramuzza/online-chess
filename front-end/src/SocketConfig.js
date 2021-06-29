import openSocket from 'socket.io-client';

const socket = openSocket("https://fs-chess-backend.herokuapp.com", {transports:['websocket']});

export default socket;
