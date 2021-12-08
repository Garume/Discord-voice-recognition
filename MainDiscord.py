import discord
from discord.ext import commands
import dislash
import json,time,random

from VoiceSocket import MyVoiceClient

with open("env.json","r") as file:
    TOKEN = json.load(file)["token"]

bot = commands.Bot(
    command_prefix='!',
    activity=discord.Game("音想世界"))

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
    
    if message.content == "!record":
        if message.guild.voice_client is None:
            await message.channel.send("接続していません")
        await message.channel.send("レコードを開始します")
        audio = await message.guild.voice_client.record()
        file = discord.File(audio)
        await message.channel.send(content="レコードを終了します",file = file)
        await message.channel.send("レコードを終了します")

    await bot.process_commands(message)

bot.run(TOKEN)



