import utils

a=4

female = utils.Drawing(
        points=[
        (a*3, a*0),
        (a*10, a*0),
        (a*10, a*2),
        (a*8, a*2),
        (a*8, a*1),
        (a*7, a*1),
        (a*5, a*3),
        (a*7, a*5),
        (a*8, a*5),
        (a*8, a*4),
        (a*10, a*4),
        (a*10, a*6),
        (a*3, a*6)
        ],
        name="Female",
    )


male = utils.Drawing(
    points=[
    (a*12, a*0),
    (a*10, a*0),
    (a*10, a*2),
    (a*8, a*2),
    (a*8, a*1),
    (a*7, a*1),
    (a*5, a*3),
    (a*7, a*5),
    (a*8, a*5),
    (a*8, a*4),
    (a*10, a*4),
    (a*10, a*6),
    (a*12, a*6)
    ],
    name="male",
)


triangle = utils.Drawing(
    points=[
    (0, 0),
    (40, 0),
    (20, 30)
    ],
    name="triangle",
)

