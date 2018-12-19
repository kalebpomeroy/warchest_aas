import React, { Component } from 'react';
import _ from 'lodash';

export default class Options extends Component {


    render() {

        if(!this.props.options.options) {
            return <span>Choose a coin</span>;
        }
        return (
            <div className='d-flex flex-justify-between'>
                {_.map(this.props.options.options, (c, o) => this.renderOption(o, c))}
            </div>
        );
    }

    renderOption(option, choices) {
        if(!choices) {
            return;
        }

        if (choices === true) {
            return <div className='option flex-self-start mx-4' onClick={() => this.props.doOption(option)}>{option}</div>;
        }

        return <div className='d-flex flex-column flex-wrap mx-1'>
            {Array.isArray(choices)
                ? _.map(choices, (c) => this.renderChoice(option, c))
                : _.map(choices, (c, unit) => _.map(c, (d) => this.renderChoice(option, d, unit)))
            }
        </div>
    }
    renderChoice(option, c, unit) {
        if(Array.isArray(c)){
            return <div onMouseOver={() => this.props.onMouseOver(c, unit)}
                        onMouseOut={() => this.props.onMouseOver()}
                        onClick={() => this.props.doOption(option, c, unit)}
                        className='option'>
                {option} {unit} ({_.join(c, ", ")})
            </div>
        }
        return <div className='option' onClick={() => this.props.doOption(option, c)}>{option} {c}</div>
    }
}
