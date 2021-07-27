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
	const [loading, setLoading] = useState(false)

	const handleSubmitMultiplayer = (e) => {
		e.preventDefault()

		socket.emit("create", { username: username })
		setLoading(true)
		socket.on("created", ({ game }) => {
			setGame(game)
			setRedirect(true)
			setLoading(false)
		})
	}

	const handleSubmitComputer = (e) => {
		e.preventDefault()

		socket.emit("createComputerGame", { username: username })
		setLoading(true)
		socket.on("createdComputerGame", ({ game }) => {
			setGame(game)
			setRedirect(true)
			setLoading(false)
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
					
					<button className={loading ? "ui loading button" : "ui button"} onClick={e => handleSubmitMultiplayer(e)} disabled={username==="" ? true : false}>
						Create Multiplayer Game
					</button>
					<button className={loading ? "ui loading button" : "ui button"} onClick={e => handleSubmitComputer(e)} disabled={username==="" ? true : false}>
						Create Game against Computer
					</button>
					{(redirect) ? <Redirect to={{pathname: "/game", state: {username: username, game: game}}} /> : ''}
				</form>
			</div>

		</Popup >
	);
}

export default NewGamePopup;