from discord.ext import commands
import discord

class Ping(commands.Cog):
    """Comandos divertidos"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # Comando de texto
    @commands.command(name="ping")
    async def ping_text(self, ctx: commands.Context):
        await ctx.send(f"Pong! {round(self.bot.latency * 1000)}ms")

    # Comando slash (aparecerá instantaneamente no seu servidor de teste)
    @discord.slash_command(name="ping", description="Responde com Pong!")
    async def ping_slash(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Pong! {round(self.bot.latency * 1000)}ms")

# Função setup moderna
async def setup(bot: commands.Bot):
    await bot.add_cog(Ping(bot))