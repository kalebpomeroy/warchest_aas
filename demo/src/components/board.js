import React, { Component } from 'react';
import _ from 'lodash';
import board from 'img/board.png';
import Coin from 'components/coin';

export default class Board extends Component {

    render() {

        return (
            <div className='img-fill col-8 p-5 border position-relative '>
                <img src={board} alt="" />
                {this.props.highlighted && this.add_coin(this.props.highlighted.coin, this.props.highlighted.coordinates, 2, true)}
                {_.map(this.props.board.coins_on, (c, u) => this.add_coin(u, c.space, 2, false, c.coins))}
                {_.map(this.props.board.wolves, (c) => this.add_coin('wolves', c, 1))}
                {_.map(this.props.board.ravens, (c) => this.add_coin('ravens', c, 1))}
            </div>
        );
    }

    add_coin(type, coordinates, z, highlighted, count) {
        var scale = 8;
        if (count === 1){
            count = false;
        }

        var q = scale * coordinates[0];
        var s = scale * coordinates[2];
        var x = 45 + (1.1*q) + z;
        var y = 42 - (1.8*s) - (0.9*q) + z;

        var pos = {
            top: y + "%",
            left: x + "%",
            zIndex: z,
            opacity: (highlighted) ? .6 : 1
        }

        return <div key={coordinates} style={pos} className={'position-absolute'}>
            <Coin name={type} selected={(!highlighted && this.props.coin === type)} count={count}/>
        </div>
    }
}
