import { combineReducers } from 'redux';
import game from './game';
import client from './client';
import gameList from './game_list';
import options from './options'
export default combineReducers({
    client,
    game,
    gameList,
    options
});
