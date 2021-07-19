"""
✘ Commands Available
• `{i}owo`
    Gives owo face (Reply to a message)
"""

import random

from . import HELP

uwus = [
    "(・`ω´・)",
    "UwU",
    "uwu",
    "OwO",
    "owo",
    "(●__●)",
    "(゜o゜;",
    "⊙.☉",
    "(ô_ô)",
    "~:o",
    "¶-¶",
    "(*^*)",
    "(•_•)",
    "(⑉⊙ȏ⊙)",
    "*(^O^)*",
    "(°_°)",
]


@ultroid_cmd(pattern="owo")
async def faces(ult):
    uff = random.choice(uwus)
    return await eor(ult, f"{uff}")


