export default (state = {}, action) => {
    switch (action.type) {
        case 'SET_CLIENT_ID':
            return {
                id: action.clientId
            }
        default:
            return state
    }
}
