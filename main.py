import discord
import pykakasi
import re

# 漢字をひらがなに変換するツールの準備
kks = pykakasi.kakasi()

# Discordボットの準備
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} がオンラインになりました！')

@client.event
async def on_message(message):
    # ボット自身のメッセージには反応しない
    if message.author.bot:
        return

    # 1. 「鰆」が含まれているかチェック（最優先）
    if "鰆" in message.content:
        await message.channel.send("うおおおおお！！！！！")
        return  # ここで処理を終了し、以下の判定は行わない

    # 2. 直接「さわら」や「さわーらん」と書かれている場合は反応しない（除外設定）
    if "さわら" in message.content or "さわーらん" in message.content:
        return  # 何も返信せずにここで処理を終了する

    # 3. ここまで残ったメッセージだけをひらがなに変換する
    result = kks.convert(message.content)
    hiragana_text = "".join([item['hira'] for item in result])

    # 「さ」→「わ」→「ら」の順番で並んでいるかチェック
    if re.search(r'さ.*わ.*ら', hiragana_text):
        await message.channel.send("略してさわらやんけ")

# 取得したトークンを入れて実行
client.run('MTUxNzUzMDAzMTMxODg5NjY4MQ.GDtzo0.y2J9ozH5_VDRFwNqpEUtGbT16WSLpHleFhaf-Q')
