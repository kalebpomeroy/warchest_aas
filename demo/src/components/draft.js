import React, { Component } from 'react';
import { connect } from 'react-redux';
import { draft } from 'actions/game';

import wolves from 'img/wolves.png';
import ravens from 'img/ravens.png';
import classNames from 'classnames';

import _ from 'lodash';

class Draft extends Component {

    render() {
        var game = this.props.game.game;
        var clientId = this.props.client.id;
        var purple = "purple-text text-darken-4";
        return (

            <div className="d-flex flex-justify-around">
                <div>
                    <h3 className={(game.wolves === clientId) ? purple : ''}>Wolves</h3>
                    {_.map(game.cards.wolves, (c) => this.renderCard(c))}
                </div>
                <div>
                    <h3>
                        {game.active_player === 'wolves' && <img src={wolves} alt="" width={50}/>}
                    Draft Pool
                        {game.active_player === 'ravens' && <img src={ravens} alt="" width={50}/>}

                    </h3>
                    <div style={{"maxHeight": "500px"}} className='d-flex flex-column flex-wrap'>
                        {_.map(game.cards.draft, (c) => this.renderCard(c, game.active_client === clientId))}
                    </div>
                </div>
                <div>
                    <h3 className={(game.ravens === clientId) ? purple : ''}>Ravens</h3>
                    {_.map(game.cards.ravens, (c) => this.renderCard(c))}
                </div>
            </div>
        );
    }

    renderCard(card, draftable) {
        const classes = classNames('card border py-4 p-2 m-3', {
            'border-red': draftable
        });
        return <div key={card} className={classes} onClick={draftable && (() => this.props.draft(this.props.game.game.id, card))}>
            {card}
        </div>;
    }
}

const mapStateToProps = state => ({
 ...state
})

const mapDispatchToProps = dispatch => ({
    draft: (g, c) => dispatch(draft(g, c))
})

export default connect(mapStateToProps, mapDispatchToProps)(Draft);
