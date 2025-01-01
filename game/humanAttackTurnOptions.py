from enums import CardType, EnergyType, Stage
from pokemonTcg import printPokemon, printNonPokemonCard
from cards import FusionStrikeEnergyFS244, DoubleTurboEnergyBS151
from naiveAI import naiveAiChoose
import random

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
        printNonPokemonCard(FusionStrikeEnergyFS244())
      elif energyCardNames[energyCardIndex] == 'Double Turbo Energy':
        printNonPokemonCard(DoubleTurboEnergyBS151())
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
    printNonPokemonCard(energy[int(text[1])])
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

def battleVipPassSecondPokemon(game, player):
  print('\nDo you want to pick a second Pokemon?')

  print('\nCommads:')
  print('yes')
  print('no')

  text = input()

  if text == 'no':
    return None
  
  basicPokemon = []
  basicPokemonIndexes = []

  for index, card in enumerate(game.players[player].deck):
    if card.cardType == CardType.Pokemon and card.stage == Stage.Basic:
      basicPokemon.append(card)
      basicPokemonIndexes.append(index)

  print('\nPick a second Basic Pokemon from your deck.')

  for index, pokemon in enumerate(basicPokemon):
    print(f'{index}  {pokemon.name}')

  print('\nCommands:')
  print('details {x}: get details about Pokemon')
  print('choose {x}: choose Pokemon')

  textPokemon = input()

  textPokemon = textPokemon.split()

  if text[0] == 'details' and int(text[1]) < len(basicPokemon):
    printPokemon(basicPokemon[int(text[1])])
    return battleVipPassSecondPokemon(game, player)
  elif text[0] == 'choose' and int(text[1]) < len(basicPokemon):
    return basicPokemonIndexes[int(text[1])]
  else:
    print('what?')
    return battleVipPassSecondPokemon(game, player)
  
def cramomaticHeads(game, player):
  print('\nYour coin flip landed on heads.')

  print('\nPick a card from your deck to put into your hand.')

  for index, card in enumerate(game.players[player].deck):
    print(f'{index}   {card.name}')

  print('\nCommands:')
  print('details {x}: get details about card')
  print('choose {x}: choose card')

  text = input()

  text = text.split()

  if text[0] == 'details' and int(text[1]) < len(game.players[player].deck):
    printNonPokemonCard(game.players[player].deck[int(text[1])])
    return cramomaticHeads(game, player)
  elif text[0] == 'choose' and int(text[1]) < len(game.players[player].deck):
    return int(text[1])
  else:
    print('what?')
    return cramomaticHeads(game, player)

def ultraBallPickPokemon(game, player):
  print('\nPick a Pokemon from your deck to put into your hand.')

  pokemon = []
  pokemonIndexes = []

  for index, card in enumerate(game.players[player].deck):
    if card.cardType == CardType.Pokemon:
      pokemon.append(card)
      pokemonIndexes.append(index)

  if len(pokemon) == 0:
    print('There are no Pokemon in your deck. Ultra Ball ends.')

    return None

  for index, card in enumerate(pokemon):
    print(f'{index}   {card.name}')

  print('\nCommands:')
  print('details {x}: get details about Pokemon')
  print('choose {x}: choose Pokemon')

  text = input()

  text = text.split()

  if text[0] == 'details' and int(text[1]) < len(pokemon):
    printPokemon(pokemon[int(text[1])])
    return ultraBallPickPokemon(game, player)
  elif text[0] == 'choose' and int(text[1]) < len(pokemon):
    return pokemonIndexes[int(text[1])]
  else:
    print('what?')
    return ultraBallPickPokemon(game, player)

def ultraBallDiscardSecondCard(game, player, hand):
  print('\nPick second card from your hand to discard.')

  for index, card in enumerate(hand):
    print(f'{index}   {card.name}')

  print('\nCommands:')
  print('details {x}: get details about card')
  print('choose {x}: choose card')

  text = input()

  text = text.split()

  if text[0] == 'details' and int(text[1]) < len(game.players[player].hand):
    printNonPokemonCard(game.players[player].hand[int(text[1])])
    return determineItemEffectParams(game, player, opponent, item)
  elif text[0] == 'choose' and int(text[1]) < len(game.players[player].hand):
    discardCard2Index = int(text[1])

    return discardCard2Index, ultraBallPickPokemon(game, player)
  else:
    print('what?')
    return ultraBallDiscardSecondCard(game, player, hand)

def lostVacuumPickCard(game, player, opponent):
  print('\nPick a card to put into the Lost Zone.')

  count = 0
  cardInfo = []

  print('\nSTADIUM')

  if game.players[player].stadium != None:
    print(f'{count}   {game.players[player].stadium.name}')

    count += 1
    cardInfo.append({ 'lostZoneCardOwner': player, 'lostZoneCardStadium': True})
  elif game.players[opponent].stadium != None:
    print(f'{count}   {game.players[opponent].stadium.name}')

    count += 1
    cardInfo.append({ 'lostZoneCardOwner': opponent, 'lostZoneCardStadium': True})

  print('\nOPPONENT\'S TOOLS')

  if game.players[opponent].activePokemon.tool != None:
    print(f'{count}  {game.players[opponent].activePokemon.tool.name} 
          (attached to Active Pokemon {game.players[opponent].activePokemon.name})')
    
    count += 1
    cardInfo.append({ 'lostZoneCardOwner': opponent, 'lostZoneCardStadium': False, 'lostZoneCardLocation': 'activePokemon' })

  for index, pokemon in enumerate(game.players[opponent].bench):
    if pokemon.tool != None:
      print(f'{count}  {pokemon.tool.name} (attached to Bench Pokemon {pokemon.name})')
    
      count += 1
      cardInfo.append({ 'lostZoneCardOwner': opponent, 'lostZoneCardStadium': False, 
                       'lostZoneCardLocation': 'bench', 'lostZoneCardIndex': index })

  print('\nYOUR TOOLS')

  if game.players[player].activePokemon.tool != None:
    print(f'{count}  {game.players[player].activePokemon.tool.name} 
          (attached to Active Pokemon {game.players[player].activePokemon.name})')

    count += 1
    cardInfo.append({ 'lostZoneCardOwner': player, 'lostZoneCardStadium': False, 'lostZoneCardLocation': 'activePokemon' })

  for index, pokemon in enumerate(game.players[player].bench):
    if pokemon.tool != None:
      print(f'{count}  {pokemon.tool.name} (attached to Bench Pokemon {pokemon.name})')

      count += 1
      cardInfo.append({ 'lostZoneCardOwner': player, 'lostZoneCardStadium': False, 
                       'lostZoneCardLocation': 'bench', 'lostZoneCardIndex': index })
      
  print('\nCommands:')
  print('details {x}: get card details')
  print('choose {x}: choose card')

  text = input()

  text = text.split()

  if text[0] == 'details' and int(text[1]) < len(cardInfo):
    if cardInfo[int(text[1])]['lostZoneCardStadium']:
      printNonPokemonCard(game.players[cardInfo[int(text[1])]['lostZoneCardOwner']].stadium)
    else:
      if cardInfo[int(text[1])]['lostZoneCardLocation'] == 'activePokemon':
        printNonPokemonCard(game.players[cardInfo[int(text[1])]['lostZoneCardOwner']].activePokemon.tool)
      else:
        printNonPokemonCard(game.players[cardInfo[int(text[1])]['lostZoneCardOwner']]
                            .bench[cardInfo[int(text[1])]['lostZoneCardIndex']].tool)
  
    return lostVacuumPickCard(game, player, opponent)
  elif text[0] == 'choose' and int(text[1]) < len(cardInfo):
    return cardInfo[int(text[1])]
  else:
    print('what?')
    return lostVacuumPickCard(game, player, opponent)

def escapeRopePlayerChoose(game, player, opponent, opponentChosenIndex):
  print('\nPick a Pokemon from your Bench to switch with your Active Pokemon.')

  for index, pokemon in enumerate(game.players[player].bench):
    print(f'{index}   {pokemon.name}')

  print('\nCommands:')
  if opponentChosenIndex != None:
    print('check: get details about opponent\'s chosen Pokemon')
  print('details {x}: get details about Pokemon')
  print('choose {x}: choose Pokemon')

  text = input()

  text = text.split()

  if text[0] == 'details' and int(text[1]) < len(game.players[player].bench):
    printPokemon(game.players[player].bench[int(text[1])])
    return escapeRopePlayerChoose(game, player, opponent, opponentChosenIndex)
  elif text[0] == 'choose' and int(text[1]) < len(game.players[player].bench):
    return int(text[1])
  elif text[0] == 'check' and opponentChosenIndex != None:
    printPokemon(game.players[opponent].bench[opponentChosenIndex])
    return escapeRopePlayerChoose(game, player, opponent, opponentChosenIndex)
  else:
    print('what?')
    return escapeRopePlayerChoose(game, player, opponent, opponentChosenIndex)

def palPadSecondSupporter(game, player, supporterCards):
  print('\nPick a second Supporter card from your discard pile to put into your hand.')

  for index, card in enumerate(supporterCards):
    print(f'{index}   {card.name}')

  print('\nCommands:')
  print('details {x}: get details about card')
  print('choose {x}: choose card')
  print('none: don\'t choose a second Supporter card')
  # TODO make uniform if you ask yes or no before choosing or give option 'none'

  text = input()

  text = text.split()

  if text[0] == 'details' and int(text[1]) < len(supporterCards):
    printNonPokemonCard(supporterCards[int(text[1])])
    return palPadSecondSupporter(game, player, supporterCards)
  elif text[0] == 'choose' and int(text[1]) < len(supporterCards):
    return int(text[1])
  elif text[0] == 'none':
    return None
  else:
    print('what?')
    return palPadSecondSupporter(game, player, supporterCards)

def determineItemEffectParams(game, player, opponent, item):
  if item.name == 'Battle VIP Pass':
    basicPokemon = []
    basicPokemonIndexes = []

    for index, card in enumerate(game.players[player].deck):
      if card.cardType == CardType.Pokemon and card.stage == Stage.Basic:
        basicPokemon.append(card)
        basicPokemonIndexes.append(index)

    if len(basicPokemon) == 0:
      print('There are no Basic Pokemon in your deck. Battle VIP Pass ends.')

      return { 'pokemon1Index': None, 'pokemon2Index': None }

    print('\nPick a Basic Pokemon from your deck.')

    for index, pokemon in enumerate(basicPokemon):
      print(f'{index}  {pokemon.name}')

    print('\nCommands:')
    print('details {x}: get details about Pokemon')
    print('choose {x}: choose Pokemon')

    text = input()

    text = text.split()

    if text[0] == 'details' and int(text[1]) < len(basicPokemon):
      printPokemon(basicPokemon[int(text[1])])
      return determineItemEffectParams(game, player, opponent, item)
    elif text[0] == 'choose' and int(text[1]) < len(basicPokemon):
      pokemon1Index = basicPokemonIndexes[int(text[1])]

      if len(game.players[player].bench) == 5 or len(basicPokemon) == 1:
        return game

      pokemon2Index = battleVipPassSecondPokemon(game, player)

      return { 'pokemon1Index': pokemon1Index, 'pokemon2Index': pokemon2Index }
    else:
      print('what?')
      return determineItemEffectParams(game, player, opponent, item)
    
  elif item.name == 'Cram-O-Matic':
    print('\nPick an item to discard from your hand.')

    itemCards = []
    itemCardIndexes = []

    for index, card in enumerate(game.players[player].hand):
      if card.cardType == CardType.Item:
        itemCards.append(card)
        itemCardIndexes.append(index)

    for index, card in enumerate(itemCards):
      print(f'{index}   {card.name}')

    print('\nCommands:')
    print('details {x}: get details about item')
    print('choose {x}: choose item')

    text = input()

    text = text.split()

    if text[0] == 'details' and int(text[1]) < len(itemCards):
      printNonPokemonCard(itemCards[int(text[1])])
      return determineItemEffectParams(game, player, opponent, item)
    elif text[0] == 'choose' and int(text[1]) < len(itemCards):
      discardItemIndex = itemCardIndexes[int(text[1])]

      coinFlip = random.randint(0, 1)

      if coinFlip == 1:
        return { 'discardItemIndex': discardItemIndex, 'heads': True, 'deckCardIndex': cramomaticHeads(game, player) }
      
      return { 'discardItemIndex': discardItemIndex, 'heads': False } 
    else:
      print('what?')
      return determineItemEffectParams(game, player, opponent, item)
    
  elif item.name == 'Power Tablet':
    return { }
  
  elif item.name == 'Ultra Ball':
    # TODO reveal the card for later ML needs

    print('\nPick first card from your hand to discard.')

    hand = game.players[player].hand

    for index, card in enumerate(hand):
      print(f'{index}   {card.name}')

    print('\nCommands:')
    print('details {x}: get details about card')
    print('choose {x}: choose card')

    text = input()

    text = text.split()

    if text[0] == 'details' and int(text[1]) < len(game.players[player].hand):
      printNonPokemonCard(game.players[player].hand[int(text[1])])
      return determineItemEffectParams(game, player, opponent, item)
    elif text[0] == 'choose' and int(text[1]) < len(game.players[player].hand):
      discardCard1Index = int(text[1])

      hand.pop(discardCard1Index)

      discardCard2Index, pokemonDeckIndex = ultraBallDiscardSecondCard(game, player, hand)

      return { 'discardCard1Index': discardCard1Index, 'discardCard2Index': discardCard2Index, 'pokemonDeckIndex': pokemonDeckIndex }

    else:
      print('what?')
      return determineItemEffectParams(game, player, opponent, item)

  elif item.name == 'Lost Vacuum':
    print('\nPick a card from your hand to discard.')

    for index, card in enumerate(game.players[player].hand):
      print(f'{index}   {card.name}')

    print('\nCommands:')
    print('details {x}: get details about card')
    print('choose {x}: choose card')

    text = input()

    text = text.split()

    if text[0] == 'details' and int(text[1]) < len(game.players[player].hand):
      printNonPokemonCard(game.players[player].hand[int(text[1])])
      return determineItemEffectParams(game, player, opponent, item)
    elif text[0] == 'choose' and int(text[1]) < len(game.players[player].hand):
      entryFeeLostZoneCardIndex = int(text[1])

      cardInfo = lostVacuumPickCard(game, player, opponent)

      cardInfo['entryFeeLostZoneCardIndex'] = entryFeeLostZoneCardIndex

      return cardInfo
    else:
      print('what?')
      return determineItemEffectParams(game, player, opponent, item)
    
  elif item.name == 'Nest Ball':
    print('\nPick a Basic Pokemon from your deck to put onto your Bench.')

    basicPokemon = []
    basicPokemonIndexes = []

    for index, card in enumerate(game.players[player].deck):
      if card.cardType == CardType.Pokemon and card.stage == Stage.Basic:
        basicPokemon.append(card)
        basicPokemonIndexes.append(index)

    if len(basicPokemon) == 0:
      print('There are no Basic Pokemon in your deck. Nest Ball ends.')

      return { 'pokemonDeckIndex': None }

    for index, pokemon in enumerate(basicPokemon):
      print(f'{index}   {pokemon.name}')

    print('\nCommands:')
    print('details {x}: get details about Pokemon')
    print('choose {x}: choose Pokemon')

    text = input()

    text = text.split()

    if text[0] == 'details' and int(text[1]) < len(basicPokemon):
      printPokemon(basicPokemon[int(text[1])])
      return determineItemEffectParams(game, player, opponent, item)
    elif text[0] == 'choose' and int(text[1]) < len(basicPokemon):
      return { 'pokemonDeckIndex': basicPokemonIndexes[int(text[1])] }
    else:
      print('what?')
      return determineItemEffectParams(game, player, opponent, item)

  elif item.name == 'Switch Cart':
    print('\nPick a Pokemon from your Bench to switch with your Active Pokemon.')

    for index, pokemon in enumerate(game.players[player].bench):
      print(f'{index}   {pokemon.name}')

    print('\nCommands:')
    print('details {x}: get details about Pokemon')
    print('choose {x}: choose Pokemon')

    text = input()

    text = text.split()

    if text[0] == 'details' and int(text[1]) < len(game.players[player].bench):
      printPokemon(game.players[player].bench[int(text[1])])
      return determineItemEffectParams(game, player, opponent, item)
    elif text[0] == 'choose' and int(text[1]) < len(game.players[player].bench):
      return { 'benchPokemonIndex': int(text[1]) }
    else:
      print('what?')
      return determineItemEffectParams(game, player, opponent, item)

  elif item.name == 'Escape Rope':
    opponentChosenIndex = None

    if len(game.players[opponent].bench) == 0:
      print('\nYour opponent has no benched Pokemon. Their Active Pokemon will stay in the Active Pokemon spot.')
    else:
      opponentChosenIndex = naiveAiChoose(game.players[opponent].bench)

      print(f'\nYour opponent has chosen to put out {game.players[opponent].bench[opponentChosenIndex].name}.')

    if len(game.players[player].bench) == 0:
      print('\nYou have no benched Pokemon. Your Active Pokemon will stay in the Active Pokemon spot. Escape Rope ends.')

      return { 'opponentBenchIndex': opponentChosenIndex }
    else:
      playerPokemonIndex = escapeRopePlayerChoose(game, player, opponent, opponentChosenIndex)

      return { 'playerBenchIndex': playerPokemonIndex, 'opponentBenchIndex': opponentChosenIndex }
        
  elif item.name == 'Pal Pad':
    print('\nPick first Supporter card from your discard pile to shuffle into your deck.')

    supporterCards = []
    supporterCardIndexes = []

    for index, card in enumerate(game.players[player].discardPile):
      if card.cardType == CardType.Supporter:
        supporterCards.append(card)
        supporterCardIndexes.append(index)

    for index, card in enumerate(supporterCards):
      print(f'{index}   {card.name}')

    print('\nCommands:')
    print('details {x}: get details about card')
    print('choose {x}: choose card')

    text = input()

    text = text.split()

    if text[0] == 'details' and int(text[1]) < len(supporterCards):
      printNonPokemonCard(supporterCards[int(text[1])])
      return determineItemEffectParams(game, player, opponent, item)
    elif text[0] == 'choose' and int(text[1]) < len(supporterCards):
      firstChosenIndex = supporterCardIndexes[int(text[1])]

      supporterCards.pop(int(text[1]))
      supporterCardIndexes.pop(int(text[1]))

      if len(supporterCards) == 0:
        print('There are no more Supporter cards in your discard pile. Pal Pad ends.')

        return { 'firstChosenIndex': firstChosenIndex }
      else:
        secondChosenIndex = palPadSecondSupporter(game, player, supporterCards)

        if secondChosenIndex == None:
          return { 'firstChosenIndex': firstChosenIndex }

        return { 'firstChosenIndex': firstChosenIndex, 'secondChosenIndex': supporterCardIndexes[secondChosenIndex] }
    else:
      print('what?')
      return determineItemEffectParams(game, player, opponent, item)
    
  else:
    raise Exception('item not found')
    
def playItem(game, player, opponent):
  itemCards = []
  itemCardIndexes = []

  for index, card in enumerate(game.players[player].hand):
    if card.cardType == CardType.Item and card.canplay(game, player, opponent):
      itemCards.append(card)
      itemCardIndexes.append(index)
    
  print('\nWhich item do you want to play?')

  for index, card in enumerate(itemCards):
    print(f'{index}   {card.name}')

  print('\nCommands:')
  print('details {x}: show item card details')
  print('choose {x}: choose item card')

  text = input()

  text = text.split()

  if text[0] == 'details' and int(text[1]) < len(itemCards):
    printNonPokemonCard(itemCards[int(text[1])])
    return playItem(game, player, opponent)
  elif text[0] == 'choose' and int(text[1]) < len(itemCards):
    game.playItem(player, itemCardIndexes[int(text[1])], determineItemEffectParams(game, player, opponent, itemCards[int(text[1])]))

    return game
  else:
    print('what?')
    return playItem(game, player, opponent)

def playStadium(game, player, opponent):
  stadiumCards = []
  stadiumCardIndexes = []

  for index, card in enumerate(game.players[player].hand):
    if card.cardType == CardType.Stadium:
      stadiumCards.append(card)
      stadiumCardIndexes.append(index)
    
  print('\nWhich Stadium do you want to play?')

  for index, card in enumerate(stadiumCards):
    print(f'{index}   {card.name}')

  print('\nCommands:')
  print('details {x}: show stadium card details')
  print('choose {x}: choose stadium card')

  text = input()

  text = text.split()

  if text[0] == 'details' and int(text[1]) < len(stadiumCards):
    printNonPokemonCard(stadiumCards[int(text[1])])
    return playStadium(game, player, opponent)
  elif text[0] == 'choose' and int(text[1]) < len(stadiumCards):
    game.playStadium(player, stadiumCardIndexes[int(text[1])])

    return game
  else:
    print('what?')
    return playStadium(game, player, opponent)

def playToolWhichPokemon(game, player):
  print('\nOnto which Pokemon do you want to attach the Tool?')

  print(f'0   {game.players[player].activePokemon.name} (Active Pokemon)')

  for index, pokemon in enumerate(game.players[player].bench):
    print(f'{index + 1}   {pokemon.name} (On Bench)')

  print('\nCommands:')
  print('details {x}: show Pokemon details')
  print('choose {x}: choose Pokemon')

  text = input()

  text = text.split()

  if text[0] == 'details' and int(text[1]) <= len(game.players[player].bench):
    if int(text[1]) == 0:
      printPokemon(game.players[player].activePokemon)
    else:
      printPokemon(game.players[player].bench[int(text[1]) - 1])

    return playToolWhichPokemon(game, player)
  elif text[0] == 'choose' and int(text[1]) <= len(game.players[player].bench) + 1:
    return int(text[1])
  else:
    print('what?')
    return playToolWhichPokemon(game, player)

def playTool(game, player, opponent):
  toolCards = []
  toolCardIndexes = []

  for index, card in enumerate(game.players[player].hand):
    if card.cardType == CardType.Tool:
      toolCards.append(card)
      toolCardIndexes.append(index)
    
  print('\nWhich Tool do you want to play?')

  for index, card in enumerate(toolCards):
    print(f'{index}   {card.name}')

  print('\nCommands:')
  print('details {x}: show tool card details')
  print('choose {x}: choose tool card')

  text = input()

  text = text.split()

  if text[0] == 'details' and int(text[1]) < len(toolCards):
    printNonPokemonCard(toolCards[int(text[1])])
    return playTool(game, player, opponent)
  elif text[0] == 'choose' and int(text[1]) < len(toolCards):
    pokemonChoice = playToolWhichPokemon(game, player)

    if pokemonChoice == 0:
      game.playTool(player, toolCardIndexes[int(text[1])], 'activePokemon')
    else:
      game.playTool(player, toolCardIndexes[int(text[1])], 'bench', pokemonChoice - 1)

    return game
  else:
    print('what?')
    return playTool(game, player, opponent)

def elesasSparkleChooseSecondPokemon(game, player, fusionStrikePokemon, fusionStrikePokemonLocations):
  print('\nDo you want to pick a second Fusion Strike Pokemon to attach a Fusion Strike Energy from your deck to (if one is found while searching)?')

  print('\nCommands:')
  print('yes')
  print('no')

  text = input()

  if text == 'no':
    return None, None

  for index, pokemon in enumerate(fusionStrikePokemon):
    print(f'{index}   {pokemon.name}')

  print('\nCommands:')
  print('details {x}: get details about Pokemon')
  print('choose {x}: choose Pokemon')

  text = input()

  text = text.split()

  if text[0] == 'details' and int(text[1]) < len(fusionStrikePokemon):
    printPokemon(fusionStrikePokemon[int(text[1])])
    return elesasSparkleChooseSecondPokemon(game, player)
  elif text[0] == 'choose' and int(text[1]) < len(fusionStrikePokemon):
    if int(text[1]) == 0:
      pokemon2Location = 'activePokemon'
      pokemon2Index = None
    else:
      pokemon2Location = 'bench'
      pokemon2Index = int(text[1]) - 1

    return pokemon1Location, pokemon1Index
  else:
    print('what?')
    return elesasSparkleChooseSecondPokemon(game, player)

def determineSupporterEffectParams(game, player, opponent, supporter):
  if supporter.name == 'Boss\'s Orders (Ghetsis)':
    print('\nPick a Pokemon from your opponent\'s Bench to switch with their Active Pokemon.')

    for index, pokemon in enumerate(game.players[opponent].bench):
      print(f'{index}   {pokemon.name}')

    print('\nCommands:')
    print('details {x}: get details about Pokemon')
    print('choose {x}: choose Pokemon')

    text = input()

    text = text.split()

    if text[0] == 'details' and int(text[1]) < len(game.players[opponent].bench):
      printPokemon(game.players[opponent].bench[int(text[1])])
      return determineSupporterEffectParams(game, player, opponent, supporter)
    elif text[0] == 'choose' and int(text[1]) < len(game.players[opponent].bench):
      return { 'opponent': opponent, 'benchPokemonIndex': int(text[1]) }
    else:
      print('what?')
      return determineSupporterEffectParams(game, player, opponent, supporter)
  
  elif supporter.name == 'Elesa\'s Sparkle':
    print('\nChoose a Fusion Strike Pokemon to attach a Fusion Strike Energy card from your deck to (if you have one upon searching.)')

    fusionStrikePokemon = []
    fusionStrikePokemonLocations = []

    if game.players[player].activePokemon.fusionStrike:
      fusionStrikePokemon.append(game.players[player].activePokemon)
      fusionStrikePokemonLocations.append({ 'location': 'activePokemon', 'index': None })

    for index, pokemon in enumerate(game.players[player].bench):
      if pokemon.fusionStrike:
        fusionStrikePokemon.append(pokemon)
        fusionStrikePokemonLocations.append({ 'location': 'bench', 'index': index })

    for index, pokemon in enumerate(fusionStrikePokemon):
      print(f'{index}   {pokemon.name}')

    print('\nCommands:')
    print('details {x}: get details about Pokemon')
    print('choose {x}: choose Pokemon')

    text = input()

    text = text.split()

    if text[0] == 'details' and int(text[1]) < len(fusionStrikePokemon):
      printPokemon(fusionStrikePokemon[int(text[1])])
      return determineSupporterEffectParams(game, player, opponent, supporter)
    elif text[0] == 'choose' and int(text[1]) < len(fusionStrikePokemon):
      if int(text[1]) == 0:
        pokemon1Location = 'activePokemon'
        pokemon1Index = None
      else:
        pokemon1Location = 'bench'
        pokemon1Index = int(text[1]) - 1

      fusionStrikePokemon.pop(int(text[1]))
      fusionStrikePokemonLocations.pop(int(text[1]))

      pokemon2Location, pokemon2Index = elesasSparkleChooseSecondPokemon(game, player, fusionStrikePokemon, fusionStrikePokemonLocations)

      return { 'pokemon1Location': pokemon1Location, 'pokemon1Index': pokemon1Index, 'pokemon2Location': pokemon2Location, 'pokemon2Index': pokemon2Index }
    else:
      print('what?')
      return determineSupporterEffectParams(game, player, opponent, supporter)
    
  elif supporter.name == 'Iono' or supporter.name == 'Judge':
    return { 'opponent': opponent }

def playSupporter(game, player, opponent):
  supporterCards = []
  supporterCardIndexes = []

  for index, card in enumerate(game.players[player].hand):
    if card.cardType == CardType.Supporter:
      supporterCards.append(card)
      supporterCardIndexes.append(index)
    
  print('\nWhich Supporter do you want to play?')

  for index, card in enumerate(supporterCards):
    print(f'{index}   {card.name}')

  print('\nCommands:')
  print('details {x}: show supporter card details')
  print('choose {x}: choose supporter card')

  text = input()

  text = text.split()

  if text[0] == 'details' and int(text[1]) < len(supporterCards):
    printNonPokemonCard(supporterCards[int(text[1])])
    return playSupporter(game, player, opponent)
  elif text[0] == 'choose' and int(text[1]) < len(supporterCards):
    game.playSupporter(player, supporterCardIndexes[int(text[1])])

    return game
  else:
    print('what?')
    return playSupporter(game, player, opponent)

def attachEnergyPickPokemon(game, player):
  print('\nOnto which Pokemon do you want to attach the Energy?')

  print(f'0   {game.players[player].activePokemon.name} (Active Pokemon)')

  for index, pokemon in enumerate(game.players[player].bench):
    print(f'{index + 1}   {pokemon.name} (On Bench)')

  print('\nCommands:')
  print('details {x}: show Pokemon details')
  print('choose {x}: choose Pokemon')

  text = input()

  text = text.split()

  if text[0] == 'details' and int(text[1]) <= len(game.players[player].bench) + 1:
    if int(text[1]) == 0:
      printPokemon(game.players[player].activePokemon)
    else:
      printPokemon(game.players[player].bench[int(text[1]) - 1])

    return attachEnergyPickPokemon(game, player)
  elif text[0] == 'choose' and int(text[1]) <= len(game.players[player].bench) + 1:
    if int(text[1]) == 0:
      return 'activePokemon', None
    else:
      return 'bench', int(text[1]) - 1
  else:
    print('what?')
    return attachEnergyPickPokemon(game, player)

def attachEnergy(game, player):
  print('\nWhich Energy card do you want to attach?')

  energyCards = []
  energyCardIndexes = []

  for index, card in enumerate(game.players[player].hand):
    if card.cardType == CardType.Energy:
      energyCards.append(card)
      energyCardIndexes.append(index)

  for index, card in enumerate(energyCards):
    print(f'{index}   {card.name}')

  print('\nCommands:')
  print('details {x}: show energy card details')
  print('choose {x}: choose energy card')

  text = input()

  text = text.split()

  if text[0] == 'details' and int(text[1]) < len(energyCards):
    printNonPokemonCard(energyCards[int(text[1])])
    return attachEnergy(game, player)
  elif text[0] == 'choose' and int(text[1]) < len(energyCards):
    pokemonLocation, pokemonIndex = attachEnergyPickPokemon(game, player)

    game.attachEnergy(player, energyCardIndexes[int(text[1]), pokemonLocation, pokemonIndex])

    return game
  else:
    print('what?')
    return attachEnergy(game, player)

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
  'playItem': playItem,
  'playStadium': playStadium,
  'playTool': playTool,
  'playSupporter': playSupporter,
  'attachEnergy': attachEnergy
}