import discord
from discord.ext import commands
from controllers import players_controller
import os

DISCORD_CHANNEL = [int(code)
                   for code in os.getenv("DISCORD_CHANNEL").split(';')]


class PlayTime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def playtop(self, ctx):
        if(ctx.message.channel.id in DISCORD_CHANNEL):
            try:
                embed = discord.Embed(
                    title="Top Playtime",
                    description="Players with the highest playtime of the server.",
                    color=discord.Colour.green(),
                )

                play_top = players_controller.toplist_playedtime(limit=12)

                embed.set_thumbnail(
                    url=f'https://cravatar.eu/helmavatar/{play_top[0]["username"]}/120.png')

                for player in play_top:
                    embed.add_field(
                        name=player['username'],
                        value=player['played_time'],
                        inline=True,
                    )

                await ctx.send(
                    embed=embed
                )
            except Exception as e:
                print(e)

                await ctx.send('This command could not be executed. Please contact the administrator.')

    def _playertime(user):
        return players_controller.player_playtime(username=user)

    @commands.command(pass_context=True)
    async def playtime(self, ctx, user: str = None):
        if(ctx.message.channel.id in DISCORD_CHANNEL):
            username = user or ctx.message.author.display_name
            try:
                embed = discord.Embed(
                    title=f"{username} playtime",
                    description="This is the overall playtime",
                    color=discord.Colour.green(),
                )

                player_playtime = players_controller.player_playtime(
                    username)

                embed.set_thumbnail(
                    url=f'https://cravatar.eu/helmavatar/{player_playtime[0]["username"]}/120.png')

                for player in player_playtime:

                    embed.add_field(
                        name=player['username'],
                        value=player['played_time'],
                        inline=True,
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
    bot.add_cog(PlayTime(bot))
