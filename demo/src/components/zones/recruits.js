import React, { Component } from 'react';
import _ from 'lodash';
import Coin from 'components/coin';

export default class RecruitZone extends Component {
    render() {

        return (

            <div className='d-flex flex-column'>
                {_.map(this.props.cards, (c) => this.renderCard(c))}
            </div>
        );
    }

    renderCard(c) {


        var recruit = _.reduce(this.props.zones.recruit.coins, (t, coin) => (coin === c) ? t + 1 : t, 0);
        // var dead = _.reduce(this.props.zones.dead.coins, (t, coin) => (coin === c) ? t + 1 : t);
        var faceup = _.reduce(this.props.zones.faceup.coins, (t, coin) => (coin === c) ? t + 1 : t, 0);
        var facedown = _.reduce(this.props.zones.facedown, (t, coin) => (coin === c) ? t + 1 : t, 0);
        return <div className='p-1 d-flex flex-justify-around' key={c}>

            <Coin name={c}  count={recruit} />
            <div className='d-flex flex-column flex-justify-around'>
                total:  {this.props.game.cards.units[c].count}<br />
                discard: {facedown + faceup}<br />
                dead: 0
            </div>
        </div>
    }
}
