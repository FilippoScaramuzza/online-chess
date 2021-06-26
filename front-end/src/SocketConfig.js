import openSocket from 'socket.io-client';

const socket = openSocket("https://chesson-line.herokuapp.com:4000", {transports:['websocket']});

export default socket;
