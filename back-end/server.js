const express = require('express');
const app = express();
const cors = require('cors');
const mongoose = require('mongoose');
const PORT = 4000;

app.use(cors());
app.use(express.json());

// mongoose.connect("mongodb+srv://dbadmin:3XtVylN6CqpLoEQ0@cluster0.mmdxo.mongodb.net/onlinechess?retryWrites=true&w=majority", 
//                     { useNewUrlParser: true, useUnifiedTopology: true });
// const conn = mongoose.connection;

let games = []

app.post('/creategame', (req, res) => {
	var id = '';
	var characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
	var charactersLength = characters.length;
	for (var i = 0; i < 11; i++) {
		id += characters.charAt(Math.floor(Math.random() *
			charactersLength));
	}
	console.log("User " + req.body.username + " requested a new match");
	games.push({id: id, players: [req.body.username]})
	console.log("Game " + id + " created!")
	res.status(200).json({'id': id});
});

app.get('/game/:id', (req, res) => {
	res.status(200).json(games.filter(game => game.id === req.params.id))
});

app.listen(PORT, function () {
	console.log("Server is running on Port: " + PORT);
});