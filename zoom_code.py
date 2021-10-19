import json
import discord
from discord.ext import commands
import random
from PIL import Image
import glob
import os

# gain et perte de LP par difficulté
gain_easy = 5
gain_medium = 10
gain_hard = 15
gain_boss = 22

loss_easy = 8
loss_medium = 4
loss_hard = 3
loss_boss = 2

# infos
zoom_infos = [False]
lol1 = [x.replace("champions/champions1/","") for x in glob.glob("champions/champions1/*_*.*")]
lol2 = [x.replace("champions/champions2/","") for x in glob.glob("champions/champions2/*_*.*")]
lol = lol1 + lol2
essais_max = 4

class zoom_code(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self,message):
      # si un message est envoyé dans la conv où la commande a été appelée
      if zoom_infos[0] and message.channel == zoom_infos[1].channel and not message.content.startswith('!'):
          contexte = zoom_infos[1]
          difficulty = zoom_infos[5]
          # ajoute le joueur s'il est nouveau
          add_new_player(message.author.name)
          if message.content.lower() == zoom_infos[3]: # bonne réponse
            await times_up(zoom_infos[1], zoom_infos[2], zoom_infos[3], zoom_infos[4], zoom_infos[5], zoom_infos[6])
            await contexte.channel.send('Bonne réponse '+message.author.name+' !')
            update(message.author.name, True, difficulty)
          else:
            if zoom_infos[4] == essais_max or message.content.lower() == 'stop':
              champion = zoom_infos[3]
              await times_up(zoom_infos[1], zoom_infos[2], zoom_infos[3], zoom_infos[4], zoom_infos[5], zoom_infos[6])
              await contexte.channel.send('C\'était **'+champion.replace(champion[0], champion[0].upper(), 1)+'** !')
              update(message.author.name, False, difficulty)
            else:
              update(message.author.name, False, difficulty)
          if len(zoom_infos) > 1:
            zoom_infos[4] += 1

    @commands.command()
    async def zoom(self,ctx, arg=None):
      if str(arg).lower() == 'help':
        embed = discord.Embed(
          title = 'Zoom',
          # description = elo,
          colour = discord.Colour.purple()
          )
        rules = 'Une image zoomée d\'un personnage de League Of Legends est envoyée, les joueurs ont 4 tentatives pour trouver duquel il s\'agit.\nOn peut choisir un niveau de difficulté en ajoutant les arguments suivants après `!zoom`:\n- _easy_\n- _hard_\n- _boss_\nLe niveau de base est _medium_.\n\nLes apostrophes et les accents dans les noms ne sont pas comptés mais les espaces sont conservés. Par exemple **kog\'maw** et **maître yi** doivent être respectivement écrit **kogmaw** et ** maitre yi**.\nAttention: **jarvan** s\'écrit **jarvan IV**\n\nLe gain et la perte de LP fonctionnent de la manière suivante:\n- _easy_ : Gain = '+str(gain_easy)+', Perte = '+str(loss_easy)+'\n- _medium_ : Gain = '+str(gain_medium)+', Perte = '+str(loss_medium)+'\n- _hard_ : Gain = '+str(gain_hard)+', Perte = '+str(loss_hard)+'\n- _boss_ : Gain = '+str(gain_boss)+', Perte = '+str(loss_boss)+'\nLa perte de LP est effective à **chaque** mauvaise réponse.\nIl y a '+str(len(lol))+' images différentes.'
        file = discord.File('bot_image/kindred.png', filename='image.png')
        embed.set_image(url="attachment://image.png")
        embed.add_field(name='Règles', value=rules,inline=False)
        await ctx.send(file=file, embed=embed)
      else:
        # récupération du nom de l'auteur de la commande
        username = ctx.message.author.name
        if str(arg).lower() == 'hard':
          difficulty = 'hard'
          cut = 5
        elif str(arg).lower() == 'easy':
          cut = 3
          difficulty = 'easy'
        elif str(arg).lower() == 'boss':
          cut = 7
          difficulty = 'boss'
        elif arg == None:
          cut = 4
          difficulty = 'medium'
        else:
          cut = 4
          difficulty = 'medium'
        if not zoom_infos[0]:
          # nombre d'images disponibles
          number = len(lol)
          # indice de l'image tirée
          r = random.randint(1, number) - 1
          picture = lol[r]
          num = ""
          x = 0
          while picture[x] != "_":
            num += picture[x]
            x += 1
          champion = picture.replace(num+"_","")
          if(".jpg" in champion):
            champion = champion.replace(".jpg","")
          elif(".png" in champion):
            champion = champion.replace(".png","")
          elif(".jpeg" in champion):
            champion = champion.replace(".jpeg","")
          # ajout des infos
          zoom_infos[0] = True
          zoom_infos.append(ctx)
          zoom_infos.append(picture)
          zoom_infos.append(champion)
          zoom_infos.append(0)
          zoom_infos.append(difficulty)
          zoom_infos.append(int(num))
          # dans quel dossier est l'image
          if int(num) > len(lol1):
            image = Image.open('champions/champions2/'+picture)
          else:
            image = Image.open('champions/champions1/'+picture)
          largeur = image.size[0]
          hauteur = image.size[1]
          left = random.randint(0, int(largeur-(largeur/cut)))
          right = left + int((largeur/cut))
          top = random.randint(0, int(hauteur-(hauteur/cut)))
          bottom = top + int((hauteur/cut))
          image_zoomed = image.crop((left, top, right, bottom))
          image_zoomed.convert('RGB').save('champions/zoom.jpg')
          await ctx.channel.send(file=discord.File('champions/zoom.jpg'))
          os.remove('champions/zoom.jpg')
        else:
          await ctx.channel.send(username+' une partie est déjà en cours !')

    @commands.command()
    async def profile(self,ctx, arg=None):
      if arg == None:
        username = ctx.message.author.name
      else:
        username = str(arg)
      with open('zoom.json') as json_file:
        data = json.load(json_file)
      if username in data:
        elo = convert_point_into_elo(data[username]['elo'])
        ligue = ""
        i = 0
        while elo[i] != ' ':
          ligue += elo[i]
          i += 1
        embed = discord.Embed(
          title = username,
          description = elo,
          colour = discord.Colour.blue()
          )
        #embed.set_footer(text='footer')
        file = discord.File('rank/'+ligue.lower()+'.png', filename='image.png')
        embed.set_image(url="attachment://image.png")
        wr = int(100*data[username]['winrate'])
        embed.add_field(name='Winrate global', value=str(wr)+'%',inline=True)
        embed.add_field(name='Nombre de partie', value=data[username]['nb_games'],inline=True)
        # winrate easy
        if data[username]['nb_easy'] == 0:
          wr_easy = 0
        else:
          wr_easy = int(100*data[username]['nb_win_easy']/data[username]['nb_easy'])
        # winrate medium
        if data[username]['nb_medium'] == 0:
          wr_medium = 0
        else:
          wr_medium = int(100*data[username]['nb_win_medium']/data[username]['nb_medium'])
        # winrate hard
        if data[username]['nb_hard'] == 0:
          wr_hard = 0
        else:
          wr_hard = int(100*data[username]['nb_win_hard']/data[username]['nb_hard'])
        # winrate boss
        if data[username]['nb_boss'] == 0:
          wr_boss = 0
        else:
          wr_boss = int(100*data[username]['nb_win_boss']/data[username]['nb_boss'])
        # ajouts de fields
        embed.add_field(name='Winrate Easy', value=str(wr_easy)+'%',inline=True)
        embed.add_field(name='Winrate Medium', value=str(wr_medium)+'%',inline=True)
        embed.add_field(name='Winrate Hard', value=str(wr_hard)+'%',inline=True)
        embed.add_field(name='Winrate Boss', value=str(wr_boss)+'%',inline=True)
        if data[username]['bo5'][0]: # si le joueur est en bo
          win = get_value_promo(username)[0]
          loose = get_value_promo(username)[1]
          embed.add_field(name='BO', value=str(win)+'W - '+str(loose)+'L',inline=False)
        await ctx.channel.send(file=file, embed=embed)  
      else:
        await ctx.channel.send(username+' n\'a pas de profil') 

    @commands.command()
    async def rank(self,ctx):
      with open('zoom.json') as json_file:
        data = json.load(json_file)
      k = list(data.keys())
      elo = [data[x]['elo'] for x in k]
      t = []
      bo = []
      for x in range(len(k)):
          if elo[x] < 0:
              bo.append((k[x], elo[x]))
          else:
              t.append((k[x], elo[x]))
      bo.sort(key=takeSecond)
      t.sort(key=takeSecond,reverse=True)
      res = bo + t
      message = ''
      for i in range(len(res)):
          message += '_'+res[i][0]+'_ : '+convert_point_into_elo(res[i][1])+'\n'
      await ctx.channel.send(message)

def setup(client):
    client.add_cog(zoom_code(client))

async def times_up(contexte, picture, champion, nb_essai, difficulty, num):
      zoom_infos[0] = False
      if len(zoom_infos) > 1:
        if num > len(lol1):
          await zoom_infos[1].send(file=discord.File('champions/champions2/'+picture))
        else:
          await zoom_infos[1].send(file=discord.File('champions/champions1/'+picture))
        zoom_infos.remove(contexte)
        zoom_infos.remove(picture)
        zoom_infos.remove(champion)
        zoom_infos.remove(nb_essai)
        zoom_infos.remove(difficulty)
        zoom_infos.remove(num)
        @commands.command()
        async def rank(self,ctx):
          with open('zoom.json') as json_file:
            data = json.load(json_file)
          k = list(data.keys())
          elo = [data[x]['elo'] for x in k]
          t = []
          bo = []
          for x in range(len(k)):
              if elo[x] < 0:
                  bo.append((k[x], elo[x]))
              else:
                  t.append((k[x], elo[x]))
          bo.sort(key=takeSecond)
          t.sort(key=takeSecond,reverse=True)
          res = bo + t
          message = ''
          for i in range(len(res)):
              message += '_'+res[i][0]+'_ : '+convert_point_into_elo(res[i][1])+'\n'
          await ctx.channel.send(message)

def create_json():
  data = {}
  with open('zoom.json', 'w') as outfile:
    json.dump(data, outfile)

def add_new_player(name):
  with open('zoom.json') as json_file:
    data = json.load(json_file)
    if name not in data:
      data[name] = {
          'elo': 0,
          'bo5': (False, [-1,-1,-1,-1,-1], 0, 'not started'),
          'winrate': 1,
          'nb_win':0,
          'nb_games':0,
          'nb_easy':0,
          'nb_medium':0,
          'nb_hard':0,
          'nb_boss':0,
          'nb_win_easy':0,
          'nb_win_medium':0,
          'nb_win_hard':0,
          'nb_win_boss':0
      }
      with open('zoom.json', 'w') as outfile:
          json.dump(data, outfile)

def convert_point_into_elo(point):
  ligue = ""
  if point >= 0 and point < 400:
    ligue += 'Iron '
    if point >= 0 and point < 100:
      ligue += '4 - '+str(point)
    elif point >= 100 and point < 200:
      ligue += '3 - '+str(point-100)
    elif point >= 200 and point < 300:
      ligue += '2 - '+str(point-200)
    elif point >= 300 and point < 400:
      ligue += '1 - '+str(point-300)

  if point >= 400 and point < 800:
    ligue += 'Bronze '
    if point >= 400 and point < 500:
      ligue += '4 - '+str(point-400)
    elif point >= 500 and point < 600:
      ligue += '3 - '+str(point-500)
    elif point >= 600 and point < 700:
      ligue += '2 - '+str(point-600)
    elif point >= 700 and point < 800:
      ligue += '1 - '+str(point-700)

  if point >= 800 and point < 1200:
    ligue += 'Silver '
    if point >= 800 and point < 900:
      ligue += '4 - '+str(point-800)
    elif point >= 900 and point < 1000:
      ligue += '3 - '+str(point-900)
    elif point >= 1000 and point < 1100:
      ligue += '2 - '+str(point-1000)
    elif point >= 1100 and point < 1200:
      ligue += '1 - '+str(point-1100)

  if point >= 1200 and point < 1600:
    ligue += 'Gold '
    if point >= 1200 and point < 1300:
      ligue += '4 - '+str(point-1200)
    elif point >= 1300 and point < 1400:
      ligue += '3 - '+str(point-1300)
    elif point >= 1400 and point < 1500:
      ligue += '2 - '+str(point-1400)
    elif point >= 1500 and point < 1600:
      ligue += '1 - '+str(point-1500)

  if point >= 1600 and point < 2000:
    ligue += 'Platinum '
    if point >= 1600 and point < 1700:
      ligue += '4 - '+str(point-1600)
    elif point >= 1700 and point < 1800:
      ligue += '3 - '+str(point-1700)
    elif point >= 1800 and point < 1900:
      ligue += '2 - '+str(point-1800)
    elif point >= 1900 and point < 2000:
      ligue += '1 - '+str(point-1900)

  if point >= 2000 and point < 2400:
    ligue += 'Diamond '
    if point >= 2000 and point < 2100:
      ligue += '4 - '+str(point-2000)
    elif point >= 2100 and point < 2200:
      ligue += '3 - '+str(point-2100)
    elif point >= 2200 and point < 2300:
      ligue += '2 - '+str(point-2200)
    elif point >= 2300 and point < 2400:
      ligue += '1 - '+str(point-2300)

  elif point >= 2400 and point < 2800:
    ligue += 'Master '+str(point-2400)
  elif point >= 2800 and point < 3200:
    ligue += 'GrandMaster '+str(point-2400)
  elif point >= 3200:
    ligue += 'Challenger '+str(point-2400)

  # bo
  if point == -1:
    ligue = 'Iron 1 - 100'
  elif point == -2:
    ligue = 'Bronze 1 - 100'
  elif point == -3:
    ligue = 'Silver 1 - 100'
  elif point == -4:
    ligue = 'Gold 1 - 100'
  elif point == -5:
    ligue = 'Platinum 1 - 100'
  elif point == -6:
    ligue = 'Diamond 1 - 100'
  return ligue+' LP'

def update(name, win, difficulty):
  with open('zoom.json') as json_file:
    data = json.load(json_file)
    data[name]['nb_games'] += 1
    if win:
      data[name]['nb_win'] += 1
      if difficulty == 'easy':
        lp_gain(name, gain_easy, 'nb_easy', 'nb_win_easy', data)
      elif difficulty == 'medium':
        lp_gain(name, gain_medium, 'nb_medium', 'nb_win_medium', data)
      elif difficulty == 'hard':
        lp_gain(name, gain_hard, 'nb_hard', 'nb_win_hard', data)
      elif difficulty == 'boss':
        lp_gain(name, gain_boss, 'nb_boss', 'nb_win_boss', data)
    else:
      if difficulty == 'easy':
        lp_loss(name, loss_easy, 'nb_easy', data)
      elif difficulty == 'medium':
        lp_loss(name, loss_medium, 'nb_medium', data)
      elif difficulty == 'hard':
        lp_loss(name, loss_hard, 'nb_hard', data)
      elif difficulty == 'boss':
        lp_loss(name, loss_boss, 'nb_boss', data)
    data[name]['winrate'] = data[name]['nb_win']/data[name]['nb_games']
    with open('zoom.json', 'w') as outfile:
          json.dump(data, outfile)
    
def is_on_promo(name, point, gain, data):
  on_promo = data[name]['bo5'][0]
  if gain < 0 and not data[name]['bo5'][0]:
    return False
  if point + gain >= 400 and point < 400:
    data[name]['bo5'][0] = True
    data[name]['elo'] = -1
    data[name]['bo5'][3] = 'not started'
    on_promo = True
  elif point + gain >= 800 and point > 400 and point < 800:
    data[name]['bo5'][0] = True
    data[name]['elo'] = -2
    data[name]['bo5'][3] = 'not started'
    on_promo = True
  elif point + gain >= 1200 and point > 800 and point < 1200:
    data[name]['bo5'][0] = True
    data[name]['elo'] = -3
    data[name]['bo5'][3] = 'not started'
    on_promo = True
  elif point + gain >= 1600 and point > 1200 and point < 1600:
    data[name]['bo5'][0] = True
    data[name]['elo'] = -4
    data[name]['bo5'][3] = 'not started'
    on_promo = True
  elif point + gain >= 2000 and point > 1600 and point < 2000:
    data[name]['bo5'][0] = True
    data[name]['elo'] = -5
    data[name]['bo5'][3] = 'not started'
    on_promo = True
  elif point + gain >= 2400 and point > 2000 and point < 2400:
    data[name]['bo5'][0] = True
    data[name]['elo'] = -6
    data[name]['bo5'][3] = 'not started'
    on_promo = True
  return on_promo

def won_promo(name, data):
  nb_win = 0
  for x in data[name]['bo5'][1]:
    if x == 1:
      nb_win += 1
  return nb_win == 3

def lost_promo(name, data):
  nb_loose = 0
  for x in data[name]['bo5'][1]:
    if x == 0:
      nb_loose += 1
  return nb_loose == 3

def lp_gain(name, gain, nb, nb_win, data):
  if is_on_promo(name, data[name]['elo'], gain, data):
    indice = data[name]['bo5'][2]
    if data[name]['bo5'][3] == 'not started':
      data[name]['bo5'][3] = 'started'
    else:
      data[name]['bo5'][1][indice] = 1
      data[name]['bo5'][2] += 1
    if won_promo(name, data):
      data[name]['bo5'] = (False, [-1,-1,-1,-1,-1], 0, 'not started')
      if data[name]['elo'] == -1:
        data[name]['elo'] = 415
      elif data[name]['elo'] == -2:
        data[name]['elo'] = 815
      elif data[name]['elo'] == -3:
        data[name]['elo'] = 1215
      elif data[name]['elo'] == -4:
        data[name]['elo'] = 1615
      elif data[name]['elo'] == -5:
        data[name]['elo'] = 2015
      elif data[name]['elo'] == -6:
        data[name]['elo'] = 2415
  else:
    data[name]['elo'] += gain
  data[name][nb] += 1
  data[name][nb_win] += 1

def lp_loss(name, loss, nb, data):
  if is_on_promo(name, data[name]['elo'], -loss, data):
    indice = data[name]['bo5'][2]
    if data[name]['bo5'][3] == 'not started':
      data[name]['bo5'][3] = 'started'
    else:
      data[name]['bo5'][1][indice] = 0
      data[name]['bo5'][2] += 1
    if lost_promo(name, data):
      data[name]['bo5'] = (False, [-1,-1,-1,-1,-1], 0, 'not started')
      if data[name]['elo'] == -1:
        data[name]['elo'] = 370
      elif data[name]['elo'] == -2:
        data[name]['elo'] = 770
      elif data[name]['elo'] == -3:
        data[name]['elo'] = 1170
      elif data[name]['elo'] == -4:
        data[name]['elo'] = 1570
      elif data[name]['elo'] == -5:
        data[name]['elo'] = 1970
      elif data[name]['elo'] == -6:
        data[name]['elo'] = 2370
  elif data[name]['elo'] - loss >= 0:
      data[name]['elo'] -= loss
      # pour eviter qu'un B4 15 LP qui perd 15 LP se retrouve en BO Iron 1 - 100 LP
      if data[name]['elo'] == 400:
        data[name]['elo'] = 390
      elif data[name]['elo'] == 800:
        data[name]['elo'] = 790
      elif data[name]['elo'] == 1200:
        data[name]['elo'] = 119
      elif data[name]['elo'] == 1600:
        data[name]['elo'] = 1590
      elif data[name]['elo'] == 2000:
        data[name]['elo'] = 1990
      elif data[name]['elo'] == 2400:
        data[name]['elo'] = 2390
  else:
    data[name]['elo'] = 0
  data[name][nb] += 1

def get_value_promo(name):
  with open('zoom.json') as json_file:
    data = json.load(json_file)
  win = 0
  loose = 0
  for x in data[name]['bo5'][1]:
    if x == 1:
      win += 1
    elif x == 0:
      loose += 1
  return (win,loose)

def takeSecond(elem):
    return elem[1]

def give_lp_back(players):
  with open('zoom.json') as json_file:
    data = json.load(json_file)
    for p in players:
      data[p[0]]['elo'] += p[1]
      with open('zoom.json', 'w') as outfile:
          json.dump(data, outfile)