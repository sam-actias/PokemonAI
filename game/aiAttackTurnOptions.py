from naiveAI import naiveAiChoose
from enums import CardType, EnergyType, Stage

aiChoose = naiveAiChoose

def crossFusionStrikePsychicLeapShuffleIn(game, player, opponent, benchedFusionStrikeMoves, benchedFusionStrikeIndexes, moveIndex):
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

    choose = aiChoose(game.players[player].bench)

    print(f'Your opponent chose {game.players[player].bench[choose].name} to replace Mew VMAX as their active Pokemon.')

    return game.players[player].activePokemon.moves['crossFusionStrike']['do'](game, player, 
        benchedFusionStrikeIndexes[moveIndex], benchedFusionStrikeMoves[moveIndex].name, { 'game': game, 
        'player': player, 'opponent': opponent, 'shuffleIn': True, 'newActivePokemonIndex': int(text[1]) })
    
def crossFusionStrikeEnergyMixPickPokemon(game, player, energyCardNames, 
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

  choose = aiChoose(fusionStrikePokemon)

  print(f'Your opponent chose {fusionStrikePokemon[choose]["pokemonName"]} to attach {energyCardNames[energyCardIndex]} to.')

  # TODO: modify so that vars get returned instead of using the game method here?
  return game.players[player].activePokemon.moves['crossFusionStrike']['do'](game, player, 
      benchedFusionStrikeIndexes[moveIndex], benchedFusionStrikeMoves[moveIndex].name, { 'game': game, 'player': player, 
      'deckIndex': energyCardIndexes[energyCardIndex], 'pokemonLocation': fusionStrikePokemon[int(text[1])]['pokemonLocation'], 
      'pokemonIndex': fusionStrikePokemon[choose]['pokemonIndex'] })

def crossFusionStrikeMoveChoices(game, player, opponent, benchedFusionStrikeMoves, benchedFusionStrikeIndexes, moveIndex):
  if benchedFusionStrikeMoves[moveIndex].name == 'maxMiracle':
    print('Mew VMAX used benched Fusion Strike Pokemon Mew VMAX\'s Max Miracle attack.')

    return game.players[player].activePokemon.moves['crossFusionStrike']['do'](game, player, 
          benchedFusionStrikeIndexes[moveIndex], benchedFusionStrikeMoves[moveIndex].name, 
          { 'game': game, 'player': player, 'opponent': opponent })
  
  elif benchedFusionStrikeMoves[moveIndex].name == 'technoBlast':
    print('Mew VMAX used benched Fusion Strike Pokemon Genesect\'s Techno Blast attack.')

    return game.players[player].activePokemon.moves['crossFusionStrike']['do'](game, player, 
          benchedFusionStrikeIndexes[moveIndex], benchedFusionStrikeMoves[moveIndex].name, 
          { 'game': game, 'player': player, 'opponent': opponent })
  
  elif benchedFusionStrikeMoves[moveIndex].name == 'melodiousEcho':
    print('Mew VMAX used benched Fusion Strike Pokemon Meloetta\'s Melodious Echo attack.')

    return game.players[player].activePokemon.moves['crossFusionStrike']['do'](game, player, 
          benchedFusionStrikeIndexes[moveIndex], benchedFusionStrikeMoves[moveIndex].name, 
          { 'game': game, 'player': player, 'opponent': opponent })
  
  elif benchedFusionStrikeMoves[moveIndex].name == 'energyMix':
    print('Mew VMAX used benched Fusion Strike Pokemon Mew V\'s Energy Mix attack.')

    energyCardNames = []
    energyCardIndexes = []

    for index, card in enumerate(game.players[player].deck):
      if card.cardType == CardType.Energy and card.name not in energyCardNames:
        energyCardNames.append(card.name)
        energyCardIndexes.append(index)

    energyCardNamesAmt = len(energyCardNames)

    if energyCardNamesAmt == 0:
      print('There are no energy cards in your opponent\'s deck. Energy Mix ends.')

      game.players[player].deck = game.shuffle(game.players[player].deck)

      return game

    print('\nYour opponent picks an energy card they want to attach to one of their Fusion Strike Pokemon.')

    energyCardIndex = aiChoose(energyCardNames)

    print(f'\nYour opponent picks {energyCardNames[energyCardIndex]} energy card from their deck to attach to one of their Fusion Strike Pokemon.')

    return crossFusionStrikeEnergyMixPickPokemon(game, player, energyCardNames, 
              benchedFusionStrikeMoves, benchedFusionStrikeIndexes, moveIndex, energyCardIndexes, energyCardIndex)

  elif benchedFusionStrikeMoves[moveIndex].name == 'psychicLeap':
    print('Mew VMAX used benched Fusion Strike Pokemon Mew V\'s Psychic Leap attack.')
    if len(game.players[player].bench) == 0:
      print('There are no benched Pokemon to replace Mew VMAX, so cannot shuffle Mew VMAX into the deck. Psychic Leap ends.')
      return game.players[player].activePokemon.moves['crossFusionStrike']['do'](game, player, 
          benchedFusionStrikeIndexes[moveIndex], benchedFusionStrikeMoves[moveIndex].name, { 'game': game, 
          'player': player, 'opponent': opponent, 'shuffleIn': False })

    chooseYesNo = aiChoose(['no', 'yes'])

    if chooseYesNo:
      print('Your opponent chose to shuffle Mew VMAX and all attached cards into their deck as part of the Psychic Leap.')
      crossFusionStrikePsychicLeapShuffleIn(game, player, opponent)

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

    availablePokemon = []

    availablePokemon.append(game.players[opponent].activePokemon)

    for index, pokemon in enumerate(game.players[opponent].bench):
      availablePokemon.append(pokemon)

    choose1 = aiChoose(game.players[opponent].bench)

    if choose1 == 0:
      howToPutDamageCounters.append({ 'pokemonLocation': 'activePokemon', 'pokemonIndex': None })

      print(f'\nYour opponent chose {game.players[opponent].activePokemon.name} to put the first damage counter (10 HP) on.')
    else:
      howToPutDamageCounters.append({ 'pokemonLocation': 'bench', 'pokemonIndex': choose1 - 1 })

      print(f'\nYour opponent chose {game.players[opponent].bench[choose1 - 1].name} to put the first damage counter (10 HP) on.')
    
    choose2 = aiChoose(game.players[opponent].bench)

    if choose2 == 0:
      howToPutDamageCounters.append({ 'pokemonLocation': 'activePokemon', 'pokemonIndex': None })

      print(f'\nYour opponent chose {game.players[opponent].activePokemon.name} to put the first damage counter (10 HP) on.')
    else:
      howToPutDamageCounters.append({ 'pokemonLocation': 'bench', 'pokemonIndex': choose2 - 1 })

      print(f'\nYour opponent chose {game.players[opponent].bench[choose1 - 1].name} to put the first damage counter (10 HP) on.')

    choose3 = aiChoose(game.players[opponent].bench)

    if choose3 == 0:
      howToPutDamageCounters.append({ 'pokemonLocation': 'activePokemon', 'pokemonIndex': None })

      print(f'\nYour opponent chose {game.players[opponent].activePokemon.name} to put the first damage counter (10 HP) on.')
    else:
      howToPutDamageCounters.append({ 'pokemonLocation': 'bench', 'pokemonIndex': choose3- 1 })

      print(f'\nYour opponent chose {game.players[opponent].bench[choose1 - 1].name} to put the first damage counter (10 HP) on.')

    choose4 = aiChoose(game.players[opponent].bench)

    if choose4 == 0:
      howToPutDamageCounters.append({ 'pokemonLocation': 'activePokemon', 'pokemonIndex': None })

      print(f'\nYour opponent chose {game.players[opponent].activePokemon.name} to put the first damage counter (10 HP) on.')
    else:
      howToPutDamageCounters.append({ 'pokemonLocation': 'bench', 'pokemonIndex': choose4 - 1 })

      print(f'\nYour opponent chose {game.players[opponent].bench[choose1 - 1].name} to put the first damage counter (10 HP) on.')

    choose5 = aiChoose(game.players[opponent].bench)

    if choose5 == 0:
      howToPutDamageCounters.append({ 'pokemonLocation': 'activePokemon', 'pokemonIndex': None })

      print(f'\nYour opponent chose {game.players[opponent].activePokemon.name} to put the first damage counter (10 HP) on.')
    else:
      howToPutDamageCounters.append({ 'pokemonLocation': 'bench', 'pokemonIndex': choose5 - 1 })

      print(f'\nYour opponent chose {game.players[opponent].bench[choose1 - 1].name} to put the first damage counter (10 HP) on.')
      
    return game.players[player].activePokemon.moves['crossFusionStrike']['do'](game, player, 
                benchedFusionStrikeIndexes[moveIndex], benchedFusionStrikeMoves[moveIndex].name, { 'game': game,
                'player': player, 'opponent': opponent, 'howToPutDamageCounters': howToPutDamageCounters })

def crossFusionStrike(game, player, opponent):
  print('Your opponent used Mew VMAX\'s Cross Fusion Strike attack.')

  benchedFusionStrikeIndexes = []
  benchedFusionStrikeMoves = []

  for index, pokemon in enumerate(game.players[player].bench):
    if pokemon.fusionStrike == True:
      for move in list(pokemon.moves.keys()):
        if pokemon.moves[move]['canDo'] == True:
          benchedFusionStrikeIndexes.append(index)
          benchedFusionStrikeMoves.append(pokemon.moves[move])

    moveIndex = benchedFusionStrikeIndexes[aiChoose(benchedFusionStrikeIndexes)]

    return crossFusionStrikeMoveChoices(game, player, opponent, benchedFusionStrikeMoves, benchedFusionStrikeIndexes, moveIndex)

def maxMiracle(game, player, opponent):
  print('Your opponent used Mew VMAX\'s Max Miracle attack.')

  return game.players[player].activePokemon.moves['maxMiracle']['do'](game, player, opponent)

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
  'attachEnergy': attachEnergy,
  'useStadiumEffect': useStadiumEffect,
  'useToolEffect': useToolEffect
}