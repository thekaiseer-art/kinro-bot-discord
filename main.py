import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Lista de cogs para carregar
initial_extensions = [
    "cogs.fun.ping",        # ping.py
    "cogs.fun",             # pasta fun/__init__.py
    "cogs.moderation",      # pasta moderation/__init__.py
    "cogs.util"             # pasta util/__init__.py
]

for ext in initial_extensions:
    try:
        bot.load_extension(ext)
        print(f"✅ Cog {ext} carregada com sucesso")
    except Exception as e:
        print(f"❌ Erro ao carregar {ext}: {e}")

@bot.event
async def on_ready():
    print(f"Bot online: {bot.user}")

TOKEN = os.environ.get("DISCORD_TOKEN")
bot.run(TOKEN)