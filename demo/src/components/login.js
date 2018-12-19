import React, { Component } from 'react';
import { connect } from 'react-redux';
import { setClientId } from 'actions/game'

class Login extends Component {
    constructor(props){
        super(props);
        this.state = {
            clientId: ""
        }
    }

    render() {
        return (

            <div>
                <div className="col s12">
                    <label>Client ID: &nbsp;</label>
                    <input type='input' value={this.state.clientId} onChange={(e) => this.setState({clientId: e.target.value})}/>
                </div>
                <br />
                <div className="col s12">
                    <button className="waves-effect waves-light btn" onClick={() => this.props.setClientId(this.state.clientId)}>Set</button>
                </div>
            </div>
        );
    }
}

const mapStateToProps = state => ({
 ...state
})

const mapDispatchToProps = dispatch => ({
    setClientId: (c) => dispatch(setClientId(c))
})

export default connect(mapStateToProps, mapDispatchToProps)(Login);
