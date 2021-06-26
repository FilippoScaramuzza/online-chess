import openSocket from 'socket.io-client';

const socket = openSocket("http://vast-woodland-86915.herokuapp.com/", {transports:['websocket']});

export default socket;
