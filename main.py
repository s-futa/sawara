import discord
import pykakasi
import re
import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

# --- 1. HTTPサーバーの設定 (Render対策) ---
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # サイトにアクセスされたら「Bot is alive!」と返すだけのシンプルな処理
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Bot is alive!')

def run_server():
    # Renderが指定する PORT 環境変数を取得（設定されていなければ8080）
    port = int(os.environ.get('PORT', 8080))
    server = HTTPServer(('', port), SimpleHTTPRequestHandler)
    print(f"HTTPサーバーをポート {port} で起動しました。")
    server.serve_forever()

# ボットの処理を邪魔しないよう、別スレッドでHTTPサーバーを起動
thread = threading.Thread(target=run_server)
thread.daemon = True
thread.start()


# --- 2. Discordボットの設定 ---
kks = pykakasi.kakasi()

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} がオンラインになりました！')

@client.event
async def on_message(message):
    if message.author.bot:
        return

    # 1. 「鰆」が含まれているかチェック
    if "鰆" in message.content:
        await message.reply("うおおおおお！！！！！") # replyに変更
        return

    # 2. 除外判定（ひらがな化してから判定するとカタカナもカバーできる）
    result = kks.convert(message.content)
    hiragana_text = "".join([item['hira'] for item in result])
    
    # 「さわら」「さわーらん」のひらがな版・カタカナ版をまとめてチェック
    # (pykakasiで変換したhiragana_textで判定するため、ひらがな条件のみでOK)
    if "さわら" in hiragana_text or "さわーらん" in hiragana_text:
        return

    # 3. 「さ」→「わ」→「ら」の順番チェック
    if re.search(r'さ.*わ.*ら', hiragana_text):
        await message.reply("略してさわらやんけ") # replyに変更


# --- 3. トークンの読み込みと実行 ---
# 環境変数 DISCORD_TOKEN からトークンを取得
TOKEN = os.environ.get('DISCORD_TOKEN')

if TOKEN is None:
    print("エラー: 環境変数 DISCORD_TOKEN が設定されていません。")
else:
    client.run(TOKEN)
