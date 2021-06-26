import React, { Component } from 'react'; // eslint-disable-line no-unused-vars
import PropTypes from 'prop-types';
import Chess from 'chess.js';
import socket from '../SocketConfig';

import Chessboard from 'chessboardjsx';

class HumanVsHuman extends Component {
  static propTypes = { children: PropTypes.func };

  state = {
    id: this.props.id,
    myTurn: true,
    fen: 'start',
    orientation: this.props.orientation,
    // square styles for active drop squares
    dropSquareStyle: {},
    // custom square styles
    squareStyles: {},
    // square with the currently clicked piece
    pieceSquare: '',
    // currently clicked square
    square: '',
    history: []
  };

  componentDidMount() {
    this.game = new Chess();
    this.setState({orientation: this.props.orientation})
    this.setState({id: this.props.id})
    if(this.state.orientation==='black') this.setState({myTurn: false})
    
    socket.on("moved", ({from, to}) => {
      this.game.move({
        from: from,
        to: to,
        promotion: 'q' // always promote to a queen for example simplicity
      });
      // illegal move
      this.setState(({ history, pieceSquare }) => ({
        fen: this.game.fen(),
        history: this.game.history({ verbose: true }),
        squareStyles: squareStyling({ pieceSquare, history }),
        myTurn: true
      }));
    })
  }

  componentDidUpdate(prevProps) {
    if(prevProps.orientation !== this.props.orientation) {
      this.setState({orientation: this.props.orientation})
      if(this.props.orientation === 'black') this.setState({myTurn: false})
    }
    if(prevProps.id !== this.props.id) {
      this.setState({id: this.props.id})
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
    // see if the move is legal
    if(!this.state.myTurn) return;
    let move = this.game.move({
      from: sourceSquare,
      to: targetSquare,
      promotion: 'q' // always promote to a queen for example simplicity
    });

    console.log("SQUARES")
    console.log(sourceSquare)
    console.log(targetSquare)

    // illegal move
    if (move === null) return;
    this.setState(({ history, pieceSquare }) => ({
      fen: this.game.fen(),
      history: this.game.history({ verbose: true }),
      squareStyles: squareStyling({ pieceSquare, history })
    }));
    
    socket.emit("move", {id: this.state.id, from: sourceSquare, to: targetSquare})
    this.setState({myTurn: false})
  };

  onMouseOverSquare = square => {
    // get list of possible moves for this square
    let moves = this.game.moves({
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
    if(!this.state.myTurn) return;
    this.setState(({ history }) => ({
      squareStyles: squareStyling({ pieceSquare: square, history }),
      pieceSquare: square
    }));

    let move = this.game.move({
      from: this.state.pieceSquare,
      to: square,
      promotion: 'q' // always promote to a queen for example simplicity
    });

    // illegal move
    if (move === null) return;
    socket.emit("move", {id: this.state.id, from: this.state.pieceSquare, to: square})
    this.setState({myTurn: false})
    this.setState({
      fen: this.game.fen(),
      history: this.game.history({ verbose: true }),
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
      <HumanVsHuman orientation={props.orientation} id={props.id}>
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
