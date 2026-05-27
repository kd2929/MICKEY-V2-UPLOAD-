from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
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

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.getLogger("pyrogram").setLevel(logging.WARNING)

# ========== CHANGE THIS ==========
ADMIN_CHANNEL = "https://t.me/+C342HY3uQco0NDc9"  # 🔴 Replace with your channel link
# =================================

# ========== PRE-FORMATTED MESSAGES ==========

START_MSG = (
    "╭─〔 🌟 SYSTEM 〕─╮\n"
    "│ 👤 Hello, Sargio\n"
    "│ ⚡ Running Smooth\n"
    "│ 🛠️ /master\n"
    "├───────────────\n"
    "│ 📥 SUPPORT\n"
    "│ • DRM / Non-DRM\n"
    "│ • MPD / IAS\n"
    "│ • PW / ClassPlus\n"
    "│ • Allen / Kalam\n"
    "╰───────────────╯"
)

MASTER_PROMPT = (
    "╭─〔 🗂️ MASTER 〕─╮\n"
    "│ 📥 Send .txt File\n"
    "│ ✉️ Or Send Links\n"
    "╰───────────────╯"
)

BATCH_PROMPT = (
    "╭─〔 📦 BATCH 〕─╮\n"
    "│ 📝 Enter Name\n"
    "│ ⚡ /d = auto\n"
    "╰───────────────╯"
)

APP_PROMPT = (
    "╭─〔 📱 APP 〕─╮\n"
    "│ 💬 Enter App Name\n"
    "╰───────────────╯"
)

RES_PROMPT = (
    "╭─〔 ⚙️ RES 〕─╮\n"
    "│ 📺 360 / 480 / 720\n"
    "╰───────────────╯"
)

CREDITS_PROMPT = (
    "╭─〔 👑 CREDITS 〕─╮\n"
    "│ 🏷️ Enter Name\n"
    "╰───────────────╯"
)

THUMB_PROMPT = (
    "╭─〔 🖼️ THUMB 〕─╮\n"
    "│ 🌐 Send URL\n"
    "│ ❌ no = skip\n"
    "╰───────────────╯"
)

CHANNEL_PROMPT = (
    "╭─〔 📢 CHANNEL 〕─╮\n"
    "│ 🆔 Send Channel ID\n"
    "│ ⚡ /d = current\n"
    "╰───────────────╯"
)

PROCESSING_MSG = (
    "╭─〔 🚀 PROCESS 〕─╮\n"
    "│ ⚡ Starting...\n"
    "╰───────────────╯"
)

SUCCESS_MSG = (
    "╭─〔 🎉 DONE 〕─╮\n"
    "│ ✅ All Completed\n"
    "╰───────────────╯"
)

RESTART_MSG = (
    "╭─〔 🔴 RESTART 〕─╮\n"
    "│ 🔄 Restarting...\n"
    "╰───────────────╯"
)

ADMIN_BUTTON = InlineKeyboardMarkup([
    [InlineKeyboardButton("🔑 Contact Admin", url=ADMIN_CHANNEL)]
])

# ========== DYNAMIC MESSAGES WITH QUOTES ==========

def access_denied_msg(chat_id):
    return (
        f"╭─〔 ⚠️ DENIED 〕─╮\n"
        f"│ 🚫 Not Premium\n"
        f"│ 🆔 `{chat_id}`\n"
        f"├───────────────\n"
        f"│ 💬 Upgrade Now\n"
        f"╰───────────────╯"
    )

def links_found_msg(total):
    return (
        f"╭─〔 🔗 LINKS 〕─╮\n"
        f"│ 📊 Total ➤ `{total}`\n"
        f"╰───────────────╯\n\n"
        f"🔢 Send Start Index:"
    )

def target_batch_msg(b_name):
    return (
        f"╭─〔 🎯 BATCH 〕─╮\n"
        f"│ 📦 `{b_name}`\n"
        f"╰───────────────╯"
    )

def downloading_msg(name, quality):
    return (
        f"╭─〔 ⏳ DOWNLOAD 〕─╮\n"
        f"│ 🎥 `{name}`\n"
        f"│ 📺 `{quality}p`\n"
        f"╰───────────────╯"
    )

def video_caption(count, name1, quality, b_name):
    # Shorten if too long
    title_display = name1[:45] if len(name1) > 45 else name1
    batch_display = b_name[:20] if len(b_name) > 20 else b_name
    
    return (
        f"╭─〔 🎥 VIDEO 〕─╮\n"
        f"│ 🔢 {str(count).zfill(3)}\n"
        f"│ 📗 `{title_display}`\n"
        f"│ 🎬 `{quality}` 📦 `{batch_display}`\n"
        f"╰───────────────╯\n"
        f"🎥 `{title_display} [{quality}].mkv`\n\n"
        f"⚡ 『sargio』"
    )

def pdf_caption(count, name1, b_name):
    title_display = name1[:45] if len(name1) > 45 else name1
    batch_display = b_name[:20] if len(b_name) > 20 else b_name
    
    return (
        f"╭─〔 📄 PDF 〕─╮\n"
        f"│ 🔢 {str(count).zfill(3)}\n"
        f"│ 📗 `{title_display}`\n"
        f"│ 📦 `{batch_display}`\n"
        f"╰───────────────╯\n"
        f"📄 `{title_display}.pdf`\n\n"
        f"⚡ 『sargio』"
    )


# ========== BOT COMMANDS ==========

@bot.on_message(filters.command(["start"]))
async def start_cmd(bot: Client, m: Message):
    await m.reply_text(START_MSG, reply_markup=ADMIN_BUTTON)

@bot.on_message(filters.command("stop"))
async def restart_handler(bot, m):
    if m.chat.id not in Config.VIP_USERS:
        await m.reply_text(access_denied_msg(m.chat.id), reply_markup=ADMIN_BUTTON)
        return
    await m.reply_text(RESTART_MSG, True)
    os.execl(sys.executable, sys.executable, *sys.argv)

@bot.on_message(filters.command(["master"]))
async def master_cmd(bot: Client, m: Message):
    # Premium check
    if m.chat.id not in Config.VIP_USERS:
        await m.reply_text(access_denied_msg(m.chat.id), reply_markup=ADMIN_BUTTON)
        return

    try:
        status_msg = await m.reply_text("⏳ **Initializing...**")
        
        await status_msg.edit(MASTER_PROMPT)
        input_msg: Message = await bot.listen(m.chat.id)
        
        path = f"./downloads/{m.chat.id}"
        temp_dir = "./temp"
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        os.makedirs(temp_dir)
        
        file_name = "batch"
        if input_msg.document:
            x = await input_msg.download()
            await input_msg.delete(True)
            file_name = os.path.splitext(os.path.basename(x))[0]
            with open(x, "r") as f:
                content = f.read()
            links = [i.split("://", 1) for i in content.split("\n") if i.strip()]
            os.remove(x)
        else:
            content = input_msg.text
            links = [i.split("://", 1) for i in content.split("\n") if i.strip()]
            await input_msg.delete(True)
        
        await status_msg.edit(links_found_msg(len(links)))
        input0: Message = await bot.listen(m.chat.id)
        start_index = int(input0.text) if input0.text.isdigit() else 1
        await input0.delete(True)
        
        await status_msg.edit(BATCH_PROMPT)
        input1: Message = await bot.listen(m.chat.id)
        b_name = file_name if input1.text == '/d' else input1.text
        await input1.delete(True)
        
        await status_msg.edit(APP_PROMPT)
        input111: Message = await bot.listen(m.chat.id)
        app_name = input111.text
        await input111.delete(True)
        
        await status_msg.edit(RES_PROMPT)
        input2: Message = await bot.listen(m.chat.id)
        quality = input2.text
        await input2.delete(True)
        
        await status_msg.edit(CREDITS_PROMPT)
        input3: Message = await bot.listen(m.chat.id)
        credits = "『sargio』" if input3.text == 'de' else input3.text
        await input3.delete(True)
        
        await status_msg.edit(THUMB_PROMPT)
        input6: Message = await bot.listen(m.chat.id)
        thumb = input6.text
        await input6.delete(True)
        
        await status_msg.edit(CHANNEL_PROMPT)
        input7: Message = await bot.listen(m.chat.id)
        channel_id = m.chat.id if "/d" in input7.text else int(input7.text)
        await input7.delete(True)
        
        await status_msg.edit(PROCESSING_MSG)
        
        try:
            await bot.send_message(chat_id=channel_id, text=target_batch_msg(b_name))
        except Exception as e:
            await m.reply_text(f"╭─〔 ⚠️ ERROR 〕─╮\n│ 🚫 `{e}`\n╰───────────────╯")
            return
        
        await status_msg.delete()
        
        count = start_index
        mpd = None
        
        for i in range(count - 1, len(links)):
            V = links[i][1]
            url = "https://" + V
            
            if "*" in url:
                mpd, keys = url.split("*")
            elif "classplusapp.com" in url:
                if '4b06bf8d61c41f8310af9b2624459378203740932b456b07fcf817b737fbae27' in url:
                    pattern = re.compile(r'https://videos\.classplusapp\.com/([a-f0-9]+)/([a-zA-Z0-9]+)\.m3u8')
                    match = pattern.match(url)
                    if match:
                        urlx = f"https://videos.classplusapp.com/b08bad9ff8d969639b2e43d5769342cc62b510c4345d2f7f153bec53be84fe35/{match.group(2)}/{match.group(2)}.m3u8"
                        url = requests.get(f'https://api.classplusapp.com/cams/uploader/video/jw-signed-url?url={urlx}', headers=headers.cp).json()['url']
                else:
                    url = requests.get(f'https://api.classplusapp.com/cams/uploader/video/jw-signed-url?url={url}', headers=headers.cp).json()['url']
            elif '/master.mpd' in url:                
                id = url.split("/")[-2] 
                policy = requests.post('https://api.penpencil.xyz/v1/files/get-signed-cookie', headers=headers.pw, json={'url': f"https://d1d34p8vz63oiq.cloudfront.net/" + id + "/master.mpd"}).json()['data']
                url = "https://sr-get-video-quality.selav29696.workers.dev/?Vurl=" + "https://d1d34p8vz63oiq.cloudfront.net/" + id + f"/hls/{quality}/main.m3u8" + policy
            elif "visionias" in url:
                async with ClientSession() as session:
                    async with session.get(url, headers=headers.vision) as resp:
                        text = await resp.text()
                        url = re.search(r"(https://*.?playlist.m3u8.?)", text).group(1)
            
            name1 = links[i][0].replace("\t", "").replace(":", " ").replace("/", "").replace("+", "").replace("#", "").replace("|", "").replace("@", "").replace("*", "").replace(".", "").replace("https", "").replace("http", "").strip()
            name = f'{str(count).zfill(3)}){name1[:60]}'
            
            if "youtu" in url:
                ytf = f"b[height<={quality}][ext=mp4]/bv[height<={quality}][ext=mp4]+ba[ext=m4a]/b[ext=mp4]"
            else:
                ytf = f"b[height<={quality}]/bv[height<={quality}]+ba/b/bv+ba"
            
            if "kalampublication" in url:
                cmd = f'yt-dlp -o "{name}.mp4" "{url}" --add-header "User-Agent: okhttp/4.12.0" --add-header "mobilenumber: aDhYejdQcVIyd0IxazlEZg==" --add-header "referer: https://hello-aws-uat.kalampublication.in"'
            elif "jw-prod" in url:
                cmd = f'yt-dlp -o "{name}.mp4" "{url}"'
            else:
                cmd = f'yt-dlp -f "{ytf}" "{url}" -o "{name}.mp4"'
            
            try:
                if "drive" in url or ".pdf" in url or "pdfs" in url:
                    cmd = f'yt-dlp -o "{name}.pdf" "{url}"'
                    os.system(f"{cmd} -R 25 --fragment-retries 25")
                    await bot.send_document(chat_id=channel_id, document=f'{name}.pdf', caption=pdf_caption(count, name1, b_name))
                    os.remove(f'{name}.pdf')
                
                elif mpd and keys:
                    prog = await bot.send_message(channel_id, downloading_msg(name, quality))
                    await helper.download_and_dec_video(mpd, keys, path, name, quality)
                    await prog.delete()
                    await helper.merge_and_send_vid(bot, m, video_caption(count, name1, quality, b_name), name, prog, path, url, thumb, channel_id)
                
                else:
                    prog = await bot.send_message(channel_id, downloading_msg(name, quality))
                    if "kalampublication" in url:
                        res_file = await helper.download_kalam_video(url, name)
                    else:
                        res_file = await helper.download_video(url, cmd, name)
                    await prog.delete()
                    await helper.send_vid(bot, m, video_caption(count, name1, quality, b_name), res_file, thumb, name, prog, url, channel_id)
                
                count += 1
                await asyncio.sleep(0.3)
                
            except Exception as e:
                continue
        
        await bot.send_message(channel_id, SUCCESS_MSG)
        
    except FloodWait as fw:
        await asyncio.sleep(fw.value)
    except Exception as e:
        try:
            await m.reply_text(f"╭─〔 ⚠️ ERROR 〕─╮\n│ 🚫 Failed\n╰───────────────╯")
        except:
            pass

bot.run()
