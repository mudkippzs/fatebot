PLAYER_CHARACTER_SHEET = {
	"attributes": {
		"stre": 3,
		"dex": 4,
		"sta": 4,
		"cha": 3,
		"man": 2,
		"app": 3,
		"per": 4,
		"inte": 3,
		"wits": 4
	},

	"epic_attributes": {
		"epic_stre": 1,
		"epic_dex": 3,
		"epic_sta": 2,
		"epic_cha": 3,
		"epic_man": 2,
		"epic_app": 3,
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
	"virtues": [3,1,0,0],
	"inventory": [],
	"knacks": ["Hurl to the Horizon", "Lightning Sprinter", "Trick Shooter", "Untouchable Opponent", "Holy Fortitude", "Solipsitic Wellbeing", "Inspirational Figure", "Opening Gambit"],
	"boons": ["Blessing of Bravery", "Battle Cry", "Warrior Ideal"],
	"relics": [
		["Dogtags of Mars",1],
		["Aphrodite's Kiss", 1],
		["Spear of Thermopylae", 1],
		["Shield of Leonidas", 2],
	],
	"creatures": [],
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
		"gun": [5, "5L", None, None],
		"spear": [5, "5L", 2, None],
		"shield": [None, "3B", 3, None],
		"melee": [None, None, None, None],
		"range": [None, None, None, None],
		"dodge": [None, None, None, None],
		"parry": [None, None, None, None],
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
	"abilities":	{
		"academics": 0,
		"animal_ken": 0,
		"art": 0,
		"athletics": 3,
		"awareness": 3,
		"brawl": 3,
		"command": 1,
		"control": 2,
		"craft": 0,
		"empathy": 0,
		"fortitude": 1,
		"integrity": 0,
		"investigation": 1,
		"larceny": 0,
		"marksmanship": 3,
		"medicine": 2,
		"melee": 3,
		"occult": 0,
		"politics": 1,
		"presence": 2,
		"science": 0,
		"stealth": 2,
		"survival": 2,
		"thrown": 2
	},
	"armor": {
		"bludgeon": 0,
		"lethal": 0,
		"aggrevated": 0
	},

	"soak": {
		"bludgeon": 0,
		"lethal": 0,
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