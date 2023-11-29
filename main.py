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
LINUX_COMMAND1 = f"lxc-stop {os.environ['CT']}"
LINUX_COMMAND2 = f"lxc-stop {os.environ['CT']} -r"
LINUX_COMMAND3 = f"lxc-start {os.environ['CT']}"

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

async def pinganddo(lcm, message):
    with paramiko.SSHClient() as clientp:
        try:
            clientp = paramiko.SSHClient()
            clientp.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            clientp.connect(
                hostname=HOSTNAME, port=22, username=USERNAME, password=PASSWORD
            )
            stdin, stdout, stderr = clientp.exec_command(lcm)
            await message.channel.send(message)
        except Exception as e:
            await message.channel.send(f"エラー！: {e}")

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
        await pinganddo(LINUX_COMMAND3, "サーバーを起動しました")

    # サーバー停止
    if message.content.startswith("$サーバーを停止して"):
        await pinganddo(LINUX_COMMAND1, "サーバーを停止しました")

    # サーバー再起動
    if message.content.startswith("$サーバーを再起動して"):
        await pinganddo(LINUX_COMMAND2, "サーバーを再起動しました")

# os.environを用いて環境変数を表示させます
client.run(os.environ["DISTOKEN"])
