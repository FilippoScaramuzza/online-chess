import './css/App.css'
import { Header, Icon } from 'semantic-ui-react'
import { BrowserRouter as Router, Route } from "react-router-dom"
import NewGamePopup from './NewGamePopup'
import JoinGamePopup from './JoinGamePopup'
import ChessBoard from './ChessBoard'

function App() {
  return (
<Router>
    <div className="main">
      <Header as='h2' icon>
        <Icon name='chess' />
        Online Chess
        <Header.Subheader>
          Play Chess Online with your friends!
        </Header.Subheader>
      </Header><br /><br />
      <Route path="/" exact component={NewGamePopup} />
      <Route path="/" exact component={JoinGamePopup} />
      <Route path="/game" component={ChessBoard} />
    </div>
    </Router>
  );
}

export default App;
