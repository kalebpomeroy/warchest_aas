export default (state = {loading: true}, action) => {
    switch (action.type) {
        case 'DO_OPTION':
            return {
            }
        case 'GET_OPTION_SUCCESS':
            return {
                loading: false,
                options: action.game.options,
                coin: action.game.coin
            }
        default:
            return state
    }
}
