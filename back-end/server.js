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

const logServerStatus = () => {
	console.clear()
	console.log(`Current online users: \t${io.engine.clientsCount}`)
	console.log(`Currently on-going games:`)
	console.log(games)
}

io.on("connection", (socket) => {
	logServerStatus();

	socket.on("create", ({ username }) => {
		let id = Math.random().toString(36).slice(9);
		games.push({
			id: id,
			players: [username],
			pgn: "",
			status: 'starting'
		})
		socket.join(id)
		socket.emit("created", { game: games[games.length - 1] })

		logServerStatus();
	});

	socket.on("fetch", ({ id }) => {
		games.forEach(game => {
			if (game.id === id) {
				if (![...socket.rooms].indexOf(id) >= 0)
					socket.join(id)
				socket.to(id).emit("fetch", { game: game })
				socket.emit("fetch", { game: game })
			}
		});

		logServerStatus();
	});

	socket.on("join", ({ username, id }) => {
		let gamefound = false;
		let usernameAlreadyInUse = false;
		games.forEach(game => {
			if (game.id === id) {
				if (game.players[0] === username) {
					usernameAlreadyInUse = true;
				}
				else {
					game.players.push(username);
					game.status = 'ongoing';
					socket.join(id);
					socket.emit("joined", { game: game });
					gamefound = true;
				}
			}
		});

		if (!gamefound) {
			socket.emit("gamenotfound");
		}

		if (usernameAlreadyInUse) {
			socket.emit("usernamealreadyinuse");
		}

		logServerStatus();
	});

	socket.on("move", ({ id, from, to, pgn }) => {
		games.forEach(game => {
			if (game.id === id) {
				game.pgn = pgn
				socket.to(id).emit("moved", { from: from, to: to })
				socket.to(id).emit("fetch", {game: game})
				socket.emit("fetch", {game: game})
			}
		})

		logServerStatus();
	})

	socket.on("resign", ({ id }) => {
		socket.to(id).emit("resigned")
		let index = -1;
		
		games.forEach(game => {
			if (game.id === id) {
				game.status = 'resigned'
				index = games.indexOf(game)
			}
		})
		
		if (index > -1) {
			games.splice(index, 1);
		}

		// array = [2, 9]
		logServerStatus();
	})

	socket.on("checkmate", ({ id }) => {
		socket.to(id).emit("checkmate")
		let index = -1;
		games.forEach(game => {
			if (game.id === id) {
				index = games.indexOf(game)
			}
		})

		if(index > -1) {
			games.splice(index, 1);
		}
		logServerStatus();
	})

	socket.on("disconnecting", () => {
		socket.rooms.forEach(room => {
			socket.to(room).emit("disconnected")
			if (io.sockets.adapter.rooms.get(room).size === 1) {
				let game = games.filter(g => g.id === room)[0]
				let index = games.indexOf(game)
				if (index > -1) {
					games.splice(index, 1);
				}
			}
		})

		logServerStatus();
	})
});

server.listen(process.env.PORT || PORT, function () {
	console.log("Server is running on Port: " + PORT);
	logServerStatus()
});