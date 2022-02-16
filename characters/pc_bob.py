PLAYER_CHARACTER_SHEET = {
    "attributes": {
        "stre": 2,
        "dex": 4,
        "sta": 2,
        "cha": 5,
        "man": 5,
        "app": 1,
        "per": 1,
        "inte": 3,
        "wits": 5
    },
    "epic_attributes": {
        "epic_stre": 0,
        "epic_dex": 1,
        "epic_sta": 0,
        "epic_cha": 3,
        "epic_man": 3,
        "epic_app": 0,
        "epic_per": 0,
        "epic_int": 0,
        "epic_wits": 1
    },
    "stre_mod": 0,
    "dex_mod": 0,
    "sta_mod": 0,
    "cha_mod": 0,
    "man_mod": 0,
    "app_mod": 0,
    "per_mod": 0,
    "inte_mod": 0,
    "wits_mod": 0,
    "legend_points_total": 0,
    "legend_points_current": 0,
    "willpower_total": 0,
    "willpower_current": 0,
    "virtues": [3,2,0,0],
    "inventory": [],
    "knacks": ["God's Honest", "Blurt It Out", "Divine Figurehead", "Cat's Grace", "Social Chameleon"],
    "boons": ["Animal Communication", "Warrior Ideal", "Penetrating Glare", "Smoking Mirror"],
    "relics": [["Divine Bazooka", 1], ["Bodkin", 1],],
    "creatures": [["Nala the Flying Dog", 5],],
	"movement": {
		"dash": 0,
		"move": 0,
		"climb": 0,
		"jump": {
			"horizontal": 0,
			"vertical": 0
		}
	},
    "combat": { # 1: speed, 2: damage, 3: def, 4: dv minus
	    "bazooka": [10, "35L", None, None],
	    "bodkin": [3, "6L", 2, None],
        "melee": [None, None, None, None],
        "range": [None, None, None, None],
        "dodge": [7, None, None, None],
        "parry": [5, None, None, None],
        "coordattack": [5, None, None, -2],
        "dash": [3, None, None, -2],
        "aim": [3, None, None, -1],
        "guard": [3, None, None, 0],
        "move": [0, None, None, 0],
        "grapple": [None, None, None, None],
        "inactive": [5, None, None, None],
    },
    "health": {
        "bludgeon": 0,
        "lethal": 0,
        "aggrevated": 0
    },
    "abilities":    {
        "academics": 0,
        "animal_ken": 3,
        "art": 0,
        "athletics": 4,
        "awareness": 0,
        "brawl": 3,
        "command": 0,
        "control": 1,
        "craft": 4,
        "empathy": 0,
        "fortitude": 2,
        "integrity": 0,
        "investigation": 0,
        "larceny": 0,
        "marksmanship": 5,
        "medicine": 0,
        "melee": 0,
        "occult": 1,
        "presence": 5,
        "politics": 0,
        "science": 0,
        "stealth": 2,
        "survival": 0,
        "thrown": 0
    },
    "armor": {
        "bludgeon": 4,
        "lethal": 2,
        "aggrevated": 0
    },
    "soak": {
        "bludgeon": 3,
        "lethal": 2,
        "aggrevated": 0
    },
    "armor_mod": {
        "bludgeon": 0,
        "lethal": 0,
        "aggrevated": 0
    },
    "soak_mod": {
        "bludgeon": 0,
        "lethal": 0,
        "aggrevated": 0
    }
}