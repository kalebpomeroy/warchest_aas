import React, { Component } from 'react';
import { connect } from 'react-redux';
import { getGames, createGames, joinGame } from 'actions/game'
import _ from 'lodash';

class GameList extends Component {


    componentWillMount() {
        this.props.getGames();
    }

    render() {
        return (
            <div className='p-3'>
                <button className="btn my-2" onClick={() => this.props.createGames()}>Create Game</button>

                {_.map(this.props.gameList.games, (game) => (
                    <div className="Box" key={game.id}>

                        <div className="Box-body">
                            <strong>{game.id}</strong>
                            {game.status}

                            Created By: {game.wolves}

                            {(this.props.client.id === game.wolves) && "Waiting for player 2..."}
                            {(this.props.client.id !== game.wolves) &&
                             <button className="waves-effect waves-light btn"
                                     onClick={() => this.props.joinGame(game.id) }>
                                Join
                             </button>}
                        </div>
                    </div>
                ))}
            </div>
        );
    }

}

const mapStateToProps = state => ({
 ...state
})

const mapDispatchToProps = dispatch => ({
    getGames: () => dispatch(getGames()),
    createGames: () => dispatch(createGames()),
    joinGame: (id) => dispatch(joinGame(id))
})

export default connect(mapStateToProps, mapDispatchToProps)(GameList);
