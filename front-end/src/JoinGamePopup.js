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
	const [gameNotFound, setGameNotFound] = useState(false)
	const [usernameAlreadyInUse, setUsernameAlreadyInUse] = useState(false)
	const [loading, setLoading] = useState(false)

	const handleSubmit = (e) => {
		e.preventDefault()

		setLoading(true)

		socket.emit("join", { username: username, id: gameid })

		socket.on("joined", ({ game }) => {
			setGame(game)
			setRedirect(true)
			setLoading(false)
		})

		socket.on("gamenotfound", () => {
			setLoading(false)
			setGameNotFound(true)
			setUsernameAlreadyInUse(false)
		})

		socket.on("usernamealreadyinuse", () => {
			setLoading(false)
			setUsernameAlreadyInUse(true)
			setGameNotFound(false)
		})
	}

	return (
		<Popup open={open} onClose={() => setOpen(undefined)} trigger={
			<button className="ui button" >
				Join Game
			</button>
		} modal>
			<div className="modal">
				<form className="ui form">
				<h3 className="ui horizontal divider header">
					Choose a Username
				</h3>
				<div style={{ textAlign: "center", color:'red' }}>{usernameAlreadyInUse ? "Username already choosen!" : ""}</div>
					<input value={username} onChange={e => { setUsername(e.target.value) }}></input>
				<h3 className="ui horizontal divider header">
					Game ID
				</h3>
				<div style={{ textAlign: "center", color:'red' }}>{gameNotFound ? "Game not found, enter a valid ID" : ""}</div>
					<input value={gameid} onChange={e => { setGameid(e.target.value.toLowerCase()) }}></input>
					<br /><br />
					
					<button className={loading ? "ui loading button" : "ui button"} onClick={e => handleSubmit(e)} disabled={username === "" || gameid === "" ? true : false}>
						Join
					</button>
					{(redirect) ? <Redirect to={{pathname: "/game", state: {username: username, game: game}}} /> : ''}
				</form>
			</div>

		</Popup >
	);
}

export default NewGamePopup;