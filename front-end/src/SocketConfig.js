import openSocket from 'socket.io-client';

const socket = openSocket("https://vast-woodland-86915.herokuapp.com", {transports:['websocket']});

export default socket;
