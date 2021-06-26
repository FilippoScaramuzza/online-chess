import React, { useState } from 'react';
import Popup from 'reactjs-popup';
import { Redirect } from 'react-router-dom';
import "./css/NewGamePopup.css";
import socket from './SocketConfig';

function NewGamePopup() {
	const [open, setOpen] = useState(undefined)
	const [username, setUsername] = useState('')
	const [gameid, setGameid] = useState('')
	const [game, setGame] = useState()
	const [redirect, setRedirect] = useState(false)

	const handleSubmit = (e) => {
		e.preventDefault()
		socket.on("connect", () => {
			console.log("Connected socket");
		});

		socket.emit("join", { username: username, id: gameid })

		socket.on("joined", ({ game }) => {
			console.log("JOINED")
			console.log(game)
			setGame(game)
			setRedirect(true)
		})
	}

	return (
		<Popup open={open} onClose={() => setOpen(undefined)} trigger={
			<button className="ui button" >
				Join Game
			</button>
		} modal>
			<div className="modal">
				<div style={{ textAlign: "center" }}></div>
				<form className="ui form">
				<h3 className="ui horizontal divider header">
					Choose a Username
				</h3>
					<input value={username} onChange={e => { setUsername(e.target.value) }}></input>
				<h3 className="ui horizontal divider header">
					Game ID
				</h3>
					<input value={gameid} onChange={e => { setGameid(e.target.value) }}></input>
					<br /><br />
					
					<button className="ui button" onClick={e => handleSubmit(e)}>
						Join
					</button>
					{(redirect) ? <Redirect to={{pathname: "/game", state: {username: username, game: game}}} /> : ''}
				</form>
			</div>

		</Popup >
	);
}

export default NewGamePopup;