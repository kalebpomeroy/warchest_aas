import React, { Component } from 'react';
import _ from 'lodash';
import Coin from '../coin';

export default class HandZone extends Component {
    render() {

        return (

            <div className='d-flex'>
                {this.props.zone.coins && this.renderFaceUp(this.props.zone.coins)}

                {!this.props.zone.coins && this.renderFaceDown(this.props.zone.count)}
            </div>
        );
    }
    renderFaceUp(coins){
        if (this.props.bonus){
            return <div>
                <Coin name={this.props.bonus}  onClick={() => this.props.getOption(this.props.bonus)}/>
                {_.map(coins, (c, i) => <Coin key={i} name={c} disabled={true} /> )   }
            </div>
        }
        return _.map(coins, (c, i) => <Coin key={i} name={c} onClick={() => this.props.getOption(c)}/>);
    }
    renderFaceDown(count) {
        return _.times(count, (i) => <Coin key={i} name='facedown' />)
    }
}
