# Made By @Midhun_xD, Base Of Module By @kandnub 
# Ported and customized by @Hackintush 

"""
✘ Commands Available -
• `Waifu Harem Automatic Detection`
   Set var `ENABLE_HAREM` as `True`
"""

import io
import os
import re
import time
import urllib
import shutil
from pathlib import Path
from sys import *
from re import findall
import requests
from bs4 import BeautifulSoup
from telethon import events
from PIL import Image
from . import *

from cython.misc._supporter import logging
from cython.misc._decorators import decorator, wrapper, register, ultroid_cmd

ENABLE_HAREM = os.environ.get("ENABLE_HAREM", True)

sedpath = Config.TMP_DOWNLOAD_DIRECTORY

logger = logging.getLogger("[--WARNING--]")

if not os.path.isdir(sedpath):
    os.makedirs(sedpath)

opener = urllib.request.build_opener()
useragent = "Mozilla/5.0 (Linux; Android 9; SM-G960F Build/PPR1.180610.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74.0.3729.157 Mobile Safari/537.36"
opener.addheaders = [("User-agent", useragent)]

async def convert_to_image(event, bot):
    lmao = await event.get_reply_message()
    if not (
            lmao.gif
            or lmao.audio
            or lmao.voice
            or lmao.video
            or lmao.video_note
            or lmao.photo
            or lmao.sticker
            or lmao.media
    ):
        await event.edit("`Format Not Supported.`")
        return
    else:
        try:
            c_time = time.time()
            downloaded_file_name = await bot.download_media(
                lmao.media,
                sedpath,
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(d, t, event, c_time, "`Downloading...`")
                ),
            )
        except Exception as e:  # pylint:disable=C0103,W0703
            await event.edit(str(e))
        else:
            await event.edit(
                "Downloaded to `{}` successfully.".format(downloaded_file_name)
            )
    if not os.path.exists(downloaded_file_name):
        await event.edit("Download Unsucessfull :(")
        return
    if lmao and lmao.photo:
        lmao_final = downloaded_file_name
    elif lmao.sticker and lmao.sticker.mime_type == "application/x-tgsticker":
        rpath = downloaded_file_name
        image_name20 = os.path.join(sedpath, "SED.png")
        cmd = f"lottie_convert.py --frame 0 -if lottie -of png {downloaded_file_name} {image_name20}"
        stdout, stderr = (await runcmd(cmd))[:2]
        os.remove(rpath)
        lmao_final = image_name20
    elif lmao.sticker and lmao.sticker.mime_type == "image/webp":
        pathofsticker2 = downloaded_file_name
        image_new_path = sedpath + "image.png"
        im = Image.open(pathofsticker2)
        im.save(image_new_path, "PNG")
        if not os.path.exists(image_new_path):
            await event.edit("`Wasn't Able To Fetch Shot.`")
            return
        lmao_final = image_new_path
    elif lmao.audio:
        sed_p = downloaded_file_name
        hmmyes = sedpath + "stark.mp3"
        imgpath = sedpath + "starky.jpg"
        os.rename(sed_p, hmmyes)
        await runcmd(f"ffmpeg -i {hmmyes} -filter:v scale=500:500 -an {imgpath}")
        os.remove(sed_p)
        if not os.path.exists(imgpath):
            await event.edit("`Wasn't Able To Fetch Shot.`")
            return
        lmao_final = imgpath
    elif lmao.gif or lmao.video or lmao.video_note:
        sed_p2 = downloaded_file_name
        jpg_file = os.path.join(sedpath, "image.jpg")
        await take_screen_shot(sed_p2, 0, jpg_file)
        os.remove(sed_p2)
        if not os.path.exists(jpg_file):
            await event.edit("`Couldn't Fetch. SS`")
            return
        lmao_final = jpg_file
    return lmao_final

async def ParseSauce(googleurl):
    source = opener.open(googleurl).read()
    soup = BeautifulSoup(source, "html.parser")
    results = {"similar_images": "", "best_guess": ""}
    try:
        for similar_image in soup.findAll("input", {"class": "gLFyf"}):
            url = "https://www.google.com/search?tbm=isch&q=" + urllib.parse.quote_plus(
                similar_image.get("value")
            )
            results["similar_images"] = url
    except BaseException:
        pass
    for best_guess in soup.findAll("div", attrs={"class": "r5a77d"}):
        results["best_guess"] = best_guess.get_text()
    return results

if ENABLE_HAREM:
    @ultroid_cmd(events.NewMessage(func=lambda x: x.sender_id == int(792028928, 1232515770)))
    async def ihave3000waifu_uwantsome(event):
        if event.is_private:
            return
        if event.media:
            if 'Add' in event.raw_text:
                logger.info("OwO! A Waifu.")
                waifu_moment = io.BytesIO()
                waifu_dl_moment = await bot.download_media(event.media, waifu_moment)
                try:
                    image = Image.open(waifu_moment)
                except OSError:
                    await ultroid_bot.send_message(Var.LOG_CHANNEL, "`A Waifu Appeared By Was Unable To Parse Image! Sorry :( \nError : OSError`")
                    return
                name = "waifu.png"
                image.save(name, "PNG")
                image.close()
                searchUrl = "https://www.google.com/searchbyimage/upload"
                file_img = {"encoded_image": (name, open(name, "rb")), "image_content": ""}
                response = requests.post(searchUrl, files=file_img, allow_redirects=False)
                os.remove(name)
                if response.status_code == 400:
                    await ultroid_bot.send_message(Var.LOG_CHANNEL, "`A Waifu Appeared By Was Unable To Parse Image! Sorry :( \nError : Bad Status Code`")
                    return
                fetchUrl = response.headers["Location"]
                match = await ParseSauce(fetchUrl + "&preferences?hl=en&fg=1#languages")
                guessp = match["best_guess"]
                if not guessp:
                    await ultroid_bot.send_message(Var.LOG_CHANNEL, "`A Waifu Appeared By Was Unable To Reverse Search Image! Sorry :(`")
                    return
                guess = guessp.replace("Results for", "").replace(" ", "")
                await ultroid_bot.send_message(event.chat_id, f"/protecc {guess}")
                await ultroid_bot.send_message(Var.LOG_CHANNEL, f"**#Waifu_Moment** \n**Guessed Waifu :** `{guess}` \n**Chat ID :** `{event.chat_id}` \n**Powered By CɪᴘʜᴇʀX**")


HELP.update({f"{__name__.split('.')[1]}": f"{__doc__.format(i=Var.HNDLR)}"})
