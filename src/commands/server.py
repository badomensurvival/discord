import discord
from discord.ext import commands
from controllers import server_controller
import os

DISCORD_CHANNEL = [int(code)
                   for code in os.getenv("DISCORD_CHANNEL").split(';')]


class Server(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    # @commands.Cog.listener()
    # async def on_member_join(self, member):
    #     channel = member.guild.system_channel
    #     if channel is not None:
    #         await channel.send('Welcome {0.mention}.'.format(member))

    @ commands.command(name='playerlist')
    async def _playerlist(self, ctx):
        if(ctx.message.channel.id in DISCORD_CHANNEL):
            try:
                query = server_controller.query()
                online_players = query.players.online
                max_player = query.players.max
                current_players = query.players.names

                await ctx.send(
                    f'Online players ({online_players}/{max_player}) \n`{", ".join(current_players) if online_players > 0 else "No players online"}`'
                )
            except Exception as e:
                print(e)

                await ctx.send('This command could not be executed. Please contact the administrator.')


def setup(bot):
    bot.add_cog(Server(bot))
