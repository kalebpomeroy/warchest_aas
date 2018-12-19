import axios from 'axios';
const KEY = 'warchest:client:id';

const get_headers = function() {
    return {
        'X-Client-Id': localStorage.getItem(KEY),
        'Content-Type': 'application/json'
    }
}

export const getGame = (id) => dispatch => {
    dispatch({
        type: 'GET_GAME',
    })
    id = id = 'mine';

    axios.get('http://localhost:3030/games/' + id, {headers: get_headers()})
         .then(function (response) {
            dispatch({
                type: 'GET_GAME_SUCCESS',
                game: response.data
            })
    })
}

export const getOption = (id, coin) => dispatch => {
    dispatch({
        type: 'GET_OPTION',
    })

    axios.get('http://localhost:3030/games/' + id + '/action/' + coin, {headers: get_headers()})
         .then(function (response) {
            dispatch({
                type: 'GET_OPTION_SUCCESS',
                game: response.data
            })
    })
}

export const doOption = (id, coin, action, data) => dispatch => {
    dispatch({
        type: 'DO_OPTION',
    })

    var d = {
        data: data,
        action: action
    }
    axios.post('http://localhost:3030/games/' + id + '/action/' + coin, d, {headers: get_headers()})
         .then(function (response) {
            dispatch({
                type: 'DO_OPTION_SUCCESS',
                game: response.data
            })
    })
}

export const getGames = () => dispatch => {
    dispatch({
        type: 'GET_GAME_LIST',
    })

    axios.get('http://localhost:3030/games', {headers: get_headers()})
         .then(function (response) {
            dispatch({
            type: 'GET_GAME_LIST_SUCCESS',
            games: response.data.games
        })
    })
}


export const createGames = () => dispatch => {
    dispatch({
        type: 'CREATE_GAME',
    })

    axios.post('http://localhost:3030/games', {}, {headers: get_headers()})
         .then(function (response) {
            dispatch({
            type: 'CREATE_GAME_SUCCESS',
            game: response.data
        })
    })
}

export const joinGame = (id) => dispatch => {
    dispatch({
        type: 'JOIN_GAME',
    })

    axios.post('http://localhost:3030/games/' + id, {}, {headers: get_headers()})
         .then(function (response) {
            dispatch({
            type: 'JOIN_GAME_SUCCESS',
            game: response.data
        });
    })
}

export const draft = (gameId, card) => dispatch => {
    dispatch({
        type: 'DRAFT_CARD',
    })

    axios.post('http://localhost:3030/games/' + gameId + '/draft', {pick: card}, {headers: get_headers()})
         .then(function (response) {
            dispatch({
            type: 'DRAFT_CARD_SUCCESS',
            game: response.data
        });
    })
}


export const getClientId = (clientId) => dispatch => {
    dispatch({
        type: "SET_CLIENT_ID",
        clientId: localStorage.getItem(KEY)
    })
}


export const setClientId = (clientId) => dispatch => {
    localStorage.setItem(KEY, clientId);
    dispatch({
        type: "SET_CLIENT_ID",
        clientId: clientId
    })
}
