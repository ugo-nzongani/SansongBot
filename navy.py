import numpy as np
import matplotlib.colors as mlc
import matplotlib.pyplot as plt
import random
from discord.ext import commands
import discord

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

def create_dict():
    d = {}
    letters_maj = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    letters_min = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
    for i in range(10):
        for j in range(10):
            d[letters_maj[i]+str(j+1)] = str(i)+str(j)
            d[letters_min[i]+str(j+1)] = str(i)+str(j)
    return d
    
dico = create_dict()

class navy(commands.Cog):
    def __init__(self, client):
        self.client = client

    # bataille navale
    @commands.command()
    async def b(self,ctx, arg=None):
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
          hit, coule = player_attack(all_grid[username][2], all_grid[username][3], dico, str(arg), all_grid[username][5])
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
            if(player_lost(all_grid[username][2], all_grid[username][3])):
              # on supprime toutes les données relatives à la partie
              in_game.remove(username)
              del all_grid[username]
              await ctx.send(username+' a gagné !')
            # test si le bot a gagné
            elif(player_lost(all_grid[username][0], all_grid[username][1])):
              # on supprime toutes les données relatives à la partie
              in_game.remove(username)
              del all_grid[username]
              await ctx.send('J\'ai gagné !')
            # AFFICHAGE DE LA GRILLE DU JOUEUR MISE A JOUR AVEC LATTAQUE DU BOT
            print_grid(all_grid[username][0], 'player_grid', 'Grille de '+username)
            print_grid(all_grid[username][3], 'ennemy_grid_view', 'Grille de Sansong')
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
          player_grid, player_grid_view, ennemy_grid, ennemy_grid_view, player_boat, ennemy_boat = create_grid()
          print(player_boat)
          # mode bateau trouvé
          boat_found = False
          # mode direction trouvé
          direction_found = False
          # ajout du joueur au dictionnaire de jeu
          all_grid[username] = (player_grid, player_grid_view, ennemy_grid, ennemy_grid_view, player_boat, ennemy_boat, boat_found, direction_found)
          # enregistrements des images des grilles dans le dossier navy_grid
          print_grid(all_grid[username][0], 'player_grid', 'Grille de '+username)
          print_grid(all_grid[username][3], 'ennemy_grid_view', 'Grille de Sansong')
          print_grid(all_grid[username][2], 'ennemy_grid', 'Vrai grille de Sansong')
          await ctx.send(file=discord.File('navy_grid/player_grid.png'))
          await ctx.send(file=discord.File('navy_grid/ennemy_grid_view.png'))
          await ctx.send('**Tape !b <case> pour attaquer !**\n_Exemple: !b B5_')
        # le joueur a écrit un paramètre non valide
        else:
          await ctx.send(username+' tu dois écrire **!b start** pour commencer une partie !')
          
def setup(client):
    client.add_cog(navy(client))

def print_grid(data, name, titre):
  letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
  numeros = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

  letters_len = len(letters)
  numeros_len = len(numeros)

  figure, ax = plt.subplots()
  if(is_in(data, 2)):
    if(is_in(data, 1)):
      color_map = mlc.LinearSegmentedColormap.from_list('ColorMap', ["Aqua", "Red","Grey"])
    else:
      color_map = mlc.LinearSegmentedColormap.from_list('ColorMap', ["Aqua", "Grey"])
  else:
    color_map = mlc.LinearSegmentedColormap.from_list('ColorMap', ["Aqua", "Red"])
  ax.imshow(data, cmap=color_map, interpolation='none')

  #ax.set_xlabel('Steps', fontsize=13)
  ax.set_xticks(np.arange(0, numeros_len, 1))
  ax.set_xticks(np.arange(-0.5, numeros_len, 1), minor=True)
  ax.set_xticklabels(np.arange(1, numeros_len + 1, 1),color='w',size=15)

  #ax.set_ylabel('States', fontsize=13)
  ax.set_yticks(np.arange(0, letters_len, 1))
  ax.set_yticks(np.arange(-.5, letters_len, 1), minor=True)
  ax.set_yticklabels(letters,color='w',size=15)

  ax.grid(which='minor', color='w',linewidth=2)
  ax.set_title(titre, fontsize=15, fontweight='bold',color='w')
  figure.set_figheight(6)
  figure.set_figwidth(6)
  figure.savefig(fname='navy_grid/'+name,transparent=True)  

# get_case(data, 'A1')
def get_case(data, d, i):
    index_i = int(d[i][0])
    index_j = int(d[i][1])
    return data[index_i][index_j]

def empty_neighborhood(data, i, j):
    if(i == 0):
        if(j == 0):
            return data[i][j+1] == 0 and data[i+1][j] == 0 and data[i+1][j+1] == 0
        elif(j == 9):
            return data[i][j-1] == 0 and data[i+1][j-1] == 0 and data[i+1][j] == 0
        else:
            return data[i][j-1] == 0 and data[i][j+1] == 0 and data[i+1][j-1] == 0 and data[i+1][j] == 0 and data[i+1][j+1] == 0
    elif(j == 0):
        if(i == 9):
            return data[i-1][j] == 0 and data[i-1][j+1] == 0 and data[i][j+1] == 0
        else:
            return data[i][j+1] == 0 and data[i-1][j] == 0 and data[i-1][j+1] == 0 and data[i+1][j] == 0 and data[i+1][j+1] == 0
    elif(i == 9):
        if(j == 9):
            return data[i][j-1] == 0 and data[i-1][j] == 0 and data[i-1][j-1] == 0
        else:
            return data[i][j-1] == 0 and data[i][j+1] == 0 and data[i-1][j-1] == 0 and data[i-1][j] == 0 and data[i-1][j+1] == 0
    elif(j == 9):
        return data[i][j-1] == 0 and data[i-1][j] == 0 and data[i-1][j-1] == 0 and data[i+1][j] == 0 and data[i+1][j-1] == 0
    else:
        return data[i][j-1] == 0 and data[i][j+1] == 0 and data[i-1][j-1] == 0 and data[i-1][j] == 0 and data[i-1][j+1] == 0 and data[i+1][j-1] == 0 and data[i+1][j] == 0 and data[i+1][j+1] == 0

def place_boat(data, nb_case):
  # done vaut False tant qu'un bateau soit placé sans etre dans le voisinage d'un bateau deja placé
  done = False
  while(not done):
    direction = random.randint(0, 1)
    placed = False
    while(not placed):
      # tableau contenant les coordonnées des cases contenant le bateau placé
      coord = [] 
      i = random.randint(0, 9)
      j = random.randint(0, 9)
      if(data[i][j] == 0 and empty_neighborhood(data, i, j)):
          #data[i][j] = -1
          coord.append((i,j))
          placed = True

    if(direction == 1): # horizontale
        pivot = j
        borne_inf = pivot - 1
        borne_supp = pivot + 1
        if(pivot == 0):
            borne_inf = 1
        elif(pivot == 9):
            borne_supp = 8
        for k in range(nb_case - 1):
          placed = False
          while(not placed):
            r = random.randint(borne_inf, borne_supp)
            if((i,r) not in coord):
              #data[i][r] = -1
              coord.append((i,r))
              if(r > pivot and borne_supp < 9): # on va vers la droite
                borne_supp += 1
              elif(r < pivot and borne_inf > 0): # vers la gauche
                borne_inf -= 1
              placed = True

    else: # verticale
        pivot = i
        borne_inf = pivot - 1
        borne_supp = pivot + 1
        if(pivot == 0):
          borne_inf = 1
        elif(pivot == 9):
          borne_supp = 8
        for k in range(nb_case - 1):
          placed = False
          while(not placed):
            r = random.randint(borne_inf, borne_supp)
            if((r,j) not in coord):
              #data[r][j] = -1
              coord.append((r,j))
              if(r > pivot and borne_supp < 9): # on descend
                borne_supp += 1
              elif(r < pivot and borne_inf > 0): # on monte
                borne_inf -= 1
              placed = True

    cpt = 0
    #print(coord)
    for k in coord:
      #data[k[0]][k[1]] = 0
      if(empty_neighborhood(data, k[0], k[1])):
        cpt += 1
    if(cpt == nb_case):
      for k in coord:
        data[k[0]][k[1]] = 1
      done = True
  return coord
      
def empty_grid():
  grid = [
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0]
  ]
  return grid

def init():
    data = empty_grid()
    boat = place_boat(data, 5)
    boat.append(place_boat(data, 4))
    boat.append(place_boat(data, 3))
    boat.append(place_boat(data, 3))
    boat.append(place_boat(data, 2))
    return data, boat

# fonction permettant au joueur 'humain' d'attaquer (d est le dictionnaire
# et coord une case, exemple: 'A1')
def player_attack(data, data_view, d, coord, boat):
    coule = False
    if(get_case(data_view, d, coord) == 2): # case deja attaquée
      hit = 0
    elif(get_case(data, d, coord) == 0): # raté
      data_view[int(d[coord][0])][int(d[coord][1])] = 2
      hit = 2
    elif(get_case(data, d, coord) == 1): # touché
      data_view[int(d[coord][0])][int(d[coord][1])] = 1
      # suppression de la case attaqué du tableau contenant la position des bateaux
      coule = remove_if_is_in(boat, (int(d[coord][0]), int(d[coord][1])))
      hit = 1
    return hit, coule

# renvoi True si le joueur possédant la grille data a perdu
def player_lost(data, data_view):
    end = True
    for i in range(len(data)):
        for j in range(len(data[i])):
            if(data[i][j] == 1 and data_view[i][j] != 1):
                end = False
    return end

# renvoi les grilles des joueurs et leurs vues
def create_grid():
  player_grid, player_boat = init()
  player_grid_view = empty_grid()
  ennemy_grid, ennemy_boat = init()
  ennemy_grid_view = empty_grid()
  return player_grid, player_grid_view, ennemy_grid, ennemy_grid_view, player_boat, ennemy_boat

# renvoi True si n est dans data
def is_in(data, n):
  for i in range(len(data)):
    for j in range(len(data[i])):
      if(data[i][j] == n):
        return True
  return False

# supprime la case du tableau contenant les positions des bateaux si elle contient un bateau et renvoi True si le bateau est coulé
def remove_if_is_in(boat, case):
    coule = False
    for i in range(len(boat)):
        for j in range(len(boat[i])):
            if(boat[i][j] == case):
                # si après ce coup le bateau est coulé
                if(len(boat[i]) == 1):
                  coule = True
                boat[i].remove(case)
                break
    return coule

'''
Pour gérer les attaques du bot:
- data: grille ennemie (celle du joueur)
- data_view: vue de la grille ennemie
- boat: coordonnées des bateaux de l'ennemi
- boat_found: indique le bot est entrain d'attaquer un bateau
- direction_found: indique si le bot a trouvé la bonne direction
- coord: coordonnées de la case attaquée
'''
'''
def bot_attack(data, data_view, boat, boat_found, direction_found, coord):
  # si le bot est entrain d'attaquer un bateau
  if(boat_found):
    # si la direction est trouvée
    if(direction_found):

    # la direction n'est pas trouvée
    else:
      # calcul des voisins disponibles
      neighbors = get_neighborhood(data, i, j)
      # tirage au sort d'une case voisine a attaquer
      index = random.randint(0, len(neighbors)-1)

  # s'il n'est pas entrain d'attaquer, il choisit une case au hasard
  else:
    # done vaut True quand le bot a attaqué une case valide
    done = False
    while(not done):
      # tir au hasard les coordonnées d'une case à attaquer
      i = random.randint(0, 9)
      j = random.randint(0, 9)
      # case vide
      if(data[i][j] == 0):
        done = True
        # MAJ de la vue
        data_view[i][j] = 2
        # pour indiquer que la case a été attaquée
        data[i][j] = 2
      # case contient un bateau
      elif(data[i][j] == 1):
        done = True
        # MAJ de la vue
        data_view[i][j] = 1
        # pour indiquer que la case a été attaquée
        data[i][j] = 2
        boat_found = True
        # enregistre les coordonnées de la case
        coord = (i,j)
      # si la case a deja été attaquée on boucle
'''
# renvoi les cases voisines horizontales et verticales de data[i][j]     
def get_neighborhood(data, i, j):
    if(i == 0):
        if(j == 0):
            return (data[i][j+1], data[i+1][j], data[i+1][j+1])
        elif(j == 9):
            return (data[i][j-1], data[i+1][j-1], data[i+1][j])
        else:
            return (data[i][j-1], data[i][j+1], data[i+1][j-1], data[i+1][j], data[i+1][j+1])
    elif(j == 0):
        if(i == 9):
            return (data[i-1][j], data[i-1][j+1], data[i][j+1])
        else:
            return (data[i][j+1], data[i-1][j], data[i-1][j+1], data[i+1][j], data[i+1][j+1])
    elif(i == 9):
        if(j == 9):
            return (data[i][j-1], data[i-1][j], data[i-1][j-1])
        else:
            return (data[i][j-1], data[i][j+1], data[i-1][j-1], data[i-1][j], data[i-1][j+1])
    elif(j == 9):
        return (data[i][j-1], data[i-1][j], data[i-1][j-1], data[i+1][j], data[i+1][j-1])
    else:
        return (data[i][j-1], data[i][j+1], data[i-1][j-1], data[i-1][j], data[i-1][j+1], data[i+1][j-1], data[i+1][j], data[i+1][j+1])