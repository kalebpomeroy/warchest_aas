export default (state = {loading: true}, action) => {
    switch (action.type) {

        case 'DO_OPTION_SUCCESS':
        case 'GET_GAME_SUCCESS':
        case 'CREATE_GAME_SUCCESS':
        case 'JOIN_GAME_SUCCESS':
        case 'DRAFT_CARD_SUCCESS':
            return {
                loading: false,
                game: action.game
            }
        default:
            return state
    }
}
