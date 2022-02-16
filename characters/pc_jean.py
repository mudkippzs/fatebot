PLAYER_CHARACTER_SHEET = {
	"attributes": {
		"stre": 2,
		"dex": 4,
		"sta": 3,
		"cha": 2,
		"man": 3,
		"app": 2,
		"per": 4,
		"inte": 3,
		"wits": 4
	},
	"epic_attributes": {
		"epic_stre": 0,
		"epic_dex": 1,
		"epic_sta": 0,
		"epic_cha": 0,
		"epic_man": 1,
		"epic_app": 0,
		"epic_per": 1,
		"epic_int": 2,
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
	"virtues": [2,1,1,1],
	"inventory": [],
	"knacks": ["Cat's Grace", "Blurt it Out!", "Broad-Spectrum Reception", "Cobra Reflexes", "Math Genius", "Cipher"],
	"boons": ["Fire Immunity", "Bolster Fire", "Echo Sounding", "Shaping"],
	"relics": [
		["Amber-tinted Eye-glasses of Zeus", 3],
		["Work-coat of Hephaestus", 1],
		["Hephaestus' Neckercheif", 1],
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
		"sword": [5, "4L,3B", 1, None],
		"revolver": [4, "3L", None, None],
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
		"athletics": 2,
		"awareness": 3,
		"brawl": 3,
		"command": 0,
		"control": 3,
		"craft": 3,
		"empathy": 2,
		"fortitude": 1,
		"integrity": 1,
		"investigation": 2,
		"larceny": 0,
		"marksmanship": 0,
		"medicine": 0,
		"melee": 3,
		"occult": 0,
		"presence": 2,
		"politics": 0,
		"science": 2,
		"stealth": 0,
		"survival": 3,
		"thrown": 0
	},
	"armor": {
		"bludgeon": 3,
		"lethal": 2,
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