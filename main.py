from keep_alive import keep_alive
from discord.ext import commands
import discord
import os
import random
import navy
import zoom_code
import music
import tssg
import other
import science

# préfixe des commandes du bot
prefix = '!'
client = commands.Bot(command_prefix=prefix,help_command=None) # discord.Client()

# nom des classes
cogs = [music,tssg,other,science,zoom_code,navy]
for i in range(len(cogs)):
  cogs[i].setup(client)
    
# photo du bot
new_pdp = False
pfp_path = "bot_image/gibli.png"

# reconnaissance de mots
tension = ["tension", "Tension", "TENSION"]
wakateam = ["wakateam", "Wakateam", "waka team"]
wakateam_response = ["Vazy Wakateam tu vas y arriver !", "baka...", "WAKATEAM !!!!!!!!!!!!!!!!", "1 2 3 WAKATEAM !!!!!"]
words_response = ["tempête !"]

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))
  # pour changer la pdp
  if new_pdp:
    fp = open(pfp_path, 'rb')
    pfp = fp.read()
    await client.user.edit(avatar=pfp)

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

@client.command()
async def help(ctx):
  draw = '`!draw` - Envoi un lien vers un tableau interactif\n'
  music = '`!join`\n`!play` - Prends l\'URL d\'une vidéo Youtube en argument\n`!pause`\n`!resume`\n`!leave`\n\n'
  calculs = '`!eq2 a b c` - Résout une équation de la forme ax² + bx + c = 0, on peut ajouter l\'argument plot pour afficher la courbe\nExemple: `!eq2 5 9 -1 plot`\n`!cano a b c` - Donne la forme canonique d\'un polynôme de la forme ax² + bx + c\n\n'
  tssg = '`!reaver`\n`!kda`\n`!minecraft`\n`!rap`\n`!jap`\n`!drive - Liste des gages en attente`\n\n'
  other = draw+'`!me` - You\n`!you` - Me\n!quote`\n`!cours` - Liste de cours disponibles\nPour plus d\'informations: `!cours help`'
  zoom = '`!zoom` - Une image zoomée d\'un personnage de League Of Legends est envoyée, les joueurs ont 4 tentatives pour trouver duquel il s\'agit.\nPour plus d\'informations: `!zoom help`\n`!profile` - Affichage de son profile\n`!rank` - Ranking de tous les joueurs\n\n'
  navy = '`!b` - Bataille navale en cours de construction\n\n'
  embed = discord.Embed(
          title = 'Commandes',
          # description = elo,
          colour = discord.Colour.blue()
          )
  #embed.set_footer(text='footer')
  file = discord.File('bot_image/gibli.png', filename='image.png')
  embed.set_image(url="attachment://image.png")
  embed.add_field(name='Musique', value=music,inline=False)
  embed.add_field(name='Calculs', value=calculs,inline=False)
  embed.add_field(name='TSSG', value=tssg,inline=False)
  embed.add_field(name='Zoom', value=zoom,inline=False)
  embed.add_field(name='Bataille Navale', value=navy,inline=False)
  embed.add_field(name='Autres', value=other,inline=False)
  await ctx.message.author.send(file=file, embed=embed)

# Pour rendre les LP perdus
# zoom_code.give_lp_back([("Re\u00e4ver",-300)])
keep_alive()
client.run(os.getenv('TOKEN'))