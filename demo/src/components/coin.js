import React, { Component } from 'react';

const COLORS = {
    wolves: '#333',
    ravens: '#aaa',

    archer: '#bef5cb',
    berserker: '#165c26',
    crossbowman: '#86181d',
    ensign: '#85e89d',
    facedown: '#333',
    footman: '#b392f0',
    footmanb: '#b392f0',
    heavycavalry: '#c24e00',
    knight: '#2188ff',
    lancer: '#d73a49',
    lightcavalry: '#28a745',
    marshall: '#b31d28',
    mercenary: '#9e1c23',
    pikeman: '#ffdf5d',
    royalguard: '#fdaeb7',
    royaltoken: '#777',
    scout: '#044289',
    swordsman: '#005cc5',
    warriorpriest: '#3a1d6e',
}

export default class Coin extends Component {
    render() {
        var color = {
            'backgroundColor': COLORS[this.props.name]
        }
        if(this.props.onClick) {
            color.cursor = 'pointer'
        }
        if(this.props.selected) {
            color.border = "4px solid yellow";
        }
        if(this.props.disabled) {
            color.opacity = "0.4";
        }
        return (
            <div style={color}
                 onClick={this.props.onClick}
                 className='coin d-flex text-white flex-items-center flex-justify-around'>
                <div className='d-flex flex-column flex-items-center'>
                    {this.props.name}<br />
                    {this.props.count && <span>({this.props.count})</span>}
                </div>
            </div>
        );
    }
}
