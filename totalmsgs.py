# credit https://t.me/I_m_FlaSh

"""
✘ Commands Available -
• `{i}totals`
    Returns your total messages count in current chat
    
• `{i}totals [username]/<reply>`
    Returns total msg count of user in current chat
"""

from . import *


@ultroid_cmd(pattern="totals ?(.*)")
async def _(e):
  match = e.pattern_match.group(1)
  if match:
    user = match
  elif e.is_reply:
    user = (await e.get_reply_message()).sender_id
  else:
    user = 'me'
  a = await ultroid_bot.get_messages(e.chat_id, 0, from_user=user)
  user = await ultroid_bot.get_entity(user)
  await eor(e, f"Total messages of `{user.first_name}` here = {a.total}")


HELP.update({f"{__name__.split('.')[1]}": f"{__doc__.format(i=HNDLR)}"})  
