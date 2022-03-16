from discord_components import Button, Select, SelectOption


CHOOSE_ACTION = [
    [
        Button(
            label="Melee!", custom_id="attack", style=2),
        Button(
            label="Shoot!", custom_id="shoot", style=2),
        Button(
            label="Throw!", custom_id="throw", style=2)
    ],
    [
        Button(
            label="Aim!", custom_id="aim", style=3),
        Button(
            label="Guard!", custom_id="guard", style=1),
        Button(
            label="Grapple!", custom_id="grapple", style=2)
    ]
]

CHOOSE_ACTION_2 = [
    [
        [
            Button(
                label="Move!", custom_id="move", style=2),
            Button(
                label="Dash!", custom_id="dash", style=2),
            Button(
                label="Jump!", custom_id="jump", style=2)
        ]
    ]
]
