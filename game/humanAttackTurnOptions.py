from enums import CardType, EnergyType, Stage
from pokemonTcg import printPokemon, printEnergyCard
from cards import FusionStrikeEnergyFS244, DoubleTurboEnergyBS151

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
      if energyCardNames[energyCardIndex] == 'Fusion Strike Energy':
        printEnergyCard(FusionStrikeEnergyFS244())
      elif energyCardNames[energyCardIndex] == 'Double Turbo Energy':
        printEnergyCard(DoubleTurboEnergyBS151())
      else:
        print('what?')
        return crossFusionStrikeMoveChoices(game, player, opponent, benchedFusionStrikeMoves, benchedFusionStrikeIndexes, moveIndex)
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

def energyMix(game, player, opponent):
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

def retreatChoose(game, player):
  print('Pick an energy card to discard.\n')
      
  count = 0
  energy = []

  if game.players[player].activePokemon.attachedEnergy[EnergyType.FusionStrikeEnergy] > 0:
    for i in range(game.players[player].activePokemon.attachedEnergy[EnergyType.FusionStrikeEnergy]):
      print(f'{count}   Fusion Strike Energy')
      energy.append(EnergyType.FusionStrikeEnergy)
      count += 1

  if game.players[player].activePokemon.attachedEnergy[EnergyType.DoubleTurboEnergy] > 0:
    for i in range(game.players[player].activePokemon.attachedEnergy[EnergyType.DoubleTurboEnergy]):
      print(f'{count}   Double Turbo Energy')
      energy.append(EnergyType.DoubleTurboEnergy)
      count += 1

  if game.players[player].activePokemon.attachedEnergy[EnergyType.Water] > 0:
    for i in range(game.players[player].activePokemon.attachedEnergy[EnergyType.Water]):
      print(f'{count}   Water Energy')
      energy.append(EnergyType.Water)
      count += 1

  print('\nCommands:')
  print('details {x}: get card details')
  print('choose {x}: choose an energy card')

  text = input()

  text = text.split()

  if text[0] == 'choose':
    return energy[int(text[1])]
  elif text[0] == 'details':
    printEnergyCard(energy[int(text[1])])
    return retreatChoose(game, player)
  else:
    print('what?')
    return retreatChoose(game, player)

def retreatPickABenchedPokemon(game, player):
  print('\nPick a benched Pokemon to replace your active Pokemon.')

  for index, pokemon in enumerate(game.players[player].bench):
    print(f'{index}   {pokemon.name}')

  print('\nCommands:')
  print('details {x}: get details about a Pokemon')
  print('choose {x}: choose a Pokemon')

  text = input()

  text = text.split()

  if text[0] == 'details':
    printPokemon(game.players[player].bench[int(text[1])])
    retreatPickABenchedPokemon(game, player)
  elif text[0] == 'choose':
    return int(text[1])
  else:
    print('what?')
    retreatPickABenchedPokemon(game, player)

def retreat(game, player, opponent):
  if game.players[player].activePokemon.retreatCost > 0:
    print(f'\nYou need to discard {game.players[player].activePokemon.retreatCost} energy card(s) 
          from {game.players[player].activePokemon.name} in order to retreat.')
    
    energyToDiscard = []

    for i in range(game.players[player].activePokemon.retreatCost):
      energyToDiscard.append(retreatChoose(game, player))

    newPokemonIndex = retreatPickABenchedPokemon(game, player)

    return game.retreat(player, newPokemonIndex, energyToDiscard)

def playBasicPokemonToBench(game, player, opponent):
  if len(game.players[player].bench) < 5: 
    print('\nWhich Basic Pokemon in your hand do you want to play onto your Bench?')

    basicPokemon = []
    basicPokemonIndexes = []

    for index, card in enumerate(game.players[player].hand):
      if card.cardType == CardType.Pokemon and card.stage == Stage.Basic:
        basicPokemon.add(card)
        basicPokemonIndexes.add(index)

    for index, pokemon in enumerate(basicPokemon):
      print(f'{index}   {pokemon.name}')

    print('\nCommands:')
    print('details {x}: get card details')
    print('choose {x}: choose a Pokemon')

    text = input()

    text = text.split()

    if text[0] == 'details' and int(text[1]) < len(basicPokemon):
      printPokemon(basicPokemon[int(text[1])])
      return playBasicPokemonToBench(game, player, opponent)
    elif text[0] == 'choose' and int(text[1]) < len(basicPokemon):
      game.players[player].bench.append(basicPokemon[int(text[1])])
      game.players[player].hand.pop(basicPokemonIndexes[int(text[1])])

      return game
    else:
      print('what?')
      return playBasicPokemonToBench(game, player, opponent)

  raise Exception('bench is already full')

def choosePokemonToEvolveFrom(game, player, canEvolveFrom, evolutionPokemonHandIndex):
  print('\nPick a Pokemon to evolve with your chosen evolution Pokemon.')

  for index, pokemonThatCanEvolve in enumerate(canEvolveFrom):
    if pokemonThatCanEvolve['pokemonLocation'] == 'activePokemon':
      print(f'{index}   {pokemonThatCanEvolve.name} (Active Pokemon)')
    else:
      print(f'{index}   {pokemonThatCanEvolve.name} (Bench)')

  print('\nCommands:')
  print('details {x}: get Pokemon details')
  print('choose {x}: choose Pokemon to evolve')

  text = input()

  text = text.split()

  if text[0] == 'details' and int(text[1]) < len(canEvolveFrom):
    printPokemon(canEvolveFrom[int(text[1])])
    return choosePokemonToEvolveFrom(game, player, canEvolveFrom, evolutionPokemonHandIndex)
  if text[0] == 'choose' and int(text[1]) < len(canEvolveFrom):
    game.evolve(player, canEvolveFrom[0]['pokemonLocation'], canEvolveFrom[0]['pokeonIndex'], 
                  evolutionPokemonHandIndex)
    return game
  else:
    print('what?')
    return choosePokemonToEvolveFrom(game, player, canEvolveFrom, evolutionPokemonHandIndex)

def evolvePokemon(game, player, opponent):
  print('\nWhich evolution Pokemon in your hand do you want to play?')

  evolutionPokemonHand = []
  evolutionPokemonHandIndexes = []

  for index, card in enumerate(game.players[player].hand):
    if card.cardType == CardType.Pokemon and not card.stage == Stage.Basic:
      canPlay = False

      for pokemon in card.evolvesFrom:
        if game.players[player].activePokemon.name == pokemon.name:
          canPlay = True

        for benchPokemon in game.players[player].bench:
          if benchPokemon.name == pokemon.name:
            canPlay = True
      
      if canPlay:
        evolutionPokemonHand.append(card)
        evolutionPokemonHandIndexes.append(index)
  
  for index, pokemon in enumerate(evolutionPokemonHand):
    print(f'{index}   {pokemon.name}')

  print('\nCommands:')
  print('details {x}: get details about Pokemon')
  print('choose {x}: choose evolution Pokemon to play')

  text = input()

  text = text.split()

  if text[0] == 'details' and int(text[1]) < len(evolutionPokemonHand):
    printPokemon(evolutionPokemonHand[int(text[0])])
    return evolvePokemon(game, player, opponent)
  elif text[0] == 'choose' and int(text[1]) < len(evolutionPokemonHand):
    canEvolveFrom = []

    for pokemon in evolutionPokemonHand[int(text(1))].evolvesFrom:
      if game.players[player].activePokemon.name == pokemon.name:
        canEvolveFrom.append({ 'name': pokemon.name, 'pokemonLocation': 'activePokemon', 'pokemonIndex': None })

      for index, benchPokemon in enumerate(game.players[player].bench):
        if benchPokemon.name == pokemon.name:
          canEvolveFrom.append({ 'name': pokemon.name, 'pokemonLocation': 'bench', 'pokemonIndex': index})

    if len(canEvolveFrom) == 1:
      game.evolve(player, canEvolveFrom[0]['pokemonLocation'], canEvolveFrom[0]['pokeonIndex'], 
                  evolutionPokemonHandIndexes[int(text(1))])
      
      return game
    else:
      return choosePokemonToEvolveFrom(game, player, canEvolveFrom, evolutionPokemonHandIndexes[int(text(1))])
  else:
    print('what?')
    return evolvePokemon(game, player, opponent)



humanAttackTurnOptions = {
  'crossFusionStrike': crossFusionStrike,
  'maxMiracle': maxMiracle,
  'energyMix': energyMix,
  'psychicLeap': psychicLeap,
  'technoBlast': technoBlast,
  'melodiousEcho': melodiousEcho,
  'glisteningDroplets': glisteningDroplets,
  'retreat': retreat,
  'playBasicPokemonToBench': playBasicPokemonToBench,
  'evolvePokemon': evolvePokemon,
  'playItem': playItem
}