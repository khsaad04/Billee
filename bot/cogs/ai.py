from discord.ext import commands
from prsaw import RandomStuff

with open("data/prsaw_key.0", "r", encoding="utf-8") as tf:
    api_key = tf.read()

rs = RandomStuff(async_mode=True, api_key=api_key)


class ai(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener("on_message")
    async def on_message(self, message):
        if not message.author.bot:
            if message.channel.name == "chatbot":
                response = await rs.get_ai_response(message.content)
                await message.reply(response[0]["message"])
            else:
                return
        else:
            return


def setup(bot):
    bot.add_cog(ai(bot))