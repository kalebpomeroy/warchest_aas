SCOUT = 'scout'
LIGHT_CAVALRY = 'lightcavalry'
ARCHER = 'archer'
LANCER = 'lancer'
CROSSBOWMAN = 'crossbowman'
SWORDSMAN = 'swordsman'
MERCENARY = 'mercenary'
BERSERKER = 'berserker'
WARRIOR_PRIEST = 'warriorpriest'
HEAVY_CAVALRY = 'heavycavalry'
FOOTMAN = 'footman'
FOOTMAN_B = 'footmanb'
ENSIGN = 'ensign'
MARSHALL = 'marshall'
KNIGHT = 'knight'
ROYAL_GUARD = 'royalguard'
PIKEMAN = 'pikeman'
ROYAL_TOKEN = 'royaltoken'

UNITS = {
    # deploy
    SCOUT: {'count': 5},

    # When calculating movement, add 1 space
    LIGHT_CAVALRY: {'count': 5},

    # When calculating attack, only show valid
    ARCHER: {'count': 4},
    LANCER: {'count': 4},
    CROSSBOWMAN: {'count': 5},

    # After action, don't flip initiative, but game in a weird state
    SWORDSMAN: {'count': 5},       # Prompt move/pass
    MERCENARY: {'count': 5},       # Prompt activate/pass
    BERSERKER: {'count': 5},       # Prompt activate/pass
    WARRIOR_PRIEST: {'count': 4},  # Draw, Prompt use (could be pass)

    # Tactic: a list of moves + attacks, up to 36 combinations
    HEAVY_CAVALRY: {'count': 4},

    # NFC
    FOOTMAN: {'count': 5},
    ENSIGN: {'count': 5},
    MARSHALL: {'count': 5},

    # When determining attack targets, throw out the knight if !bolstered
    KNIGHT: {'count': 4},

    # After attacked, prompt to remove from stack
    ROYAL_GUARD: {'count': 5},

    # After attacked, remove attacker from the board
    PIKEMAN: {'count': 4},
}
