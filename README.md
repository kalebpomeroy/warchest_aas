Setup:
```
mkvirtualenv warchest
pip install -r requirements.txt
python app.py
```
In a new tab:
`npm start`

In two different browsers, go to localhost:3000 and click "login" and set a client ID (it's ghetto)

One of the browsers should be able to create the game, and the other join. 

# TODO:
- Real Login
- ELO system with Leaderboard
- Queue up instead of joining/creating (with an option to challenge friends somehow)
- Data Analysis: Track draft popularity and a bunch of other stuff
- Deployable/buildable
- Demo
    - Show discard piles and bag counts
    - Show abilities
    - Actual hex map/math instead of the hacky nonsense
        - Animate moving?
    - Coin images
    - Show bolstered units
    - Show initiative
    - design/styling overhaul
    - Draft use actual cards


# To Test
- Most of the Tactics (esp footmen)
- Spectator mode

# BUGS:
- Attacking
- 'Test' script no longer works, due to some small changes for demo app
- DEMO: Creating/joining a game should change the state
- Moving footmanb moves footman
