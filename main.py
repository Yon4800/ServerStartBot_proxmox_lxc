import os
from dotenv import load_dotenv
from wakeonlan import send_magic_packet

import discord

# .envファイルの内容を読み込見込む
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


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
        send_magic_packet(os.environ["WOL"])
        await message.channel.send("サーバーを起動しました")

    # サーバー停止
    if message.content.startswith("$サーバーを停止して"):
        os.system(
            f"sshpass -p {os.environ['RPASSWD']} ssh -o StrictHostKeyChecking no -o UserKnownHostsFile=/dev/null {os.environ['RUSERNAME']}@{os.environ['SSH']} 'echo {os.environ['RPASSWD']} | sudo -S shutdown -h now'"
        )
        await message.channel.send("サーバーを停止しました")

    # サーバー再起動
    if message.content.startswith("$サーバーを再起動して"):
        os.system(
            f"sshpass -p {os.environ['RPASSWD']} ssh -o StrictHostKeyChecking no -o UserKnownHostsFile=/dev/null {os.environ['RUSERNAME']}@{os.environ['SSH']} 'echo {os.environ['RPASSWD']} | sudo -S reboot'"
        )
        await message.channel.send("サーバーを再起動しました")


# os.environを用いて環境変数を表示させます
client.run(os.environ["DISTOKEN"])
