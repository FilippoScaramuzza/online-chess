import openSocket from 'socket.io-client';

const socket = openSocket("http://192.168.1.86:4000", {transports:['websocket']});

export default socket;