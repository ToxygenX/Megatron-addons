"""
✘ Commands Available -

• `{i}wiki <search query>`
    Wikipedia search from telegram.
"""

import wikipedia
from wikipedia.exceptions import DisambiguationError, PageError, WikipediaException

from . import *


def _summary_for(query: str) -> str:
    try:
        return wikipedia.summary(query, sentences=3, auto_suggest=True)
    except DisambiguationError as exc:
        options = [opt for opt in exc.options if opt]
        if not options:
            raise PageError(query)
        # Try the closest disambiguation results instead of dying.
        errors = []
        for option in options[:4]:
            try:
                return wikipedia.summary(option, sentences=3, auto_suggest=False)
            except Exception as err:
                errors.append(str(err))
        return (
            "**Multiple matches found. Try one of these:**\n"
            + "\n".join(f"- `{option}`" for option in options[:8])
        )
    except PageError:
        # If the exact page does not exist, fall back to searching titles.
        matches = wikipedia.search(query, results=5, suggestion=True)[0]
        if not matches:
            raise PageError(query)
        return wikipedia.summary(matches[0], sentences=3, auto_suggest=False)


@cipherx_cmd(pattern="wiki ?(.*)")
async def wiki(e):
    srch = (e.pattern_match.group(1) or "").strip()
    if not srch:
        return await e.eor("`Give some text to search on wikipedia !`")
    msg = await e.eor(f"`Searching {srch} on wikipedia..`")
    try:
        result = _summary_for(srch)
        await msg.edit(f"**Search Query :** {srch}\n\n**Results :** {result[:3900]}")
    except PageError:
        await msg.edit("`No Wikipedia page found for that query.`")
    except WikipediaException as err:
        await msg.edit(f"`Wikipedia error:` `{err}`")
    except Exception as err:
        await msg.edit(f"**ERROR** : `{err}`")
