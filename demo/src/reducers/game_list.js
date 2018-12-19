export default (state = {}, action) => {
    console.log(action.type, action)
    switch (action.type) {
        case 'GET_GAME_LIST':
            return {
                loading: true
            }
        case 'GET_GAME_LIST_SUCCESS':
            return {
                loading: false,
                games: action.games
            }
        default:
            return state
    }
}
