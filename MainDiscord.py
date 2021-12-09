import discord
from discord.ext import commands
import dislash
import json,time,random

from numpy import e, record
from GenText import getTextwithAudio

from VoiceSocket import MyVoiceClient
from Youtube_search import Youtube_Serch
from Ytdl import YTDLSource

with open("env.json","r") as file:
    TOKEN = json.load(file)["token"]

bot = commands.Bot(
    command_prefix='!',
    activity=discord.Game("音想世界"))

def check_str(text,check):
    return check in text

def check_title(text):
    if check_str(text,"ドットプレイ") or check_str(text,"ホットプレイ") or check_str(text,"ホットプレー"):
        return [True,7]
    elif check_str(text,"ホットプレート"):
        return [True,8]
    elif check_str(text,"not Play"):
        return [True,9]
    elif check_str(text,"夫 プレイ"):
        print(text[4:])
        return [True,6]
    elif check_str(text,"すとぷり"):
        return [True,5]
    elif check_str(text,"プレイ"):
        return [True,4]
    else: return False,""

@bot.event
async def on_ready():
    print("on_ready")
    print(discord.__version__)

@bot.event
async def on_message(message):
    if message.content == "!join":
        if message.author.voice is None:
            await message.channel.send("あなたはVCに接続していません")
            return
        await message.author.voice.channel.connect(cls=MyVoiceClient)
        await message.channel.send("接続しました")
        message.guild.voice_client.play(discord.FFmpegPCMAudio("start.wav"))

    if message.content == "!leave":
        if message.guild.voice_client is None:
            await message.channel.send("接続していません")
        await message.guild.voice_client.disconnect()
        await message.channel.send("接続しました")
    
    if message.content.startswith("!record"):
        if message.guild.voice_client is None:
            await message.channel.send("接続していません")
            return
        await message.guild.voice_client.disconnect()
        time.sleep(0.08)
        await message.author.voice.channel.connect(cls=MyVoiceClient)
        if len(message.content) > 7:
            record_time=int(message.content[8:])
        else:
            record_time=5
        await message.channel.send("{}秒でレコードを開始します".format(record_time))
        audio = await message.guild.voice_client.record(record_time)
        file = discord.File(audio,filename="test.wav")
        await message.channel.send(file = file)
        await message.channel.send(getTextwithAudio("test.wav"))
        await message.channel.send("レコードを終了します")
        message.guild.voice_client.stop()
    
    if message.content == "!stop":
        if message.guild.voice_client is None:
            await message.channel.send("接続していません。")
            return

        # 再生中ではない場合は実行しない
        if not message.guild.voice_client.is_playing():
            await message.channel.send("再生していません。")
            return

        message.guild.voice_client.stop()

        await message.channel.send("ストップしました。")

    if check_title(message.content)[0]:
        title_len = check_title(message.content)[1]
        title = message.content[title_len:]
        print(title_len)
        print(title)
        
        video = Youtube_Serch().youtube_search(title)
        player = await YTDLSource.from_url(video[1], loop=bot.loop,stream=True)

        print(video)
        await message.guild.voice_client.play(player)
        await message.channel.send('{} を再生します。'.format(player.title))

    await bot.process_commands(message)

bot.run(TOKEN)


