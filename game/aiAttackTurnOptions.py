from naiveAI import naiveAiChoose

aiChoose = naiveAiChoose

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

    moveIndex = benchedFusionStrikeIndexes[aiChoose(benchedFusionStrikeIndexes)]

    return crossFusionStrikeMoveChoices(game, player, opponent, benchedFusionStrikeMoves, benchedFusionStrikeIndexes, moveIndex)
  else:
    print('what?')
    return crossFusionStrike(game, player)

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