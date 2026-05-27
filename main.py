from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from pyromod import listen
from aiohttp import ClientSession
from config import Config
import helper
import time
import sys
import shutil
import os, re
import requests
import headers
import logging
import asyncio

bot = Client(
    "bot",
    bot_token=Config.BOT_TOKEN,
    api_id=Config.API_ID,
    api_hash=Config.API_HASH
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

@bot.on_message(filters.command(["start"]))
async def account_login(bot: Client, m: Message):
    start_msg = (
        f"╭━━━〔 🌟 sʏsᴛᴇᴍ ᴀᴄᴛɪᴠᴇ 〕━━━╮\n"
        f"┃ 👤 ʜᴇʟʟᴏ, ᴍᴀsᴛᴇʀ!\n"
        f"┃ 🟢 sᴛᴀᴛᴜs ➠ ʀᴜɴɴɪɴɢ sᴍᴏᴏᴛʜʟʏ ⚡\n"
        f"┃ 🛠️ ᴄᴏᴍᴍᴀɴᴅ ➠ /ᴍᴀsᴛᴇʀ\n"
        f"📥 sᴜᴘᴘᴏʀᴛᴇᴅ ᴜʀʟs ➠\n"
        f"├• ᴀʟʟ ɴᴏɴ-ᴅʀᴍ + ᴅʀᴍ ᴘʀᴏᴛᴇᴄᴛᴇᴅ\n"
        f"├• ᴍᴘᴇɢ ᴅᴀsʜ / ᴠɪsɪᴏɴ ɪᴀs\n"
        f"├• ᴘʜʏsɪᴄsᴡᴀʟʟᴀʜ / ᴄʟᴀssᴘʟᴜs\n"
        f"├• ᴀʟʟᴇɴ / ᴋᴀʟᴀᴍ ᴘᴜʙʟɪᴄᴀᴛɪᴏɴ\n\n"
        f"⚡ ᴅᴇᴠᴇʟᴏᴘᴇʀ ➠ "
    )
    await m.reply_text(start_msg)

@bot.on_message(filters.command("stop"))
async def restart_handler(bot, m):
    if m.chat.id not in Config.VIP_USERS:
        print(f"User ID not in AUTH_USERS", m.chat.id)
        access_denied = (
            f"╭━━━〔 ⚠️ ᴀᴄᴄᴇss ᴅᴇɴɪᴇᴅ 〕━━━╮\n"
            f"┃ 🚫 ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀ ᴘʀᴇᴍɪᴜᴍ ᴍᴇᴍʙᴇʀ!\n"
            f"┃ 🔑 ʏᴏᴜʀ ɪᴅ ➠ `{m.chat.id}`\n"
            f"┃ 📝 ᴜᴘɢʀᴀᴅᴇ ➠ sᴇɴᴅ ɪᴅ ᴛᴏ ᴀᴅᴍɪɴ\n\n"
            f"💬 *ᴘʟᴇᴀsᴇ ᴜᴘɢʀᴀᴅᴇ ʏᴏᴜʀ ᴘʟᴀɴ ᴛᴏ ᴜɴʟᴏᴄᴋ.*"
        )
        await bot.send_message(m.chat.id, access_denied)
        return
    
    stop_msg = (
        f"╭━━━〔 🚦 sʏsᴛᴇᴍ sᴛᴏᴘᴘᴇᴅ 〕━━━╮\n"
        f"┃ 🔴 ʙᴏᴛ ɪs ʀᴇsᴛᴀʀᴛɪɴɢ ɴᴏᴡ..."
    )
    await m.reply_text(stop_msg, True)
    os.execl(sys.executable, sys.executable, *sys.argv)

@bot.on_message(filters.command(["master"]))
async def account_login(bot: Client, m: Message):
    try:
        master_prompt = (
            f"╭━━━〔 🗂️ ᴍᴀsᴛᴇʀ sᴇᴛᴜᴘ 〕━━━╮\n"
            f"┃ 📥 sᴇɴᴅ ᴍᴀsᴛᴇʀ .ᴛxᴛ ғɪʟᴇ\n"
            f"┃ ✉️ *ᴏʀ sᴇɴᴅ ᴅɪʀᴇᴄᴛ ʟɪɴᴋs ᴀs ᴛᴇxᴛ!*"
        )
        editable = await m.reply_text(master_prompt)
        input: Message = await bot.listen(editable.chat.id)
        path = f"./downloads/{m.chat.id}"
        temp_dir = "./temp"
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        os.makedirs(temp_dir)
        if input.document:
            x = await input.download()
            await input.delete(True)
            file_name = os.path.splitext(os.path.basename(x))[0]
        
            try:
                with open(x, "r") as f:
                    content = f.read()
                content = content.split("\n")
                links = [i.split("://", 1) for i in content]
                os.remove(x)
            except Exception as e:
                err_msg = (
                    f"╭━━━〔 ⚠️ ᴇʀʀᴏʀ 〕━━━╮\n"
                    f"┃ 🚫 ғᴀɪʟᴇᴅ ᴛᴏ ᴘʀᴏᴄᴇss ғɪʟᴇ!\n"
                    f"┃ 📝 `{e}`"
                )
                await m.reply_text(err_msg)
                os.remove(x)
                return
        else:
            content = input.text
            content = content.split("\n")
            links = [i.split("://", 1) for i in content]
            await input.delete(True)
            
        links_found = (
            f"╭━━━〔 🔗 ʟɪɴᴋs ғᴏᴜɴᴅ 〕━━━╮\n"
            f"┃ 📊 ᴛᴏᴛᴀʟ ʟɪɴᴋs ➠ `{len(links)}`\n\n"
            f"🔢 *sᴇɴᴅ ғʀᴏᴍ ᴡʜᴇʀᴇ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ sᴛᴀʀᴛ (ᴅᴇғᴀᴜʟᴛ ɪs 1):*"
        )
        await editable.edit(links_found)
        
        if m.chat.id not in Config.VIP_USERS:
            print(f"User ID not in AUTH_USERS", m.chat.id)
            access_denied = (
                f"╭━━━〔 ⚠️ ᴀᴄᴄᴇss ᴅᴇɴɪᴇᴅ 〕━━━╮\n"
                f"┃ 🚫 ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀ ᴘʀᴇᴍɪᴜᴍ ᴍᴇᴍʙᴇʀ!\n"
                f"┃ 🔑 ʏᴏᴜʀ ɪᴅ ➠ `{m.chat.id}`\n"
                f"┃ 📝 ᴜᴘɢʀᴀᴅᴇ ➠ sᴇɴᴅ ɪᴅ ᴛᴏ ᴀᴅᴍɪɴ"
            )
            await bot.send_message(m.chat.id, access_denied)
            return
            
        input0: Message = await bot.listen(editable.chat.id)
        raw_text = input0.text
        await input0.delete(True)

        # ʙᴀᴛᴄʜ ɴᴀᴍᴇ - ᴀᴜᴛᴏ (/ʙ) ᴏʀ ᴍᴀɴᴜᴀʟ ᴛʏᴘɪɴɢ
        batch_prompt = (
            f"╭━━━〔 📦 ʙᴀᴛᴄʜ sᴇᴛᴜᴘ 〕━━━╮\n"
            f"┃ 📝 ᴇɴᴛᴇʀ ʙᴀᴛᴄʜ ɴᴀᴍᴇ\n"
            f"┃ 🧭 *ᴛʏᴘᴇ ᴍᴀɴᴜᴀʟʟʏ ᴏʀ sᴇɴᴅ /ʙ ғᴏʀ ᴀᴜᴛᴏ*"
        )
        await editable.edit(batch_prompt)
        input1: Message = await bot.listen(editable.chat.id)
        raw_text0 = input1.text
        await input1.delete(True)
        if raw_text0 == '/b':
            b_name = file_name
        else:
            b_name = raw_text0
            
        # ᴀᴘᴘ ɴᴀᴍᴇ - ᴀᴜᴛᴏ (/ᴀ) ᴏʀ ᴍᴀɴᴜᴀʟ ᴛʏᴘɪɴɢ
        app_prompt = (
            f"╭━━━〔 📱 ᴀᴘᴘ sᴇᴛᴜᴘ 〕━━━╮\n"
            f"┃ 💬 ᴇɴᴛᴇʀ ᴀᴘᴘ ɴᴀᴍᴇ\n"
            f"┃ 🧭 *ᴛʏᴘᴇ ᴍᴀɴᴜᴀʟʟʏ ᴏʀ sᴇɴᴅ /ᴀ ғᴏʀ ᴅᴇғᴀᴜʟᴛ*"
        )
        await editable.edit(app_prompt)
        input111: Message = await bot.listen(editable.chat.id)
        app_name = input111.text
        await input111.delete(True)
        if app_name == '/a':
            app_name = "ᴅᴇғᴀᴜʟᴛ ᴀᴘᴘ"

        # ǫᴜᴀʟɪᴛʏ - ᴀᴜᴛᴏ sʜᴏʀᴛᴄᴜᴛs (/ǫ360, /ǫ480, /ǫ720) ᴏʀ ᴍᴀɴᴜᴀʟ ᴛʏᴘɪɴɢ
        res_prompt = (
            f"╭━━━〔 ⚙️ ʀᴇsᴏʟᴜᴛɪᴏɴ sᴇᴛᴜᴘ 〕━━━╮\n"
            f"┃ 📺 ᴇɴᴛᴇʀ ᴠɪᴅᴇᴏ ǫᴜᴀʟɪᴛʏ\n"
            f"┃ 💡 *ᴍᴀɴᴜᴀʟ: 360, 480, 720 ᴏʀ ᴀᴜᴛᴏ: /ǫ360, /ǫ480, /ǫ720*"
        )
        await editable.edit(res_prompt)
        input2: Message = await bot.listen(editable.chat.id)
        raw_text2 = input2.text
        await input2.delete(True)
        # ᴀᴜᴛᴏ sʜᴏʀᴛᴄᴜᴛs
        if raw_text2 == '/q360':
            raw_text2 = '360'
        elif raw_text2 == '/q480':
            raw_text2 = '480'
        elif raw_text2 == '/q720':
            raw_text2 = '720'

        # ᴄʀᴇᴅɪᴛs - ᴀᴜᴛᴏ (/ᴄ) ᴏʀ ᴍᴀɴᴜᴀʟ ᴛʏᴘɪɴɢ
        credits_prompt = (
            f"╭━━━〔 👑 ᴄʀᴇᴅɪᴛs sᴇᴛᴜᴘ 〕━━━╮\n"
            f"┃ 🏷️ ᴇɴᴛᴇʀ ʏᴏᴜʀ ɴᴀᴍᴇ / ʙʏ\n"
            f"┃ 🧭 *ᴛʏᴘᴇ ᴍᴀɴᴜᴀʟʟʏ ᴏʀ sᴇɴᴅ /ᴄ ғᴏʀ ᴅᴇғᴀᴜʟᴛ*"
        )
        await editable.edit(credits_prompt)
        input3: Message = await bot.listen(editable.chat.id)
        raw_text3 = input3.text
        await input3.delete(True)
        if raw_text3 == '/c':
            MR = "『Sᴀʀɢɪᴏ』❤️"
        elif raw_text3 == 'de':
            MR = "Sᴀʀɢɪᴏ ❤️"
        else:               
            MR = raw_text3
    
        # ᴛʜᴜᴍʙɴᴀɪʟ - ᴀᴜᴛᴏ (/ᴛ ғᴏʀ sᴋɪᴘ) ᴏʀ ᴍᴀɴᴜᴀʟ ᴜʀʟ
        thumb_prompt = (
            f"╭━━━〔 🖼️ ᴛʜᴜᴍʙɴᴀɪʟ sᴇᴛᴜᴘ 〕━━━╮\n"
            f"┃ 🌐 sᴇɴᴅ ᴛʜᴜᴍʙɴᴀɪʟ ᴜʀʟ\n"
            f"┃ 🧭 *sᴇɴᴅ ᴜʀʟ ᴏʀ /ᴛ ᴛᴏ sᴋɪᴘ*"
        )
        await editable.edit(thumb_prompt)
        input6: Message = await bot.listen(editable.chat.id)
        thumb = input6.text
        await input6.delete(True)
        if thumb == '/t':
            thumb = 'no'
        
        # ᴄʜᴀɴɴᴇʟ ɪᴅ - ᴀᴜᴛᴏ (/ᴅ) ᴏʀ ᴍᴀɴᴜᴀʟ ɪᴅ
        channel_prompt = (
            f"╭━━━〔 📢 ᴜᴘʟᴏᴀᴅ ᴛᴀʀɢᴇᴛ 〕━━━╮\n"
            f"┃ 🆔 sᴇɴᴅ ᴄʜᴀɴɴᴇʟ ɪᴅ\n"
            f"┃ 🧭 *sᴇɴᴅ ɪᴅ ᴏʀ /ᴅ ғᴏʀ ᴄᴜʀʀᴇɴᴛ ᴄʜᴀᴛ*\n\n"
            f"⚠️ *ɴᴏᴛᴇ: ᴍᴀᴋᴇ sᴜʀᴇ ᴛᴏ ᴀᴅᴅ ʙᴏᴛ ᴀs ᴀᴅᴍɪɴ!*"
        )
        await editable.edit(channel_prompt)
        input7: Message = await bot.listen(editable.chat.id)
        if "/d" in input7.text:
            channel_id = m.chat.id
        else:
            channel_id = input7.text
        await input7.delete()

        # ᴜᴘᴅᴀᴛᴇ ǫᴜᴀʟɪᴛʏ ɪɴ ᴛɪᴛʟᴇ ғᴏʀ ɴᴇxᴛ ᴘʀᴏᴍᴘᴛs
        quality_display = raw_text2 if raw_text2 else "?"
        
        processing_prompt = (
            f"╭━━━〔 🚀 ᴘʀᴏᴄᴇssɪɴɢ - {quality_display}p 〕━━━╮\n"
            f"┃ ⚡ ᴍᴀʟɪᴋ, ᴍᴇʀᴀ ᴋᴀᴀᴍ sʜᴜʀᴜ!\n"
            f"┃ ⏳ *sᴛᴀʀᴛɪɴɢ ᴅᴏᴡɴʟᴏᴀᴅs sʜᴏʀᴛʟʏ...*"
        )
        await editable.edit(processing_prompt)
        try:
            target_batch = (
                f"╭━━━〔 🎯 ᴛᴀʀɢᴇᴛ ʙᴀᴛᴄʜ - {quality_display}p 〕━━━╮\n"
                f"┃ 📦 **{b_name}**"
            )
            await bot.send_message(chat_id=channel_id, text=target_batch)
        except Exception as e:
            fail_prompt = (
                f"╭━━━〔 ⚠️ ғᴀɪʟ ʀᴇᴀsᴏɴ 〕━━━╮\n"
                f"┃ 🚫 `{e}`\n\n"
                f"🌟 ʙᴏᴛ ᴍᴀᴅᴇ ʙʏ @Sᴀʀɢɪᴏ 🌟"
            )
            await m.reply_text(fail_prompt)
            return
        await editable.delete()
        if len(links) == 1:
            count = 1
        else:
            count = int(raw_text)
        mpd = None
        for i in range(count - 1, len(links)):
            V = links[i][1]
            url = "https://" + V
            if "*" in url:
                mpd, keys = url.split("*")
                print(mpd, keys)
            elif "vimeo" in url:
                text = requests.get(url, headers=headers.allen).text
                pattern = r'https://[^/?#]+\.[^/?#]+(?:/[^/?#]+)+\.(?:m3u8)'
                urls = re.findall(pattern, text)
                for url in urls:
                    print(url)
                    break
            elif 'classplusapp.com' in url:
                if '4b06bf8d61c41f8310af9b2624459378203740932b456b07fcf817b737fbae27' in url:
                    pattern = re.compile(r'https://videos\.classplusapp\.com/([a-f0-9]+)/([a-zA-Z0-9]+)\.m3u8')
                    match = pattern.match(url)
                    if match:
                        urlx = f"https://videos.classplusapp.com/b08bad9ff8d969639b2e43d5769342cc62b510c4345d2f7f153bec53be84fe35/{match.group(2)}/{match.group(2)}.m3u8"
                        url = requests.get(f'https://api.classplusapp.com/cams/uploader/video/jw-signed-url?url={urlx}', headers=headers.cp).json()['url']
                else:
                    url = requests.get(f'https://api.classplusapp.com/cams/uploader/video/jw-signed-url?url={url}', headers=headers.cp).json()['url']
            elif '/master.mpd' in url:                
                id =  url.split("/")[-2] 
                policy = requests.post('https://api.penpencil.xyz/v1/files/get-signed-cookie', headers=headers.pw, json={'url': f"https://d1d34p8vz63oiq.cloudfront.net/" + id + "/master.mpd"}).json()['data']
                url = "https://sr-get-video-quality.selav29696.workers.dev/?Vurl=" + "https://d1d34p8vz63oiq.cloudfront.net/" + id + f"/hls/{raw_text2}/main.m3u8" + policy
                print(url)
            elif "visionias" in url:
                async with ClientSession() as session:
                    async with session.get(url, headers=headers.vision) as resp:
                        text = await resp.text()
                        url = re.search(r"(https://*.?playlist.m3u8.?)", text).group(1)
                        print(url)

            # ʀᴇᴍᴏᴠᴇ sᴛᴀʀᴛɪɴɢ ɴᴜᴍʙᴇʀ ғʀᴏᴍ ᴛᴏᴘɪᴄ ɴᴀᴍᴇ
            name1_original = links[i][0].replace("\t", "").replace(":", " ").replace("/", "").replace("+", "").replace("#", "").replace("|", "").replace("@", "").replace("*", "").replace(".", "").replace("https", "").replace("http", "").strip()
            # ʀᴇᴍᴏᴠᴇ ʟᴇᴀᴅɪɴɢ ɴᴜᴍʙᴇʀ(s) ғʀᴏᴍ ᴛᴏᴘɪᴄ
            name1 = re.sub(r'^\d+\s*', '', name1_original)
            name = f'{str(count).zfill(3)}){name1[:60]}'
            
            # ᴋᴀʟᴀᴍ ᴘᴜʙʟɪᴄᴀᴛɪᴏɴ ʜᴀɴᴅʟɪɴɢ
            if "kalampublication" in url:
                ytf = "best"
                cmd = f'yt-dlp -o "{name}.mp4" "{url}" --add-header "User-Agent: okhttp/4.12.0" --add-header "mobilenumber: aDhYejdQcVIyd0IxazlEZg==" --add-header "referer: https://hello-aws-uat.kalampublication.in"'
            elif "youtu" in url:
                ytf = f"b[height<={raw_text2}][ext=mp4]/bv[height<={raw_text2}][ext=mp4]+ba[ext=m4a]/b[ext=mp4]"
            else:
                ytf = f"b[height<={raw_text2}]/bv[height<={raw_text2}]+ba/b/bv+ba"
                
            if "jw-prod" in url:
                cmd = f'yt-dlp -o "{name}.mp4" "{url}"'
            elif "kalampublication" not in url:
                cmd = f'yt-dlp -f "{ytf}" "{url}" -o "{name}.mp4"'    
                
            try:
                # ᴄᴜsᴛᴏᴍ sᴛʏʟɪsʜ ᴜɪ ғᴏʀ ᴠɪᴅᴇᴏ ᴅᴇᴛᴀɪʟs
                cc = (
                    f"╭━━━〔 🎓 ᴠɪᴅᴇᴏ ᴅᴇᴛᴀɪʟs - {raw_text2}p 〕━━━╮\n"
                    f"┃ 🔢 ɪᴅ ➠ {str(count).zfill(3)}\n"
                    f"┃ 📚 ᴛᴏᴘɪᴄ ➠ {name1}\n"
                    f"┃ 🏷️ ǫᴜᴀʟɪᴛʏ ➠ {raw_text2}\n"
                    f"┃ 📦 ʙᴀᴛᴄʜ ➠ {b_name}\n"
                    f"┃ 📱 ᴀᴘᴘ ➠ {app_name}\n\n"
                    f"🎥 ғɪʟᴇ ➠ {name1} [{raw_text2}].ᴍᴋᴠ\n\n"
                    f"⚡ ᴅᴏᴡɴ ʙʏ ➠ {MR}"
                )

                # ᴄᴜsᴛᴏᴍ sᴛʏʟɪsʜ ᴜɪ ғᴏʀ ᴘᴅғ ᴅᴇᴛᴀɪʟs
                cc1 = (
                    f"╭━━━〔 📄 ᴘᴅғ ᴅᴇᴛᴀɪʟs - {raw_text2}p 〕━━━╮\n"
                    f"┃ 🔢 ɪᴅ ➠ {str(count).zfill(3)}\n"
                    f"┃ 📚 ᴛᴏᴘɪᴄ ➠ {name1}\n"
                    f"┃ 📦 ʙᴀᴛᴄʜ ➠ {b_name}\n"
                    f"┃ 📱 ᴀᴘᴘ ➠ {app_name}\n\n"
                    f"📄 ғɪʟᴇ ➠ {name1}.ᴘᴅғ\n\n"
                    f"⚡ ᴅᴏᴡɴ ʙʏ ➠ {MR}"
                )                 

                if "drive" in url or ".pdf" in url or "pdfs" in url:
                    try:
                        cmd = f'yt-dlp -o "{name}.pdf" "{url}"'
                        download_cmd = f"{cmd} -R 25 --fragment-retries 25"
                        os.system(download_cmd)
                        await bot.send_document(chat_id=channel_id, document=f'{name}.pdf', caption=cc1)
                        count += 1
                        os.remove(f'{name}.pdf')
                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        continue

                elif mpd and keys:
                    Show = (
                        f"╭━━━〔 ⏳ ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ - {raw_text2}p 〕━━━╮\n"
                        f"┃ 🎥 ɴᴀᴍᴇ ➠ `{name}`\n"
                        f"┃ 🏷️ ǫᴜᴀʟɪᴛʏ ➠ `{raw_text2}p`\n\n"
                        f"⏰ ʙᴏᴛ ᴍᴀᴅᴇ ʙʏ 『Sᴀʀɢɪᴏ』"
                    )
                    prog = await bot.send_message(channel_id, Show)
                    await helper.download_and_dec_video(mpd, keys, path, name, raw_text2)
                    await prog.delete(True)
                    await helper.merge_and_send_vid(bot, m, cc, name, prog, path, url, thumb,channel_id)
                    count += 1
                    await asyncio.sleep(0.5)
                else:
                    mpd = None
                    Show = (
                        f"╭━━━〔 ⏳ ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ - {raw_text2}p 〕━━━╮\n"
                        f"┃ 🎥 ɴᴀᴍᴇ ➠ `{name}`\n"
                        f"┃ 🏷️ ǫᴜᴀʟɪᴛʏ ➠ `{raw_text2}p`\n\n"
                        f"⏰ ʙᴏᴛ ᴍᴀᴅᴇ ʙʏ 『Sᴀʀɢɪᴏ』"
                    )
                    prog = await bot.send_message(channel_id, Show)
                    
                    if "kalampublication" in url:
                        res_file = await helper.download_kalam_video(url, name)
                    else:
                        res_file = await helper.download_video(url, cmd, name)
                        
                    filename = res_file
                    await prog.delete(True)
                    await helper.send_vid(bot, m, cc, filename, thumb, name, prog, url, channel_id)
                    count += 1
                    await asyncio.sleep(0.5)

            except Exception as e:
                continue
        try:
            success_done = (
                f"╭━━━〔 🌟 sᴜᴄᴄᴇss - {raw_text2}p 〕━━━╮\n"
                f"┃ 🎉 ᴀʟʟ ʟᴇᴄᴛᴜʀᴇs ᴅᴏᴡɴʟᴏᴀᴅᴇᴅ!"
            )
            await bot.send_message(channel_id, success_done)
        except FloodWait as fw:
            await asyncio.sleep(fw.value)
            await bot.send_message(channel_id, success_done)
    except FloodWait as fw:
        await asyncio.sleep(fw.value)
        try:
            await m.reply_text(f"**⚠️ᴛᴀsᴋ ᴄᴏᴍᴘʟᴇᴛᴇᴅ ᴡɪᴛʜ sᴏᴍᴇ ɪssᴜᴇs⚠️**")
        except:
            pass
        return
    except Exception as e:
        try:
            await m.reply_text(f"**⚠️sᴏʀʀʏ ʙᴏss⚠️**\n\n**ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ, ᴘʟᴇᴀsᴇ ᴛʀʏ ᴀɢᴀɪɴ**")
        except:
            pass
        return

bot.run()
