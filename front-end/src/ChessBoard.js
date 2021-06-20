import React, { useLayoutEffect, useRef, useState } from 'react';
import WithMoveValidation from "./integrations/WithMoveValidation";
import { useParams } from "react-router-dom";
import axios from 'axios';

function ChessBoard() {

	const [game, setGame] = useState(undefined);

	const firstUpdate = useRef(true);

	useLayoutEffect(() => {
		if(firstUpdate.current) {
			firstUpdate.current = false;
			console.log("mounted");
			fetchGame();
			return;
		}
	});

	const boardsContainer = {
		display: "flex",
		justifyContent: "space-around",
		alignItems: "center",
		flexWrap: "wrap",
		width: "100vw",
		marginTop: 30,
		marginBottom: 50
	};

	const fetchGame = () => {
		axios.get('http://localhost:4000/game/' + id, {
			headers: {
				'Content-Type': 'application/json'
			}
		}).then(res => {
			setGame(res.data[0]);
		});
	}

	
	let { id } = useParams();

	return (
		<>
			<div style={boardsContainer}>
				<WithMoveValidation />
			</div>
			<p>Player 1 (White): {(game === undefined) ? "" : game.players[0]}</p> <br />
			<p>Player 2 (Black): waiting...</p>
			<button onClick={fetchGame}>Fetch</button>
		</>
	);
}

export default ChessBoard;