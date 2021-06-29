import React, { Component } from 'react'; // eslint-disable-line no-unused-vars
import PropTypes from 'prop-types';
import Chess from 'chess.js';
import socket from '../SocketConfig';

import Chessboard from 'chessboardjsx';

class HumanVsHuman extends Component {
  static propTypes = { children: PropTypes.func };

  state = {
    id: this.props.id,
    fen: 'start',
    orientation: this.props.orientation,
    pgn: this.props.pgn,
    // square styles for active drop squares
    dropSquareStyle: {},
    // custom square styles
    squareStyles: {},
    // square with the currently clicked piece
    pieceSquare: '',
    // currently clicked square
    square: '',
    game: new Chess(),
    history: []
  };

  componentDidMount() {
    this.setState({orientation: this.props.orientation})
    this.setState({id: this.props.id})
    this.setState({pgn: this.props.pgn})
    if(this.props.pgn !== "") {
      let g = new Chess()
      g.load_pgn(this.props.pgn)
      this.setState({game: g})
    }
    
    socket.on("moved", ({from, to}) => {
      this.state.game.move({
        from: from,
        to: to,
        promotion: 'q' // always promote to a queen for example simplicity
      });
      // illegal move
      this.setState(({ history, pieceSquare }) => ({
        fen: this.state.game.fen(),
        history: this.state.game.history({ verbose: true }),
        squareStyles: squareStyling({ pieceSquare, history }),
      }));
    })
  }

  componentDidUpdate(prevProps) {
    if(prevProps.orientation !== this.props.orientation) {
      this.setState({orientation: this.props.orientation})
    }
    if(prevProps.id !== this.props.id) {
      this.setState({id: this.props.id})
    }
    if(prevProps.pgn !== this.props.pgn) {
      this.setState({pgn: this.props.pgn})
      if(this.props.pgn !== "") {
        let g = new Chess()
        g.load_pgn(this.props.pgn)
        this.setState({game: g})
        this.setState({fen: g.fen()})
        
      }
    }
  }

  // keep clicked square style and remove hint squares
  removeHighlightSquare = () => {
    this.setState(({ pieceSquare, history }) => ({
      squareStyles: squareStyling({ pieceSquare, history })
    }));
  };

  // show possible moves
  highlightSquare = (sourceSquare, squaresToHighlight) => {
    // const highlightStyles = [sourceSquare, ...squaresToHighlight].reduce(
    //   (a, c) => {
    //     return {
    //       ...a,
    //       ...{
    //         [c]: {
    //           background:
    //             'radial-gradient(circle, #fffc00 36%, transparent 40%)',
    //           borderRadius: '50%'
    //         }
    //       },
    //       ...squareStyling({
    //         history: this.state.history,
    //         pieceSquare: this.state.pieceSquare
    //       })
    //     };
    //   },
    //   {}
    // );

    this.setState(({ squareStyles }) => ({
      squareStyles: { ...squareStyles }
    }));
  };

  onDrop = ({ sourceSquare, targetSquare }) => {
    if(this.state.game.turn() === 'w' && this.state.orientation !== "white") return
    if(this.state.game.turn() === 'b' && this.state.orientation !== "black") return

    let move = this.state.game.move({
      from: sourceSquare,
      to: targetSquare,
      promotion: 'q' // always promote to a queen for example simplicity
    });

    // illegal move
    if (move === null) return;
    this.setState(({ history, pieceSquare }) => ({
      fen: this.state.game.fen(),
      history: this.state.game.history({ verbose: true }),
      squareStyles: squareStyling({ pieceSquare, history })
    }));
    
    socket.emit("move", {id: this.state.id, from: sourceSquare, to: targetSquare, pgn: this.state.game.pgn()})

  };

  onMouseOverSquare = square => {
    // get list of possible moves for this square
    let moves = this.state.game.moves({
      square: square,
      verbose: true
    });

    // exit if there are no moves available for this square
    if (moves.length === 0) return;

    let squaresToHighlight = [];
    for (var i = 0; i < moves.length; i++) {
      squaresToHighlight.push(moves[i].to);
    }

    this.highlightSquare(square, squaresToHighlight);
  };

  onMouseOutSquare = square => this.removeHighlightSquare(square);

  // central squares get diff dropSquareStyles
  onDragOverSquare = square => {
    this.setState({
      dropSquareStyle: { boxShadow: 'inset 0 0 1px 2px rgb(100, 100, 100)' }
    });
  };

  onSquareClick = square => {
    if(this.state.game.turn() === 'w' && this.state.orientation !== "white") return
    if(this.state.game.turn() === 'b' && this.state.orientation !== "black") return

    this.setState(({ history }) => ({
      squareStyles: squareStyling({ pieceSquare: square, history }),
      pieceSquare: square
    }));

    let move = this.state.game.move({
      from: this.state.pieceSquare,
      to: square,
      promotion: 'q' // always promote to a queen for example simplicity
    });

    // illegal move
    if (move === null) return;
    socket.emit("move", {id: this.state.id, from: this.state.pieceSquare, to: square, pgn: this.state.game.pgn()})
    this.setState({
      fen: this.state.game.fen(),
      history: this.state.game.history({ verbose: true }),
      pieceSquare: ''
    });
  };

  render() {
    const { fen, dropSquareStyle, squareStyles, orientation } = this.state;

    return this.props.children({
      squareStyles,
      position: fen,
      orientation: orientation,
      onMouseOverSquare: this.onMouseOverSquare,
      onMouseOutSquare: this.onMouseOutSquare,
      onDrop: this.onDrop,
      dropSquareStyle,
      onDragOverSquare: this.onDragOverSquare,
      onSquareClick: this.onSquareClick,
      onSquareRightClick: this.onSquareRightClick
    });
  }
}

export default function WithMoveValidation(props) {
  return (
    <div>
      <HumanVsHuman orientation={props.orientation} id={props.id} pgn={props.pgn}>
        {({
          position,
          orientation,
          onDrop,
          onMouseOverSquare,
          onMouseOutSquare,
          squareStyles,
          dropSquareStyle,
          onDragOverSquare,
          onSquareClick,
          onSquareRightClick
        }) => (
          <Chessboard
            id="humanVsHuman"
            calcWidth={({ screenWidth }) => (screenWidth < 500 ? 350 : 480)}
            position={position}
            onDrop={onDrop}
            onMouseOverSquare={onMouseOverSquare}
            onMouseOutSquare={onMouseOutSquare}
            boardStyle={{
              borderRadius: '5px',
              boxShadow: `0 5px 20px rgba(0, 0, 0, 0.5)`
            }}
            squareStyles={squareStyles}
            dropSquareStyle={dropSquareStyle}
            onDragOverSquare={onDragOverSquare}
            onSquareClick={onSquareClick}
            onSquareRightClick={onSquareRightClick}
            orientation={orientation}
          />
        )}
      </HumanVsHuman>
    </div>
  );
}

const squareStyling = ({ pieceSquare, history }) => {
  const sourceSquare = history.length && history[history.length - 1].from;
  const targetSquare = history.length && history[history.length - 1].to;

  return {
    [pieceSquare]: { backgroundColor: 'rgba(200, 200, 0, 0.4)' },
    ...(history.length && {
      [sourceSquare]: {
        backgroundColor: 'rgba(200, 200, 0, 0.4)'
      }
    }),
    ...(history.length && {
      [targetSquare]: {
        backgroundColor: 'rgba(200, 200, 0, 0.4)'
      }
    })
  };
};
