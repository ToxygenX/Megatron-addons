"""
✘ Commands Available -

• `{i}limited`
   Check you are limited or not

"""

from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError

from . import *


@ultroid_cmd(pattern="limited$")
async def demn(ult):
    chat = "@SpamBot"
    msg = await eor(ult, "Checking If You Are Limited...")
    async with ultroid_bot.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=178220800)
            )
            await conv.send_message("/start")
            response = await response
            await ultroid_bot.send_read_acknowledge(chat)
        except YouBlockedUserError:
            await msg.edit("Boss! Please Unblock @SpamBot ")
            return
        await msg.edit(f"~ {response.message.message}")


HELP.update({f"{__name__.split('.')[1]}": f"{__doc__.format(i=HNDLR)}"})
