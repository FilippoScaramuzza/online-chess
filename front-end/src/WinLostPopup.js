import React, { useEffect, useState } from 'react';
import { Button } from 'semantic-ui-react';
import Popup from 'reactjs-popup';
import { Link } from 'react-router-dom';
import "./css/NewGamePopup.css";

function WinLostPopup(props) {
    const [open, setOpen] = useState(undefined)
    const [win, setWin] = useState(props.win)
    const [lost, setLost] = useState(props.lost)
    const [draw, setDraw] = useState(props.draw)
    const [resigned, setResigned] = useState(props.resigned)

    useEffect(() => {
        if (props.win || props.lost || props.draw) {
            setOpen(true)
        }
        setWin(props.win)
        setLost(props.lost)
        setDraw(props.draw)
        setResigned(props.resigned)
        
    }, [props.win, props.lost, props.draw, props.resigned])

    const renderMessage = () => {
        if (win || lost)
            return `You ${win ? "won" : ""}${lost ? "lost" : ""}${resigned ? " by resignation!" : "!"}`
        else if (draw) {
            return `It is a draw!`
        }
    }

    return (
        <Popup open={open} onClose={() => {
            setOpen(undefined);
            setWin(false);
            setLost(false);
        }} modal>
            <div className="modal">
                <h3 className="ui horizontal divider header">
                    {renderMessage()}
                </h3>
                <br />
                <Link to="/">
                    <Button>Back to home!</Button>
                </Link>
            </div>

        </Popup >
    );
}

export default WinLostPopup;
