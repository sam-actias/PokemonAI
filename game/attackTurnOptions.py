from enums import CardType
from pokemonTcg import printPokemon

def energyMixPickPokemon(game, player, energyCardNames, energyCardIndexes, energyCardIndex):
  fusionStrikePokemon = []

  if game.players[player].activePokemon.fusionStrike:
    fusionStrikePokemon.append({ 'pokemonName': game.players[player].activePokemon.name, 
                                'pokemonLocation': 'activePokemon', 'pokemonIndex': None })

  for index, pokemon in enumerate(game.players[player].bench):
    if pokemon.fusionStrike:
      fusionStrikePokemon.append({ 'pokemonName': pokemon.name, 'pokemonLocation': 'bench', 'pokemonIndex': index })

  print(f'\nPick a Pokemon to attach {energyCardNames[int(text[1])]} to.')

  for index, pokemon in enumerate(fusionStrikePokemon):
    print(f'{index}   {pokemon['pokemonName']}')

  print('\nCommands:')
  print('details {x}: card details')
  print('choose {x}: choose a Pokemon\n')

  text = input()

  text = text.split()

  if text[0] == 'details' and int(text[1]) < len(fusionStrikePokemon):
    printPokemon(fusionStrikePokemon[int(text[1])])
    return energyMixPickPokemon(game, player, energyCardNames, energyCardIndexes, energyCardIndex)
  if text[0] ==  'choose' and int(text[1]) < len(fusionStrikePokemon):
    return game.players[player].activePokemon.moves['energyMix']['do'](game, player, energyCardIndexes[energyCardIndex], 
                fusionStrikePokemon[int(text[1])]['pokemonLocation'], fusionStrikePokemon[int(text[1])]['pokemonIndex'])
  else:
    print('what?')
    return energyMixPickPokemon(game, player, energyCardNames, energyCardIndexes, energyCardIndex)

def crossFusionStrikeEnergyMixPickPokemon(game, player, opponent, energyCardNames, 
      benchedFusionStrikeMoves, benchedFusionStrikeIndexes, moveIndex, energyCardIndexes, energyCardIndex):
  fusionStrikePokemon = []

  if game.players[player].activePokemon.fusionStrike:
    fusionStrikePokemon.append({ 'pokemonName': game.players[player].activePokemon.name, 
                                'pokemonLocation': 'activePokemon', 'pokemonIndex': None })

  for index, pokemon in enumerate(game.players[player].bench):
    if pokemon.fusionStrike:
      fusionStrikePokemon.append({ 'pokemonName': pokemon.name, 'pokemonLocation': 'bench', 'pokemonIndex': index })

  print(f'\nPick a Pokemon to attach {energyCardNames[int(text[1])]} to.')

  for index, pokemon in enumerate(fusionStrikePokemon):
    print(f'{index}   {pokemon['pokemonName']}')

  print('\nCommands:')
  print('details {x}: card details')
  print('choose {x}: choose a Pokemon\n')

  text = input()

  text = text.split()

  if text[0] == 'details' and int(text[1]) < len(fusionStrikePokemon):
    printPokemon(fusionStrikePokemon[int(text[1])])
    return crossFusionStrikeEnergyMixPickPokemon(game, player, opponent, energyCardNames, 
      benchedFusionStrikeMoves, benchedFusionStrikeIndexes, moveIndex, energyCardIndexes, energyCardIndex)
  if text[0] ==  'choose' and int(text[1]) < len(fusionStrikePokemon):
    return game.players[player].activePokemon.moves['crossFusionStrike']['do'](game, player, 
      benchedFusionStrikeIndexes[moveIndex], benchedFusionStrikeMoves[moveIndex].name, { 'game': game, 'player': player, 
      'deckIndex': energyCardIndexes[energyCardIndex], 'pokemonLocation': fusionStrikePokemon[int(text[1])]['pokemonLocation'], 
      'pokemonIndex': fusionStrikePokemon[int(text[1])]['pokemonIndex'] })
  else:
    print('what?')
    return crossFusionStrikeEnergyMixPickPokemon(game, player, opponent, energyCardNames, 
          benchedFusionStrikeMoves, benchedFusionStrikeIndexes, moveIndex, energyCardIndexes, energyCardIndex)

def crossFusionStrikePsychicLeapShuffleIn(game, player, opponent, benchedFusionStrikeMoves, benchedFusionStrikeIndexes, moveIndex):
  shuffleIn = True

  if len(game.players[player].bench) == 1:
    newActivePokemonIndex = 0
  else:
    print('\nWhat bench Pokemon do you want to replace Mew VMAX as your active Pokemon?')

    for index, pokemon in enumerate(game.players[player].bench):
      print(f'{index}   {pokemon.name}')

    print('\nCommands:')
    print('details {x}: card details')
    print('choose {x}: choose a Pokemon\n')

    text = input()
  
    text = text.split()

    if text[0] == 'details' and int(text[1]) < len(game.players[player].bench):
      printPokemon(game.players[player].bench[int(text[1])])
      return crossFusionStrikePsychicLeapShuffleIn(game, player, opponent)
    elif text[0] == 'choose' and int(text[1]) < len(game.players[player].bench):
      return game.players[player].activePokemon.moves['crossFusionStrike']['do'](game, player, 
          benchedFusionStrikeIndexes[moveIndex], benchedFusionStrikeMoves[moveIndex].name, { 'game': game, 
          'player': player, 'opponent': opponent, 'shuffleIn': True, 'newActivePokemonIndex': int(text[1]) })
    else:
      print('What?\n')
      return crossFusionStrikePsychicLeapShuffleIn(game, player, opponent)

def crossFusionStrikeMoveChoices(game, player, opponent, benchedFusionStrikeMoves, benchedFusionStrikeIndexes, moveIndex):
  if (benchedFusionStrikeMoves[moveIndex].name == 'maxMiracle' or benchedFusionStrikeMoves[moveIndex].name == 'technoBlast' or 
       benchedFusionStrikeMoves[moveIndex].name == 'melodiousEcho'):
    return game.players[player].activePokemon.moves['crossFusionStrike']['do'](game, player, 
          benchedFusionStrikeIndexes[moveIndex], benchedFusionStrikeMoves[moveIndex].name, 
          { 'game': game, 'player': player, 'opponent': opponent })
  elif benchedFusionStrikeMoves[moveIndex].name == 'energyMix':
    energyCardNames = []
    energyCardIndexes = []

    for index, card in enumerate(game.players[player].deck):
      if card.cardType == CardType.Energy and card.name not in energyCardNames:
        energyCardNames.append(card.name)
        energyCardIndexes.append(index)

    energyCardNamesAmt = len(energyCardNames)

    if energyCardNamesAmt == 0:
      print('There are no energy cards in your deck. Energy Mix ends.')

      game.players[player].deck = game.shuffle(game.players[player].deck)

      return game

    print('\nPick an energy card you want to attach to one of your Fusion Strike Pokemon.')

    for i in range(energyCardNamesAmt):
      print(f'{i}   {energyCardNames[i]}')

    print('\nCommands:')
    print('details {x}: card details')
    print('choose {x}: choose an energy card\n')

    text = input()

    text = text.split()

    energyCardIndex = int(text[1])

    if text[0] == 'details':
      # TODO: add display energy card details
      print('nothing here yet')
    elif text[0] == 'choose':
      return crossFusionStrikeEnergyMixPickPokemon(game, player, opponent, energyCardNames, 
                benchedFusionStrikeMoves, benchedFusionStrikeIndexes, moveIndex, energyCardIndexes, energyCardIndex)
    else:
      print('what?')
      return crossFusionStrikeMoveChoices(game, player, opponent, benchedFusionStrikeMoves, benchedFusionStrikeIndexes, moveIndex)

  elif benchedFusionStrikeMoves[moveIndex].name == 'psychicLeap':
    if len(game.players[player].bench) == 0:
      return game.players[player].activePokemon.moves['crossFusionStrike']['do'](game, player, 
          benchedFusionStrikeIndexes[moveIndex], benchedFusionStrikeMoves[moveIndex].name, { 'game': game, 
          'player': player, 'opponent': opponent, 'shuffleIn': False })

    print('\nDo you want to shuffle Mew VMAX and all attached cards into your deck as part of the Psychic Leap?')
    print('\nCommands:')
    print('yes: shuffle Mew VMAX and all attached cards into your deck')
    print('no: don\'t shuffle Mew VMAX and all attached cards into your deck\n')

    text = input()

    if text =='yes':
      crossFusionStrikePsychicLeapShuffleIn(game, player, opponent)
    elif text != 'no':
      print('what?')
      return crossFusionStrikeMoveChoices(game, player, opponent, benchedFusionStrikeMoves, benchedFusionStrikeIndexes, moveIndex)

    return game.players[player].activePokemon.moves['crossFusionStrike']['do'](game, player, 
          benchedFusionStrikeIndexes[moveIndex], benchedFusionStrikeMoves[moveIndex].name, { 'game': game, 
          'player': player, 'opponent': opponent, 'shuffleIn': False })
    
  elif benchedFusionStrikeMoves[moveIndex].name == 'glisteningDroplets':
    if len(game.players[opponent].bench) == 0:
      return game.players[player].activePokemon.moves['crossFusionStrike']['do'](game, player, 
          benchedFusionStrikeIndexes[moveIndex], benchedFusionStrikeMoves[moveIndex].name, 
          { 'game': game, 'player': player, 'opponent': opponent, 'howToPutDamageCounters': { 'pokemonLocation': 'activePokemon', 
              'pokemonIndex': None, 'damageAmt': 50} })
    
    howToPutDamageCounters = []

    print('\nOn which Pokemon do you want to put the first damage counter (10 HP)?')

    print(f'0   {game.players[opponent].activePokemon.name} (Active Pokemon)')

    for index, pokemon in enumerate(game.players[opponent].bench):
      print(f'{index + 1}   {game.players[opponent].bench[index].name} (On Bench)')

    print('\nCommands:')
    print('details {x}: card details')
    print('choose {x}: choose a Pokemon\n')

    text = input()

    text = text.split()

    if text[0] == 'details' and int(text[1]) <= len(game.players[opponent].bench):
      if int(text[1]) == 0:
        printPokemon(game.players[opponent].activePokemon)
      else:
        printPokemon(game.players[opponent].bench[int(text[1]) - 1])

      return crossFusionStrikeMoveChoices(game, player, opponent, benchedFusionStrikeMoves, benchedFusionStrikeIndexes, moveIndex)
    if text[0] == 'choose' and int(text[1]) <= len(game.players[opponent].bench):
      if int(text[1]) == 0:
        howToPutDamageCounters.append({ 'pokemonLocation': 'activePokemon', 'pokemonIndex': None })
      else:
        howToPutDamageCounters.append({ 'pokemonLocation': 'bench', 'pokemonIndex': int(text[1]) - 1 })
    else:
      print('what?')
      return crossFusionStrikeMoveChoices(game, player, opponent, benchedFusionStrikeMoves, benchedFusionStrikeIndexes, moveIndex)
    
    print('\nOn which Pokemon do you want to put the second damage counter (10 HP)?')

    print(f'0   {game.players[opponent].activePokemon.name} (Active Pokemon)')

    for index, pokemon in enumerate(game.players[opponent].bench):
      print(f'{index + 1}   {game.players[opponent].bench[index].name} (On Bench)')

    print('\nCommands:')
    print('details {x}: card details')
    print('choose {x}: choose a Pokemon\n')

    text = input()

    text = text.split()

    if text[0] == 'details' and int(text[1]) <= len(game.players[opponent].bench):
      if int(text[1]) == 0:
        printPokemon(game.players[opponent].activePokemon)
      else:
        printPokemon(game.players[opponent].bench[int(text[1]) - 1])

      return crossFusionStrikeMoveChoices(game, player, opponent, benchedFusionStrikeMoves, benchedFusionStrikeIndexes, moveIndex)
    if text[0] == 'choose' and int(text[1]) <= len(game.players[opponent].bench):
      if int(text[1]) == 0:
        howToPutDamageCounters.append({ 'pokemonLocation': 'activePokemon', 'pokemonIndex': None })
      else:
        howToPutDamageCounters.append({ 'pokemonLocation': 'bench', 'pokemonIndex': int(text[1]) - 1 })
    else:
      print('what?')
      return crossFusionStrikeMoveChoices(game, player, opponent, benchedFusionStrikeMoves, benchedFusionStrikeIndexes, moveIndex)
    
    print('\nOn which Pokemon do you want to put the third damage counter (10 HP)?')

    print(f'0   {game.players[opponent].activePokemon.name} (Active Pokemon)')

    for index, pokemon in enumerate(game.players[opponent].bench):
      print(f'{index + 1}   {game.players[opponent].bench[index].name} (On Bench)')

    print('\nCommands:')
    print('details {x}: card details')
    print('choose {x}: choose a Pokemon\n')

    text = input()

    text = text.split()

    if text[0] == 'details' and int(text[1]) <= len(game.players[opponent].bench):
      if int(text[1]) == 0:
        printPokemon(game.players[opponent].activePokemon)
      else:
        printPokemon(game.players[opponent].bench[int(text[1]) - 1])

      return crossFusionStrikeMoveChoices(game, player, opponent, benchedFusionStrikeMoves, benchedFusionStrikeIndexes, moveIndex)
    if text[0] == 'choose' and int(text[1]) <= len(game.players[opponent].bench):
      if int(text[1]) == 0:
        howToPutDamageCounters.append({ 'pokemonLocation': 'activePokemon', 'pokemonIndex': None })
      else:
        howToPutDamageCounters.append({ 'pokemonLocation': 'bench', 'pokemonIndex': int(text[1]) - 1 })
    else:
      print('what?')
      return crossFusionStrikeMoveChoices(game, player, opponent, benchedFusionStrikeMoves, benchedFusionStrikeIndexes, moveIndex)
    
    print('\nOn which Pokemon do you want to put the fourth damage counter (10 HP)?')

    print(f'0   {game.players[opponent].activePokemon.name} (Active Pokemon)')

    for index, pokemon in enumerate(game.players[opponent].bench):
      print(f'{index + 1}   {game.players[opponent].bench[index].name} (On Bench)')

    print('\nCommands:')
    print('details {x}: card details')
    print('choose {x}: choose a Pokemon\n')

    text = input()

    text = text.split()

    if text[0] == 'details' and int(text[1]) <= len(game.players[opponent].bench):
      if int(text[1]) == 0:
        printPokemon(game.players[opponent].activePokemon)
      else:
        printPokemon(game.players[opponent].bench[int(text[1]) - 1])

      return crossFusionStrikeMoveChoices(game, player, opponent, benchedFusionStrikeMoves, benchedFusionStrikeIndexes, moveIndex)
    if text[0] == 'choose' and int(text[1]) <= len(game.players[opponent].bench):
      if int(text[1]) == 0:
        howToPutDamageCounters.append({ 'pokemonLocation': 'activePokemon', 'pokemonIndex': None })
      else:
        howToPutDamageCounters.append({ 'pokemonLocation': 'bench', 'pokemonIndex': int(text[1]) - 1 })
    else:
      print('what?')
      return crossFusionStrikeMoveChoices(game, player, opponent, benchedFusionStrikeMoves, benchedFusionStrikeIndexes, moveIndex)
    
    print('\nOn which Pokemon do you want to put the fifth damage counter (10 HP)?')

    print(f'0   {game.players[opponent].activePokemon.name} (Active Pokemon)')

    for index, pokemon in enumerate(game.players[opponent].bench):
      print(f'{index + 1}   {game.players[opponent].bench[index].name} (On Bench)')

    print('\nCommands:')
    print('details {x}: card details')
    print('choose {x}: choose a Pokemon\n')

    text = input()

    text = text.split()

    if text[0] == 'details' and int(text[1]) <= len(game.players[opponent].bench):
      if int(text[1]) == 0:
        printPokemon(game.players[opponent].activePokemon)
      else:
        printPokemon(game.players[opponent].bench[int(text[1]) - 1])

      return crossFusionStrikeMoveChoices(game, player, opponent, benchedFusionStrikeMoves, benchedFusionStrikeIndexes, moveIndex)
    if text[0] == 'choose' and int(text[1]) <= len(game.players[opponent].bench):
      if int(text[1]) == 0:
        howToPutDamageCounters.append({ 'pokemonLocation': 'activePokemon', 'pokemonIndex': None })
      else:
        howToPutDamageCounters.append({ 'pokemonLocation': 'bench', 'pokemonIndex': int(text[1]) - 1 })
    else:
      print('what?')
      return crossFusionStrikeMoveChoices(game, player, opponent, benchedFusionStrikeMoves, benchedFusionStrikeIndexes, moveIndex)
      
    return game.players[player].activePokemon.moves['crossFusionStrike']['do'](game, player, 
                benchedFusionStrikeIndexes[moveIndex], benchedFusionStrikeMoves[moveIndex].name, { 'game': game,
                'player': player, 'opponent': opponent, 'howToPutDamageCounters': howToPutDamageCounters })

def crossFusionStrike(game, player, opponent):
  benchedFusionStrikeIndexes = []
  benchedFusionStrikeMoves = []

  for index, pokemon in enumerate(game.players[player].bench):
    if pokemon.fusionStrike == True:
      for move in list(pokemon.moves.keys()):
        if pokemon.moves[move]['canDo'] == True:
          benchedFusionStrikeIndexes.append(index)
          benchedFusionStrikeMoves.append(pokemon.moves[move])

  print('Which move from a Fusion Strike Pokemon on your bench do you want to use?')

  for index, move in enumerate(benchedFusionStrikeMoves):
    print(f'{index}   {move.name}')

  print('\nCommands:')
  print('choose {x}: choose a move to do\n')

  text = input()

  text = text.split()

  if text[0] == 'choose':
    moveIndex = int(text[1])

    return crossFusionStrikeMoveChoices(game, player, opponent, benchedFusionStrikeMoves, benchedFusionStrikeIndexes, moveIndex)
  else:
    print('what?')
    return crossFusionStrike(game, player)

def maxMiracle(game, player, opponent):
  return game.players[player].activePokemon.moves['maxMiracle']['do'](game, player, opponent)

def energyMix(game, player):
  energyCardNames = []
  energyCardIndexes = []

  for index, card in enumerate(game.players[player].deck):
    if card.cardType == CardType.Energy and card.name not in energyCardNames:
      energyCardNames.append(card.name)
      energyCardIndexes.append(index)

  energyCardNamesAmt = len(energyCardNames)

  if energyCardNamesAmt == 0:
    print('There are no energy cards in your deck. Energy Mix ends.')

    game.players[player].deck = game.shuffle(game.players[player].deck)

    return game

  print('\nPick an energy card you want to attach to one of your Fusion Strike Pokemon.')

  for i in range(energyCardNamesAmt):
    print(f'{i}   {energyCardNames[i]}')

  print('\nCommands:')
  print('details {x}: card details')
  print('choose {x}: choose an energy card\n')

  text = input()

  text = text.split()

  energyCardIndex = int(text[1])

  if text[0] == 'details':
    # TODO: add display energy card details
    print('nothing here yet')
  elif text[0] == 'choose':
    return energyMixPickPokemon(game, player, energyCardNames, energyCardIndexes, energyCardIndex)
  else:
    print('what?')
    return energyMix(game, player)

def psychicLeapShuffleIn(game, player, opponent):
  shuffleIn = True

  if len(game.players[player].bench) == 1:
    newActivePokemonIndex = 0
  else:
    print('\nWhat bench Pokemon do you want to replace Mew VMAX as your active Pokemon?')

    for index, pokemon in enumerate(game.players[player].bench):
      print(f'{index}   {pokemon.name}')

    print('\nCommands:')
    print('details {x}: card details')
    print('choose {x}: choose a Pokemon\n')

    text = input()
  
    text = text.split()

    if text[0] == 'details' and int(text[1]) < len(game.players[player].bench):
      printPokemon(game.players[player].bench[int(text[1])])
      return crossFusionStrikePsychicLeapShuffleIn(game, player, opponent)
    elif text[0] == 'choose' and int(text[1]) < len(game.players[player].bench):
      return game.players[player].activePokemon.moves['psychicLeap']['do'](game, player, opponent,
                      True, int(text[1]))
    else:
      print('What?\n')
      return psychicLeapShuffleIn(game, player, opponent)


def psychicLeap(game, player, opponent):
  if len(game.players[player].bench) == 0:
      return game.players[player].activePokemon.moves['psychicLeap']['do'](game, player, opponent, False)

  print('\nDo you want to shuffle Mew VMAX and all attached cards into your deck as part of the Psychic Leap?')
  print('\nCommands:')
  print('yes: shuffle Mew V and all attached cards into your deck')
  print('no: don\'t shuffle Mew V and all attached cards into your deck\n')

  text = input()

  if text =='yes':
    psychicLeapShuffleIn(game, player, opponent)
  elif text != 'no':
    print('what?')
    return psychicLeap(game, player, opponent)

  return game.players[player].activePokemon.moves['psychicLeap']['do'](game, player, opponent, False)

def technoBlast(game, player, opponent):
  return game.players[player].activePokemon.moves['technoBlast']['do'](game, player, opponent)

def melodiousEcho(game, player, opponent):
  return game.players[player].activePokemon.moves['melodiousEcho']['do'](game, player, opponent)

def glisteningDroplets(game, player, opponent):
  # TODO make so if check Pokemon doesn't reset the whole process of this move

  if len(game.players[opponent].bench) == 0:
      return game.players[player].activePokemon.moves['glisteningDroplets']['do'](game, player, opponent, 
                  [{ 'pokemonLocation': 'activePokemon', 'pokemonIndex': None}, { 'pokemonLocation': 'activePokemon', 'pokemonIndex': None}, 
                   { 'pokemonLocation': 'activePokemon', 'pokemonIndex': None}, { 'pokemonLocation': 'activePokemon', 'pokemonIndex': None}, 
                   { 'pokemonLocation': 'activePokemon', 'pokemonIndex': None}])
    
  howToPutDamageCounters = []

  print('\nOn which Pokemon do you want to put the first damage counter (10 HP)?')

  print(f'0   {game.players[opponent].activePokemon.name} (Active Pokemon)')

  for index, pokemon in enumerate(game.players[opponent].bench):
    print(f'{index + 1}   {game.players[opponent].bench[index].name} (On Bench)')

  print('\nCommands:')
  print('details {x}: card details')
  print('choose {x}: choose a Pokemon\n')

  text = input()

  text = text.split()

  if text[0] == 'details' and int(text[1]) <= len(game.players[opponent].bench):
    if int(text[1]) == 0:
      printPokemon(game.players[opponent].activePokemon)
    else:
      printPokemon(game.players[opponent].bench[int(text[1]) - 1])

    return glisteningDroplets(game, player, opponent)
  if text[0] == 'choose' and int(text[1]) <= len(game.players[opponent].bench):
    if int(text[1]) == 0:
      howToPutDamageCounters.append({ 'pokemonLocation': 'activePokemon', 'pokemonIndex': None })
    else:
      howToPutDamageCounters.append({ 'pokemonLocation': 'bench', 'pokemonIndex': int(text[1]) - 1 })
  else:
    print('what?')
    return glisteningDroplets(game, player, opponent)
  
  print('\nOn which Pokemon do you want to put the second damage counter (10 HP)?')

  print(f'0   {game.players[opponent].activePokemon.name} (Active Pokemon)')

  for index, pokemon in enumerate(game.players[opponent].bench):
    print(f'{index + 1}   {game.players[opponent].bench[index].name} (On Bench)')

  print('\nCommands:')
  print('details {x}: card details')
  print('choose {x}: choose a Pokemon\n')

  text = input()

  text = text.split()

  if text[0] == 'details' and int(text[1]) <= len(game.players[opponent].bench):
    if int(text[1]) == 0:
      printPokemon(game.players[opponent].activePokemon)
    else:
      printPokemon(game.players[opponent].bench[int(text[1]) - 1])

    return glisteningDroplets(game, player, opponent)
  if text[0] == 'choose' and int(text[1]) <= len(game.players[opponent].bench):
    if int(text[1]) == 0:
      howToPutDamageCounters.append({ 'pokemonLocation': 'activePokemon', 'pokemonIndex': None })
    else:
      howToPutDamageCounters.append({ 'pokemonLocation': 'bench', 'pokemonIndex': int(text[1]) - 1 })
  else:
    print('what?')
    return glisteningDroplets(game, player, opponent)
  
  print('\nOn which Pokemon do you want to put the third damage counter (10 HP)?')

  print(f'0   {game.players[opponent].activePokemon.name} (Active Pokemon)')

  for index, pokemon in enumerate(game.players[opponent].bench):
    print(f'{index + 1}   {game.players[opponent].bench[index].name} (On Bench)')

  print('\nCommands:')
  print('details {x}: card details')
  print('choose {x}: choose a Pokemon\n')

  text = input()

  text = text.split()

  if text[0] == 'details' and int(text[1]) <= len(game.players[opponent].bench):
    if int(text[1]) == 0:
      printPokemon(game.players[opponent].activePokemon)
    else:
      printPokemon(game.players[opponent].bench[int(text[1]) - 1])

    return glisteningDroplets(game, player, opponent)
  if text[0] == 'choose' and int(text[1]) <= len(game.players[opponent].bench):
    if int(text[1]) == 0:
      howToPutDamageCounters.append({ 'pokemonLocation': 'activePokemon', 'pokemonIndex': None })
    else:
      howToPutDamageCounters.append({ 'pokemonLocation': 'bench', 'pokemonIndex': int(text[1]) - 1 })
  else:
    print('what?')
    return glisteningDroplets(game, player, opponent)
  
  print('\nOn which Pokemon do you want to put the fourth damage counter (10 HP)?')

  print(f'0   {game.players[opponent].activePokemon.name} (Active Pokemon)')

  for index, pokemon in enumerate(game.players[opponent].bench):
    print(f'{index + 1}   {game.players[opponent].bench[index].name} (On Bench)')

  print('\nCommands:')
  print('details {x}: card details')
  print('choose {x}: choose a Pokemon\n')

  text = input()

  text = text.split()

  if text[0] == 'details' and int(text[1]) <= len(game.players[opponent].bench):
    if int(text[1]) == 0:
      printPokemon(game.players[opponent].activePokemon)
    else:
      printPokemon(game.players[opponent].bench[int(text[1]) - 1])

    return glisteningDroplets(game, player, opponent)
  if text[0] == 'choose' and int(text[1]) <= len(game.players[opponent].bench):
    if int(text[1]) == 0:
      howToPutDamageCounters.append({ 'pokemonLocation': 'activePokemon', 'pokemonIndex': None })
    else:
      howToPutDamageCounters.append({ 'pokemonLocation': 'bench', 'pokemonIndex': int(text[1]) - 1 })
  else:
    print('what?')
    return glisteningDroplets(game, player, opponent)
  
  print('\nOn which Pokemon do you want to put the fifth damage counter (10 HP)?')

  print(f'0   {game.players[opponent].activePokemon.name} (Active Pokemon)')

  for index, pokemon in enumerate(game.players[opponent].bench):
    print(f'{index + 1}   {game.players[opponent].bench[index].name} (On Bench)')

  print('\nCommands:')
  print('details {x}: card details')
  print('choose {x}: choose a Pokemon\n')

  text = input()

  text = text.split()

  if text[0] == 'details' and int(text[1]) <= len(game.players[opponent].bench):
    if int(text[1]) == 0:
      printPokemon(game.players[opponent].activePokemon)
    else:
      printPokemon(game.players[opponent].bench[int(text[1]) - 1])

    return glisteningDroplets(game, player, opponent)
  if text[0] == 'choose' and int(text[1]) <= len(game.players[opponent].bench):
    if int(text[1]) == 0:
      howToPutDamageCounters.append({ 'pokemonLocation': 'activePokemon', 'pokemonIndex': None })
    else:
      howToPutDamageCounters.append({ 'pokemonLocation': 'bench', 'pokemonIndex': int(text[1]) - 1 })
  else:
    print('what?')
    return glisteningDroplets(game, player, opponent)
    
  return game.players[player].activePokemon.moves['glisteningDroplets']['do'](game, player, opponent, howToPutDamageCounters)

attackTurnOptions = {
  'crossFusionStrike': crossFusionStrike,
  'maxMiracle': maxMiracle,
  'energyMix': energyMix,
  'psychicLeap': psychicLeap,
  'technoBlast': technoBlast,
  'melodiousEcho': melodiousEcho,
  'glisteningDroplets': glisteningDroplets
}