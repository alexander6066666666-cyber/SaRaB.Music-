from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import InputAudioStream
from pytgcalls.types.input_stream.quality import HighQualityAudio
import yt_dlp

API_ID = 25263876
API_HASH = "ceb4a1671e9a54dd710a5f3f3b4d4ddb"
BOT_TOKEN = "8625874672:AAG0GNY72ZoMjrG1IvZB0rIyfJmr-WHAPwA"

app = Client(
    "musicbot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

call_py = PyTgCalls(app)

@app.on_message(filters.command("play"))
async def play(_, message):
    query = message.text.split(None,1)[1]

    await message.reply("🔎 جاري البحث...")

    ydl_opts = {
        "format": "bestaudio",
        "quiet": True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch:{query}", download=False)['entries'][0]
        url = info['url']

    await call_py.join_group_call(
        message.chat.id,
        InputAudioStream(
            url,
            HighQualityAudio()
        )
    )

    await message.reply("🎵 تم تشغيل الاغنية")

app.start()
call_py.start()
print("Music Bot Running")
app.idle()