import React, { Component } from 'react';
import { connect } from 'react-redux';
import { getGame, getOption, doOption } from 'actions/game';
import Draft from 'components/draft';
import HandZone from 'components/zones/hand';
import Options from 'components/options';
import Board from 'components/board';
import RecruitZone from 'components/zones/recruits';

class Game extends Component {

    constructor(props){
        super(props);
        this.state = {
            highlighted: null
        }
    }

    componentDidMount() {
        this.interval = setInterval(() => this.props.getGame(), 5000);
    }
    componentWillUnmount() {
        clearInterval(this.interval);
    }

    componentWillMount() {
        this.props.getGame();
    }

    render() {
        if(this.props.game.loading) {
            return <p>"..."</p>;
        }
        var game = this.props.game.game;
        return (
            <div>
                {game.status === 'drafting' && <Draft />}
                {this.renderGame(game)}
            </div>
        );
    }

    renderGame(game) {
        if(game.status !== 'in_progress') {
            return false;
        }
        var bonus = game.active_client === this.props.client.id && game.should_wait && game.should_wait.unit;
        return <div className='d-flex flex-column flex-justify-between' style={{height: "650px"}}>
            <div className="d-flex">
                <div className="col-2 border">
                    <RecruitZone cards={game.cards.wolves} game={game} zones={game.zones.wolves} />
                </div>

                    <Board board={game.board} highlighted={this.state.highlighted} coin={this.state.coin} />
                <div className='col-2 border'>
                    <RecruitZone cards={game.cards.ravens} game={game} zones={game.zones.ravens} />
                </div>
            </div>

            <div className="d-flex flex-justify-between">
                <HandZone zone={game.zones.wolves.hand} bonus={bonus} getOption={(c) => this.getOption(c)} />
                {(game.active_client === this.props.client.id)
                    ? <Options options={this.props.options}
                               doOption={(a, d, u) => this.doOption(a, d, u)}
                               coin={this.state.coin}
                               onMouseOver={(c, u) => this.onMouseOver(c, u)} />
                    : "Waiting on opponent..."}
                <HandZone zone={game.zones.ravens.hand} bonus={bonus} getOption={(c) => this.getOption(c)} />
            </div>
        </div>;
    }

    onMouseOver(coordinates, unit) {
        if(!coordinates){
            return this.setState({highlighted: null})
        }
        this.setState({highlighted: {coin: unit || this.props.options.coin, coordinates: coordinates}})
    }

    getOption(coin) {
        this.props.getOption(this.props.game.game.id, coin)
        this.setState({coin: coin})
    }

    doOption(action, data, unit) {
        if(unit) {
            var d = {}
            d[unit] = data
        }
        this.props.doOption(this.props.game.game.id, this.state.coin, action, d || data)
    }
}

const mapStateToProps = state => ({
 ...state
})

const mapDispatchToProps = dispatch => ({
    getGame: () => dispatch(getGame()),
    getOption: (id, coin) => dispatch(getOption(id, coin)),
    doOption: (id, coin, action, data) => dispatch(doOption(id, coin, action, data))
})

export default connect(mapStateToProps, mapDispatchToProps)(Game);
