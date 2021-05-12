# Copyright (C) 2020-2021 by DevsExpo@Github, < https://github.com/DevsExpo >.
#
# This file is part of < https://github.com/DevsExpo/FridayUserBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/DevsExpo/blob/master/LICENSE >
#
# All rights reserved.

import os
import time

import gtts
import requests
from google_trans_new import google_translator
from googletrans import LANGUAGES
from gtts import gTTS
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from langdetect import detect
import xmltodict

from main_startup.core.decorators import friday_on_cmd
from main_startup.helper_func.basic_helpers import edit_or_reply, get_text


@friday_on_cmd(
    ["tts", "voice", "texttospeech","ttv"],
    cmd_help={
        "help": "Convert Text To Speech!",
        "example": "{ch}voice (reply to text) (Language code)",
    },
)
async def gibspeech(client, message):
    stime = time.time()
    event = await edit_or_reply(message, "`Processing...`")
    ttslang = get_text(message)
    if not message.reply_to_message:
        await event.edit("`Reply To Message To Convert Into Speech!`")
        return
    if not message.reply_to_message.text:
        await event.edit("`Reply To Message To Convert Into Speech!`")
        return
    text = message.reply_to_message.text
    language = "en" if not ttslang else ttslang
    kk = gtts.lang.tts_langs()
    if not kk.get(language):
        await event.edit("`Unsupported Language!`")
        return
    await client.send_chat_action(message.chat.id, "record_audio")
    tts = gTTS(text, lang=language)
    tts.save(f"{kk.get(language)}.ogg")
    google_translator()
    dec_s = detect(text)
    etime = time.time()
    hmm_time = round(etime - stime)
    duration = 0
    metadata = extractMetadata(createParser(f"{kk.get(language)}.ogg"))
    if metadata and metadata.has("duration"):
        duration = metadata.get("duration").seconds
    owoc = f"**TTS** \n**Detected Text Language :** `{dec_s.capitalize()}` \n**Speech Text :** `{kk.get(language)}` \n**Time Taken :** `{hmm_time}s` \n__Powered By @FridayOT__"
    await message.reply_audio(
        audio=f"{kk.get(language)}.ogg", caption=owoc, duration=duration
    )
    await client.send_chat_action(message.chat.id, action="cancel")
    os.remove(f"{kk.get(language)}.ogg")
    await event.delete()


@friday_on_cmd(
    ["tr", "translate"],
    cmd_help={
        "help": "Translate text from one Language To Another!",
        "example": "{ch}tr (reply to text) (language-code)",
    },
)
async def tr_pls(client, message):
    event = await edit_or_reply(message, "`Please Wait!`")
    lang = get_text(message)
    if not lang:
        lang = "en"
    if not message.reply_to_message:
        await event.edit("`Reply To Message To Translate It!`")
        return
    if not message.reply_to_message.text:
        await event.edit("`Reply To Message To Translate It!`")
        return
    text = message.reply_to_message.text
    translator = google_translator()
    try:
        source_lan = translator.detect(text)[1]
    except:
        source_lan = translator.detect(text)[0]
    if not LANGUAGES.get(lang):
        await event.edit("`Language Not Supported.`")
        return
    transl_lan = LANGUAGES.get(lang, "English")
    translated = translator.translate(text, lang_tgt=lang)
    tr_text = f"""**Source ({source_lan.capitalize()})**:
`{text}`
**Translation ({transl_lan.capitalize()})**:
`{translated}`"""
    if len(tr_text) >= 4096:
        url = "https://del.dog/documents"
        r = requests.post(url, data=tr_text.encode("UTF-8")).json()
        url2 = f"https://del.dog/{r['key']}"
        tr_text = (
            f"Translated Text Was Too Big, Never Mind I Have Pasted It [Here]({url2})"
        )
    await event.edit(tr_text)


@friday_on_cmd(['truecaller','trs'],
               cmd_help={
                'help': 'Get truecaller info.',
                'example': '{ch}truecaller 9182756561'})
async def geT_if(client, message):
    m_ = await edit_or_reply(message, "`Please Wait!`")
    input_str = get_text(message)
    token="Bearer a1i09--KhyMmqk5-7ub-KlU1h15F6uEkkxHnSeL_M76JohbcT8vug4l3j5S0Qvsb"
    headers={
    'Host': 'search5-noneu.truecaller.com',
    'authorization': token,
    'accept-encoding': 'gzip',
    'user-agent': 'Truecaller/10.43.5 (Android;8.0.0)'}
    res = requests.get("https://search5-noneu.truecaller.com/v2/search?q="+input_str+"&countryCode=IN&type=4&orgLat=18.6680657&orgLong=78.9109548",headers=headers)
    msg=""
    flag=False
    try:
        msg+="<b><u>INFORMATION GATHERED SUCCESSFULLY</b></u>\n\n"
        data=res.json()
        a=data["data"][0]["name"]
        flag=True
        msg+="<b>Name : </b><code>"+a+"</code>\n"
        d=data["data"][0]['addresses'][0]["city"]
        msg+="<b>Address : </b><code>"+d+"</code>\n"
        b=data["data"][0]["phones"][0]["e164Format"]
        msg+="<b>Phone No : </b><code>"+b+"</code>\n"
        c=data["data"][0]["phones"][0]["carrier"]
        msg+="<b>Network : </b><code>"+c+"</code>\n"
        e=data["data"][0]['internetAddresses'][0]["id"]
        msg+="<b>email : </b><code>"+e+"</code>\n"
    except Exception:
        pass
    if flag:
        return await m_.edit("Information not found")
    return await m_.edit(msg)


@friday_on_cmd(['weather','climate','we'],
               cmd_help={
                'help': 'Get Weather info of town or pincode',
                'example': '{ch}weather hyderabad'})
async def geW_if(client, message):
    m_ = await edit_or_reply(message, "`Please Wait!`")
    city = get_text(message)
    data='{"params":"aroundLatLngViaIP=true&hitsPerPage=15&language=en&query='+city+'&type=city"}'
    ses=requests.session()
    res=ses.post("https://places-dsn.algolia.net/1/places/query",data=data).json()
    cords=res["hits"][0]["_geoloc"]
    res=ses.get("https://1weather.onelouder.com/feeds/onelouder2/fm.php?LAT="+str(round(cords["lat"],2))+"&LON="+str(round(cords["lng"],2))+"&UNITS=all")
    data=xmltodict.parse(res.text)
    flag=True
    msg=""
    try:
        msg+="<b><u>INFORMATION GATHERED SUCCESSFULLY</b></u>\n\n"
        today=data["locations"]["location"]
        msg+=("<b>city:  </b><code>"+today["@city"]+" ("+today["@country"]+")"+"</code>\n")
        details=today["sfc_ob"]
        msg+=("<b>temperature:  </b><code>"+details["temp_C"]+" c"+"</code>\n")
        msg+=("<b>apparent temp:  </b><code>"+details["apparent_temp_C"]+" c"+"</code>\n")
        msg+=("<b>Weather report:  </b><code>"+details["wx"]+"</code>\n")
        msg+=("<b>Wind Speed:  </b><code>"+str(details["wnd_spd_kph"])+"kmph ("+str(details["wnd_dir"])+")"+"</code>\n")
        msg+=("<b>Humidity:  <b><code>"+details["rh_pct"]+" %"+"</code>\n")
        flag=False
    except Exception:
        pass
    if flag:
        return await m_.edit("Information not found")
    return await m_.edit(msg)
