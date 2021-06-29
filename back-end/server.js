const express = require('express');
const app = express();
const cors = require('cors');
const server = require("http").createServer(app);
const io = require("socket.io")(server);
const PORT = 4000;

app.use(cors());
app.use(express.json());

// mongoose.connect("mongodb+srv://dbadmin:3XtVylN6CqpLoEQ0@cluster0.mmdxo.mongodb.net/onlinechess?retryWrites=true&w=majority", 
//                     { useNewUrlParser: true, useUnifiedTopology: true });
// const conn = mongoose.connection;

let games = []

app.get('/', function (req, res) {
	res.send('Server is running correctly')
  })

io.on("connection", (socket) => {

	console.log("Client connected")

	socket.on("create", ({ username }) => {
		let id = Math.random().toString(36).slice(9); 
		games.push({
			id: id,
			players: [username],
			pgn: ""
		})
		socket.join(id)
		console.log(`${username} created a new game: ${games[games.length-1].id}!`)
		socket.emit("created", {game: games[games.length-1]})
	});

	socket.on("fetch", ({id}) => {
		console.log(games)
		games.forEach(game => {
			if(game.id === id) {
				if(![...socket.rooms].indexOf(id) >= 0)
					socket.join(id)
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

	socket.on("move", ({id, from, to, pgn}) => {
		console.log(`Player moved in game ${id}`)
		games.forEach(game => {
			if(game.id === id) {
				game.pgn = pgn
				socket.to(id).emit("moved", {from: from, to: to})
			}
		})
	})

	socket.on("disconnecting", () => {
		
		console.log(socket.rooms)
		socket.rooms.forEach(room => {
			socket.to(room).emit("disconnected")
			console.log("Client disconnected")
		})
	})

});

server.listen(process.env.PORT || PORT, function () {
	console.log("Server is running on Port: " + PORT);
});