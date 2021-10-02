from discord.ext import commands
import discord
import random

reavers = ['Liba Senpai !', 'bts sio XD', 'a reaver le gusta las hamburguesas', 'Graves, Udyr, Hecarim... Intéressant...', 'mAjEsTiKwOlF','xreaver33', 'Ce sera 12 nuggets pour moi !','LIBA SENPAIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII', '60% de winrate (en plat)', 'Le Titan Originel Primordial Ancestral', 'Il économise...']

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
    async def jap(self,ctx):
      await ctx.send('https://youtu.be/rTsej-PCNBg')

    @commands.command()
    async def minecraft(self,ctx):
      serveur = 'Serveur: '+ '**Pas de serveur pour le moment**' + '\n'
      version = 'Version: '+ '1.15.1' + '\n'
      description = 'Comptes: Premiums & Crackés' + '\n'
      ressources_pack = [
        'Ressources packs:' + '\n',
        'TSSG: https://www.dropbox.com/s/jvslc1m3zyst4cp/TSSGBlock.zip?dl=0'+ '\n',
      'Hide & Seek: https://www.dropbox.com/s/0h65f1od6u22hg3/HideNseek.zip?dl=0'+ '\n'
      ]
      await ctx.send(serveur+version+description+ressources_pack[0]+ressources_pack[1]+ressources_pack[2])

def setup(client):
    client.add_cog(tssg(client))