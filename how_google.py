"""
✘ Commands Available -
•`{i}htg <text>`
   How to Google.
   Some peoples don't know how to google so help them 🙃🙂.
"""


import requests

from . import *


@ultroid_cmd(pattern="htg ?(.*)")
async def _(e):
    text = event.pattern_match.group(1)
    if not text:
        return await eod(e, "`Give some text`")
    url = "https://da.gd/s?url=https://lmgtfy.com/?q={}%26iie=1".format(
        text.replace(" ", "+")
    )
    response = requests.get(url).text
    if response:
        await eor(e, "[{}]({})\n`Learn How to Google :)` ".format(text, response.rstrip()))
    else:
        await eod(e, "`Something is wrong. please try again later.`")


HELP.update({f"{__name__.split('.')[1]}": f"{__doc__.format(i=HNDLR)}"})
