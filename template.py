from discord.ext import commands

class template(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def commande1(self,ctx):
        await ctx.channel.send('1')

def setup(client):
    client.add_cog(template(client))