import './css/App.css'
import { Header, Icon } from 'semantic-ui-react'
import { BrowserRouter as Router, Route } from "react-router-dom"
import NewGamePopup from './NewGamePopup'
import ChessBoard from './ChessBoard'

function App() {
  return (
    <>
      <div className="main">
        <Header as='h2' icon>
          <Icon name='chess' />
          Online Chess
          <Header.Subheader>
            Play Chess Online with your friends! 
          </Header.Subheader>
        </Header><br /><br />
        <Router>
          <Route path="/" exact component={NewGamePopup} />
          <Route path="/game/:id" component={ChessBoard} />
        </Router>
      </div>
    </>
  );
}

export default App;
