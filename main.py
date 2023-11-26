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
        if res.is_reached():
            with paramiko.SSHClient() as client:
                client = paramiko.SSHClient()
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                client.connect(
                    hostname=HOSTNAME, port=22, username=USERNAME, password=PASSWORD
                )
                stdin, stdout, stderr = client.exec_command(LINUX_COMMAND1)
                if stderr == None | stderr == "":
                    for line in stderr:
                        await message.channel.send("エラー！:", line)
                else:
                    await message.channel.send("サーバーを再起動しました:", line)
        else:
            await message.channel.send("サーバーは既に閉じているか起動中です。")

    # サーバー再起動
    if message.content.startswith("$サーバーを再起動して"):
        if res.is_reached():
            with paramiko.SSHClient() as client:
                client = paramiko.SSHClient()
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                client.connect(
                    hostname=HOSTNAME, port=22, username=USERNAME, password=PASSWORD
                )
                stdin, stdout, stderr = client.exec_command(LINUX_COMMAND2)
                if stderr == None | stderr == "":
                    for line in stderr:
                        await message.channel.send("エラー！:", line)
                else:
                    await message.channel.send("サーバーを再起動しました:", line)
        else:
            await message.channel.send("サーバーが閉じているので起動してください:")


# os.environを用いて環境変数を表示させます
client.run(os.environ["DISTOKEN"])
