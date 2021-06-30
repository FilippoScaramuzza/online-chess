import React, { useEffect, useState } from 'react'
import WithMoveValidation from "./integrations/WithMoveValidation";
import { Button, Icon } from 'semantic-ui-react';
import { useLocation } from 'react-router-dom';
import socket from './SocketConfig';

function ChessBoard() {
	const location = useLocation()
	const state = location.state
	const [game, setGame] = useState(state.game)
	const [orientation, setOrientation] = useState()
	const [disconnected, setDisconnected] = useState(false)
	const [resigned, setResigned] = useState(false)
	const boardsContainer = {
		display: "flex",
		justifyContent: "space-around",
		alignItems: "center",
		flexWrap: "wrap",
		width: "100vw",
		marginTop: 30,
		marginBottom: 50
	}

	useEffect(() => {
		socket.emit("fetch", { id: state.game.id })
		socket.on("fetch", ({ game }) => {
			setGame(game)
			setDisconnected(false)
			if (state.username === game.players[0]) {
				setOrientation("white")
			}
			else {
				setOrientation("black")
			}
		});
		socket.on("disconnected", () => {
			setDisconnected(true)
		})
		socket.on("resigned", () => {
			setResigned(true)
		})
	}, [state.game.id, state.username]);

	const handleResignClick = () => {
		socket.emit("resign", {id: game.id})
	}

	return (
		<>
			{disconnected ? <><p style={{ color: "red" }}>Opponent disconnected...</p><br /></> : ""}
			{resigned ? <><p style={{ color: "green" }}>Opponent resigned, you won!</p><br /></> : ""}
			{/**/}
			<div style={{
				alignItems: "center",
				flexWrap: "wrap",
				width: "100vw",
				marginBottom: "20px"
			}}>
				<div>
					<span style={{ marginRight: "100px" }}><span style={{ color: "grey" }}>Player 1 (White):</span> {(game.players[0]) ? game.players[0] : "waiting..."}</span>
					<span><span style={{ color: "grey" }}>Player 2 (Black):</span> {(game.players[1]) ? game.players[1] : "waiting..."}</span>
				</div>
			</div>

			Gamne ID: <input readOnly value={game.id} />
			<Button animated='vertical' className='resign' style={{marginLeft: "20px"}} onClick={handleResignClick}>
				<Button.Content hidden>Resign</Button.Content>
				<Button.Content visible>
					<Icon name='flag' />
				</Button.Content>
			</Button>
			<div style={boardsContainer}>
				<WithMoveValidation id={game.id} pgn={game.pgn} orientation={orientation} />
			</div>
		</>
	);
}

export default ChessBoard;