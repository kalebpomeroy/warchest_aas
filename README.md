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
