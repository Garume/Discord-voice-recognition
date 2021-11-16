import discord
import json,time,random

with open("env.json","r") as file:
    TOKEN = json.load(file)["token"]

saikoros = ["",
            "⚫ ⚫ ⚫　　　　⚫ ⚪ ⚫　　　　⚫ ⚫ ⚫",
            "⚪ ⚫ ⚫　　　　⚫ ⚫ ⚫　　　　⚫ ⚫ ⚪",
            "⚪ ⚫ ⚫　　　　⚫ ⚪ ⚫　　　　⚫ ⚫ ⚪",
            "⚪ ⚫ ⚪　　　　⚫ ⚫ ⚫　　　　⚪ ⚫ ⚪",
            "⚪ ⚫ ⚪　　　　⚫ ⚪ ⚫　　　　⚪ ⚫ ⚪",
            "⚪ ⚫ ⚪　　　　⚪ ⚫ ⚪　　　　⚪ ⚫ ⚪"]
# 接続に必要なオブジェクトを生成
client = discord.Client()

def saikoro():
    a = random.randint(1,6)
    b = random.randint(1,6)
    c = random.randint(1,6)
    if a == b and b == c:
        pec = 2.8
    elif a == b or b == c or c == a:
        pec = 41.7
    else:
        pec = 55.6
    embed=discord.Embed(title="🎲サイコロWORLD🎲", description="この目は{}%の確立だ！！".format(pec), color=0x4ef401)
    embed.set_thumbnail(url="https://illustkun.com/wp-content/uploads/illustkun-03417-dice.png")
    embed.add_field(name=str(saikoros[a]), value=a, inline=True)
    embed.add_field(name=str(saikoros[b]), value=b, inline=True)
    embed.add_field(name=str(saikoros[c]), value=c, inline=True)
    embed.add_field(name="出た目", value="{} {} {}".format(a,b,c), inline=True)
    return embed

# 起動時に動作する処理
@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('ログインしました')

# メッセージ受信時に動作する処理
@client.event
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return
    # 「/neko」と発言したら「にゃーん」が返る処理
    if message.content == '/neko':
        await message.channel.send('にゃーん')
    if message.content == '/スピード':
        start = time.time()
        await message.channel.send("レスポンス速度を計測中です")
        elapsed_time = time.time() - start
        await message.channel.send("%s" % (elapsed_time))
    if message.content == '/さいころ':
        await message.channel.send(embed=saikoro())
# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)