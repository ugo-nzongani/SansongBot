from discord.ext import commands
import discord
import random

reavers = ['Liba Senpai !', 'bts sio XD', 'a reaver le gusta las hamburguesas', 'Graves, Udyr, Hecarim... Intéressant...', 'mAjEsTiKwOlF','xreaver33', 'Ce sera 12 nuggets pour moi !','LIBA SENPAIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII', '60% de winrate (en plat)', 'Le Titan Originel Primordial Ancestral', 'Il économise...','From SIO to Google']

class tssg(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def kda(self,ctx):
      nb = 139
      r = random.randint(1, nb)
      await ctx.send(file=discord.File('reaver_kda/reaver kda'+str(r)+'.png'))

    @commands.command()
    async def reaver(self,ctx):
      await ctx.send(random.choice(reavers))

    @commands.command()
    async def rap(self,ctx):
      await ctx.send('https://www.youtube.com/watch?v=2w30JecoQ5A')

    @commands.command()
    async def drive(self,ctx):
      await ctx.send('https://docs.google.com/spreadsheets/d/1EsmBQBvwMUQiyrxF5WKkcmEl6AyQYl0x3IY1AUgMdWg/edit?usp=sharing')

    @commands.command()
    async def jap(self,ctx):
      await ctx.send('https://youtu.be/rTsej-PCNBg')

    @commands.command()
    async def minecraft(self,ctx):
      serveur = '_Pas de serveur pour le moment_'
      version = '1.15.1'
      description = 'Comptes Premiums & Crackés\nLoup-Garous - Hide & Seek - Build - ~~Dojo~~'
      ressources_pack = '_TSSG_\n https://www.dropbox.com/s/jvslc1m3zyst4cp/TSSGBlock.zip?dl=0\n_Hide & Seek_\n https://www.dropbox.com/s/0h65f1od6u22hg3/HideNseek.zip?dl=0'
      embed = discord.Embed(
          title = 'Minecraft',
          # description = elo,
          colour = discord.Colour.green()
          )
      file = discord.File('bot_image/moon.png', filename='image.png')
      embed.set_image(url="attachment://image.png")
      embed.add_field(name='Serveur', value=serveur,inline=False)
      embed.add_field(name='Version', value=version,inline=False)
      embed.add_field(name='Description', value=description,inline=False)
      embed.add_field(name='Ressources packs', value=ressources_pack,inline=False)
      await ctx.send(file=file, embed=embed)

def setup(client):
    client.add_cog(tssg(client))