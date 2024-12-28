from enums import CardType

def crossFusionStrikeMoveChoices(game, player, opponent, benchedFusionStrikeMoves, benchedFusionStrikeIndexes):
  moveIndex = int(text[1])

  if benchedFusionStrikeMoves[moveIndex].name == 'maxMiracle':
    return game.players[player].activePokemon.moves[benchedFusionStrikeMoves[moveIndex]]['do'](game, player, 
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
    print('choose {x}: choose an energy card\n')

    text = input()

    text = text.split()

    if text[0] == 'choose':
      energyCardIndex = int(text[1])

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
      print('choose {x}: choose a Pokemon\n')

      text = input()

      text = text.split()

      if text[0] ==  'choose':
        return game.players[player].activePokemon.moves[benchedFusionStrikeMoves[moveIndex]]['do'](game, player, 
          benchedFusionStrikeIndexes[moveIndex], benchedFusionStrikeMoves[moveIndex].name, { 'game': game, 'player': player, 
          'deckIndex': energyCardIndexes[energyCardIndex], 'pokemonLocation': fusionStrikePokemon[int(text[1])]['pokemonLocation'], 
          'pokemonIndex': fusionStrikePokemon[int(text[1])]['pokemonIndex'] })
      else:
        print('what?')
        crossFusionStrikeMoveChoices(game, player, opponent, benchedFusionStrikeMoves, benchedFusionStrikeIndexes)
    else:
      print('what?')
      crossFusionStrikeMoveChoices(game, player, opponent, benchedFusionStrikeMoves, benchedFusionStrikeIndexes)

    # add other Fusion Strike moves
      

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
    crossFusionStrikeMoveChoices(game, player, opponent, benchedFusionStrikeMoves, benchedFusionStrikeIndexes)
  else:
    print('what?')
    crossFusionStrike(game, player)

turnOptions = {
  'crossFusionStrike': crossFusionStrike
}