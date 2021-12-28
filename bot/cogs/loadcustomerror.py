import discord
from bot.tools.error import CommandErrorHandler
from discord.ext import commands


def setup(bot):
    bot.add_cog(CommandErrorHandler(bot))
