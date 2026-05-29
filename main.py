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
        f"╭━━━〔 🌟 𝙎𝙔𝙎𝙏𝙀𝙈 𝘼𝘾𝙏𝙄𝙑𝙀 〕━━━╮\n"
        f"┃ 👤 𝙃𝙚𝙡𝙡𝙤, 𝙈𝙖𝙨𝙩𝙚𝙧!\n"
        f"┃ 🟢 𝙎𝙩𝙖𝙩𝙪𝙨 ➠ 𝙍𝙪𝙣𝙣𝙞𝙣𝙜 𝙎𝙢𝙤𝙤𝙩𝙝𝙡𝙮 ⚡\n"
        f"┃ 🛠️ 𝘾𝙤𝙢𝙢𝙖𝙣𝙙 ➠ /master\n"
        f"╰━━━━━━━━━━━━━━━━━━━━━━━━━━━━╯\n\n"
        f"📥 𝙎𝙪𝙥𝙥𝙤𝙧𝙩𝙚𝙙 𝙐𝙍𝙇𝙨 ➠\n"
        f"├• 𝘼𝙡𝙡 𝙉𝙤𝙣-𝘿𝙍𝙈 + 𝘿𝙍𝙈 𝙋𝙧𝙤𝙩𝙚𝙘𝙩𝙚𝙙\n"
        f"├• 𝙈𝙥𝙚𝙜 𝘿𝙖𝙨𝙝 / 𝙑𝙞𝙨𝙞𝙤𝙣 𝙄𝘼𝙎\n"
        f"├• 𝙋𝙝𝙮𝙨𝙞𝙘𝙨𝙒𝙖𝙡𝙡𝙖𝙝 / 𝘾𝙡𝙖𝙨𝙨𝙋𝙡𝙪𝙨\n"
        f"├• 𝘼𝙡𝙡𝙚𝙣 / 𝙆𝙖𝙡𝙖𝙢 𝙋𝙪𝙗𝙡𝙞𝙘𝙖𝙩𝙞𝙤𝙣\n\n"
        f"⚡ 𝘿𝙚𝙫𝙚𝙡𝙤𝙥𝙚𝙧 ➠ @Sargio"
    )
    await m.reply_text(start_msg)

@bot.on_message(filters.command("stop"))
async def restart_handler(bot, m):
    if m.chat.id not in Config.VIP_USERS:
        print(f"User ID not in AUTH_USERS", m.chat.id)
        access_denied = (
            f"╭━━━〔 ⚠️ 𝘼𝘾𝘾𝙀𝙎𝙎 𝘿𝙀𝙉𝙄𝙀𝘿 〕━━━╮\n"
            f"┃ 🚫 𝙔𝙤𝙪 𝙖𝙧𝙚 𝙣𝙤𝙩 𝙖 𝙋𝙧𝙚𝙢𝙞𝙪𝙢 𝙈𝙚𝙢𝙗𝙚𝙧!\n"
            f"┃ 🔑 𝙔𝙤𝙪𝙧 𝙄𝘿 ➠ `{m.chat.id}`\n"
            f"┃ 📝 𝙐𝙥𝙜𝙧𝙖𝙙𝙚 ➠ Send ID to admin\n"
            f"╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯\n\n"
            f"💬 *Please upgrade your plan to unlock.*"
        )
        await bot.send_message(m.chat.id, access_denied)
        return
    
    stop_msg = (
        f"╭━━━〔 🚦 𝙎𝙔𝙎𝙏𝙀𝙈 𝙎𝙏𝙊𝙋𝙋𝙀𝘿 〕━━━╮\n"
        f"┃ 🔴 𝘽𝙤𝙩 𝙞𝙨 𝙧𝙚𝙨𝙩𝙖𝙧𝙩𝙞𝙣𝙜 𝙣𝙤𝙬...\n"
        f"╰━━━━━━━━━━━━━━━━━━━━━━━━━━━━╯"
    )
    await m.reply_text(stop_msg, True)
    os.execl(sys.executable, sys.executable, *sys.argv)

@bot.on_message(filters.command(["master"]))
async def account_login(bot: Client, m: Message):
    try:
        master_prompt = (
            f"╭━━━〔 🗂️ 𝙈𝘼𝙎𝙏𝙀𝙍 𝙎𝙀𝙏𝙐𝙋 〕━━━╮\n"
            f"┃ 📥 𝙎𝙚𝙣𝙙 𝙈𝙖𝙨𝙩𝙚𝙧 .𝙏𝙓𝙏 𝙁𝙞𝙡𝙚\n"
            f"┃ ✉️ *Or send direct links as text!*\n"
            f"╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯"
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
                    f"╭━━━〔 ⚠️ 𝙀𝙍𝙍𝙊𝙍 〕━━━╮\n"
                    f"┃ 🚫 Failed to process file!\n"
                    f"┃ 📝 `{e}`\n"
                    f"╰━━━━━━━━━━━━━━━━━━╯"
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
            f"╭━━━〔 🔗 𝙇𝙄𝙉𝙆𝙎 𝙁𝙊𝙐𝙉𝘿 〕━━━╮\n"
            f"┃ 📊 𝙏𝙤𝙩𝙖𝙡 𝙇𝙞𝙣𝙠𝙨 ➠ `{len(links)}`\n"
            f"╰━━━━━━━━━━━━━━━━━━━━━━━━━━╯\n\n"
            f"🔢 *Send from where you want to start (Default is 1):*"
        )
        await editable.edit(links_found)
        
        if m.chat.id not in Config.VIP_USERS:
            print(f"User ID not in AUTH_USERS", m.chat.id)
            access_denied = (
                f"╭━━━〔 ⚠️ 𝘼𝘾𝘾𝙀𝙎𝙎 𝘿𝙀𝙉𝙄𝙀𝘿 〕━━━╮\n"
                f"┃ 🚫 𝙔𝙤𝙪 𝙖𝙧𝙚 𝙣𝙤𝙩 𝙖 𝙋𝙧𝙚𝙢𝙞𝙪𝙢 𝙈𝙚𝙢𝙗𝙚𝙧!\n"
                f"┃ 🔑 𝙔𝙤𝙪𝙧 𝙄𝘿 ➠ `{m.chat.id}`\n"
                f"┃ 📝 𝙐𝙥𝙜𝙧𝙖𝙙𝙚 ➠ Send ID to admin\n"
                f"╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯"
            )
            await bot.send_message(m.chat.id, access_denied)
            return
            
        input0: Message = await bot.listen(editable.chat.id)
        raw_text = input0.text
        await input0.delete(True)

        batch_prompt = (
            f"╭━━━〔 📦 𝘽𝘼𝙏𝘾𝙃 𝙎𝙀𝙏𝙐𝙋 〕━━━╮\n"
            f"┃ 📝 𝙀𝙣𝙩𝙚𝙧 𝘽𝙖𝙩𝙘𝙝 𝙉𝙖𝙢𝙚\n"
            f"┃ 🧭 *Or send /d to auto-grab file name*\n"
            f"╰━━━━━━━━━━━━━━━━━━━━━━━━━━╯"
        )
        await editable.edit(batch_prompt)
        input1: Message = await bot.listen(editable.chat.id)
        raw_text0 = input1.text
        await input1.delete(True)
        if raw_text0 == '/d':
            b_name = file_name
        else:
            b_name = raw_text0
            
        app_prompt = (
            f"╭━━━〔 📱 𝘼𝙋𝙋 𝙎𝙀𝙏𝙐𝙋 〕━━━╮\n"
            f"┃ 💬 𝙀𝙣𝙩𝙚𝙧 𝘼𝙥𝙥 𝙉𝙖𝙢𝙚\n"
            f"╰━━━━━━━━━━━━━━━━━━━━━━━━╯"
        )
        await editable.edit(app_prompt)
        input111: Message = await bot.listen(editable.chat.id)
        app_name = input111.text
        await input111.delete(True)

        res_prompt = (
            f"╭━━━〔 ⚙️ 𝙍𝙀𝙎𝙊𝙇𝙐𝙏𝙄𝙊𝙉 〕━━━╮\n"
            f"┃ 📺 𝙀𝙣𝙩𝙚𝙧 𝙑𝙞𝙙𝙚ο 𝙌𝙪𝙖𝙡𝙞𝙩𝙮\n"
            f"┃ 💡 *Eg: 360 | 480 | 720*\n"
            f"╰━━━━━━━━━━━━━━━━━━━━━━━━╯"
        )
        await editable.edit(res_prompt)
        input2: Message = await bot.listen(editable.chat.id)
        raw_text2 = input2.text
        await input2.delete(True)

        credits_prompt = (
            f"╭━━━〔 👑 𝘾𝙍𝙀𝘿𝙄𝙏𝙎 𝙎𝙀𝙏𝙐𝙋 〕━━━╮\n"
            f"┃ 🏷️ 𝙀𝙣𝙩𝙚𝙧 𝙔𝙤𝙪𝙧 𝙉𝙖𝙢𝙚 / 𝘽𝙮\n"
            f"┃ 💡 *Eg: 『ᎷΔŞŦᏋ🇷』❤️*\n"
            f"╰━━━━━━━━━━━━━━━━━━━━━━━━━━╯"
        )
        await editable.edit(credits_prompt)
        input3: Message = await bot.listen(editable.chat.id)
        raw_text3 = input3.text
        await input3.delete(True)
        if raw_text3 == 'de':
            MR = "Sargio ❤️"
        else:               
            MR = raw_text3
    
        thumb_prompt = (
            f"╭━━━〔 🖼️ 𝙏𝙃𝙐𝙈𝘽𝙉𝘼𝙄𝙇 〕━━━╮\n"
            f"┃ 🌐 𝙎𝙚𝙣𝙙 𝙏𝙝𝙪𝙢𝙗𝙣𝙖𝙞𝙡 𝙐𝙍𝙇\n"
            f"┃ 🚫 *Or type 'no' to skip*\n"
            f"╰━━━━━━━━━━━━━━━━━━━━━━━━╯"
        )
        await editable.edit(thumb_prompt)
        input6: Message = await bot.listen(editable.chat.id)
        thumb = input6.text
        await input6.delete(True)
        
        channel_prompt = (
            f"╭━━━〔 📢 𝙐𝙋𝙇𝙊𝘼𝘿 𝙏𝘼𝙍𝙂𝙀𝙏 〕━━━╮\n"
            f"┃ 🆔 𝙎𝙚𝙣𝙙 𝘾𝙝𝙖𝙣𝙣𝙚𝙡 𝙄𝘿\n"
            f"┃ 🧭 *Or send /d to use current chat*\n"
            f"╰━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╯\n\n"
            f"⚠️ *Note: Make sure to add Bot as admin!*"
        )
        await editable.edit(channel_prompt)
        input7: Message = await bot.listen(editable.chat.id)
        if "/d" in input7.text:
            channel_id = m.chat.id
        else:
            channel_id = input7.text
        await input7.delete()

        processing_prompt = (
            f"╭━━━〔 🚀 𝙋𝙍𝙊𝘾𝙀𝙎𝙎𝙄𝙉加 〕━━━╮\n"
            f"┃ ⚡ 𝙈𝙖𝙡𝙞𝙠, 𝙈𝙚𝙧𝙖 𝙆𝙖𝙖𝙢 𝙎𝙝𝙪𝙧𝙪!\n"
            f"┃ ⏳ *Starting downloads shortly...*\n"
            f"╰━━━━━━━━━━━━━━━━━━━━━━━━━╯"
        )
        await editable.edit(processing_prompt)
        try:
            target_batch = (
                f"╭━━━〔 🎯 𝙏𝘼𝙍𝙂𝙀𝙏 𝘽𝘼𝙏𝘾𝙃 〕━━━╮\n"
                f"┃ 📦 **{b_name}**\n"
                f"╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯"
            )
            await bot.send_message(chat_id=channel_id, text=target_batch)
        except Exception as e:
            fail_prompt = (
                f"╭━━━〔 ⚠️ 𝙁𝘼𝙄𝙇 𝙍𝙀𝘼𝙎𝙊𝙉 〕━━━╮\n"
                f"┃ 🚫 `{e}`\n"
                f"╰━━━━━━━━━━━━━━━━━━━━━━━━━━╯\n\n"
                f"🌟 Bot Made By @Sargio 🌟"
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

            name1 = links[i][0].replace("\t", "").replace(":", " ").replace("/", "").replace("+", "").replace("#", "").replace("|", "").replace("@", "").replace("*", "").replace(".", "").replace("https", "").replace("http", "").strip()
            name = f'{str(count).zfill(3)}){name1[:60]}'
            
            # Kalam Publication handling
            if "kalampublication" in url:
                ytf = "best"
                cmd = f'yt-dlp -o "{name}.mp4" "{url}" --add-header "User-Agent: okhttp/4.12.0" --add-header "mobilenumber: aDhYejdQcVIyd0IxazlEZg==" --add-header "referer: https://hello-aws-uat.kalampublication.in"'
            elif "youtu" in url:
                ytf = f"b[height<={raw_text2}][ext=mp4]/bv[height<={raw_text2}][ext=mp4]+ba[ext=m4a]/b[ext=mp4]"
            else:
                ytf = f"b[height<={raw_text2}]/bv[height<={raw_text2}]+ba/b/bv+ba"
                
            if "jw-prod" in url:
                cmd = f'yt-dlp -o "{name}.mp4" "{url}"'
            elif "kalampublication" not in url:  # Don't override Kalam command
                cmd = f'yt-dlp -f "{ytf}" "{url}" -o "{name}.mp4"'    
                
            try:
                # Custom Stylish UI for Video Details
                cc = (
                    f"╭━━━〔 🎓 𝙑𝙄𝘿𝙀𝙊 𝘿𝙀𝙏𝘼𝙄𝙇𝙎 〕━━━╮\n"
                    f"┃ 🔢 𝙄𝘿 ➠ {str(count).zfill(3)}\n"
                    f"┃ 📚 𝙏𝙤𝙥𝙞𝙘 ➠ {name1}\n"
                    f"┃ 🏷️ 𝙏𝙞𝙩𝙡𝙚 ➠ {raw_text2}\n"
                    f"┃ 📦 𝘽𝙖𝙩𝙘𝙝 ➠ {b_name}\n"
                    f"┃ 📱 𝘼𝙥𝙥 ➠ {app_name}\n"
                    f"╰━━━━━━━━━━━━━━━━━━━╯\n\n"
                    f"🎥 𝙁𝙞𝙡𝙚 ➠ {name1} [{raw_text2}].mkv\n\n"
                    f"⚡ 𝘿𝙤𝙬𝙣 𝘽𝙮 ➠ {MR}"
                )

                # Custom Stylish UI for PDF Details
                cc1 = (
                    f"╭━━━〔 📄 𝙋𝘿𝙁 𝘿𝙀𝙏𝘼𝙄𝙇𝙎 〕━━━╮\n"
                    f"┃ 🔢 𝙄𝘿 ➠ {str(count).zfill(3)}\n"
                    f"┃ 📚 𝙏𝙤𝙥𝙞𝙘 ➠ {name1}\n"
                    f"┃ 📦 𝘽𝙖𝙩𝙘𝙝 ➠ {b_name}\n"
                    f"┃ 📱 𝘼𝙥𝙥 ➠ {app_name}\n"
                    f"╰━━━━━━━━━━━━━━━━━━━╯\n\n"
                    f"📄 𝙁𝙞𝙡𝙚 ➠ {name1}.pdf\n\n"
                    f"⚡ 𝘿𝙤𝙬𝙣 𝘽𝙮 ➠ {MR}"
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
                        f"╭━━━〔 ⏳ 𝘿𝙊𝙒𝙉𝙇𝙊𝘼𝘿𝙄𝙉𝙂 〕━━━╮\n"
                        f"┃ 🎥 𝙉𝙖𝙢𝙚 ➠ `{name}`\n"
                        f"┃ 🏷️ 𝙌𝙪𝙖𝙡𝙞𝙩𝙮 ➠ `{raw_text2}p`\n"
                        f"╰━━━━━━━━━━━━━━━━━━━━━━━━━━╯\n"
                        f"⏰ Bot Made By 『sargio』"
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
                        f"╭━━━〔 ⏳ 𝘿𝙊𝙒𝙉𝙇𝙊𝘼𝘿𝙄𝙉𝙂 〕━━━╮\n"
                        f"┃ 🎥 𝙉𝙖𝙢𝙚 ➠ `{name}`\n"
                        f"┃ 🏷️ 𝙌𝙪𝙖𝙡𝙞𝙩𝙮 ➠ `{raw_text2}p`\n"
                        f"╰━━━━━━━━━━━━━━━━━━━━━━━━━━╯\n"
                        f"⏰ Bot Made By 『sargio』"
                    )
                    prog = await bot.send_message(channel_id, Show)
                    
                    # Use special function for Kalam videos
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
                f"╭━━━〔 🌟 𝙎𝙐𝘾𝘾𝙀𝙎𝙎 〕━━━╮\n"
                f"┃ 🎉 𝘼𝙡𝙡 𝙇𝙚𝙘𝙩𝙪𝙧𝙚𝙨 𝘿𝙤𝙬𝙣𝙡𝙤𝙖𝙙𝙚𝙙!\n"
                f"╰━━━━━━━━━━━━━━━━━━━━━╯"
            )
            await bot.send_message(channel_id, success_done)
        except FloodWait as fw:
            await asyncio.sleep(fw.value)
            await bot.send_message(channel_id, success_done)
    except FloodWait as fw:
        await asyncio.sleep(fw.value)
        try:
            await m.reply_text(f"**⚠️Task Completed with some issues⚠️**")
        except:
            pass
        return
    except Exception as e:
        try:
            await m.reply_text(f"**⚠️Sorry Boss⚠️**\n\n**Error occurred, please try again**")
        except:
            pass
        return

bot.run()
