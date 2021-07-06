import React, { useEffect, useState } from 'react'
import WithMoveValidation from "./integrations/WithMoveValidation";
import { Button, Icon } from 'semantic-ui-react';
import { useLocation } from 'react-router-dom';
import socket from './SocketConfig';
import WinLostPopup from './WinLostPopup';

import './css/ChessBoard.css'

function ChessBoard() {
	const location = useLocation()
	const state = location.state
	const [game, setGame] = useState(state.game)
	const [orientation, setOrientation] = useState()
	const [disconnected, setDisconnected] = useState(false)
	const [resigned, setResigned] = useState(false)
	const [opponentResigned, setOpponentResigned] = useState(false)
	const boardsContainer = {
		display: "flex",
		justifyContent: "space-around",
		alignItems: "center",
		flexWrap: "wrap",
		width: "100vw"
	}

	useEffect(() => {
		socket.emit("fetch", { id: state.game.id })
		socket.on("fetch", ({ game }) => {
			setGame(game)
			console.log(game.pgn)
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
			setOpponentResigned(true)
		})
	}, [state.game.id, state.username]);

	const handleResignClick = () => {
		socket.emit("resign", { id: game.id })
		setResigned(true)
	}

	return (
		<div>
			<div className="game_details">

				{disconnected ? <><p style={{ color: "red" }}>Opponent disconnected...</p><br /></> : ""}
				<WinLostPopup win={opponentResigned ? true : false} lost={resigned ? true : false} resigned={(opponentResigned || resigned) ? true : false} />
				<div>
					<div>
						<span><span style={{ color: "grey" }}>Player 1 (White):</span> {(game.players[0]) ? game.players[0] : "waiting..."}</span><br className="newline"/>
						<span><span style={{ color: "grey" }}>Player 2 (Black):</span> {(game.players[1]) ? game.players[1] : "waiting..."}</span>
					</div>
				</div>
				<br/>
				<br/>
				Gamne ID: <input readOnly value={game.id} />
				<Button animated='vertical' className='resign' style={{ marginLeft: "20px" }} onClick={handleResignClick}>
					<Button.Content hidden>Resign</Button.Content>
					<Button.Content visible>
						<Icon name='flag' />
					</Button.Content>
				</Button>
			</div>
			<div style={boardsContainer} className="chessboard">
				<WithMoveValidation id={game.id} pgn={game.pgn} orientation={orientation} />
			</div>
		</div>
	);
}

export default ChessBoard;