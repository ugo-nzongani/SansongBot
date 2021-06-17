import json

# gain et perte de LP par difficulté
gain_easy = 5
gain_medium = 10
gain_hard = 15
gain_boss = 22

loss_easy = 8
loss_medium = 4
loss_hard = 3
loss_boss = 2

def create_json():
  data = {}
  with open('zoom.txt', 'w') as outfile:
    json.dump(data, outfile)

def add_new_player(name):
  with open('zoom.txt') as json_file:
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
      with open('zoom.txt', 'w') as outfile:
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
  with open('zoom.txt') as json_file:
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
    with open('zoom.txt', 'w') as outfile:
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
  elif point + gain >= 2000 and point > 2000 and point < 2400:
    data[name]['bo5'][0] = True
    data[name]['elo'] = -5
    data[name]['bo5'][3] = 'not started'
    on_promo = True
  elif point + gain >= 2400 and point > 2400 and point < 2800:
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
  with open('zoom.txt') as json_file:
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