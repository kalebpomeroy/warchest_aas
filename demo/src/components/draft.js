import React, { Component } from 'react';
import { connect } from 'react-redux';
import { draft } from '../actions/game';

import Coin from 'components/coin';
import _ from 'lodash';

class Draft extends Component {

    render() {
        var game = this.props.game.game;
        var clientId = this.props.client.id;
        var purple = "purple-text text-darken-4";
        var your_turn = game.active_client === clientId;
        return (

            <div className="d-flex flex-justify-around">
                <div>
                    <h3 className={(your_turn) ? purple : ''}>Wolves</h3>
                    {_.map(game.cards.wolves, (c) => this.renderCard(c))}
                </div>
                <div>
                    <h3>
                        Draft Options:
                        {(your_turn) ? " Your Turn" : " Waiting for opponent to pick..."}
                    </h3>
                    <div style={{"maxHeight": "500px"}} className='d-flex flex-column flex-wrap'>
                        {_.map(game.cards.draft, (c) => this.renderCard(c, your_turn))}
                    </div>
                </div>
                <div>
                    <h3 className={(your_turn) ? purple : ''}>Ravens</h3>
                    {_.map(game.cards.ravens, (c) => this.renderCard(c))}
                </div>
            </div>
        );
    }

    renderCard(card, draftable) {
        return <div className='m-2'>
            <Coin key={card}
                  name={card}
                  onClick={(draftable) ? (() => this.props.draft(this.props.game.game.id, card)) : undefined} />
        </div>
    }
}

const mapStateToProps = state => ({
 ...state
})

const mapDispatchToProps = dispatch => ({
    draft: (g, c) => dispatch(draft(g, c))
})

export default connect(mapStateToProps, mapDispatchToProps)(Draft);
