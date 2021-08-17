import openSocket from 'socket.io-client';

const socket = openSocket("https://onlinechess-py-backend.herokuapp.com", {transports: ['websocket']})
//const socket = openSocket("http://192.168.1.162:8080")

export default socket;
