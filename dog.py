"""
✘ **Commands Available :**
• `{i}dog <some_text>`
•  Makes Dog Meme with your text
"""

import os
import re
import emoji
from asyncio import TimeoutError
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.account import UpdateNotifySettingsRequest

from . import *


def remove_emoji(string):
    return emoji.get_emoji_regexp().sub(u'', string)

@ultroid_cmd(pattern="dog ?(.*)")
async def doge_says(e):
    if e.fwd_from:
        return
    here = e.chat_id
    args = e.pattern_match.group(1)
    if not args:
        await eor(e, "`Give me a text`")
        return
    eris = await eor(e, "`...`")
    args = str(remove_emoji(args))
    chat = "DogeStickerBot"
    async with ultroid_bot.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(
                    incoming=True,
                    from_users=chat,
                    func=lambda a: a.document,
                )
            )
            await ultroid_bot.send_message(
                chat, args,
            )
            response = await response
        except YouBlockedUserError:
            await eris.edit(f"`Unblock @{chat} first`")
            return
        except asyncio.TimeoutError:
            await eris.edit("`Bot didn't respond in time`")
            return
        file_ = response.message
        await eris.delete()
        p = await file_.download_media("doge.webp")
        await ultroid_bot.send_file(
            here,
            p,
            reply_to=e.reply_to_msg_id if e.is_reply else None,
            caption="CipherX Bot",
        )
        await ultroid_bot.send_read_acknowledge(chat)
        os.remove(p)


