import discord
from discord.ext import commands
import sqlite3
import time
import random

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ==========================
# BANCO DE DADOS
# ==========================

def init_db():
    conn = sqlite3.connect("kions.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS player_kions (
        user_id INTEGER PRIMARY KEY,
        kions INTEGER DEFAULT 0,
        last_daily INTEGER DEFAULT 0
    )
    """)
    conn.commit()
    conn.close()

init_db()

# ==========================
# FUNÇÕES
# ==========================

def get_user(user_id):
    conn = sqlite3.connect("kions.db")
    cursor = conn.cursor()
    cursor.execute("SELECT kions, last_daily FROM player_kions WHERE user_id = ?", (user_id,))
    data = cursor.fetchone()

    if data is None:
        cursor.execute("INSERT INTO player_kions (user_id, kions, last_daily) VALUES (?, 0, 0)", (user_id,))
        conn.commit()
        conn.close()
        return 0, 0

    conn.close()
    return data

def update_kions(user_id, amount):
    conn = sqlite3.connect("kions.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE player_kions SET kions = kions + ? WHERE user_id = ?", (amount, user_id))
    conn.commit()
    conn.close()

def update_daily(user_id):
    conn = sqlite3.connect("kions.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE player_kions SET last_daily = ? WHERE user_id = ?", (int(time.time()), user_id))
    conn.commit()
    conn.close()

# ==========================
# EVENTO
# ==========================

@bot.event
async def on_ready():
    print("🌟 Sistema de Kions iniciado com sucesso!")

# ==========================
# COMANDO SALDO
# ==========================

@bot.command()
async def kions(ctx):
    saldo, _ = get_user(ctx.author.id)

    embed = discord.Embed(
        title="💰 Carteira de Kions",
        description=f"{ctx.author.mention}, aqui está o saldo atual da sua carteira:",
        color=discord.Color.gold()
    )

    embed.add_field(name="Saldo Disponível", value=f"✨ **{saldo} Kions**", inline=False)
    embed.set_footer(text="Continue participando para ganhar mais Kions!")

    await ctx.send(embed=embed)

# ==========================
# RECOMPENSA DIÁRIA
# ==========================

@bot.command()
async def daily(ctx):
    saldo, last_daily = get_user(ctx.author.id)
    now = int(time.time())

    if now - last_daily >= 86400:
        reward = random.randint(1500, 2000)
        update_kions(ctx.author.id, reward)
        update_daily(ctx.author.id)

        embed = discord.Embed(
            title="🎁 Recompensa Diária Coletada!",
            description=f"{ctx.author.mention}, você reivindicou sua recompensa diária com sucesso!",
            color=discord.Color.green()
        )

        embed.add_field(name="Kions Recebidos", value=f"🌟 **{reward} Kions**", inline=False)
        embed.add_field(name="Novo Saldo", value=f"💎 **{saldo + reward} Kions**", inline=False)
        embed.set_footer(text="Volte amanhã para receber mais recompensas!")

        await ctx.send(embed=embed)

    else:
        remaining = 86400 - (now - last_daily)
        hours = remaining // 3600
        minutes = (remaining % 3600) // 60

        embed = discord.Embed(
            title="⏳ Recompensa Já Coletada",
            description=f"{ctx.author.mention}, você já coletou sua recompensa diária.",
            color=discord.Color.red()
        )

        embed.add_field(
            name="Tempo Restante",
            value=f"🕒 Volte em **{hours} horas e {minutes} minutos**.",
            inline=False
        )

        embed.set_footer(text="A paciência também recompensa 😉")

        await ctx.send(embed=embed)

# ==========================
# INICIAR BOT
# ==========================

bot.run("MTQ3NjI5NDQ1NTUyNjAzNTgwMA.G1PwKJ.RAGHSHKQd5RVVIBGyBu4v-7XO4w4Nh4j-wwAMw")