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
    SWORDSMAN: {'count': 5},       # Prompt move/pass
    MERCENARY: {'count': 5},       # Prompt activate/pass
    BERSERKER: {'count': 5},       # Prompt activate/pass
    WARRIOR_PRIEST: {'count': 4},  # Draw, Prompt use (could be pass)
    FOOTMAN: {'count': 5},         # After tactic, prompt for weird state
    ROYAL_GUARD: {'count': 5},     # After attacked, prompt non-active

    HEAVY_CAVALRY: {'count': 4},
    CROSSBOWMAN: {'count': 5},
    # LANCER: {'count': 4},
    # ARCHER: {'count': 4},
    # KNIGHT: {'count': 4},
    # PIKEMAN: {'count': 4},
    # SCOUT: {'count': 5},
    # LIGHT_CAVALRY: {'count': 5},
    # ENSIGN: {'count': 5},
    # MARSHALL: {'count': 5},
}
