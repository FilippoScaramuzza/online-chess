import React, { useEffect, useState } from 'react'
import WithMoveValidation from "./integrations/WithMoveValidation";
import { Button, Icon, Input, Dropdown } from 'semantic-ui-react';
import { useLocation } from 'react-router-dom';
import socket from './SocketConfig';
import WinLostPopup from './WinLostPopup';
import Parser from 'html-react-parser';

import './css/ChessBoard.css'

function ChessBoard() {
	const location = useLocation()
	const locState = location.state
	const [game, setGame] = useState(locState.game)
	const [orientation, setOrientation] = useState()
	const [disconnected, setDisconnected] = useState(false)
	const [resigned, setResigned] = useState(false)
	const [opponentResigned, setOpponentResigned] = useState(false)
	const [pieces, setPieces] = useState("neo")
	const [board, setBoard] = useState("green.svg")

	const boardsContainer = {
		display: "flex",
		justifyContent: "space-around",
		alignItems: "center",
		flexWrap: "wrap",
		width: "100vw"
	}

	useEffect(() => {

		socket.emit("fetch", { id: locState.game.id })
		socket.on("fetch", ({ game }) => {
			console.log("RICEVUTO FETCH")
			
			setGame(game)
			setDisconnected(false)
			if (locState.username === game.players[0]) {
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

	}, [locState.game.id, locState.username]);

	const handleResignClick = () => {
		socket.emit("resign", { id: game.id })
		setResigned(true)
	}

	const displayMoves = () => {
		let moves = game.pgn.split(" ")
		let rows = "";
		for (let i = 1; i < moves.length; i += 3) {
			rows += `<tr class="${i % 2 === 0 ? "even-row" : "odd-row"}">` +
				`<td className="index"><span>${moves[i - 1]}</span></td>` +
				`<td className="white"><span>${moves[i]}</span></td>` +
				`<td className="black"><span>${moves[i + 1] ? moves[i + 1] : ""}</span></td>` +
				"</tr>"
		}

		return rows;
	}

	return (
		<div>
			<div className="game_details">

				{disconnected ? <><p style={{ color: "red" }}>Opponent disconnected...</p><br /></> : ""}
				<WinLostPopup win={opponentResigned ? true : false} lost={resigned ? true : false} draw={false} resigned={(opponentResigned || resigned) ? true : false} />
				<div>
					<div>
						<span><span style={{ color: "grey" }}>Player 1 (White):</span> {(game.players[0]) ? game.players[0] : "waiting..."}</span><br className="newline" />
						<span><span style={{ color: "grey" }}>Player 2 (Black):</span> {(game.players[1]) ? game.players[1] : "waiting..."}</span>
					</div>
				</div>
				<br />
				<br />
				<span>Gamne ID:</span>
				<Input readOnly style={{ width: "65px" }} value={game.id} />
				<Dropdown icon="setting" style={{ color: "white", marginLeft: "20px" }} pointing className='link item'>
					<Dropdown.Menu>
						<Dropdown.Item>
							<Dropdown text='Pieces'>
								<Dropdown.Menu>
									<Dropdown.Item onClick={() => { setPieces("classic") }}>Classic</Dropdown.Item>
									<Dropdown.Item onClick={() => { setPieces("light") }}>Light</Dropdown.Item>
									<Dropdown.Item onClick={() => { setPieces("neo") }}>Neo</Dropdown.Item>
									<Dropdown.Item onClick={() => { setPieces("tournament") }}>Tournament</Dropdown.Item>
									<Dropdown.Item onClick={() => { setPieces("newspaper") }}>Newspaper</Dropdown.Item>
									<Dropdown.Item onClick={() => { setPieces("ocean") }}>Ocean</Dropdown.Item>
									<Dropdown.Item onClick={() => { setPieces("8bit") }}>8-Bit</Dropdown.Item>
								</Dropdown.Menu>
							</Dropdown>
							<Dropdown.Divider /><br />
							<Dropdown text='Board'>
								<Dropdown.Menu>
									<Dropdown.Item onClick={() => { setBoard("brown.svg") }}>Brown</Dropdown.Item>
									<Dropdown.Item onClick={() => { setBoard("blue.svg") }}>Blue</Dropdown.Item>
									<Dropdown.Item onClick={() => { setBoard("green.svg") }}>Green</Dropdown.Item>
									<Dropdown.Item onClick={() => { setBoard("wood4.jpg") }}>Wood</Dropdown.Item>
									<Dropdown.Item onClick={() => { setBoard("newspaper.png") }}>Newspaper</Dropdown.Item>
									<Dropdown.Item onClick={() => { setBoard("leather.jpg") }}>Leather</Dropdown.Item>
									<Dropdown.Item onClick={() => { setBoard("metal.jpg") }}>Metal</Dropdown.Item>
								</Dropdown.Menu>
							</Dropdown>
						</Dropdown.Item>
					</Dropdown.Menu>
				</Dropdown>
				<Button animated='vertical' className='resign' style={{ marginLeft: "20px" }} onClick={handleResignClick}>
					<Button.Content hidden>Resign</Button.Content>
					<Button.Content visible>
						<Icon name='flag' />
					</Button.Content>
				</Button><br />
				<Button animated='vertical' className='resign' style={{ marginLeft: "20px" }} onClick={() => socket.emit("fetch", { id: locState.game.id })}>
					<Button.Content hidden>Fetch</Button.Content>
					<Button.Content visible>
						<Icon name='refresh' />
					</Button.Content>
				</Button><br />
				{/* <span>{game.pgn}</span> */}
				<div className="moves-div">
					<br />
					<p style={{ fontSize: "20px", color: "white" }}>Moves:</p>

					<table>
						<tbody>
							{Parser(displayMoves())}
						</tbody>
					</table>
				</div>
			</div>
			<div style={boardsContainer} className="chessboard">
				<WithMoveValidation id={game.id} pgn={game.pgn} orientation={orientation} pieces={pieces} board={board} />
			</div>
		</div>
	);
}

export default ChessBoard;
