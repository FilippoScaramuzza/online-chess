import React, { useState } from 'react';
import Popup from 'reactjs-popup';
import { Redirect } from 'react-router-dom';
import "./css/NewGamePopup.css";
import socket from './SocketConfig';

function NewGamePopup() {
	const [open, setOpen] = useState(undefined)
	const [username, setUsername] = useState('')
	const [game, setGame] = useState()
	const [redirect, setRedirect] = useState(false)

	const handleSubmit = (e) => {
		e.preventDefault()
		socket.on("connect", () => {
			console.log("Connected socket");
		});

		socket.emit("create", { username: username })

		socket.on("created", ({ game }) => {
			setGame(game)
			setRedirect(true)
		})
	}

	return (
		<Popup open={open} onClose={() => setOpen(undefined)} trigger={
			<button className="ui button" >
				New Game
			</button>
		} modal>
			<div className="modal">
				<h3 className="ui horizontal divider header">
					Choose a Username
				</h3>
				<div style={{ textAlign: "center" }}></div>
				<form className="ui form">
					<input value={username} onChange={e => { setUsername(e.target.value) }}></input>
					<br /><br />
					
					<button className="ui button" onClick={e => handleSubmit(e)} disabled={username==="" ? true : false}>
						Create
					</button>
					{(redirect) ? <Redirect to={{pathname: "/game", state: {username: username, game: game}}} /> : ''}
				</form>
			</div>

		</Popup >
	);
}

export default NewGamePopup;