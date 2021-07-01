import React, { useEffect, useState } from 'react';
import { Button } from 'semantic-ui-react';
import Popup from 'reactjs-popup';
import { Link } from 'react-router-dom';
import "./css/NewGamePopup.css";
import socket from './SocketConfig';

function NewGamePopup(props) {
	const [open, setOpen] = useState(undefined)
    const [win, setWin] = useState(props.win)
    const [lost, setLost] = useState(props.lost)
    const [resigned, setResigned] = useState(props.resigned)

    useEffect( () => {
        if(props.win || props.lost) {
            setOpen(true)
        }
        setWin(props.win)
        setLost(props.lost)
        setResigned(props.resigned)
    }, [props.win, props.lost, props.resigned])

	return (
		<Popup open={open} onClose={() => setOpen(undefined)} modal>
			<div className="modal">
				<h3 className="ui horizontal divider header">
					You {win ? "won" : ""} {lost ? "lost" : ""} {resigned ? "by resignation!" : "!"}
				</h3>
                <br />
                <Link to="/">
                    <Button>Back to home!</Button>
                </Link>
			</div>

		</Popup >
	);
}

export default NewGamePopup;