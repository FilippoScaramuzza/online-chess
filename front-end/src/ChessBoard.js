import React, { useEffect, useState } from 'react'
import WithMoveValidation from "./integrations/WithMoveValidation";
import { useLocation} from 'react-router-dom';
import socket from './SocketConfig';

function ChessBoard() {
	const  location  = useLocation()
	const state = location.state
	const [game, setGame] = useState(state.game)
	const [orientation, setOrientation] = useState()
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
		socket.emit("fetch", {id: state.game.id})
		socket.on("fetch", ({game})=>{
			setGame(game)
			if(state.username === game.players[0]){
				setOrientation("white")
			}
			else {				
				setOrientation("black")
			}
			console.log(game.id)
		});
	}, [state.game.id, state.username]);

	return (
		<>
			Gamne ID: <input readOnly value={game.id}/>
			<div style={boardsContainer}>
				<WithMoveValidation id={game.id} orientation={orientation} />
			</div>
			<p>Player 1 (White): {(game.players[0]) ? game.players[0] : "waiting..."}</p> <br />
			<p>Player 2 (Black): {(game.players[1]) ? game.players[1] : "waiting..."}</p>
		</>
	);
}

export default ChessBoard;