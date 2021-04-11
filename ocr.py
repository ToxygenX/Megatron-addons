"""
✘ Commands Available -

• `{i}ocr <language code><reply to a photo>`
    text recognition service.

"""


from . import *
from telegraph import upload_file as uf
import requests as r

TE = "`API not found, Please get it from ocr.space and set\n\ncommand `{i}setredis OCR_API your-api-key`"


@ultroid_cmd(pattern="ocr ?(.*)")
async def ocrify(ult):
    if not ult.is_reply:
        return await eor(ult, "`Reply to Photo...`")
    msg = await eor(ult, "`Processing...`")
    OAPI = udB.get("OCR_API")
    if not OAPI:
        return await msg.edit(TE)
    pat = ult.pattern_match.group(1)
    repm = await ult.get_reply_message()
    if not (repm.media and repm.media.photo):
        return await msg.edit("`Not a Photo..`")
    dl = await repm.download_media()
    if pat:
        atr = f"&language={pat}&"
    else:
        atr = "&"
    tt = uf(dl)
    li = "https://telegra.ph" + tt[0]
    gr = r.get(
        f"https://api.ocr.space/parse/imageurl?apikey={OAPI}{atr}url={li}"
        ).json()
    trt = gr["ParsedResults"][0]["ParsedText"]
    await msg.edit(f"**🎇 ⲞⲤR Ⲣⲟʀⲧⲁⳑ\n\Rⲉⲋυⳑⲧⲋ ~ ** `{trt}`")


HELP.update({f"{__name__.split('.')[1]}": f"{__doc__.format(i=HNDLR)}"})
