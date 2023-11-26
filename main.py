import os
from dotenv import load_dotenv
from wakeonlan import send_magic_packet

import discord

import pings

import paramiko

# .envファイルの内容を読み込見込む
load_dotenv()

HOSTNAME = os.environ["SSH"]
USERNAME = os.environ["RUSERNAME"]
PASSWORD = os.environ["RPASSWD"]
LINUX_COMMAND1 = f"echo {os.environ['RPASSWD']} | sudo -S shutdown -h now"
LINUX_COMMAND2 = f"echo {os.environ['RPASSWD']} | sudo -S reboot"

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
        with paramiko.SSHClient() as clientp:
            try:
                clientp = paramiko.SSHClient()
                clientp.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                clientp.connect(
                    hostname=HOSTNAME, port=22, username=USERNAME, password=PASSWORD
                )
                stdin, stdout, stderr = clientp.exec_command(LINUX_COMMAND1)
                await message.channel.send("サーバーを停止しました")
            except Exception as e:
                await message.channel.send("エラー！:", e)

    # サーバー再起動
    if message.content.startswith("$サーバーを再起動して"):
        with paramiko.SSHClient() as clientp:
            try:
                clientp = paramiko.SSHClient()
                clientp.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                clientp.connect(
                    hostname=HOSTNAME, port=22, username=USERNAME, password=PASSWORD
                )
                stdin, stdout, stderr = clientp.exec_command(LINUX_COMMAND2)
                await message.channel.send("サーバーを再起動しました")
            except Exception as e:
                await message.channel.send("エラー！:", e)


# os.environを用いて環境変数を表示させます
client.run(os.environ["DISTOKEN"])
