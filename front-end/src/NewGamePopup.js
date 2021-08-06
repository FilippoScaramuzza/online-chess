import React, { useState } from 'react';
import Popup from 'reactjs-popup';
import { Redirect } from 'react-router-dom';
import "./css/NewGamePopup.css";
import socket from './SocketConfig';
import { Form, Checkbox } from 'semantic-ui-react'

function NewGamePopup() {
	const [open, setOpen] = useState(undefined)
	const [username, setUsername] = useState('')
	const [game, setGame] = useState()
	const [redirect, setRedirect] = useState(false)
	const [loading, setLoading] = useState(false)

	const [ai, setAi] = useState('random')

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

		socket.emit("createComputerGame", { username: username, ai: ai })
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

					<Form>
						<Form.Group inline  widths='equal'>
							<Form.Field>
								Selected AI: <b>{ai}</b>
							</Form.Field>
							<Form.Field>
								<Checkbox
									radio
									label='Random Moves'
									name='checkboxRadioGroup'
									value='random'
									checked={ai === 'random'}
									onChange={() => setAi('random')}
								/>
							</Form.Field>
							<Form.Field>
								<Checkbox
									radio
									label='Stockfish 14'
									name='checkboxRadioGroup'
									value='stockfish'
									checked={ai === 'stockfish'}
									onChange={() => setAi('stockfish')}
								/>
							</Form.Field>
							<Form.Field>
								<Checkbox
									radio
									label='Pure Minimax'
									name='checkboxRadioGroup'
									value='minimax'
									checked={ai === 'minimax'}
									onChange={() => setAi('minimax')}
								/>
							</Form.Field>
							<Form.Field>
								<Checkbox
									radio
									label='Minimax and ML'
									name='checkboxRadioGroup'
									value='ml'
									checked={ai === 'ml'}
									onChange={() => setAi('ml')}
								/>
							</Form.Field>
						</Form.Group>
					</Form>
					<br />
					<button className={loading ? "ui loading button" : "ui button"} onClick={e => handleSubmitMultiplayer(e)} disabled={username === "" ? true : false}>
						Create Multiplayer Game
					</button>
					<br className='button-spacing' />
					<br className='button-spacing' />
					<button className={loading ? "ui loading button" : "ui button"} onClick={e => handleSubmitComputer(e)} disabled={username === "" ? true : false}>
						Create Game against Computer
					</button>
					{(redirect) ? <Redirect to={{ pathname: "/game", state: { username: username, game: game } }} /> : ''}
				</form>
			</div>

		</Popup >
	);
}

export default NewGamePopup;