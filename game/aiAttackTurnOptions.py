from naiveAI import naiveAiChoose
from enums import CardType, EnergyType, Stage
from printCards import printPokemon
import random

aiChoose = naiveAiChoose

# player means the player who is using the move
# opponent menas the other player, even if it's the user
# I know it's confusing
# TODO fix??

def crossFusionStrikePsychicLeapShuffleIn(game, player, opponent, benchedFusionStrikeMoves, benchedFusionStrikeIndexes, moveIndex):
  if len(game.players[player].bench) == 1:
    newActivePokemonIndex = 0

    print(f'Your opponent chooses to replace active Pokemon Mew V MAX with {game.players[player].bench[newActivePokemonIndex].name}.')

    return game.players[player].activePokemon.moves['crossFusionStrike']['do'](game, player, 
        benchedFusionStrikeIndexes[moveIndex], benchedFusionStrikeMoves[moveIndex].name, { 'game': game, 
        'player': player, 'opponent': opponent, 'shuffleIn': True, 'newActivePokemonIndex': newActivePokemonIndex })
  else:
    choose = aiChoose(game.players[player].bench)

    print(f'Your opponent chose {game.players[player].bench[choose].name} to replace Mew VMAX as their active Pokemon.')

    return game.players[player].activePokemon.moves['crossFusionStrike']['do'](game, player, 
        benchedFusionStrikeIndexes[moveIndex], benchedFusionStrikeMoves[moveIndex].name, { 'game': game, 
        'player': player, 'opponent': opponent, 'shuffleIn': True, 'newActivePokemonIndex': choose })
    
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
    print('Active Pokemon Mew VMAX used benched Fusion Strike Pokemon Mew VMAX\'s Max Miracle attack.')

    return game.players[player].activePokemon.moves['crossFusionStrike']['do'](game, player, 
          benchedFusionStrikeIndexes[moveIndex], benchedFusionStrikeMoves[moveIndex].name, 
          { 'game': game, 'player': player, 'opponent': opponent })
  
  elif benchedFusionStrikeMoves[moveIndex].name == 'technoBlast':
    print('Active Pokemon Mew VMAX used benched Fusion Strike Pokemon Genesect\'s Techno Blast attack.')

    return game.players[player].activePokemon.moves['crossFusionStrike']['do'](game, player, 
          benchedFusionStrikeIndexes[moveIndex], benchedFusionStrikeMoves[moveIndex].name, 
          { 'game': game, 'player': player, 'opponent': opponent })
  
  elif benchedFusionStrikeMoves[moveIndex].name == 'melodiousEcho':
    print('Active Pokemon Mew VMAX used benched Fusion Strike Pokemon Meloetta\'s Melodious Echo attack.')

    return game.players[player].activePokemon.moves['crossFusionStrike']['do'](game, player, 
          benchedFusionStrikeIndexes[moveIndex], benchedFusionStrikeMoves[moveIndex].name, 
          { 'game': game, 'player': player, 'opponent': opponent })
  
  elif benchedFusionStrikeMoves[moveIndex].name == 'energyMix':
    print('Active Pokemon Mew VMAX used benched Fusion Strike Pokemon Mew V\'s Energy Mix attack.')

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
    print('Active Pokemon Mew VMAX uses benched Fusion Strike Pokemon Mew V\'s Psychic Leap attack.')
    if len(game.players[player].bench) == 0:
      print('There are no benched Pokemon to replace Mew VMAX, so cannot shuffle Mew VMAX into the deck. Psychic Leap ends.')
      return game.players[player].activePokemon.moves['crossFusionStrike']['do'](game, player, 
          benchedFusionStrikeIndexes[moveIndex], benchedFusionStrikeMoves[moveIndex].name, { 'game': game, 
          'player': player, 'opponent': opponent, 'shuffleIn': False })

    chooseYesNo = aiChoose(['no', 'yes'])

    if chooseYesNo:
      print('Your opponent chooses to shuffle Mew VMAX and all attached cards into their deck as part of the Psychic Leap.')
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

      print(f'\nYour opponent chooses {game.players[opponent].activePokemon.name} to put the first damage counter (10 HP) on.')
    else:
      howToPutDamageCounters.append({ 'pokemonLocation': 'bench', 'pokemonIndex': choose1 - 1 })

      print(f'\nYour opponent chooses {game.players[opponent].bench[choose1 - 1].name} to put the first damage counter (10 HP) on.')
    
    choose2 = aiChoose(game.players[opponent].bench)

    if choose2 == 0:
      howToPutDamageCounters.append({ 'pokemonLocation': 'activePokemon', 'pokemonIndex': None })

      print(f'\nYour opponent chooses {game.players[opponent].activePokemon.name} to put the second damage counter (10 HP) on.')
    else:
      howToPutDamageCounters.append({ 'pokemonLocation': 'bench', 'pokemonIndex': choose2 - 1 })

      print(f'\nYour opponent chooses {game.players[opponent].bench[choose1 - 1].name} to put the second damage counter (10 HP) on.')

    choose3 = aiChoose(game.players[opponent].bench)

    if choose3 == 0:
      howToPutDamageCounters.append({ 'pokemonLocation': 'activePokemon', 'pokemonIndex': None })

      print(f'\nYour opponent chooses {game.players[opponent].activePokemon.name} to put the third damage counter (10 HP) on.')
    else:
      howToPutDamageCounters.append({ 'pokemonLocation': 'bench', 'pokemonIndex': choose3- 1 })

      print(f'\nYour opponent chooses {game.players[opponent].bench[choose1 - 1].name} to put the third damage counter (10 HP) on.')

    choose4 = aiChoose(game.players[opponent].bench)

    if choose4 == 0:
      howToPutDamageCounters.append({ 'pokemonLocation': 'activePokemon', 'pokemonIndex': None })

      print(f'\nYour opponent chooses {game.players[opponent].activePokemon.name} to put the fourth damage counter (10 HP) on.')
    else:
      howToPutDamageCounters.append({ 'pokemonLocation': 'bench', 'pokemonIndex': choose4 - 1 })

      print(f'\nYour opponent chooses {game.players[opponent].bench[choose1 - 1].name} to put the fourth damage counter (10 HP) on.')

    choose5 = aiChoose(game.players[opponent].bench)

    if choose5 == 0:
      howToPutDamageCounters.append({ 'pokemonLocation': 'activePokemon', 'pokemonIndex': None })

      print(f'\nYour opponent chooses {game.players[opponent].activePokemon.name} to put the fifth damage counter (10 HP) on.')
    else:
      howToPutDamageCounters.append({ 'pokemonLocation': 'bench', 'pokemonIndex': choose5 - 1 })

      print(f'\nYour opponent chooses {game.players[opponent].bench[choose1 - 1].name} to put the fifth damage counter (10 HP) on.')
      
    return game.players[player].activePokemon.moves['crossFusionStrike']['do'](game, player, 
                benchedFusionStrikeIndexes[moveIndex], benchedFusionStrikeMoves[moveIndex].name, { 'game': game,
                'player': player, 'opponent': opponent, 'howToPutDamageCounters': howToPutDamageCounters })

def crossFusionStrike(game, player, opponent):
  print('Your opponent uses Active Pokemon Mew VMAX\'s Cross Fusion Strike attack.')

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
  print('Your opponent uses Active Pokemon  Mew VMAX\'s Max Miracle attack.')

  return game.players[player].activePokemon.moves['maxMiracle']['do'](game, player, opponent)

def energyMixPickPokemon(game, player, energyCardNames, energyCardIndexes, energyCardIndex):
  fusionStrikePokemon = []

  if game.players[player].activePokemon.fusionStrike:
    fusionStrikePokemon.append({ 'pokemonName': game.players[player].activePokemon.name, 
                                'pokemonLocation': 'activePokemon', 'pokemonIndex': None })

  for index, pokemon in enumerate(game.players[player].bench):
    if pokemon.fusionStrike:
      fusionStrikePokemon.append({ 'pokemonName': pokemon.name, 'pokemonLocation': 'bench', 'pokemonIndex': index })

  print(f'\nYour opponent picks a Pokemon to attach {energyCardNames[energyCardIndex]} to.')

  for index, pokemon in enumerate(fusionStrikePokemon):
    print(f'{index}   {pokemon['pokemonName']}')

  choose = aiChoose(fusionStrikePokemon)

  print(f'Your opponent chooses {fusionStrikePokemon[choose]["pokemonName"]} to attach {energyCardNames[energyCardIndex]} to.')

  return game.players[player].activePokemon.moves['energyMix']['do'](game, player, energyCardIndexes[energyCardIndex], 
                fusionStrikePokemon[choose]['pokemonLocation'], fusionStrikePokemon[choose]['pokemonIndex'])

def energyMix(game, player, opponent):
  print('Your opponent uses Active Pokemon Mew V\'s Energy Mix attack.')
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

  for i in range(energyCardNamesAmt):
    print(f'{i}   {energyCardNames[i]}')

  choose = aiChoose(energyCardNames)

  energyCardIndex = choose

  print(f'\nYour opponent picks {energyCardNames[energyCardIndex]} energy card.')

  return energyMixPickPokemon(game, player, energyCardNames, energyCardIndexes, energyCardIndex)

def psychicLeapShuffleIn(game, player, opponent):
  if len(game.players[player].bench) == 1:
    newActivePokemonIndex = 0

    print(f'Your opponent chooses to replace active Pokemon Mew V with {game.players[player].bench[newActivePokemonIndex].name}.')

    return game.players[player].activePokemon.moves['psychicLeap']['do'](game, player, opponent,
                      True, newActivePokemonIndex)
  else:
    choose = aiChoose(game.players[player].bench)

    print(f'Your opponent chooses to replace active Pokemon Mew V with {game.players[player].bench[choose].name}.')

    return game.players[player].activePokemon.moves['psychicLeap']['do'](game, player, opponent,
                      True, choose)

def psychicLeap(game, player, opponent):
  print('Your opponent uses Active Pokemon Mew V\'s Psychic Leap attack.')

  if len(game.players[player].bench) == 0:
      return game.players[player].activePokemon.moves['psychicLeap']['do'](game, player, opponent, False)

  choose = aiChoose(['no', 'yes'])

  if choose:
    print('Your opponent chooses to shuffle Mew V and all attached cards into their deck as part of Psychic Leap.')

    psychicLeapShuffleIn(game, player, opponent)
  else:
    print('Your opponent chooses not to shuffle Mew V into their deck as part of Psychic Leap.')

  return game.players[player].activePokemon.moves['psychicLeap']['do'](game, player, opponent, False)

def technoBlast(game, player, opponent):
  print('Your opponent uses Active Pokemon Genesect V\'s Techno Blast attack.')

  return game.players[player].activePokemon.moves['technoBlast']['do'](game, player, opponent)

def melodiousEcho(game, player, opponent):
  print('Your opponent uses Active Pokemon Meloetta\'s Melodious Echo attack.')

  return game.players[player].activePokemon.moves['melodiousEcho']['do'](game, player, opponent)

def glisteningDroplets(game, player, opponent):
  if len(game.players[opponent].bench) == 0:
      return game.players[player].activePokemon.moves['glisteningDroplets']['do'](game, player, opponent, 
                  [{ 'pokemonLocation': 'activePokemon', 'pokemonIndex': None}, { 'pokemonLocation': 'activePokemon', 'pokemonIndex': None}, 
                   { 'pokemonLocation': 'activePokemon', 'pokemonIndex': None}, { 'pokemonLocation': 'activePokemon', 'pokemonIndex': None}, 
                   { 'pokemonLocation': 'activePokemon', 'pokemonIndex': None}])
    
  howToPutDamageCounters = []

  print('\nYour opponent chooses how to distribute 5 damage counters (10 HP each)')

  pokemonList = [game.players[opponent].activePokemon]

  for pokemon in game.players[opponent].bench:
    pokemonList.append(pokemon)

  choose1 = aiChoose(pokemonList)

  if choose1 == 0:
    howToPutDamageCounters.append({ 'pokemonLocation': 'activePokemon', 'pokemonIndex': None })

    print(f'\nYour opponent chooses {game.players[opponent].activePokemon.name} to put the first damage counter (10 HP) on.')
  else:
    howToPutDamageCounters.append({ 'pokemonLocation': 'bench', 'pokemonIndex': choose1 - 1 })

    print(f'\nYour opponent chooses {game.players[opponent].bench[choose1 - 1]} to put the first damage counter (10 HP) on.')
  
  choose2 = aiChoose(game.players[opponent].bench)

  if choose2 == 0:
    howToPutDamageCounters.append({ 'pokemonLocation': 'activePokemon', 'pokemonIndex': None })

    print(f'\nYour opponent chooses {game.players[opponent].activePokemon.name} to put the second damage counter (10 HP) on.')
  else:
    howToPutDamageCounters.append({ 'pokemonLocation': 'bench', 'pokemonIndex': choose2 - 1 })

    print(f'\nYour opponent chooses {game.players[opponent].bench[choose1 - 1].name} to put the second damage counter (10 HP) on.')

  choose3 = aiChoose(game.players[opponent].bench)

  if choose3 == 0:
    howToPutDamageCounters.append({ 'pokemonLocation': 'activePokemon', 'pokemonIndex': None })

    print(f'\nYour opponent chooses {game.players[opponent].activePokemon.name} to put the third damage counter (10 HP) on.')
  else:
    howToPutDamageCounters.append({ 'pokemonLocation': 'bench', 'pokemonIndex': choose3- 1 })

    print(f'\nYour opponent chooses {game.players[opponent].bench[choose1 - 1].name} to put the third damage counter (10 HP) on.')

  choose4 = aiChoose(game.players[opponent].bench)

  if choose4 == 0:
    howToPutDamageCounters.append({ 'pokemonLocation': 'activePokemon', 'pokemonIndex': None })

    print(f'\nYour opponent chooses {game.players[opponent].activePokemon.name} to put the fourth damage counter (10 HP) on.')
  else:
    howToPutDamageCounters.append({ 'pokemonLocation': 'bench', 'pokemonIndex': choose4 - 1 })

    print(f'\nYour opponent chooses {game.players[opponent].bench[choose1 - 1].name} to put the fourth damage counter (10 HP) on.')

  choose5 = aiChoose(game.players[opponent].bench)

  if choose5 == 0:
    howToPutDamageCounters.append({ 'pokemonLocation': 'activePokemon', 'pokemonIndex': None })

    print(f'\nYour opponent chooses {game.players[opponent].activePokemon.name} to put the fifth damage counter (10 HP) on.')
  else:
    howToPutDamageCounters.append({ 'pokemonLocation': 'bench', 'pokemonIndex': choose5 - 1 })

    print(f'\nYour opponent chooses {game.players[opponent].bench[choose1 - 1].name} to put the fifth damage counter (10 HP) on.')
    
  return game.players[player].activePokemon.moves['glisteningDroplets']['do'](game, player, opponent, howToPutDamageCounters)

def retreatChoose(energyAttached):
  count = 0
  energy = []

  if energyAttached[EnergyType.FusionStrikeEnergy] > 0:
    for i in range(energyAttached[EnergyType.FusionStrikeEnergy]):
      print(f'{count}   Fusion Strike Energy')
      energy.append(EnergyType.FusionStrikeEnergy)
      count += 1

  if energyAttached[EnergyType.DoubleTurboEnergy] > 0:
    for i in range(energyAttached[EnergyType.DoubleTurboEnergy]):
      print(f'{count}   Double Turbo Energy')
      energy.append(EnergyType.DoubleTurboEnergy)
      count += 1

  if energyAttached[EnergyType.Water] > 0:
    for i in range(energyAttached[EnergyType.Water]):
      print(f'{count}   Water Energy')
      energy.append(EnergyType.Water)
      count += 1

  choose = aiChoose(energy)

  print(f'Your opponent chooses to discard {energy[choose]} energy card.')

  return energy[choose]

def retreatPickABenchedPokemon(game, player):
  print('\nYour opponent must pick a benched Pokemon to replace their active Pokemon.')

  choose = aiChoose(game.players[player].bench)

  print(f'Your opponent chooses {game.players[player].bench[choose].name} to replace their active Pokemon.')

  return choose

def retreat(game, player, opponent):
  if game.players[player].activePokemon.retreatCost > 0:
    print(f'\nYour opponent needs to discard {game.players[player].activePokemon.retreatCost} energy card(s) from {game.players[player].activePokemon.name} in order to retreat.')
    
    energyToDiscard = []

    energyAttached = game.players[player].activePokemon.attachedEnergy

    for i in range(game.players[player].activePokemon.retreatCost):
      chosenEnergy = retreatChoose(energyAttached)

      energyToDiscard.append(chosenEnergy)

      energyAttached[chosenEnergy] -= 1

    newPokemonIndex = retreatPickABenchedPokemon(game, player)

    return game.retreat(player, newPokemonIndex, energyToDiscard)

def playBasicPokemonToBench(game, player, opponent):
  if len(game.players[player].bench) < 5: 
    basicPokemon = []
    basicPokemonIndexes = []

    for index, card in enumerate(game.players[player].hand):
      if card.cardType == CardType.Pokemon and card.stage == Stage.Basic:
        basicPokemon.add(card)
        basicPokemonIndexes.add(index)

    choose = aiChoose(basicPokemon)

    print(f'Your opponent chooses to play {basicPokemon[choose].name} to their bench.')

    game.players[player].bench.append(basicPokemon[choose])
    game.players[player].hand.pop(basicPokemonIndexes[choose])

    return game

  raise Exception('bench is already full')

def choosePokemonToEvolveFrom(game, player, canEvolveFrom, evolutionPokemonHandIndex, evolvedPokemonName):
  choose = aiChoose(canEvolveFrom)

  print(f'Your opponent chooses to evolve {canEvolveFrom[choose]["name"]} into {evolvedPokemonName}.')

  game.evolve(player, canEvolveFrom[choose]['pokemonLocation'], canEvolveFrom[choose]['pokemonIndex'], 
                evolutionPokemonHandIndex)
  return game

def evolvePokemon(game, player, opponent):
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
  
  choose = aiChoose(evolutionPokemonHand)

  canEvolveFrom = []

  for pokemon in evolutionPokemonHand[choose].evolvesFrom:
    if game.players[player].activePokemon.name == pokemon.name:
      canEvolveFrom.append({ 'name': pokemon.name, 'pokemonLocation': 'activePokemon', 'pokemonIndex': None })

    for index, benchPokemon in enumerate(game.players[player].bench):
      if benchPokemon.name == pokemon.name:
        canEvolveFrom.append({ 'name': pokemon.name, 'pokemonLocation': 'bench', 'pokemonIndex': index})

  if len(canEvolveFrom) == 1:
    if canEvolveFrom[0]['pokemonLocation'] == 'activePokemon':
      print(f'Your opponent evolves {game.players[player].activePokemon.name} into {evolutionPokemonHand[choose].name}.')
    else:
      print(f'Your opponent evolves {game.players[player].bench[canEvolveFrom[0]["pokemonIndex"]].name} into {evolutionPokemonHand[choose].name}.')

    game.evolve(player, canEvolveFrom[0]['pokemonLocation'], canEvolveFrom[0]['pokeonIndex'], 
                evolutionPokemonHandIndexes[choose])
    
    return game
  else:
    return choosePokemonToEvolveFrom(game, player, canEvolveFrom, evolutionPokemonHandIndexes[choose], 
                                     evolutionPokemonHand[choose].name)

def battleVipPassSecondPokemon(game, player, firstPokemonIndex):
  chooseYesNo = aiChoose(['no', 'yes'])

  if not chooseYesNo:
    print('Your opponent chooses not to pick a second Basic Pokemon from their deck.')

    return None
  
  basicPokemon = []
  basicPokemonIndexes = []

  for index, card in enumerate(game.players[player].deck):
    if card.cardType == CardType.Pokemon and card.stage == Stage.Basic:
      basicPokemon.append(card)
      basicPokemonIndexes.append(index)

  basicPokemon.pop(firstPokemonIndex)
  basicPokemonIndexes.pop(firstPokemonIndex)

  choose = aiChoose(basicPokemon)

  print(f'Your opponent chooses {basicPokemon[choose].name} from their deck to put on their bench.')

  return basicPokemonIndexes[choose]

def cramomaticHeads(game, player):
  print('\nYour opponent\'s coin flip landed on heads.')

  print('\nYour opponent picks a card from their deck to put into their hand.')

  choose = aiChoose(game.players[player].deck)

  return choose

def ultraBallPickPokemon(game, player):
  print('\nYour opponent picks a Pokemon from their deck to put into their hand.')

  pokemon = []
  pokemonIndexes = []

  for index, card in enumerate(game.players[player].deck):
    if card.cardType == CardType.Pokemon:
      pokemon.append(card)
      pokemonIndexes.append(index)

  if len(pokemon) == 0:
    print('There are no Pokemon in your opponent\'s deck. Ultra Ball ends.')

    return None

  choose = aiChoose(pokemon)

  print(f'Your opponent chooses {pokemon[choose].name} from their deck to put into their hand.')

  return pokemonIndexes[choose]


def ultraBallDiscardSecondCard(game, player, hand):
  print('\nYour opponent picks a second card from their hand to discard.')

  choose = aiChoose(hand)

  discardCard2Index = choose

  return discardCard2Index, ultraBallPickPokemon(game, player)

def lostVacuumPickCard(game, player, opponent):
  print('\nYour opponent picks a Tool or Stadium in play to put into the Lost Zone.')

  count = 0
  cardInfo = []

  if game.players[player].stadium != None:
    cardInfo.append({ 'lostZoneCardOwner': player, 'lostZoneCardStadium': True})
  elif game.players[opponent].stadium != None:
    cardInfo.append({ 'lostZoneCardOwner': opponent, 'lostZoneCardStadium': True})

  if game.players[opponent].activePokemon.tool != None:
    cardInfo.append({ 'lostZoneCardOwner': opponent, 'lostZoneCardStadium': False, 'lostZoneCardLocation': 'activePokemon' })

  for index, pokemon in enumerate(game.players[opponent].bench):
    if pokemon.tool != None:
      cardInfo.append({ 'lostZoneCardOwner': opponent, 'lostZoneCardStadium': False, 
                       'lostZoneCardLocation': 'bench', 'lostZoneCardIndex': index })

  if game.players[player].activePokemon.tool != None:
    cardInfo.append({ 'lostZoneCardOwner': player, 'lostZoneCardStadium': False, 'lostZoneCardLocation': 'activePokemon' })

  for index, pokemon in enumerate(game.players[player].bench):
    if pokemon.tool != None:
      cardInfo.append({ 'lostZoneCardOwner': player, 'lostZoneCardStadium': False, 
                       'lostZoneCardLocation': 'bench', 'lostZoneCardIndex': index })
      
  choose = aiChoose(cardInfo)

  if cardInfo[choose]['lostZoneCardStadium']:
    print(f'Your opponent chooses to put the Stadium card in play {game.players[cardInfo[choose]['lostZoneCardOwner']].stadium.name} into the Lost Zone.')
  else:
    if cardInfo[choose]['lostZoneCardLocation'] == 'activePokemon':
      print(f'Your opponent chooses to put the Tool card attached to {game.players[cardInfo[choose]['lostZoneCardOwner']].activePokemon.name} into the Lost Zone.')
    else:
      print(f'Your opponent chooses to put the Tool card attached to {game.players[cardInfo[choose]['lostZoneCardOwner']].bench[cardInfo[choose]['lostZoneCardIndex']].name} into the Lost Zone.')

  return cardInfo[choose]

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
  chooseYesNo = aiChoose(['no', 'yes'])

  if not chooseYesNo:
    print('Your opponent chooses not to put a second Supporter card into their hand.')

    return None

  print('\nYour opponent picks a second Supporter card from their discard pile to put into their hand.')

  choose = aiChoose(supporterCards)

  print(f'Your opponent chooses {supporterCards[choose].name} to put into their hand.')

  return choose

def determineItemEffectParams(game, player, opponent, item):
  if item.name == 'Battle VIP Pass':
    basicPokemon = []
    basicPokemonIndexes = []

    for index, card in enumerate(game.players[player].deck):
      if card.cardType == CardType.Pokemon and card.stage == Stage.Basic:
        basicPokemon.append(card)
        basicPokemonIndexes.append(index)

    if len(basicPokemon) == 0:
      print('There are no Basic Pokemon in your opponent\'s deck. Battle VIP Pass ends.')

      return { 'pokemon1Index': None, 'pokemon2Index': None }

    print('\nYour opponent picks a Basic Pokemon from their deck.')

    choose = aiChoose(basicPokemon)

    print(f'Your opponent chooses {basicPokemon[choose].name} from their deck to put on their bench.')

    pokemon1Index = basicPokemonIndexes[choose]

    if len(game.players[player].bench) == 5 or len(basicPokemon) == 1:
      return game

    pokemon2Index = battleVipPassSecondPokemon(game, player, choose)

    return { 'pokemon1Index': pokemon1Index, 'pokemon2Index': pokemon2Index }

  elif item.name == 'Cram-O-Matic':
    print('\nYour opponent picks an item to discard from their hand.')

    itemCards = []
    itemCardIndexes = []

    for index, card in enumerate(game.players[player].hand):
      if card.cardType == CardType.Item:
        itemCards.append(card)
        itemCardIndexes.append(index)

    choose = aiChoose(itemCards)

    print(f'Your opponent chooses to discard {itemCards[choose].name} from their hand.')

    discardItemIndex = itemCardIndexes[choose]

    coinFlip = random.randint(0, 1)

    if coinFlip:
      return { 'discardItemIndex': discardItemIndex, 'heads': True, 'deckCardIndex': cramomaticHeads(game, player) }
    
    return { 'discardItemIndex': discardItemIndex, 'heads': False } 
    
  elif item.name == 'Power Tablet':
    return { }
  
  elif item.name == 'Ultra Ball':
    # TODO reveal the card for later ML needs

    print('\nYour opponent picks the first card from their hand to discard.')

    hand = game.players[player].hand

    choose = aiChoose(hand)

    discardCard1Index = choose

    hand.pop(discardCard1Index)

    discardCard2Index, pokemonDeckIndex = ultraBallDiscardSecondCard(game, player, hand)

    return { 'discardCard1Index': discardCard1Index, 'discardCard2Index': discardCard2Index, 'pokemonDeckIndex': pokemonDeckIndex }

  elif item.name == 'Lost Vacuum':
    print('\nYour opponent picks a card from their hand to put into the Lost zone.')

    choose = aiChoose(game.players[player].hand)

    print(f'Your opponent chooses to put {game.players[player].hand[choose].name} from their hand into the Lost Zone.')

    entryFeeLostZoneCardIndex = choose

    cardInfo = lostVacuumPickCard(game, player, opponent)

    cardInfo['entryFeeLostZoneCardIndex'] = entryFeeLostZoneCardIndex

    return cardInfo

  elif item.name == 'Nest Ball':
    print('\nYour opponent picks a Basic Pokemon from their deck to put onto their Bench.')

    basicPokemon = []
    basicPokemonIndexes = []

    for index, card in enumerate(game.players[player].deck):
      if card.cardType == CardType.Pokemon and card.stage == Stage.Basic:
        basicPokemon.append(card)
        basicPokemonIndexes.append(index)

    if len(basicPokemon) == 0:
      print('There are no Basic Pokemon in your oppoent\'s deck. Nest Ball ends.')

      return { 'pokemonDeckIndex': None }

    choose = aiChoose(basicPokemon)

    print(f'Your opponent chooses {basicPokemon[choose].name} from their deck to put onto their Bench.')

    return { 'pokemonDeckIndex': basicPokemonIndexes[choose] }

  elif item.name == 'Switch Cart':
    print('\nYour opponent picks a Pokemon from their Bench to switch with their Active Pokemon.')

    choose = aiChoose(game.players[player].bench)

    print(f'Your opponent chooses to switch {game.players[player].bench[choose].name} with their Active Pokemon.')

    return { 'benchPokemonIndex': choose }

  elif item.name == 'Escape Rope':
    opponentChosenIndex = None

    if len(game.players[opponent].bench) == 0:
      print('\nYou have no benched Pokemon. Your Active Pokemon will stay in the Active Pokemon spot.')

      playerPokemonIndex = None
    else:
      playerPokemonIndex = escapeRopePlayerChoose(game, player, opponent, opponentChosenIndex)

    if len(game.players[player].bench) == 0:
      print('\nYour opponent has no benched Pokemon. Their Active Pokemon will stay in the Active Pokemon spot. Escape Rope ends.')

      return { 'playerBenchIndex': playerPokemonIndex, 'opponentBenchIndex': None }
    else:
      opponentChosenIndex = naiveAiChoose(game.players[opponent].bench)

      print(f'\nYour opponent has chosen to put out {game.players[opponent].bench[opponentChosenIndex].name}.')

      return { 'playerBenchIndex': playerPokemonIndex, 'opponentBenchIndex': opponentChosenIndex }
        
  elif item.name == 'Pal Pad':
    print('\nYour opponent picks first Supporter card from your discard pile to shuffle into their deck.')

    supporterCards = []
    supporterCardIndexes = []

    for index, card in enumerate(game.players[player].discardPile):
      if card.cardType == CardType.Supporter:
        supporterCards.append(card)
        supporterCardIndexes.append(index)

    choose = aiChoose(supporterCards)

    print(f'Your opponent chooses {supporterCards[choose].name} from their discard pile to shuffle into their deck.')

    firstChosenIndex = supporterCardIndexes[choose]

    supporterCards.pop(choose)
    supporterCardIndexes.pop(choose)

    if len(supporterCards) == 0:
      print('There are no more Supporter cards in your opponent\'s discard pile. Pal Pad ends.')

      return { 'firstChosenIndex': firstChosenIndex }
    else:
      secondChosenIndex = palPadSecondSupporter(game, player, supporterCards)

      if secondChosenIndex == None:
        return { 'firstChosenIndex': firstChosenIndex }

      return { 'firstChosenIndex': firstChosenIndex, 'secondChosenIndex': supporterCardIndexes[secondChosenIndex] }

  else:
    raise Exception('item not found')

def playItem(game, player, opponent):
  itemCards = []
  itemCardIndexes = []

  for index, card in enumerate(game.players[player].hand):
    if card.cardType == CardType.Item and card.canplay(game, player, opponent):
      itemCards.append(card)
      itemCardIndexes.append(index)
    
  choose = aiChoose(itemCards)

  print(f'Your opponent plays Item {itemCards[choose].name}.')

  game.playItem(player, itemCardIndexes[choose], determineItemEffectParams(game, player, opponent, itemCards[choose]))

  return game

def playStadium(game, player, opponent):
  stadiumCards = []
  stadiumCardIndexes = []

  for index, card in enumerate(game.players[player].hand):
    if card.cardType == CardType.Stadium:
      stadiumCards.append(card)
      stadiumCardIndexes.append(index)
    
  choose = aiChoose(stadiumCards)

  print(f'Your opponent plays Stadium {stadiumCards[choose].name}.')

  game.playStadium(player, stadiumCardIndexes[choose])

  return game

def playToolWhichPokemon(game, player):
  pokemon = []

  pokemon.append(game.players[player].activePokemon)

  for benchPokemon in game.players[player].bench:
    pokemon.append(benchPokemon)

  choose = aiChoose(pokemon)

  return choose

def playTool(game, player, opponent):
  toolCards = []
  toolCardIndexes = []

  for index, card in enumerate(game.players[player].hand):
    if card.cardType == CardType.Tool:
      toolCards.append(card)
      toolCardIndexes.append(index)
    
  choose = aiChoose(toolCards)

  pokemonChoice = playToolWhichPokemon(game, player)

  if pokemonChoice == 0:
    print(f'Your opponent plays Tool {toolCards[choose].name} on their Active Pokemon {game.players[player].activePokemon.name}.')

    game.playTool(player, toolCardIndexes[choose], 'activePokemon')
  else:
    print(f'Your opponent plays Tool {toolCards[choose].name} on their benched Pokemon {game.players[player].bench[pokemonChoice - 1].name}.')

    game.playTool(player, toolCardIndexes[choose], 'bench', pokemonChoice - 1)

  return game

def elesasSparkleChooseSecondPokemon(game, player, fusionStrikePokemon, fusionStrikePokemonLocations):
  chooseYesNo = aiChoose(['no', 'yes'])

  if not chooseYesNo:
    print('Your opponent chooses not to pick a second Fusion Strike Pokemon to attach a Fusion Strike Energy from their deck to.')

    return None, None

  choose = aiChoose(fusionStrikePokemon)

  if choose == 0:
    pokemon2Location = 'activePokemon'
    pokemon2Index = None
  else:
    pokemon2Location = 'bench'
    pokemon2Index = choose - 1

  return pokemon2Location, pokemon2Index

def determineSupporterEffectParams(game, player, opponent, supporter):
  if supporter.name == 'Boss\'s Orders (Ghetsis)':
    print('\nYour opponent picks a Pokemon from your Bench to switch with your Active Pokemon.')

    choose = aiChoose(game.players[opponent].bench)

    print(f'Your opponent chooses to switch {game.players[opponent].bench[choose].name} with your Active Pokemon.')

    return { 'opponent': opponent, 'benchPokemonIndex': choose }

  elif supporter.name == 'Elesa\'s Sparkle':
    print('\nYour opponent chooses a Fusion Strike Pokemon to attach a Fusion Strike Energy card from their deck to (if they have one upon searching.)')

    fusionStrikePokemon = []
    fusionStrikePokemonLocations = []

    if game.players[player].activePokemon.fusionStrike:
      fusionStrikePokemon.append(game.players[player].activePokemon)
      fusionStrikePokemonLocations.append({ 'location': 'activePokemon', 'index': None })

    for index, pokemon in enumerate(game.players[player].bench):
      if pokemon.fusionStrike:
        fusionStrikePokemon.append(pokemon)
        fusionStrikePokemonLocations.append({ 'location': 'bench', 'index': index })

    choose = aiChoose(fusionStrikePokemon)

    if choose == 0:
      pokemon1Location = 'activePokemon'
      pokemon1Index = None
    else:
      pokemon1Location = 'bench'
      pokemon1Index = choose - 1

    fusionStrikePokemon.pop(choose)
    fusionStrikePokemonLocations.pop(choose)

    pokemon2Location, pokemon2Index = elesasSparkleChooseSecondPokemon(game, player, fusionStrikePokemon, fusionStrikePokemonLocations)

    return { 'pokemon1Location': pokemon1Location, 'pokemon1Index': pokemon1Index, 'pokemon2Location': pokemon2Location, 'pokemon2Index': pokemon2Index }

  elif supporter.name == 'Iono' or supporter.name == 'Judge':
    return { 'opponent': opponent }

def playSupporter(game, player, opponent):
  supporterCards = []
  supporterCardIndexes = []

  for index, card in enumerate(game.players[player].hand):
    if card.cardType == CardType.Supporter:
      supporterCards.append(card)
      supporterCardIndexes.append(index)
    
  choose = aiChoose(supporterCards)

  print(f'Your opponent plays Supporter {supporterCards[choose].name}.')

  game.playSupporter(player, supporterCardIndexes[choose], determineSupporterEffectParams(game, player, opponent, supporterCards[choose].name))

  return game

def attachEnergyPickPokemon(game, player):
  pokemon = []

  pokemon.append(game.players[player].activePokemon)

  for benchPokemon in game.players[player].bench:
    pokemon.append(benchPokemon)

  choose = aiChoose(pokemon)

  if choose == 0:
    return 'activePokemon', None
  else:
    return 'bench', choose - 1

def attachEnergy(game, player):
  energyCards = []
  energyCardIndexes = []

  for index, card in enumerate(game.players[player].hand):
    if card.cardType == CardType.Energy:
      energyCards.append(card)
      energyCardIndexes.append(index)

  choose = aiChoose(energyCards)

  pokemonLocation, pokemonIndex = attachEnergyPickPokemon(game, player)

  if pokemonLocation == 'activePokemon':
    print(f'Your opponent attaches {energyCards[choose].name} to their Active Pokemon {game.players[player].activePokemon.name}.')
  else:
    print(f'Your opponent attaches {energyCards[choose].name} to their benched Pokemon {game.players[player].bench[pokemonIndex].name}.')

  game.attachEnergy(player, energyCardIndexes[choose], pokemonLocation, pokemonIndex)

  return game

def determineStadiumEffectParams(game, player, opponent, stadium):
  if stadium.name == 'Crystal Cave':
    return None

def useStadiumEffect(game, player, opponent):
  if not game.players[player].stadium == None:
    print(f'Your opponent uses Stadium {game.players[player].stadium.name}\'s effect.')
  else:
    print(f'Your opponent uses Stadium {game.players[opponent].stadium.name}\'s effect.')

  effectParams = determineStadiumEffectParams(game, player, opponent, game.players[player].stadium)

  game.useStadiumEffect(player, opponent, effectParams)

  return game

def determineToolEffectParams(game, player, opponent, tool):
  if tool.name == 'Forest Seal Stone':
    choose = aiChoose(game.players[player].deck)

    print(f'Your opponent chooses to put {game.players[player].deck[choose].name} from their deck into their hand.')

    return { 'deckCardIndex': choose }
  
  else:
    raise Exception('invalid tool')

def useToolEffect(game, player, opponent):
  pokemonWithTools = []

  if game.players[player].activePokemon.tool != None:
    pokemonWithTools.append(game.players[player].activePokemon)

  for pokemon in game.players[player].bench:
    if pokemon.tool != None:
      pokemonWithTools.append(pokemon)

  choose = aiChoose(pokemonWithTools)

  if choose == 0:
    print(f'Your opponent uses the effect of the Tool {game.players[player].activePokemon.tool.name} attached to their Active Pokemon {game.players[player].activePokemon.name}.')
  else:
    print(f'Your opponent uses the effect of the Tool {game.players[player].bench[choose - 1].tool.name} attached to their benched Pokemon {game.players[player].bench[choose - 1].name}.')

  if choose == 0:
    effectParams = determineToolEffectParams(game, player, opponent, game.players[player].activePokemon.tool)

    game.useToolEffect(player, opponent, effectParams, 'activePokemon')
  else:
    effectParams = determineToolEffectParams(game, player, opponent, game.players[player].bench[choose - 1].tool)

    game.useToolEffect(player, opponent, effectParams, 'bench', choose - 1)

  return game

aiAttackTurnOptions = {
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