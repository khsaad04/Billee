import sys
import traceback

import discord
from discord.ext import commands

# _____________________________________music_command_error__________________________________


class AlreadyConnectedToChannel(commands.CommandError):
    pass


class NoVoiceChannel(commands.CommandError):
    pass


class QueueIsEmpty(commands.CommandError):
    pass


class NoTracksFound(commands.CommandError):
    pass


class PlayerIsAlreadyPaused(commands.CommandError):
    pass


class NoMoreTracks(commands.CommandError):
    pass


class NoPreviousTracks(commands.CommandError):
    pass


class InvalidRepeatMode(commands.CommandError):
    pass


class VolumeTooLow(commands.CommandError):
    pass


class VolumeTooHigh(commands.CommandError):
    pass


class MaxVolume(commands.CommandError):
    pass


class MinVolume(commands.CommandError):
    pass


class NoLyricsFound(commands.CommandError):
    pass


class InvalidEQPreset(commands.CommandError):
    pass


class NonExistentEQBand(commands.CommandError):
    pass


class EQGainOutOfBounds(commands.CommandError):
    pass


class InvalidTimeString(commands.CommandError):
    pass


class CommandErrorHandler(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):

        if hasattr(ctx.command, 'on_error'):
            return

        cog = ctx.cog
        if cog:
            if cog._get_overridden_method(cog.cog_command_error) is not None:
                return

        ignored = (commands.CommandNotFound, )

        error = getattr(error, 'original', error)

        if isinstance(error, ignored):
            return

        elif isinstance(error, commands.BadArgument):
            em = discord.Embed(title="An error occurred",
                               description=f"Something went wrong, make sure you have passed the arguments correctly.",
                               color=discord.Colour.red())
            em.add_field(
                name="Usage:", value="{self.bot.prefix}{ctx.command.signature}")
            em.set_footer(text="<> is required and [] is optional")

            await ctx.send(embed=em)

        elif isinstance(error, commands.MissingRequiredArgument):
            em2 = discord.Embed(title="An error occurred",
                                description=f"You are missing required arguments.",
                                color=discord.Colour.red())
            em2.add_field(
                name="Usage:", value="{self.bot.prefix}{ctx.command.signature}")
            em2.set_footer(text="<> is required and [] is optional")

            await ctx.send(embed=em2)

        elif isinstance(error, commands.MemberNotFound):
            em3 = discord.Embed(
                title="An Error Occurred",
                description="Couldn't find the user. You can mention a member, write their id(descrim: optional) or give their user ID. Make sure you have put the information correct",
                color=discord.Colour.red())

            await ctx.send(embed=em3)

        elif isinstance(error, commands.MissingPermissions):
            em4 = discord.Embed(
                title="An Error Occurred",
                description="You don't have all the required perms to use that command :)",
                color=discord.Colour.red())

            await ctx.send(embed=em4)

        else:
            print('Ignoring exception in command {}:'.format(
                ctx.command), file=sys.stderr)
            traceback.print_exception(
                type(error), error, error.__traceback__, file=sys.stderr)


def setup(bot):
    bot.add_cog(CommandErrorHandler(bot))
