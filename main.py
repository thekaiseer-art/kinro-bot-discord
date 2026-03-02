import discord
from discord.ext import commands
import os
import asyncio

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

# 🔥 Carregar todas as cogs automaticamente
async def load_cogs():
    for root, dirs, files in os.walk("cogs"):
        for file in files:
            if file.endswith(".py") and not file.startswith("__"):
                path = os.path.join(root, file)
                path = path.replace("\\", ".").replace("/", ".")[:-3]
                await bot.load_extension(path)

@bot.event
async def on_ready():
    try:
        await bot.tree.sync()
        print("Slash commands sincronizados.")
    except Exception as e:
        print(f"Erro ao sincronizar slash: {e}")

    print(f"Logado como {bot.user} (ID: {bot.user.id})")
    print("Bot está online!")

async def main():
    async with bot:
        await load_cogs()

        token = os.getenv("TOKEN")
        if not token:
            raise ValueError("TOKEN não encontrada nas variáveis de ambiente.")

        await bot.start(token)

asyncio.run(main())