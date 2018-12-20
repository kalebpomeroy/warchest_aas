import React, { Component } from 'react';
import { connect } from 'react-redux';
import Game from './components/game'
import Login from './components/login'
import GameList from './components/game_list'
import { getClientId } from './actions/game'
import { BrowserRouter as Router, Route, Link } from "react-router-dom";

class App extends Component {

    componentWillMount() {
        this.props.getClientId();
    }

    render() {
        return (
            <Router>

                <div className="main-nav d-flex flex-justify-between px-3 pl-md-4 pr-md-4 py-3 box-shadow bg-gray-dark ">

                    <span className="brand-logo">Warchest</span>
                    <nav className='flex-self-center flex-shrink-0 text-white'>
                        <Link className='text-white px-md-1 px-lg-3' to="/play">Play</Link>
                        |
                        <Link className='text-white px-md-1 px-lg-3' to="/">Game List</Link>
                        |
                        <Link className='text-white px-md-1 px-lg-3' to="/me">{this.props.client.id || "Login"}</Link>

                    </nav>
                </div>

                <div className="content">
                    <Route path="/" exact component={GameList} />
                    <Route path="/play" component={Game} />
                    <Route path="/me" component={Login} />
                </div>
            </Router>
        );
    }
}

const mapStateToProps = state => ({
 ...state
})

const mapDispatchToProps = dispatch => ({
    getClientId: () => dispatch(getClientId())
})

export default connect(mapStateToProps, mapDispatchToProps)(App);
