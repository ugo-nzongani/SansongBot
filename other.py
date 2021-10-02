from discord.ext import commands
import random
import requests
import json

writing_course = {'on' : False}
selecting_course = {}
deleting_course = {}

class other(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self,message):
      msg = message.content
      # écriture d'un cours
      if not message.content.startswith('!') and writing_course['on'] and message.author.name in writing_course and writing_course[message.author.name][0] == message.channel:
        f = open('cours.json',)
        data = json.load(f)
        data[writing_course[message.author.name][1]] += str(message.content)
        f.close()
        with open('cours.json', 'w') as f:
          json.dump(data, f)
        writing_course['on'] = False
        del writing_course[message.author.name]
        await message.channel.send('Cours ajouté !')
      # sélection d'un cours
      if not message.content.startswith('!') and message.author.name in selecting_course and selecting_course[message.author.name][0] == message.channel:
        if str(message.content) in selecting_course[message.author.name][1]:
          f = open('cours.json',)
          data = json.load(f)
          cours = selecting_course[message.author.name][2][int(message.content)-1]
          msg = data[cours]
          await message.channel.send(msg)
          f.close()
          del selecting_course[message.author.name]
        else:
          await message.channel.send('Réessaye avec un numéro de cours valide !')
      # suppression d'un cours
      if not message.content.startswith('!') and message.author.name in deleting_course and deleting_course[message.author.name][0] == message.channel:
        if str(message.content) in deleting_course[message.author.name][1]:
          f = open('cours.json',)
          data = json.load(f)
          cours = deleting_course[message.author.name][2][int(message.content)-1]
          del data[cours]
          await message.channel.send('Cours supprimé !')
          f.close()
          with open('cours.json', 'w') as f:
            json.dump(data, f)
          del deleting_course[message.author.name]
        else:
          await message.channel.send('Réessaye avec un numéro de cours valide !')
          
    @commands.command()
    async def me(self,ctx):
        await ctx.send(ctx.message.author.name)

    @commands.command()
    async def quote(self,ctx):
        quote = get_quote()
        await ctx.channel.send(quote)

    @commands.command()
    async def draw(self,ctx):
      # https://github.com/excalidraw/excalidraw
      link = 'https://excalidraw.com/#room='
      first_part = 20
      second_part = 22
      letter_min1 = ['a','b','c','d','e','f']
      letter_min2 = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
      letter_maj = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
      for i in range(first_part):
        r = random.randint(1, 2)
        if(r == 1):
          suite = random.choice(letter_min1)
        else:
          suite = str(random.randint(0, 9))
        link += suite
      link += ','
      for i in range(second_part):
        r = random.randint(1, 3)
        if(r == 1):
          suite = random.choice(letter_min2)
        elif(r == 2):
          suite = random.choice(letter_maj)
        else:
          suite = str(random.randint(0, 9))
        link += suite
      await ctx.channel.send(link)

    @commands.command()
    async def python(self,ctx):
      code = "```python\nhomer = 0\n```"
      await ctx.send('Bienvenue dans ce tuto Python !\n'+code)

    @commands.command()
    async def cours(self,ctx, *args : str):
      username = ctx.message.author.name
      if args != ():
        if str(args[0]).lower() == 'add':
          # nom du cours
          name = ''
          for i in range(1,len(args)):
            name += ' '+args[i]
          writing_course[username] = [ctx.message.channel,name]
          f = open('cours.json',)
          data = json.load(f)
          if name not in data:
            data[name] = ''
          f.close()
          with open('cours.json', 'w') as f:
            json.dump(data, f)
          writing_course['on'] = True
        elif str(args[0]).lower() == 'delete':
          f = open('cours.json',)
          data = json.load(f)
          list_courses = ''
          cpt = 1
          cpt_list = []
          names_list = []
          for i in data.keys():
            cpt_list.append(str(cpt))
            names_list.append(i)
            list_courses += str(cpt)+' - '+i+'\n'
            cpt += 1
          await ctx.send('Choisis un cours (son numéro) à supprimer parmis les suivants:\n\n'+list_courses)
          deleting_course[username] = [ctx.message.channel,cpt_list,names_list]
        elif str(args[0]).lower() == 'help':
          await ctx.send('**!cours** donne une liste de cours disponibles\n\nPour ajouter un cours: **!cours add**\nLe prochain message correspond au cours ajouté\n\nPour supprimer un cours: **!cours delete**\nLe prochain message indique le numéro du cours à supprimer')
        else:
          await ctx.send('L\'argument '+str(args[0])+'n\'est pas valide')
      else:
        f = open('cours.json',)
        data = json.load(f)
        list_courses = ''
        cpt = 1
        cpt_list = []
        names_list = []
        for i in data.keys():
          cpt_list.append(str(cpt))
          names_list.append(i)
          list_courses += str(cpt)+' - '+i+'\n'
          cpt += 1
        await ctx.send('Choisis un cours (son numéro) parmis les suivants:\n\n'+list_courses)
        selecting_course[username] = [ctx.message.channel,cpt_list,names_list]
        
# récupère une citation pour la commande !quote
def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " - " + json_data[0]['a']
  return(quote)

def setup(client):
    client.add_cog(other(client))