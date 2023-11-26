import os
from dotenv import load_dotenv
from wakeonlan import send_magic_packet

import discord

import pings

# .envファイルの内容を読み込見込む
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

# Ping
p = pings.Ping()

res = p.ping(os.environ["SSH"])


# ログインしたとき
@client.event
async def on_ready():
    print(f"{client.user} としてログインしました")


# メッセージ反応
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # サーバー起動
    if message.content.startswith("$サーバーを起動して"):
        if res.is_reached():
            await message.channel.send("サーバーは既に起動しています")
        else:
            send_magic_packet(os.environ["WOL"])
            await message.channel.send("サーバーを起動しました")

    # サーバー停止
    if message.content.startswith("$サーバーを停止して"):
        if res.is_reached():
            try:
                os.system(
                    f"sshpass -p {os.environ['RPASSWD']} ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null {os.environ['RUSERNAME']}@{os.environ['SSH']} 'echo {os.environ['RPASSWD']} | sudo -S shutdown -h now'"
                )
                await message.channel.send("サーバーを停止しました")
            except Exception as e:
                await message.channel.send("エラー！:", e)
        else:
            await message.channel.send("サーバーは既に閉じているか起動中です。")

    # サーバー再起動
    if message.content.startswith("$サーバーを再起動して"):
        if res.is_reached():
            try:
                os.system(
                    f"sshpass -p {os.environ['RPASSWD']} ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null {os.environ['RUSERNAME']}@{os.environ['SSH']} 'echo {os.environ['RPASSWD']} | sudo -S reboot'"
                )
                await message.channel.send("サーバーを再起動しました")
            except Exception as e:
                await message.channel.send("エラー！:", e)
        else:
            await message.channel.send("サーバーが閉じているので起動してください:")


# os.environを用いて環境変数を表示させます
client.run(os.environ["DISTOKEN"])
