import discord
from discord.ext import commands
import asyncio
import os

# Pega o token do Railway (ou outra variável de ambiente)
TOKEN = os.environ.get("DISCORD_TOKEN")
if not TOKEN:
    raise ValueError("❌ Variável de ambiente DISCORD_TOKEN não encontrada!")

# Intents necessários
intents = discord.Intents.default()
intents.message_content = True  # Para comandos de texto
intents.guilds = True           # Para slash commands

bot = commands.Bot(command_prefix="!", intents=intents)

# Carrega todos os cogs automaticamente
async def load_cogs():
    for root, dirs, files in os.walk("./cogs"):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file).replace("\\", ".").replace("/", ".")[:-3]
                try:
                    await bot.load_extension(path)
                    print(f"✅ Cog carregado: {path}")
                except Exception as e:
                    print(f"❌ Erro ao carregar {path}: {e}")

@bot.event
async def on_ready():
    print(f"✅ Bot online: {bot.user}")

async def main():
    await load_cogs()
    await bot.start(TOKEN)

asyncio.run(main())