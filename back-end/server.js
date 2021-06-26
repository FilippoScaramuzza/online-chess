const express = require('express');
const app = express();
const cors = require('cors');
const server = require("http").createServer(app);
const io = require("socket.io")(server, {path: '/socket.io-client'});
io.set('transports', ['websocket']);
const PORT = 4000;

app.use(cors());
app.use(express.json());

// mongoose.connect("mongodb+srv://dbadmin:3XtVylN6CqpLoEQ0@cluster0.mmdxo.mongodb.net/onlinechess?retryWrites=true&w=majority", 
//                     { useNewUrlParser: true, useUnifiedTopology: true });
// const conn = mongoose.connection;

let games = []

io.on("connection", (socket) => {

	socket.on("create", ({ username }) => {
		let id = Math.random().toString(36).slice(2); 
		games.push({
			id: id,
			players: [username],
			fen: 'start'
		})
		socket.join(id)
		console.log(`${username} created a new game: ${games[games.length-1].id}!`)
		socket.emit("created", {game: games[games.length-1]})
	});

	socket.on("fetch", ({id}) => {
		console.log(games)
		games.forEach(game => {
			if(game.id === id) {
				socket.to(id).emit("fetch", {game: game})
				socket.emit("fetch", {game: game})
			}
		});
		
	});

	socket.on("join", ({username, id}) => {
		console.log(`${username} wants to join ${id}!`)
		games.forEach(game => {
			if(game.id === id) {
				game.players.push(username);
				socket.join(id)
				socket.emit("joined", {game: game});
			}
		});
	});

	socket.on("move", ({id, from, to}) => {
		console.log(`Player moved in game ${id}`)
		games.forEach(game => {
			if(game.id === id) {
				socket.to(id).emit("moved", {from: from, to: to})
			}
		})
	})

});

server.listen(PORT, function () {
	console.log("Server is running on Port: " + PORT);
});