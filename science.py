from discord.ext import commands
import math
import numpy as np
import matplotlib.pyplot as plt
import os
import discord

class science(commands.Cog):
    def __init__(self, client):
        self.client = client

    # résout une équation du second degré
    @commands.command()
    async def eq2(self,ctx, a : int, b : int, c : int, *args : str):
      delta = b*b - (4*a*c)
      solution = ''
      if delta == 0:
        sol = (-b)/(2*a)
        solution += 'x = '+str(sol)
      elif delta > 0:
        sol1 = (-b + math.sqrt(delta))/(2*a)
        sol2 = (-b - math.sqrt(delta))/(2*a)
        solution += 'x1 = '+str(sol1)+'\n'+'x2 = '+str(sol2)
      else:
        solution += 'Il n\'y a pas de solution réelle'
      await ctx.send('Résolution de '+str(a)+'x² + '+str(b)+'x + '+str(c)+' = 0\nΔ = '+str(delta)+'\n'+solution)
      if(args != () and str(args[0]).lower() == 'plot'):
        x = np.arange(-10, 10)
        y = []
        for i in x:
          y.append(a*i*i + b*i + c)
        figure, ax = plt.subplots()
        if(delta > 0):
          ax.scatter([sol1, sol2], [0,0], color='red')
        elif(delta == 0):
          ax.scatter([sol], [0], color='red')
        ax.plot(x,y)
        ax.grid(True)
        ax.spines['left'].set_position('zero')
        ax.spines['right'].set_color('none')
        ax.spines['bottom'].set_position('zero')
        ax.spines['top'].set_color('none')
        plt.title(str(a)+'x² + '+str(b)+'x + '+str(c)+' = 0', color='red')
        figure.savefig(fname='function/f')
        await ctx.send(file=discord.File('function/f.png'))
        os.remove('function/f.png')

    # forme canonique d'un polynome du second degré
    @commands.command()
    async def cano(self,ctx, a : int, b : int, c : int):
      delta = b*b - (4*a*c)
      alpha = -b/(2*a)
      beta = -delta/(4*a)
      await ctx.send('Forme canonique de '+str(a)+'x² + '+str(b)+'x + '+str(c)+'\n'+'a(x - α)² + β = '+str(a)+'(x - '+str(alpha)+')² + '+str(beta))

def setup(client):
    client.add_cog(science(client))

