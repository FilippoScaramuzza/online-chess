import React, { useState } from 'react';
import Popup from 'reactjs-popup';
import { Link } from 'react-router-dom';
import axios from 'axios';
import "./css/NewGamePopup.css";

function NewGamePopup() {
	const [open, setOpen] = useState(undefined)
	const [username, setUsername] = useState('')
	const [joinlink, setJoinlink] = useState("")
	const [gameid, setGameId] = useState('')

	const handleSubmit = (e) => {
		e.preventDefault();
		axios.post('http://localhost:4000/creategame', { "username": username }, {
			headers: {
				'Content-Type': 'application/json'
			}
		}).then(res => {
			setJoinlink({ pathname: "/game/" + res.data.id, state: { creatorName: username }});
			setGameId(res.data.id)
		});
	}

	const renderLink = () => {
		if (joinlink === "") return "";
		else return (
			<Link to={joinlink}>
				http://localhost:3000/game/{gameid}
			</Link>
		);
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
				<form onSubmit={handleSubmit} className="ui form">
					<input value={username} onChange={e => { setUsername(e.target.value) }}></input>
					<br /><br />
					<button className="ui button">
						Create
					</button>
					{renderLink()}
				</form>
			</div>

		</Popup >
	);
}

export default NewGamePopup;