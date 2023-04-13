import React, { Component } from 'react'; // eslint-disable-line no-unused-vars
import PropTypes from 'prop-types';
import Chess from 'chess.js';
import socket from '../SocketConfig';
import WinLostPopup from '../WinLostPopup';
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
    history: [],
    lost: false,
    win: false,
    draw: false,
    //pieces: this.props.pieces
  };

  componentDidMount() {
    this.setState({ orientation: this.props.orientation })
    this.setState({ id: this.props.id })
    this.setState({ pgn: this.props.pgn })
    let chess = new Chess()
    chess.load_pgn(this.props.pgn)

    this.setState({game:chess})

    console.log(this.state.game.pgn())
    socket.on("moved", ({ from, to }) => {

      this.state.game.move({
        from: from,
        to: to,
        promotion: 'q' // always promote to a queen for example simplicity
      });

      this.setState(({ history, pieceSquare }) => ({
        fen: this.state.game.fen(),
        history: this.state.game.history({ verbose: true }),
        squareStyles: squareStyling({ pieceSquare: to, history: this.state.game.history({ verbose: true }) })
      }));

      if (this.state.game.in_checkmate()) {
        socket.emit("checkmate", { id: this.state.id })
        this.setState({ lost: true })
        this.state.game.clear()
      }

      if (this.state.game.in_draw() || 
          this.state.game.in_stalemate() || 
          this.state.game.in_threefold_repetition() || 
          this.state.game.insufficient_material()) {
          socket.emit("draw", { id: this.state.id })
          this.setState({ draw: true })
          this.state.game.clear()
      }
    })

    socket.on("checkmate", () => {
      this.setState({ win: true })
      this.state.game.clear()
    })

    socket.on("draw", () => {
      this.setState({ draw: true })
      this.state.game.clear()
    })
  }

  componentDidUpdate(prevProps) {
    if (prevProps.orientation !== this.props.orientation) {
      this.setState({ orientation: this.props.orientation })
      //this.setState({game: new Chess()})
    }
    if (prevProps.id !== this.props.id) {
      this.setState({ id: this.props.id })
    }

    if (prevProps.pgn !== this.props.pgn) {
      let chess = new Chess()
      chess.load_pgn(this.props.pgn)
      console.log(chess.pgn())
      this.setState({game: chess})
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
    const highlightStyles = [sourceSquare, ...squaresToHighlight].reduce(
      (a, c) => {
        return {
          ...a,
          ...{
            [c]: {
              backgroundImage:
                'url(/chess-themes/target.png)',
              backgroundSize: "cover"
            }
          },
          ...squareStyling({
            history: this.state.history,
            pieceSquare: this.state.pieceSquare
          })
        };
      },
      {}
    );

    delete highlightStyles[sourceSquare]

    this.setState(({ squareStyles }) => ({
      squareStyles: { ...squareStyles, ...highlightStyles }
    }));
  };

  onDrop = ({ sourceSquare, targetSquare }) => {
    if (this.state.game.turn() === 'w' && this.state.orientation !== "white") return
    if (this.state.game.turn() === 'b' && this.state.orientation !== "black") return

    let move = this.state.game.move({
      from: sourceSquare,
      to: targetSquare,
      promotion: "q" // always promote to a queen for example simplicity
    });

    // illegal move
    if (move === null) return;

    this.setState(({ history, pieceSquare }) => ({
      fen: this.state.game.fen(),
      history: this.state.game.history({ verbose: true }),
      squareStyles: squareStyling({ pieceSquare, history: this.state.game.history({ verbose: true }) })
    }));

    socket.emit("move", { id: this.state.id, from: sourceSquare, to: targetSquare, pgn: this.state.game.pgn() })

  };

  onMouseOverSquare = square => {
    // // get list of possible moves for this square
    // let moves = this.state.game.moves({
    //   square: square,
    //   verbose: true
    // });

    // // exit if there are no moves available for this square
    // if (moves.length === 0) return;

    // let squaresToHighlight = [];
    // for (var i = 0; i < moves.length; i++) {
    //   squaresToHighlight.push(moves[i].to);
    // }

    // this.highlightSquare(square, squaresToHighlight);
  };

  highlightSquares = square => {
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

  onMouseOutSquare = square => { return; }//this.removeHighlightSquare(square);

  // central squares get diff dropSquareStyles
  onDragOverSquare = square => {
    this.setState({
      dropSquareStyle: { boxShadow: 'inset 0 0 1px 2px rgb(100, 100, 100)', cursor: "-webkit-grabbing" }
    });
  };

  onSquareClick = square => {
    if (this.state.game.turn() === 'w' && this.state.orientation !== "white") return
    if (this.state.game.turn() === 'b' && this.state.orientation !== "black") return

    this.setState(({ history }) => ({
      squareStyles: squareStyling({ pieceSquare: square, history: this.state.game.history({ verbose: true }) }),
      pieceSquare: square
    }));

    this.highlightSquares(square)

    let move = this.state.game.move({
      from: this.state.pieceSquare,
      to: square,
      promotion: "q" // always promote to a queen for example simplicity
    });

    // illegal move
    if (move === null) return;

    socket.emit("move", { id: this.state.id, from: this.state.pieceSquare, to: square, pgn: this.state.game.pgn() })

    this.setState({
      fen: this.state.game.fen(),
      history: this.state.game.history({ verbose: true }),
      pieceSquare: ""
    });
  };

  chessPieces = (theme) => {
    let pieces = ['wP', 'wN', 'wB', 'wR', 'wQ', 'wK', 'bP', 'bN', 'bB', 'bR', 'bQ', 'bK'];
    const returnPieces = {};
    pieces.map((p) => {
      returnPieces[p] = ({ squareWidth, isDragging }) => (
        <img style={{ width: squareWidth, height: squareWidth, cursor: isDragging ? "-webkit-grabbing" : "-webkit-grab", pointerEvents: "auto!important" }}
          src={`${process.env.PUBLIC_URL}/chess-themes/pieces/${theme}/${p.toLowerCase()}.png`}
          key={`${process.env.PUBLIC_URL}/chess-themes/pieces/${theme}/${p.toLowerCase()}.png`}
          alt={p.toLowerCase()}

        />
      );
      return null;
    });
    return returnPieces;
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
      onSquareRightClick: this.onSquareRightClick,
      win: this.state.win,
      lost: this.state.lost,
      draw: this.state.draw,
      pieces: this.chessPieces(this.props.pieces)
    });
  }
}

export default function WithMoveValidation(props) {

  return (
    <HumanVsHuman orientation={props.orientation} id={props.id} pieces={props.pieces} pgn={props.pgn}>
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
        onSquareRightClick,
        win,
        lost,
        draw,
        pieces
      }) => (
        <>
          <WinLostPopup win={win} lost={lost} draw={draw} reisgned={false} />
          <Chessboard
            key={props.pieces}
            id="humanVsHuman"
            calcWidth={({ screenWidth, screenHeight }) => (screenWidth < 500 ? 350 : (screenHeight / 100) * 85)}
            position={position}
            onDrop={onDrop}
            onMouseOutSquare={onMouseOutSquare}
            pieces={pieces}
            boardStyle={{
              borderRadius: '5px',
              boxShadow: `0 5px 20px rgba(0, 0, 0, 0.5)`,
              backgroundImage: `url(${process.env.PUBLIC_URL}/chess-themes/board/` + props.board + ")",
              backgroundSize: "cover"
            }}
            squareStyles={squareStyles}
            sparePieces={false}
            dropSquareStyle={dropSquareStyle}
            onDragOverSquare={onDragOverSquare}
            onSquareClick={onSquareClick}
            onSquareRightClick={onSquareRightClick}
            orientation={orientation}
            lightSquareStyle={{ backgroundColor: "transparent" }}
            darkSquareStyle={{ backgroundColor: "transparent" }}
          />
        </>
      )}
    </HumanVsHuman>
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
