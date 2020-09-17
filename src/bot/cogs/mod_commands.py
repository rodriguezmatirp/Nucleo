from typing import Union

import discord
from discord.ext import commands
from discord.ext.commands import Context

from dependencies.database import Database
from . import bot_checks


class ModCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db: Database = bot.db

    @commands.command()
    @bot_checks.check_permission_level(8)
    async def purge(self, ctx: Context, option_1: Union[discord.member.User, int] = None, option_2: int = 5):
        user = None
        if isinstance(option_1, int):
            count = option_1
        else:
            user = option_1
            count = option_2

        def user_check(message):
            return user is None or user.id == message.author.id

        if ctx.channel.guild is None:
            await ctx.send("This is not a Text channel")
            return
        if count > 500:
            count = 500
        deleted = await ctx.channel.purge(limit=count + 1, check=user_check)
        await ctx.send('Deleted {} message(s)'.format(len(deleted)), delete_after=5)


def setup(bot):
    cog = ModCommands(bot)
    bot.add_cog(cog)
