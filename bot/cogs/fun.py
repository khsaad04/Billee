import datetime as dt
import random
from os import error

import asyncpraw
import discord
from discord.ext import commands

reddit = asyncpraw.Reddit(
    client_id="GBJPsdrBzffaFxQ2M6hR-Q",
    client_secret="ceh_1lb_CD-ysgzMSlJm3AHpfV9sYw",
    username="billy123lol",
    password="billybelookinthicc",
    user_agent="billy123",
)


class Fun(commands.Cog, description="Fun commands for time pass"):
    def __init__(self, bot):
        self.bot = bot

    # meme_command

    all_subs = []

    async def gen_memes(self):
        subreddit = await reddit.subreddit('memes')
        posts = subreddit.hot(limit=25)
        async for submission in posts:
            self.all_subs.append(submission)

        subreddit2 = await reddit.subreddit('dankmemes')
        posts2 = subreddit2.hot(limit=25)
        async for submission in posts2:
            self.all_subs.append(submission)

    @commands.Cog.listener()
    async def on_ready(self):
        await self.gen_memes()

    @commands.group(name='Meme', invoke_without_command=True, case_insensitive=True)
    async def meme_group(self, ctx):

        random_sub = random.choice(self.all_subs)
        self.all_subs.remove(random_sub)
        name = random_sub.title
        url = random_sub.url
        likes = random_sub.score
        comments = random_sub.num_comments
        link = random_sub.permalink

        embed = discord.Embed(title=f"__{name}__",
                              colour=discord.Colour.random(),
                              timestamp=ctx.message.created_at,
                              url=f'https://reddit.com{link}')

        embed.set_author(name=ctx.author.display_name,
                         icon_url=ctx.author.avatar_url)

        embed.set_image(url=url)

        embed.set_footer(text=f"👍 {likes} 💬 {comments}")

        await ctx.send(embed=embed)

        if len(self.all_subs) <= 20:
            await self.all_subs.clear()
            await self.gen_memes()

    @meme_group.command(name="Reload", description="Reloads the pre loaded meme queue for the `Meme` command")
    async def reload_command(self, ctx):
        msg = await ctx.send("Reloading memes ...")
        self.all_subs.clear()
        await self.gen_memes()
        await msg.edit(content="Memes reloaded ✅")

    @meme_group.command(name='Queue', description="Shows the number of memes in queue for the `Meme` command")
    async def queue_command(self, ctx):
        mm = len(self.all_subs)
        await ctx.send(mm)

    # 8ball command
    @commands.command(name="8Ball", description="Ask any quastion for a random answer.\n`classic 8ball command`")
    async def _8ball_command(self, ctx, *, qs):
        replies = [
            '> It is certain.',
            '> It is decidedly so.',
            '> Without a doubt.',
            '> Yes definitely.',
            '> You may rely on it.',
            '> As I see it, yes.',
            '> Most likely.',
            '> Outlook good.',
            '> Yes.',
            '> Signs point to yes.',
            '> Reply hazy, try again.',
            '> Ask again later.',
            '> Better not tell you now.',
            '> Cannot predict now.',
            '> Concentrate and ask again.',
            '> Dont count on it.',
            '> My reply is no.',
            '> My sources say no.',
            '> Outlook not so good.',
            '> Very doubtful.',
        ]

        em = discord.Embed(
            title='8Ball',
            description=f'{ctx.author.display_name} asked: {qs} \n{random.choice(replies)}',
            color=discord.Color.random())

        await ctx.send(embed=em)

    @commands.command(name="React", description="A test command made to check the bot's latency for adding reactions and `ws_rate_limiting`")
    async def react_command(self, ctx):
        msg = await ctx.send("Mmm wait ...")
        s1 = dt.datetime.utcnow().second
        ms1 = dt.datetime.utcnow().microsecond
        t_delta1 = (s1+(ms1/1000000))

        emojiList = ["😀", "😁", "😂", "🤣", "😃", "😄", "😅"]
        for i in emojiList:
            await msg.add_reaction(i)
            s2 = dt.datetime.utcnow().second
            ms2 = dt.datetime.utcnow().microsecond
            t_delta2 = (s2+(ms2/1000000))

        time_delta = t_delta2 - t_delta1

        await msg.edit(content=f"reacted 7 emojis in {time_delta} seconds")
        print(dt.datetime.utcnow())

    @commands.command(name="Ping", aliases=["Latency"], description="Shows the latency of the actual bot")
    async def ping_command(self, ctx):
        await ctx.send("{0} ms.".format(round(self.bot.latency, 1)))


def setup(bot):
    bot.add_cog(Fun(bot))
