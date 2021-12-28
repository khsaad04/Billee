import asyncio

import discord
from discord.ext import commands
from bot.tools.conv import *


class Moderation(commands.Cog,
                 description="Commands for staffs to hit em' with the mute/kick/ban lmao"):
    def __init__(self, bot):
        self.bot = bot

    # kick_command
    @commands.command(name="Kick", description="Kicks a member out of guild")
    @commands.has_permissions(kick_members=True)
    async def kick_command(self,
                           ctx,
                           member: ChannelOrMemberConverter,
                           *,
                           reason="No reason provided"):
        embed = discord.Embed(
            title='User kicked',
            description=f'{member} has been kicked. for: {reason}',
            color=discord.Colour.green())
        embed.set_footer(icon_url=ctx.author.avatar_url,
                         text=f'kicked by {ctx.author.name}')
        await ctx.send(embed=embed)
        try:
            await member.send(
                f"You have been kicked from PUBGM HANGOUT for: {reason}")
        except:
            await member.kick(reason=reason)

    # ban_command
    @commands.command(name="Ban", description="Permanently bans a member out of guild")
    @commands.has_permissions(ban_members=True)
    async def ban_command(self,
                          ctx,
                          member: ChannelOrMemberConverter,
                          *,
                          reason="No reason provided"):
        embed = discord.Embed(title='User banned',
                              description=f'{member} was banned.',
                              color=discord.Colour.green())
        embed.set_footer(icon_url=ctx.author.avatar_url,
                         text=f'banned by {ctx.author.name}')
        await ctx.send(embed=embed)

        try:
            await member.send(f"You were banned from PUBGM HANGOUT for: {reason}")
        except:
            await ctx.send("Couldn't dm them")
        finally:
            await member.ban(reason=reason)

    # unban_command

    # softban_command

    # mute_command
    @commands.command(name="Mute", description="Mute a member for a specific time or forever if no  time given")
    @commands.has_permissions(kick_members=True)
    async def mute_command(self,
                           ctx,
                           member: ChannelOrMemberConverter,
                           duration: DurationConverter,
                           *,
                           reason="Not provided"):
        muted_role = ctx.guild.get_role(803518369831714816)
        multiplier = {'s': 1, 'm': 60, 'h': 3600, 'd': 216000}
        amount, unit = duration
        await member.add_roles(muted_role)
        embed = discord.Embed(
            title='User muted',
            description=f'{member} was muted for {amount}{unit}, because ```{reason}```',
            color=discord.Colour.green())
        embed.set_footer(icon_url=ctx.author.avatar_url,
                         text=f'muted by {ctx.author.name}')
        await ctx.send(embed=embed)
        await asyncio.sleep(amount * multiplier[unit])
        await member.remove_roles(muted_role)
        embed = discord.Embed(title='User unmuted',
                              description=f'{member} was unmuted.',
                              color=discord.Colour.green())
        embed.set_footer(icon_url=ctx.author.avatar_url,
                         text=f'unmuted by {ctx.author.name}')
        await ctx.send(embed=embed)

    # unmute_command
    @commands.command(name="Unmute", description="Unmutes a member who is already muted.")
    @commands.has_permissions(kick_members=True)
    async def unmute_command(self, ctx, member: ChannelOrMemberConverter):
        muted_role = ctx.guild.get_role(803518369831714816)
        await member.remove_roles(muted_role)
        embed = discord.Embed(title='User unmuted',
                              description=f'{member} was unmuted.',
                              color=discord.Colour.green())
        embed.set_footer(icon_url=ctx.author.avatar_url,
                         text=f'unmuted by {ctx.author.name}')
        await ctx.send(embed=embed)

    # set slowmode_command
    @commands.command(name="Slowmode", description="Sets a slowmode for the particular channel")
    @commands.has_permissions(manage_channels=True)
    async def slowmode_command(self, ctx, seconds: int):
        await ctx.channel.edit(slowmode_delay=seconds)
        em = discord.Embed(title="Updated Slowmode",
                           description=f"Slowmode is now {seconds}sec",
                           color=discord.Colour.green())
        await ctx.send(embed=em)

    # purge_command
    @commands.command(name='Purge', aliases=["Clear"], description="Purges the chat as per the given amount.")
    @commands.has_permissions(manage_messages=True)
    async def clear_command(self, ctx, amount=1):
        amt = amount + 1
        await ctx.channel.purge(limit=amt)
        em = discord.Embed(title="Purged",
                           description=f"deleted {amount} message(s)",
                           colour=discord.Colour.red())

        await ctx.send(embed=em, delete_after=5.0)


def setup(bot):
    bot.add_cog(Moderation(bot))
