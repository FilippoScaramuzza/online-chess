const mongoose = require('mongoose');
const Schema = mongoose.Schema;

let Game = new Schema({
    id: {type: String},
    players: {
        player1: {type: String},
        player2: {type: String},
    },
    moves: {}
});

module.exports = mongoose.model('Todo', Todo);