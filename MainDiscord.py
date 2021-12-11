from token import SLASH
import discord
from discord import message
from discord.ext import commands
import json,time,random
from dislash import slash_commands, Option, OptionType
from dislash.application_commands.slash_client import InteractionClient
from numpy import e, record
from voicerecognition.GenText import getTextwithAudio

from voicerecognition.VoiceSocket import MyVoiceClient
from youtubeUtil.Youtube_search import Youtube_Serch
from youtubeUtil.Ytdl import YTDLSource

with open("util/env.json","r") as file:
    TOKEN = json.load(file)["token"]

bot = commands.Bot(
    command_prefix='/',
    activity=discord.Game("音想世界"))

test_guilds = [815076984828198942,765546170201669652]
inter_client = InteractionClient(bot,test_guilds=test_guilds)

def check_str(text,check):
    return check in text

def check_title(text):
    if check_str(text,"ドットプレイ") or check_str(text,"ホットプレイ") or check_str(text,"ホットプレー") or check_str(text,"ウッドプレイ"):
        return [True,7]
    elif check_str(text,"ホットプレート"):
        return [True,8]
    elif check_str(text,"not Play"):
        return [True,9]
    elif check_str(text,"夫 プレイ"):
        print(text[4:])
        return [True,6]
    elif check_str(text,"すとぷり") or check_str(text,"Play"):
        return [True,5]
    elif check_str(text,"プレイ"):
        return [True,4]
    else: return False,""

@bot.event
async def on_ready():
    print("on_ready")
    print(discord.__version__)

#----------------------------------------------------------
@inter_client.slash_command(
    name = "dice",
    description = "サイコロを振ります",
    options = [
        Option("dice_count","サイコロの個数を決めてね",OptionType.INTEGER),
        Option("dice_max","サイコロの最大値を決めてね",OptionType.INTEGER)
    ]    
)
async def dice(bot,dice_count=None,dice_max=None):
    cnt=[]
    for _ in range(dice_count):
        cnt.append(str(random.randint(1,dice_max)))
    await bot.reply(" ".join(cnt))
#----------------------------------------------------------
@inter_client.slash_command(description="Sends Hello")
async def hello(interaction):
    await interaction.reply("Hello!")
#----------------------------------------------------------
@inter_client.slash_command(
    name = "join",
    description = "入室します"
)
async def join(bot):
    if bot.author.voice is None:
        await bot.send("あなたはVCに接続していません")
        return
    await bot.author.voice.channel.connect(cls=MyVoiceClient)
    await bot.send("接続しました")
    bot.guild.voice_client.play(discord.FFmpegPCMAudio("util/start.wav"))
#----------------------------------------------------------
@inter_client.slash_command(
    name = "leave",
    description = "退室します"   
)
async def leave(bot):
    if bot.guild.voice_client is None:
        await bot.send("接続していません")
        return
    await bot.guild.voice_client.disconnect()
    await bot.send("抜けました")
#----------------------------------------------------------
@inter_client.slash_command(
    name = "stop",
    description = "音楽を止めます"
       
)
async def stop(Bot):
    if Bot.guild.voice_client is None:
        await Bot.send("接続していません。")
        return

    if not Bot.guild.voice_client.is_playing():
        await Bot.send("再生していません。")
        return

    Bot.guild.voice_client.stop()
    await bot.change_presence(activity=discord.Game("音想世界"))
    await Bot.send("ストップしました。")
#----------------------------------------------------------
@inter_client.slash_command(
    name = "record",
    description = "VCを録音します",   
    options = [
        Option("record_time","秒数を決めてね",OptionType.INTEGER)
    ]
)
async def record(Bot,record_time=5):
    if Bot.guild.voice_client is None:
        await Bot.send("接続していません")
        return
    await Bot.guild.voice_client.disconnect()
    time.sleep(0.08)
    await Bot.author.voice.channel.connect(cls=MyVoiceClient)
    await Bot.send("{}秒でレコードを開始します".format(record_time))
    async with Bot.channel.typing(): # 送られてきたチャンネルで入力中と表示させる
        audio = await Bot.guild.voice_client.record(record_time)
        file = discord.File(audio,filename="test.wav")
    await Bot.send(file = file)
    await Bot.send(getTextwithAudio("util/test.wav"))
    Bot.guild.voice_client.stop()
#----------------------------------------------------------
@inter_client.slash_command(
    name = "sound",
    description = "VCで音楽を流します",   
    options = [
        Option("record_time","秒数を決めてね",OptionType.INTEGER)
    ]
)
async def sound(Bot,record_time=5):
    if Bot.guild.voice_client is None:
        await Bot.send("接続していません")
        return
    await Bot.guild.voice_client.disconnect()
    time.sleep(0.08)
    await Bot.author.voice.channel.connect(cls=MyVoiceClient)
    await Bot.send("{}秒でレコードを開始します".format(record_time))
    async with Bot.channel.typing(): # 送られてきたチャンネルで入力中と表示させる
        audio = await Bot.guild.voice_client.record(record_time)
        file = discord.File(audio,filename="test.wav")
    Bot.guild.voice_client.stop()
    await Bot.send(file = file)
    title = getTextwithAudio("util/test.wav")
    print(title)
    video = Youtube_Serch().youtube_search(title)
    player = await YTDLSource.from_url(video[1], loop=bot.loop,stream=True)
    Bot.guild.voice_client.play(player)
    Bot.guild.voice_client.pause()
    Bot.guild.voice_client.resume()
    print(video)
    await bot.change_presence(activity=discord.Game(video[0]))
    await Bot.send('{} を再生します。'.format(video[0]))
#----------------------------------------------------------

@bot.event
async def on_message(message):
    
    if check_title(message.content)[0]:
        title_len = check_title(message.content)[1]
        title = message.content[title_len:]
        print(title_len)
        print(title)
        
        video = Youtube_Serch().youtube_search(title)
        player = await YTDLSource.from_url(video[1], loop=bot.loop,stream=True)

        print(video)
        await bot.change_presence(activity=discord.Game(video[0]))
        message.guild.voice_client.play(player)
        await message.channel.send('{} を再生します。'.format(video[0]))

    await bot.process_commands(message)

bot.run(TOKEN)


