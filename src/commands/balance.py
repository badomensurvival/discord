import discord
from discord.ext import commands
from controllers import players_controller
import os

DISCORD_CHANNEL = [int(code)
                   for code in os.getenv("DISCORD_CHANNEL").split(';')]


class Balance(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def _formatted_money(self, value: float) -> str:
        money = None

        if value > 999999:
            money = value/1_000_000
            return f"{money:.2f}M"
        elif value > 999:
            money = value/1_000
            return f"{money:.2f}K"
        else:
            return f"{value:.2f}"

    @commands.command(aliases=["balancetop"])
    async def baltop(self, ctx):
        if(ctx.message.channel.id in DISCORD_CHANNEL):
            try:
                embed = discord.Embed(
                    title="Top Balance",
                    description="Players with the highest balance of the server.",
                    color=discord.Colour.gold(),
                )

                balance_top = players_controller.toplist_balance(limit=12)

                embed.set_thumbnail(
                    url=f'https://cravatar.eu/helmavatar/{balance_top[0].username}/120.png')

                for player in balance_top:

                    embed.add_field(
                        name=f"{player.username}",
                        value=self._formatted_money(player.balance),
                        inline=True,
                    )

                await ctx.send(
                    embed=embed
                )
            except:
                await ctx.send('This command could not be executed. Please contact the administrator.')

    @commands.command(aliases=["balance"], pass_context=True)
    async def bal(self, ctx, user: str or discord.Member = None):
        username = user or ctx.message.author.display_name

        if(ctx.message.channel.id in DISCORD_CHANNEL):
            try:
                embed = discord.Embed(
                    title=f"{username} balance",
                    description="This is the balance amount.",
                    color=discord.Colour.gold(),
                )

                balance_top = players_controller.player_balance(
                    username)

                embed.set_thumbnail(
                    url=f'https://cravatar.eu/helmavatar/{balance_top[0].username}/120.png')

                for player in balance_top:

                    embed.add_field(
                        name=f"{player.username}",
                        value=self._formatted_money(player.balance),
                        inline=False,
                    )

                await ctx.send(
                    embed=embed
                )
            except:
                if user:
                    await ctx.send('We could not find your profile. Please make sure you are typing the right player nickname.')
                else:
                    await ctx.send('We could not find your profile. Please make sure the nickname on discord is the same used on the server.')


def setup(bot):
    bot.add_cog(Balance(bot))
