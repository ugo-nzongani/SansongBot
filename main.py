import discord
import os
import requests
import json
import random
from keep_alive import keep_alive
from discord.ext import commands
import math
import navy
import matplotlib.pyplot as plt
from PIL import Image
import glob
import zoom_code
import numpy as np

# préfixe des commandes du bot
prefix = '!'
client = commands.Bot(command_prefix=prefix) #discord.Client()

# RECONNAISSANCE DE MOTS
tension = ["tension", "Tension", "TENSION"]
wakateam = ["wakateam", "Wakateam", "waka team"]

wakateam_response = ["Vazy Wakateam tu vas y arriver !", "baka...", "WAKATEAM !!!!!!!!!!!!!!!!", "1 2 3 WAKATEAM !!!!!"]
words_response = ["tempête !"]

# COMMANDE REAVER
reavers = ['Liba Senpai !', 'bts sio XD', 'a reaver le gusta las hamburguesas', 'Graves, Udyr, Hecarim... Intéressant...', 'mAjEsTiKwOlF','xreaver33', 'Ce sera 12 nuggets pour moi !','LIBA SENPAIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII', '60% de winrate (en plat)', 'Le Titan Originel Primordial Ancestral', 'Il économise...']

# BATAILLE NAVALE
in_game = [] # contient la liste des joueurs en jeu
all_grid = {} # dictionnaire associant à chaque joueur un quadruplet contenant:
           # - sa grille
           # - la grille de son adversaire
           # - la vue de sa grille
           # - la vue de la grille de son adversaire
           # - la position de ses bateaux
           # - la position des bateaux de son adversaire

messages_touche = ['Touché !', 'TOUCHÉ !!!!', 'Pixel !']
messages_rate = ['Raté !', 'Encore raté !', 'Fais un effort !', 'Bruh', "Comment c'est possible d'être aussi nul"]
messages_coule = ['Coulé !']
dico = navy.create_dict()

# ZOOM
zoom_infos = [False]
lol1 = [x.replace("champions/champions1/","") for x in glob.glob("champions/champions1/*_*.*")]
lol2 = [x.replace("champions/champions2/","") for x in glob.glob("champions/champions2/*_*.*")]
lol = lol1 + lol2
essais_max = 4

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

# réaction à certains messages
@client.event
async def on_message(message):
  if message.author == client.user:
    return
  msg = message.content
  '''
  if msg.startswith('-inspire'):
    quote = get_quote()
    await message.channel.send(quote)
  '''
  # reconnaissance du mot tension
  if any(word in msg for word in tension):
      await message.channel.send(random.choice(words_response))
  # reconnaissance du mot wakateam
  if any(word in msg for word in wakateam):
      await message.channel.send(random.choice(wakateam_response))
  await client.process_commands(message)
  # ZOOM
  # si un message est envoyé dans la conv où la commande a été appelée
  if zoom_infos[0] and message.channel == zoom_infos[1].channel and not message.content.startswith(prefix):
      contexte = zoom_infos[1]
      difficulty = zoom_infos[5]
      # ajoute le joueur s'il est nouveau
      zoom_code.add_new_player(message.author.name)
      if message.content.lower() == zoom_infos[3]: # bonne réponse
        await times_up(zoom_infos[1], zoom_infos[2], zoom_infos[3], zoom_infos[4], zoom_infos[5], zoom_infos[6])
        await contexte.channel.send('Bonne réponse '+message.author.name+' !')
        zoom_code.update(message.author.name, True, difficulty)
      else:
        if zoom_infos[4] == essais_max - 1 or message.content.lower() == 'stop':
          champion = zoom_infos[3]
          await times_up(zoom_infos[1], zoom_infos[2], zoom_infos[3], zoom_infos[4], zoom_infos[5], zoom_infos[6])
          await contexte.channel.send('C\'était **'+champion.replace(champion[0], champion[0].upper(), 1)+'** !')
          zoom_code.update(message.author.name, False, difficulty)
        else:
          zoom_code.update(message.author.name, False, difficulty)
      if len(zoom_infos) > 1:
        zoom_infos[4] += 1
        
# récupère une citation pour la commande !quote
def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " - " + json_data[0]['a']
  return(quote)

############################## COMMANDES ##############################
@client.command()
async def reaver(ctx):
  await ctx.send(random.choice(reavers))

@client.command()
async def rap(ctx):
  await ctx.send('https://www.youtube.com/watch?v=2w30JecoQ5A')

@client.command()
async def jap(ctx):
  await ctx.send('https://youtu.be/rTsej-PCNBg')

@client.command()
async def minecraft(ctx):
  serveur = 'Serveur: '+ '91.121.44.252:27270' + '\n'
  version = 'Version: '+ '1.15.1' + '\n'
  description = 'Comptes: Premiums & Crackés' + '\n'
  ressources_pack = [
    'Ressources packs:' + '\n',
    'TSSG: https://www.dropbox.com/s/jvslc1m3zyst4cp/TSSGBlock.zip?dl=0'+ '\n',
   'Hide & Seek: https://www.dropbox.com/s/0h65f1od6u22hg3/HideNseek.zip?dl=0'+ '\n'
   ]
  await ctx.send(serveur+version+description+ressources_pack[0]+ressources_pack[1]+ressources_pack[2])

# résout une équation du second degré
@client.command()
async def eq2(ctx, a : int, b : int, c : int, *args : str):
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
  if(args != () and str(args[0]) == 'plot'):
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

@client.command()
async def python(ctx):
  code = "```python\nhomer = 0\n```"
  await ctx.send(code)

@client.command()
async def kda(ctx):
  nb = 139
  r = random.randint(1, nb)
  await ctx.send(file=discord.File('reaver_kda/reaver kda'+str(r)+'.png'))
  
# bataille navale
@client.command()
async def b(ctx, arg=None):
  # récupération du nom de l'auteur de la commande
  username = ctx.message.author.name
  # si l'auteur de la commande est deja dans une partie
  if(username in in_game):
    if(arg == None):
      await ctx.send(username+' tu dois écrire **!b stop** ou **!b <case>**\nExemple: !b A1')
    elif(str(arg) == 'stop'):
      # on supprime toutes les données relatives à la partie
      in_game.remove(username)
      del all_grid[username]
      await ctx.send(username+' déclare forfait.')
    # si la commande de type 'lettre numero' est dans le dictionnaire (aka la case est valide, exemple: !bn A0)
    elif(str(arg) in dico):
      # jouer
      hit, coule = navy.player_attack(all_grid[username][2], all_grid[username][3], dico, str(arg), all_grid[username][5])
      if(hit != 0): # si le joueur attaque une case qu'il n'a pas encore attaqué
        # affichage du résultat de l'attaque
        if(hit == 2):
          await ctx.send(random.choice(messages_rate))
        elif(hit == 1):
          if(coule):
            await ctx.send(random.choice(messages_coule))
          else:
            await ctx.send(random.choice(messages_touche))
        # FAIRE ATTAQUER LE BOT

        # test si un des joueurs a gagné
        # test si l'auteur de la commande a gagné
        if(navy.player_lost(all_grid[username][2], all_grid[username][3])):
          # on supprime toutes les données relatives à la partie
          in_game.remove(username)
          del all_grid[username]
          await ctx.send(username+' a gagné !')
        # test si le bot a gagné
        elif(navy.player_lost(all_grid[username][0], all_grid[username][1])):
          # on supprime toutes les données relatives à la partie
          in_game.remove(username)
          del all_grid[username]
          await ctx.send('J\'ai gagné !')
        # AFFICHAGE DE LA GRILLE DU JOUEUR MISE A JOUR AVEC LATTAQUE DU BOT
        navy.print_grid(all_grid[username][0], 'player_grid', 'Grille de '+username)
        navy.print_grid(all_grid[username][3], 'ennemy_grid_view', 'Grille de Sansong')
        await ctx.send(file=discord.File('navy_grid/player_grid.png'))
        await ctx.send(file=discord.File('navy_grid/ennemy_grid_view.png'))
        await ctx.send('**Tape !b <case> pour attaquer !**\n_Exemple: !b B5_')
      # si le joueur a attaqué une case qu'il avait deja attaqué
      else:
        await ctx.send(username+' tu as déjà attaqué la case '+str(arg)+', choisis une autre case !')
    # si l'auteur de la commande rentre une commande invalide
    else:
      await ctx.send(username+' tu dois écrire **!b stop** ou **!b <case>**\n_Exemple: !b A1_')
  # si l'auteur de la commande n'est pas dans une partie
  else:
    # aucun paramètre n'a été passé
    if(arg == None):
      await ctx.send(username+' tu dois écrire **!b start** pour commencer une partie !')
    # le joueur a écrit start
    elif(str(arg) == 'start'):
      # la partie commence
      # on ajoute son username à in_game
      in_game.append(username)
      player_grid, player_grid_view, ennemy_grid, ennemy_grid_view, player_boat, ennemy_boat = navy.create_grid()
      print(player_boat)
      # mode bateau trouvé
      boat_found = False
      # mode direction trouvé
      direction_found = False
      # ajout du joueur au dictionnaire de jeu
      all_grid[username] = (player_grid, player_grid_view, ennemy_grid, ennemy_grid_view, player_boat, ennemy_boat, boat_found, direction_found)
      # enregistrements des images des grilles dans le dossier navy_grid
      navy.print_grid(all_grid[username][0], 'player_grid', 'Grille de '+username)
      navy.print_grid(all_grid[username][3], 'ennemy_grid_view', 'Grille de Sansong')
      navy.print_grid(all_grid[username][2], 'ennemy_grid', 'Vrai grille de Sansong')
      await ctx.send(file=discord.File('navy_grid/player_grid.png'))
      await ctx.send(file=discord.File('navy_grid/ennemy_grid_view.png'))
      await ctx.send('**Tape !b <case> pour attaquer !**\n_Exemple: !b B5_')
    # le joueur a écrit un paramètre non valide
    else:
      await ctx.send(username+' tu dois écrire **!b start** pour commencer une partie !')

@client.command()
async def me(ctx):
  if(str(ctx.message.author.name) == 'Homer'):
    await ctx.send('tg vicos')
  else:
    await ctx.send(ctx.message.author.name)

@client.command()
async def quote(ctx):
    quote = get_quote()
    await ctx.channel.send(quote)

@client.command()
async def draw(ctx):
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

@client.command()
async def zoom(ctx, arg=None):
  if str(arg).lower() == 'help':
    await ctx.channel.send('Une image zoomée d\'un personnage de League Of Legends est envoyée, les joueurs ont 4 tentatives pour trouver duquel il s\'agit.\nOn peut choisir un niveau de difficulté en ajoutant les mots suivants après !zoom:\n- _easy_\n- _hard_\n- _boss_\nLe niveau de base est medium.\nLes apostrophes et les accents dans les noms ne sont pas comptés mais les espaces sont conservé, **kog\'maw** et **maître yi** doivent être respectivement écrit **kogmaw** et ** maitre yi** pour être validé.\nAttention: **jarvan** s\'écrit **jarvan IV**\nLe gain et la perte de LP fonctionnent de la manière suivante:\n- _easy_ : Gain = '+str(zoom_code.gain_easy)+', Perte = '+str(zoom_code.loss_easy)+'\n- _medium_ : Gain = '+str(zoom_code.gain_medium)+', Perte = '+str(zoom_code.loss_medium)+'\n- _hard_ : Gain = '+str(zoom_code.gain_hard)+', Perte = '+str(zoom_code.loss_hard)+'\n- _boss_ : Gain = '+str(zoom_code.gain_boss)+', Perte = '+str(zoom_code.loss_boss)+'\nLa perte de LP est effective à **chaque** mauvaise réponse.\nIl y a '+str(len(lol))+' images différentes.\n!rank affiche le classement de tous les joueurs.')
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

@client.command()
async def profile(ctx, arg=None):
  if arg == None:
    username = ctx.message.author.name
  else:
    username = str(arg)
  with open('zoom.txt') as json_file:
    data = json.load(json_file)
  if username in data:
    elo = zoom_code.convert_point_into_elo(data[username]['elo'])
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
      win = zoom_code.get_value_promo(username)[0]
      loose = zoom_code.get_value_promo(username)[1]
      embed.add_field(name='BO', value=str(win)+'W - '+str(loose)+'L',inline=False)
    await ctx.channel.send(file=file, embed=embed)  
  else:
    await ctx.channel.send(username+' n\'a pas de profil') 

@client.command()
async def rank(ctx):
  with open('zoom.txt') as json_file:
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
  bo.sort(key=zoom_code.takeSecond)
  t.sort(key=zoom_code.takeSecond,reverse=True)
  res = bo + t
  message = ''
  for i in range(len(res)):
      message += '_'+res[i][0]+'_ : '+zoom_code.convert_point_into_elo(res[i][1])+'\n'
  await ctx.channel.send(message)  

@client.command()
async def command(ctx):
  titre = '-------- Commandes de Sansong --------\n'
  end = '----------------------------------------------'
  draw = '!draw (envoi un lien vers un tableau interactif)' + '\n'
  eq2 = '!eq2 a b c (résout une équation de la forme ax² + bx + c = 0, on peut ajouter l\'argument plot pour afficher la courbe, exemple: !eq2 5 9 -1 plot)' + '\n'
  await ctx.send(titre+'!reaver\n!rap\n!jap\n!minecraft\n!me\n'+eq2+'!kda\n'+'!python\n'+'!quote\n'+draw+'!zoom\n'+'!profile\n'+end)

keep_alive()
client.run(os.getenv('TOKEN'))