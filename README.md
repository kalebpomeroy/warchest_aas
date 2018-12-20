# TODO:
- Login (multiple devices)
- ELO system with Leaderboard
- Games with passcode/names
- Track draft popularity as well as a bunch of other stuff

# BUG:
- Tactics that move units seem to put them in a weird state
  The royalguard is normal, the mercenary is broken
            "royalguard" : {
				"space" : [-1, -2, 3],
			},
			"mercenary" : {
				"space" : {
					"mercenary" : [3, -3, 0]
				},
			},

# DEVELOPING:

- Install and run mongodb locally:
  - e.g. https://docs.mongodb.com/manual/tutorial/install-mongodb-on-os-x/
  - Default port
- Install python3, and requirements from requirements.txt
  - Or use pipenv!
- Run `python app.py`
- Make sure it works:
```
$ curl -X POST http://127.0.0.1:3030/register
{
  "client_id": "d0d8942d-8803-4c7f-b3b9-03a81ee5135d"
}

$ curl -H "X-Client-Id: d0d8942d-8803-4c7f-b3b9-03a81ee5135d" http://127.0.0.1:3030/games
{
  "games": []
}
```
- Run the tests:
```
pip install nose
python -m nose
```
