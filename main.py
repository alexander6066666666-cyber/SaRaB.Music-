from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import InputAudioStream
from pytgcalls.types.input_stream.quality import HighQualityAudio
import yt_dlp

API_ID = 25263876
API_HASH = "ceb4a1671e9a54dd710a5f3f3b4d4ddb"
BOT_TOKEN = "8625874672:AAG0GNY72ZoMjrG1IvZB0rIyfJmr-WHAPwA"

app = Client("musicbot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
call = PyTgCalls(app)

queue = []

async def play_music(chat_id):

    if not queue:
        return

    url = queue[0]

    await call.join_group_call(
        chat_id,
        InputAudioStream(
            url,
            HighQualityAudio()
        )
    )

@app.on_message(filters.text)
async def music(_, message):

    text = message.text

    # تشغيل
    if text.startswith("شغل"):

        query = text.replace("شغل","").strip()

        if query == "":
            return await message.reply("اكتب اسم الاغنية بعد كلمة شغل")

        msg = await message.reply("🔎 جاري البحث...")

        ydl_opts = {"format":"bestaudio","quiet":True}

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch:{query}", download=False)
            url = info["entries"][0]["url"]

        queue.append(url)

        if len(queue) == 1:
            await play_music(message.chat.id)

        await msg.edit("🎧 تم إضافة الاغنية")

    # اسكت
    elif text == "اسكت":

        await call.leave_group_call(message.chat.id)
        queue.clear()

        await message.reply("🤫 تم ايقاف الصوت")

    # تخطي
    elif text == "تخطي":

        if len(queue) > 1:
            queue.pop(0)
            await play_music(message.chat.id)
            await message.reply("⏭ تم تخطي الاغنية")
        else:
            await message.reply("ماكو اغنية ثانية")

app.start()
call.start()
print("Music bot running")
app.idle()
