from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait
from pyromod import listen
from aiohttp import ClientSession
from config import Config
import helper
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
logging.getLogger("pyrogram").setLevel(logging.INFO)

BRAND = "[Mrsargio](https://t.me/Mrsargio)"


def is_pdf_url(url):
    url_lower = url.lower()
    return url_lower.endswith(".pdf") or ".pdf" in url_lower or "pdfs" in url_lower


def make_channel_link(channel_id, message_id):
    try:
        cid = str(channel_id)
        if cid.startswith("-100"):
            cid = cid[4:]
        elif cid.startswith("-"):
            cid = cid[1:]
        return f"https://t.me/c/{cid}/{message_id}"
    except Exception:
        return None


def override_quality_in_url(url, quality):
    for q in ["144", "240", "360", "480", "720", "1080"]:
        url = url.replace(f"play_{q}p", f"play_{quality}p")
        url = url.replace(f"_{q}p.", f"_{quality}p.")
        url = url.replace(f"/{q}p/", f"/{quality}p/")
    return url


# ── /start ────────────────────────────────────────────────────────────────────
@bot.on_message(filters.command(["start"]))
async def start_handler(bot: Client, m: Message):
    await m.reply_text(
        f"╭━━〔 🚀 MICKEY V2 〕━━╮\n"
        f"┃ ⚡ Fast • Secure • Premium\n"
        f"┃ 🎯 Multi Platform Downloader\n"
        f"╰━━━━━━━━━━━━━━╯\n\n"
        f"📥 Send TXT File or Links To Start\n\n"
        f"👑 {BRAND}",
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("⚡ START DOWNLOADING ⚡", callback_data="start_master")]
        ])
    )


@bot.on_callback_query(filters.regex("^start_master$"))
async def start_master_callback(client: Client, cb):
    await cb.answer()
    await run_master(client, cb.message, cb.from_user.id, cb.message.chat.id)


# ── /stop ─────────────────────────────────────────────────────────────────────
@bot.on_message(filters.command("stop"))
async def restart_handler(bot, m):
    if m.chat.id not in Config.VIP_USERS:
        await m.reply_text(
            f"╭━━〔 ❌ ACCESS DENIED 〕━━╮\n"
            f"┃ 🆔 `{m.chat.id}`\n"
            f"┃ 🚫 Premium Access Required\n"
            f"╰━━━━━━━━━━━━━━╯\n\n"
            f"👑 {BRAND}",
            disable_web_page_preview=True
        )
        return
    await m.reply_text(f"🔄 Restarting...", disable_web_page_preview=True)
    os.execl(sys.executable, sys.executable, *sys.argv)


# ── Shared master logic ───────────────────────────────────────────────────────
async def run_master(bot: Client, m: Message, user_id: int, chat_id: int):
    try:
        if user_id not in Config.VIP_USERS:
            await m.reply_text(
                f"╭━━〔 ❌ ACCESS DENIED 〕━━╮\n"
                f"┃ 🆔 `{user_id}`\n"
                f"┃ 🚫 Premium Access Required\n"
                f"╰━━━━━━━━━━━━━━╯\n\n"
                f"👑 {BRAND}",
                disable_web_page_preview=True
            )
            return

        # ── Step 1: File / URLs ────────────────────────────────────────────
        editable = await m.reply_text(
            f"╭━━〔 📂 SEND FILE 〕━━╮\n"
            f"┃ 📄 Upload TXT File\n"
            f"┃ 🔗 Or Paste URLs\n"
            f"╰━━━━━━━━━━━━━━╯\n\n"
            f"✍️ Format:\n"
            f"`Title://URL`\n\n"
            f"👑 {BRAND}"
        )
        inp: Message = await bot.listen(editable.chat.id)

        path = f"./downloads/{chat_id}"
        temp_dir = "./temp"
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        os.makedirs(temp_dir, exist_ok=True)
        os.makedirs(path, exist_ok=True)

        file_name = "Batch"
        if inp.document:
            x = await inp.download()
            await inp.delete(True)
            file_name = os.path.splitext(os.path.basename(x))[0]
            try:
                with open(x, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                content = [line.strip() for line in content.split("\n") if line.strip()]
                links = [i.split("://", 1) for i in content if "://" in i]
                os.remove(x)
            except Exception as e:
                await editable.edit(f"❌ `{e}`")
                return
        else:
            content = [line.strip() for line in inp.text.split("\n") if line.strip()]
            links = [i.split("://", 1) for i in content if "://" in i]
            await inp.delete(True)

        total_links = len(links)
        total_videos = sum(1 for l in links if len(l) > 1 and not is_pdf_url("https://" + l[1]))

        # ── Step 2: Start number ───────────────────────────────────────────
        await editable.edit(
            f"╭━━〔 🎞️ SCAN COMPLETED 〕━━╮\n"
            f"┃ 📦 Videos Found ➠ `{total_videos}`\n"
            f"╰━━━━━━━━━━━━━━╯\n\n"
            f"⚡ Send Starting Number\n"
            f"Example ➠ `1`\n\n"
            f"👑 {BRAND}"
        )
        input0: Message = await bot.listen(editable.chat.id)
        raw_text = input0.text.strip()
        await input0.delete(True)

        # ── Step 3: Batch name ─────────────────────────────────────────────
        await editable.edit(
            f"╭━━〔 🎥 BATCH SETUP 〕━━╮\n"
            f"┃ ✏️ Send Batch Name\n"
            f"╰━━━━━━━━━━━━━━╯\n\n"
            f"📌 Send `/d` For Default Name\n\n"
            f"👑 {BRAND}"
        )
        input1: Message = await bot.listen(editable.chat.id)
        raw_text0 = input1.text.strip()
        await input1.delete(True)
        b_name = file_name if raw_text0 == '/d' else raw_text0

        # ── Step 4: App name ───────────────────────────────────────────────
        await editable.edit(
            f"╭━━〔 📡 SOURCE SETUP 〕━━╮\n"
            f"┃ 📱 Send Platform Name\n"
            f"╰━━━━━━━━━━━━━━╯\n\n"
            f"Examples:\n"
            f"`PhysicsWallah`\n"
            f"`Allen`\n"
            f"`Kalam`\n\n"
            f"👑 {BRAND}"
        )
        input111: Message = await bot.listen(editable.chat.id)
        app_name = input111.text.strip()
        await input111.delete(True)

        # ── Step 5: Quality ────────────────────────────────────────────────
        await editable.edit(
            f"╭━━〔 🎬 QUALITY SETUP 〕━━╮\n"
            f"┃ 📺 Choose Video Quality\n"
            f"╰━━━━━━━━━━━━━━╯\n\n"
            f"`144 • 240 • 360 • 480 • 720 • 1080`\n\n"
            f"👑 {BRAND}"
        )
        input2: Message = await bot.listen(editable.chat.id)
        raw_text2 = input2.text.strip()
        await input2.delete(True)

        # ── Step 6: Thumbnail ──────────────────────────────────────────────
        await editable.edit(
            f"╭━━〔 🖼️ THUMBNAIL SETUP 〕━━╮\n"
            f"┃ 🔗 Send Thumbnail URL\n"
            f"╰━━━━━━━━━━━━━━╯\n\n"
            f"❌ Send `no` To Skip\n\n"
            f"👑 {BRAND}"
        )
        input6: Message = await bot.listen(editable.chat.id)
        thumb = input6.text.strip()
        await input6.delete(True)

        # ── Step 7: Destination ────────────────────────────────────────────
        await editable.edit(
            f"╭━━〔 📢 UPLOAD DESTINATION 〕━━╮\n"
            f"┃ 📡 Send Channel ID\n"
            f"╰━━━━━━━━━━━━━━╯\n\n"
            f"Example:\n"
            f"`-1001234567890`\n\n"
            f"📥 Send `/d` To Upload Here\n\n"
            f"👑 {BRAND}"
        )
        input7: Message = await bot.listen(editable.chat.id)
        channel_id = chat_id if "/d" in input7.text else input7.text.strip()
        await input7.delete()

        try:
            channel_id = int(channel_id)
        except Exception:
            pass

        await editable.edit(
            f"╭━━〔 🚀 BATCH STARTED 〕━━╮\n"
            f"┃ 🎥 `{b_name}`\n"
            f"┃ 📡 `{app_name}`\n"
            f"┃ 🎬 `{raw_text2}p`\n"
            f"╰━━━━━━━━━━━━━━╯\n\n"
            f"⚡ Initializing Premium Upload Engine...\n\n"
            f"👑 {BRAND}",
            disable_web_page_preview=True
        )

        # ── Batch start message in channel ─────────────────────────────────
        try:
            await bot.send_message(
                chat_id=channel_id,
                text=(
                    f"╭━━〔 🚀 BATCH STARTED 〕━━╮\n"
                    f"┃ 🎥 `{b_name}`\n"
                    f"┃ 📡 `{app_name}`\n"
                    f"┃ 🎬 `{raw_text2}p`\n"
                    f"╰━━━━━━━━━━━━━━╯\n\n"
                    f"⚡ Initializing Premium Upload Engine...\n\n"
                    f"👑 {BRAND}"
                ),
                disable_web_page_preview=True
            )
        except Exception as e:
            await m.reply_text(f"❌ Can't send to channel\n`{e}`\n\nMake sure I'm an admin there.")
            return

        await editable.delete()

        count = 1 if len(links) == 1 else int(raw_text)
        seq = count
        mpd = None
        keys = None
        uploaded_topics = []

        # ── Download loop ──────────────────────────────────────────────────
        for i in range(count - 1, len(links)):
            link_parts = links[i]
            if len(link_parts) < 2:
                continue

            V = link_parts[1]
            url = "https://" + V
            raw_name = link_parts[0]

            if is_pdf_url(url):
                logging.info(f"Skipping PDF: {url}")
                continue

            url = override_quality_in_url(url, raw_text2)

            try:
                if "*" in url:
                    mpd, keys = url.split("*")
                elif "vimeo" in url:
                    page_text = requests.get(url, headers=headers.allen).text
                    found = re.findall(r'https://[^/?#]+\.[^/?#]+(?:/[^/?#]+)+\.(?:m3u8)', page_text)
                    if found:
                        url = found[0]
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
                    vid_id = url.split("/")[-2]
                    policy = requests.post(
                        'https://api.penpencil.xyz/v1/files/get-signed-cookie',
                        headers=headers.pw,
                        json={'url': f"https://d1d34p8vz63oiq.cloudfront.net/{vid_id}/master.mpd"}
                    ).json()['data']
                    url = f"https://sr-get-video-quality.selav29696.workers.dev/?Vurl=https://d1d34p8vz63oiq.cloudfront.net/{vid_id}/hls/{raw_text2}/main.m3u8{policy}"
                elif "visionias" in url:
                    async with ClientSession() as session:
                        async with session.get(url, headers=headers.vision) as resp:
                            page_text = await resp.text()
                            match = re.search(r"(https://*.?playlist.m3u8.?)", page_text)
                            if match:
                                url = match.group(1)
            except Exception as e:
                logging.error(f"URL processing error: {e}")
                seq += 1
                continue

            # Clean topic name
            name1 = (
                raw_name
                .replace("\t", "").replace(":", " ").replace("/", "")
                .replace("+", "").replace("#", "").replace("|", "")
                .replace("@", "").replace("*", "").replace(".", "")
                .replace("https", "").replace("http", "")
                .strip()
            )
            name1 = re.sub(r'^\d+\s*[)\.\-]?\s*', '', name1).strip()
            name = f'{str(seq).zfill(3)}) {name1[:55]}'

            # yt-dlp command
            if "kalampublication" in url:
                cmd = (
                    f'yt-dlp -o "{name}.mp4" "{url}" '
                    f'--no-check-certificate '
                    f'--add-header "User-Agent: okhttp/4.12.0" '
                    f'--add-header "mobilenumber: aDhYejdQcVIyd0IxazlEZg==" '
                    f'--add-header "referer: https://hello-aws-uat.kalampublication.in"'
                )
            elif "youtu" in url:
                ytf = f"b[height<={raw_text2}][ext=mp4]/bv[height<={raw_text2}][ext=mp4]+ba[ext=m4a]/b[ext=mp4]"
                cmd = f'yt-dlp -f "{ytf}" "{url}" -o "{name}.mp4"'
            elif "jw-prod" in url:
                cmd = f'yt-dlp -o "{name}.mp4" "{url}"'
            else:
                ytf = f"b[height<={raw_text2}]/bv[height<={raw_text2}]+ba/b/bv+ba"
                cmd = f'yt-dlp -f "{ytf}" "{url}" -o "{name}.mp4"'

            # Caption
            cc = (
                f"╭───────────────⭓\n"
                f"│ 🚀 𝗣𝗥𝗘𝗠𝗜𝗨𝗠 𝗗𝗢𝗪𝗡𝗟𝗢𝗔𝗗\n"
                f"├───────────────\n"
                f"│ 📌 𝗜𝗗 ➠ `{str(seq).zfill(3)}`\n"
                f"│ 📖 𝗧𝗶𝘁𝗹𝗲 ➠\n"
                f"│ ❝ `{name1[:55]}` ❞\n"
                f"│\n"
                f"│ 🎥 𝗕𝗮𝘁𝗰𝗵 ➠\n"
                f"│ ❝ `{b_name}` ❞\n"
                f"│\n"
                f"│ 🎬 𝗤𝘂𝗮𝗹𝗶𝘁𝘆 ➠ `{raw_text2}p`\n"
                f"│ 📡 𝗦𝗼𝘂𝗿𝗰𝗲 ➠ `{app_name}`\n"
                f"╰───────────────⭓\n\n"
                f"✨ 𝗣𝗼𝘄𝗲𝗿𝗲𝗱 𝗕𝘆 {BRAND}"
            )

            try:
                prog = await bot.send_message(
                    channel_id,
                    f"╭━━〔 ⬇️ DOWNLOADING 〕━━╮\n"
                    f"┃ 📌 `{str(seq).zfill(3)}`\n"
                    f"┃ ❝ `{name1[:45]}` ❞\n"
                    f"╰━━━━━━━━━━━━━━╯\n\n"
                    f"⚡ Processing Video...\n\n"
                    f"👑 {BRAND}",
                    disable_web_page_preview=True
                )

                if mpd and keys:
                    await helper.download_and_dec_video(mpd, keys, path, name, raw_text2)
                    await prog.delete(True)
                    sent_msg = await helper.merge_and_send_vid(bot, m, cc, name, prog, path, url, thumb, channel_id)
                    mpd = None
                    keys = None
                elif "kalampublication" in url:
                    res_file = await helper.download_kalam_video(url, name)
                    await prog.delete(True)
                    sent_msg = await helper.send_vid(bot, m, cc, res_file, thumb, name, prog, url, channel_id)
                else:
                    res_file = await helper.download_video(url, cmd, name)
                    await prog.delete(True)
                    sent_msg = await helper.send_vid(bot, m, cc, res_file, thumb, name, prog, url, channel_id)

                if sent_msg:
                    uploaded_topics.append((seq, name1[:60], sent_msg.id))

                seq += 1
                await asyncio.sleep(0.5)

            except Exception as e:
                logging.error(f"Error processing {name}: {e}")
                seq += 1
                continue

        # ── Topic Index ────────────────────────────────────────────────────
        if uploaded_topics:
            header_text = (
                f"╭━━〔 📋 BATCH INDEX 〕━━╮\n"
                f"┃ 🎥 `{b_name}`\n"
                f"┃ 📡 `{app_name}`\n"
                f"┃ 🎬 `{raw_text2}p`\n"
                f"╰━━━━━━━━━━━━━━╯\n"
            )
            topic_lines = []
            for seq_num, topic_name, msg_id in uploaded_topics:
                link = make_channel_link(channel_id, msg_id)
                if link:
                    topic_lines.append(f"`{str(seq_num).zfill(3)}` · [{topic_name}]({link})")
                else:
                    topic_lines.append(f"`{str(seq_num).zfill(3)}` · `{topic_name}`")

            chunk = []
            chunk_chars = 0
            first_chunk = True
            for line in topic_lines:
                if chunk_chars + len(line) > 3500:
                    text = (header_text if first_chunk else "") + "\n".join(chunk)
                    await bot.send_message(channel_id, text, disable_web_page_preview=True)
                    await asyncio.sleep(1)
                    chunk = []
                    chunk_chars = 0
                    first_chunk = False
                chunk.append(line)
                chunk_chars += len(line)

            if chunk:
                text = (header_text if first_chunk else "") + "\n".join(chunk)
                await bot.send_message(channel_id, text, disable_web_page_preview=True)

        # ── Done ───────────────────────────────────────────────────────────
        done_text = (
            f"╭━━〔 ✅ COMPLETED 〕━━╮\n"
            f"┃ 🎥 `{b_name}`\n"
            f"┃ 🎬 `{raw_text2}p`\n"
            f"┃ 📦 `{len(uploaded_topics)}` Videos Uploaded\n"
            f"╰━━━━━━━━━━━━━━╯\n\n"
            f"✨ Upload Finished Successfully\n\n"
            f"👑 {BRAND}"
        )
        try:
            await bot.send_message(channel_id, done_text, disable_web_page_preview=True)
        except FloodWait as fw:
            await asyncio.sleep(fw.value)
            await bot.send_message(channel_id, done_text, disable_web_page_preview=True)

    except FloodWait as fw:
        await asyncio.sleep(fw.value)
        try:
            await m.reply_text(f"⚠️ Flood wait hit. Batch may be partially complete.\n\n⬇️ {BRAND}", disable_web_page_preview=True)
        except Exception:
            pass
    except Exception as e:
        logging.error(f"Master handler error: {e}")
        try:
            await m.reply_text(
                f"╭━━〔 ❌ ERROR OCCURRED 〕━━╮\n"
                f"┃ ⚠️ Something Went Wrong\n"
                f"╰━━━━━━━━━━━━━━╯\n\n"
                f"`{e}`\n\n"
                f"👑 {BRAND}",
                disable_web_page_preview=True
            )
        except Exception:
            pass


# ── /master command ───────────────────────────────────────────────────────────
@bot.on_message(filters.command(["master"]))
async def master_handler(client: Client, m: Message):
    await run_master(client, m, m.from_user.id, m.chat.id)


# ── /setproxy ─────────────────────────────────────────────────────────────────
@bot.on_message(filters.command(["setproxy"]))
async def setproxy_handler(client: Client, m: Message):
    if m.from_user.id not in Config.VIP_USERS:
        await m.reply_text(
            f"╭━━〔 ❌ ACCESS DENIED 〕━━╮\n"
            f"┃ 🆔 `{m.from_user.id}`\n"
            f"┃ 🚫 Premium Access Required\n"
            f"╰━━━━━━━━━━━━━━╯\n\n"
            f"👑 {BRAND}",
            disable_web_page_preview=True
        )
        return
    parts = m.text.split(maxsplit=1)
    if len(parts) < 2 or not parts[1].strip():
        await m.reply_text(
            f"**Usage:** `/setproxy <proxy_url>`\n\n"
            f"**Formats:**\n"
            f"› `http://ip:port`\n"
            f"› `http://user:pass@ip:port`\n"
            f"› `socks5://ip:port`\n\n"
            f"⬇️ {BRAND}",
            disable_web_page_preview=True
        )
        return
    proxy_url = parts[1].strip()
    from config import save_proxy
    save_proxy(proxy_url)
    await m.reply_text(
        f"╭━━〔 🌐 PROXY UPDATED 〕━━╮\n"
        f"┃ ✅ Proxy Connected Successfully\n"
        f"╰━━━━━━━━━━━━━━╯\n\n"
        f"`{proxy_url}`\n\n"
        f"👑 {BRAND}",
        disable_web_page_preview=True
    )


# ── /delproxy ─────────────────────────────────────────────────────────────────
@bot.on_message(filters.command(["delproxy"]))
async def delproxy_handler(client: Client, m: Message):
    if m.from_user.id not in Config.VIP_USERS:
        await m.reply_text(
            f"╭━━〔 ❌ ACCESS DENIED 〕━━╮\n"
            f"┃ 🆔 `{m.from_user.id}`\n"
            f"┃ 🚫 Premium Access Required\n"
            f"╰━━━━━━━━━━━━━━╯\n\n"
            f"👑 {BRAND}",
            disable_web_page_preview=True
        )
        return
    from config import delete_proxy, load_proxy
    proxy, _ = load_proxy()
    if not proxy:
        await m.reply_text(f"ℹ️ No proxy is currently set.\n\n⬇️ {BRAND}", disable_web_page_preview=True)
        return
    delete_proxy()
    await m.reply_text(f"🗑 **Proxy Removed**\n\n⬇️ {BRAND}", disable_web_page_preview=True)


# ── /proxy ────────────────────────────────────────────────────────────────────
@bot.on_message(filters.command(["proxy"]))
async def proxy_status_handler(client: Client, m: Message):
    if m.from_user.id not in Config.VIP_USERS:
        await m.reply_text(
            f"╭━━〔 ❌ ACCESS DENIED 〕━━╮\n"
            f"┃ 🆔 `{m.from_user.id}`\n"
            f"┃ 🚫 Premium Access Required\n"
            f"╰━━━━━━━━━━━━━━╯\n\n"
            f"👑 {BRAND}",
            disable_web_page_preview=True
        )
        return
    from config import load_proxy
    proxy, worker = load_proxy()
    lines = ["**Kalam Download Status**\n"]
    lines.append(f"🌐 Worker: `{worker}`" if worker else "🌐 Worker: not set")
    lines.append(f"📡 Proxy: `{proxy}`" if proxy else "📡 Proxy: not set")
    lines.append(f"\n**Commands:**")
    lines.append(f"› `/setworker <url>` — set CF Worker")
    lines.append(f"› `/setproxy <url>` — set HTTP/SOCKS proxy")
    lines.append(f"› `/delworker` · `/delproxy` — remove")
    lines.append(f"\n⬇️ {BRAND}")
    await m.reply_text("\n".join(lines), disable_web_page_preview=True)


# ── /setworker ────────────────────────────────────────────────────────────────
@bot.on_message(filters.command(["setworker"]))
async def setworker_handler(client: Client, m: Message):
    if m.from_user.id not in Config.VIP_USERS:
        await m.reply_text(
            f"╭━━〔 ❌ ACCESS DENIED 〕━━╮\n"
            f"┃ 🆔 `{m.from_user.id}`\n"
            f"┃ 🚫 Premium Access Required\n"
            f"╰━━━━━━━━━━━━━━╯\n\n"
            f"👑 {BRAND}",
            disable_web_page_preview=True
        )
        return
    parts = m.text.split(maxsplit=1)
    if len(parts) < 2 or not parts[1].strip():
        await m.reply_text(
            f"**Usage:** `/setworker <cloudflare_worker_url>`\n\n"
            f"Example:\n`/setworker https://kalam.yourname.workers.dev`\n\n"
            f"⬇️ {BRAND}",
            disable_web_page_preview=True
        )
        return
    from config import save_worker
    worker_url = parts[1].strip()
    save_worker(worker_url)
    await m.reply_text(
        f"╭━━〔 ☁️ WORKER UPDATED 〕━━╮\n"
        f"┃ ✅ CF Worker Connected\n"
        f"╰━━━━━━━━━━━━━━╯\n\n"
        f"`{worker_url}`\n\n"
        f"👑 {BRAND}",
        disable_web_page_preview=True
    )


# ── /delworker ────────────────────────────────────────────────────────────────
@bot.on_message(filters.command(["delworker"]))
async def delworker_handler(client: Client, m: Message):
    if m.from_user.id not in Config.VIP_USERS:
        await m.reply_text(
            f"╭━━〔 ❌ ACCESS DENIED 〕━━╮\n"
            f"┃ 🆔 `{m.from_user.id}`\n"
            f"┃ 🚫 Premium Access Required\n"
            f"╰━━━━━━━━━━━━━━╯\n\n"
            f"👑 {BRAND}",
            disable_web_page_preview=True
        )
        return
    from config import delete_worker, load_proxy
    _, worker = load_proxy()
    if not worker:
        await m.reply_text(f"ℹ️ No worker is currently set.\n\n⬇️ {BRAND}", disable_web_page_preview=True)
        return
    delete_worker()
    await m.reply_text(f"🗑 **Worker Removed**\n\n⬇️ {BRAND}", disable_web_page_preview=True)


bot.run()
