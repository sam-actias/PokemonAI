from game import Game
from enums import Stage, EnergyType, CardType
from naiveAI import naiveAiChoose
from humanAttackTurnOptions import humanAttackTurnOptions
from aiAttackTurnOptions import aiAttackTurnOptions
from printCards import printPokemon, printNonPokemonCard

def printGameBoard(game):
  print('\nSYLVIA')
  print(f'Prizes: {len(game.players['SYLVIA'].prizes)}')
  print(f'Can Use VSTAR Power: {game.players['SYLVIA'].canUseVstarPower}')
  print('BENCH POKEMON')
  if len(game.players['SYLVIA'].bench) == 0:
    print('none')
  for index, pokemon in enumerate(game.players['SYLVIA'].bench):
    print(f'{index + 1}   {pokemon.name}')
  print('ACTIVE POKEMON')
  print(f'0   {game.players['SYLVIA'].activePokemon.name}')
  print(f'\nYOU')
  print('ACTIVE POKEMON')
  print(f'{len(game.players['SYLVIA'].bench) + 1}   {game.players[game.player1Name].activePokemon.name}')
  print('BENCH POKEMON')
  if len(game.players[game.player1Name].bench) == 0:
    print('none')
  for index, pokemon in enumerate(game.players[game.player1Name].bench):
    print(f'{index + len(game.players['SYLVIA'].bench) + 1}   {pokemon.name}')
  print(f'Can Use VSTAR Power: {game.players[game.player1Name].canUseVstarPower}')
  print(f'Prizes: {len(game.players[game.player1Name].prizes)}')
  print('\nSTADIUM')
  if game.players['SYLVIA'].stadium:
    print(f'{game.players[game.player1Name].bench + len(game.players['SYLVIA'].bench) + 1}   {game.players['SYLVIA'].stadium.name}')
  elif game.players[game.player1Name].stadium:
    print(f'{game.players[game.player1Name].bench + len(game.players['SYLVIA'].bench) + 1}   {game.players[game.player1Name].stadium.name}')
  else:
    print('none')
  print('\nYOUR HAND')
  for index, card in enumerate(game.players[game.player1Name].hand):
    print(f'{len(game.players[game.player1Name].bench) + len(game.players['SYLVIA'].bench) + index + 2}   {card.name}')

def doTurnOptionsAi(game, player, opponent):
  turnOptions = determineTurnOptions(game, player, game.player2Name)

  turnOptions.append('endTurn')

  choose = naiveAiChoose(turnOptions)

  if not choose == 'endTurn':
    aiAttackTurnOptions[choose](game, player, opponent)

  if (choose == 'retreat' or choose == 'playBasicPokemonToBench' or choose == 'evolvePokemon' 
    or choose == 'playItem' or choose == 'playStadium' or choose == 'playTool' 
    or choose == 'playSupporter' or choose == 'attachEnergy' or choose == 'useStadiumEffect' 
    or choose == 'useToolEffect'):
    doTurnOptionsAi(game, player, opponent)

def gameBoardDetailOptions(game):
  gameBoardDetailOptions = []

  for pokemon in game.players['SYLVIA'].bench:
    gameBoardDetailOptions.append(pokemon)

  gameBoardDetailOptions.append(game.players['SYLVIA'].activePokemon)

  gameBoardDetailOptions.append(game.players[game.player1Name].activePokemon)

  for pokemon in game.players[game.player1Name].bench:
    gameBoardDetailOptions.append(pokemon)

  if game.players['SYLVIA'].stadium:
    gameBoardDetailOptions.append(game.players['SYLVIA'].stadium)
  elif game.players[game.player1Name].stadium:
    gameBoardDetailOptions.append(game.players[game.player1Name].stadium)

  for card in game.players[game.player1Name].hand:
    gameBoardDetailOptions.append(card)

def doTurnOptionsHuman(game, player, opponent):
  printGameBoard(game)

  turnOptions = determineTurnOptions(game, player, game.player1Name)

  turnOptions.append('endTurn')

  print('\nPick a turn action. An attack ends the turn.')

  for index, option in enumerate(turnOptions):
    print(f'{index}   {option}')

  print('\nCommands:')
  print('details {x}: card details')
  print('pick {x}: pick a turn action\n')

  text = input()

  text = text.split()

  if text[0] == 'details':
    gameBoardDetailOptions = gameBoardDetailOptions()

    if gameBoardDetailOptions[int(text[1])].cardType == CardType.Pokemon:
      printPokemon(gameBoardDetailOptions[int(text[1])])
    else:
      printNonPokemonCard(gameBoardDetailOptions[int(text[1])])
  elif text[0] == 'pick':
    choose = turnOptions[int(text[1])]

    if not choose == 'endTurn':
      humanAttackTurnOptions[choose](game, player, opponent)

    if (choose == 'retreat' or choose == 'playBasicPokemonToBench' or choose == 'evolvePokemon' 
      or choose == 'playItem' or choose == 'playStadium' or choose == 'playTool' 
      or choose == 'playSupporter' or choose == 'attachEnergy' or choose == 'useStadiumEffect' 
      or choose == 'useToolEffect'):
      doTurnOptionsHuman(game, player, opponent)

  if not choose == 'endTurn':
    humanAttackTurnOptions[choose](game, player, opponent)

  if (choose == 'retreat' or choose == 'playBasicPokemonToBench' or choose == 'evolvePokemon' 
    or choose == 'playItem' or choose == 'playStadium' or choose == 'playTool' 
    or choose == 'playSupporter' or choose == 'attachEnergy' or choose == 'useStadiumEffect' 
    or choose == 'useToolEffect'):
    doTurnOptionsHuman(game, player, opponent)

def doTurn(game):
  if (game.goesFirst == 'SYLVIA' and game.players['SYLVIA'].activeTurn == 
      game.players[game.player1Name].activeTurn) or (game.goesFirst == game.player1Name and 
      game.players['SYLVIA'].activeTurn < game.players[game.player1Name].activeTurn):
    print(f'\n{game.player2Name}\'s turn!')

    game.startTurn(game.player2Name)

    doTurnOptionsAi(game, game.player2Name, game.player1Name)

    game.endTurn(game.player2Name)
  else:
    print(f'\n{game.player1Name}\'s turn!')

    game.startTurn(game.player1Name)

    doTurnOptionsHuman(game, game.player1Name, game.player2Name)

    game.endTurn(game.player1Name)

def determineTurnOptions(game, player, opponent):
  turnOptions = []

  if len(game.players[player].bench) > 0:
    energyCount = 0

    energyCount += game.players[player].activePokemon.attachedEnergy[EnergyType.FusionStrikeEnergy]
    energyCount += game.players[player].activePokemon.attachedEnergy[EnergyType.DoubleTurboEnergy]
    energyCount += game.players[player].activePokemon.attachedEnergy[EnergyType.Water]

    if energyCount >= game.players[player].activePokemon.retreatCost:
      turnOptions.append('retreat')

  for card in game.players[player].hand:
    if card.cardType == CardType.Pokemon and card.stage == Stage.Basic and len(game.players[player].bench) < 5:
      turnOptions.append('playBasicPokemonToBench')
    elif card.cardType == CardType.Pokemon and len(card.evolvesFrom) > 0:
      for pokemon in card.evolvesFrom:
        if game.players[player].activePokemon.name == pokemon.name and game.players[player].activePokemon.canEvolve:
          turnOptions.append('evolvePokemon')
        
        for benchPokemon in game.players[player].bench:
          if pokemon.name == benchPokemon.name and benchPokemon.canEvolve:
            turnOptions.append('evolvePokemon')
    elif card.cardType == CardType.Item and card.canPlay(game, player, opponent):
      turnOptions.append('playItem')
    elif card.cardType == CardType.Stadium and game.players[player].canPlayStadiumFlag and card.canPlay(game, player, opponent):
      turnOptions.append('playStadium')
    elif card.cardType == CardType.Tool and card.canPlay(game, player, opponent):
      turnOptions.append('playTool')
    elif card.cardType == CardType.Supporter and game.players[player].canUseSupporterFlag and card.canPlay(game, player, opponent):
      turnOptions.append('playSupporter')
    elif card.cardType == CardType.Energy and game.players[player].canAttachEnergy and card.canPlay(game, player, opponent):
      turnOptions.append('attachEnergy')

    if game.players[player].stadium and game.players[player].stadium.canUseEffect(game, player, opponent):
      turnOptions.append('useStadiumEffect')
    elif game.players[opponent].stadium and game.players[opponent].stadium.canUseEffect(game, player, opponent):
      turnOptions.append('useStadiumEffect')

    if game.players[player].activePokemon.tool and game.players[player].activePokemon.tool.canUseAbility(game, player, opponent):
      turnOptions.append('useToolAbility')

    for pokemon in game.players[player].bench:
      if pokemon.tool and pokemon.tool.canUseAbility(game, player, opponent):
        turnOptions.append('useToolAbility')

    for move in list(game.players[player].activePokemon.moves.keys()):
      if (game.energyForAttackCheck(game.players[player].activePokemon.attachedEnergy, game.players[player].activePokemon.moves[move]['energyRequirement']) 
              and move['canDo'](game, player)):
        turnOptions.append(move)

  uniqueTurnOptions = list(set(turnOptions))

  return uniqueTurnOptions

def pickActivePokemon(game):
  print('\nPick a Basic Pokemon from your hand to be your active Pokemon.\n')
  availableBasicPokemon = []
  availableBasicPokemonIndexes = []

  print(game.players[player1Name].hand)

  for index, card in enumerate(game.players[player1Name].hand):
    if card.cardType == CardType.Pokemon and card.stage == Stage.Basic:
      availableBasicPokemon.append(card)
      availableBasicPokemonIndexes.append(index)

  print(availableBasicPokemon)

  for index, pokemon in enumerate(availableBasicPokemon):
    print(f'{index}   {pokemon.name}')

  print('\nCommands:')
  print('details {x}: card details')
  print('pick {x}: pick a card\n')

  text = input()
  
  text = text.split()

  if text[0] == 'details':
    printPokemon(availableBasicPokemon[int(text[1])])
    return pickActivePokemon(game)
  elif text[0] == 'pick':
    return availableBasicPokemonIndexes[int(text[1])]
  else:
    print('What?\n')
    return pickActivePokemon(game)

def pickBenchPokemon(game):
  availableBasicPokemon = []
  availableBasicPokemonIndexes = []

  availableBasicPokemon.append(None)
  availableBasicPokemonIndexes.append(None)

  for index, card in enumerate(game.players[player1Name].hand):
    if card.cardType == CardType.Pokemon and card.stage == Stage.Basic:
      availableBasicPokemon.append(card)
      availableBasicPokemonIndexes.append(index)

  if len(availableBasicPokemon) == 1:
    return None

  print('\nPick a Basic Pokemon from your hand to be on your bench (up to 5 Pokemon).\n')

  for index, pokemon in enumerate(availableBasicPokemon):
    if index == 0:
        print('0   DONE')
    else:
      print(f'{index}   {pokemon.name}')


  print('\nCommands:')
  print('details {x}: card details')
  print('pick {x}: pick a card\n')

  text = input()
  
  text = text.split()

  if text[0] == 'details':
    if int(text[1]) == 0:
      print('What?\n')
      pickBenchPokemon(game)
    printPokemon(availableBasicPokemon[int(text[1])])
    pickBenchPokemon(game)
  elif text[0] == 'pick':
    if int(text[1]) == 0:
      return None
    return availableBasicPokemonIndexes[int(text[1])]
  else:
    print('What?\n')
    pickBenchPokemon(game)

player2Name = 'SYLVIA'

print(f'Hi? I\'m {player2Name}. What\'s your name?')

player1Name = input()

print(f'\nHi {player1Name}! Want to play Pokemon cards?')

input()

print('\nOkay, let\'s start')

game = Game(player1Name, False, player2Name, True)

game.startGame()

if game.goesFirst == player1Name:
  print('You go first.')
else:
  print('I go first.')

# TODO logic for showing hand to opponent during a mulligan

if len(game.players[player1Name].hand) > 7:
  extraCards = len(game.players[player1Name].hand) - 7

  print(f'You drew {extraCards} extra card(s) because of my mulligans')
elif len(game.players['SYLVIA'].hand) > 7:
  extraCards = len(game.players['SYLVIA'].hand) - 7

  print(f'I drew {extraCards} extra card(s) because of your mulligans')

availableBasicPokemon = []
availableBasicPokemonIndexes = []

for index, card in enumerate(game.players['SYLVIA'].hand):
  if card.cardType == CardType.Pokemon and card.stage == Stage.Basic:
    availableBasicPokemon.append(card)
    availableBasicPokemonIndexes.append(index)

if len(availableBasicPokemon) == 1:
  chosenActivePokemonIndex = 0
else:
  chosenActivePokemonIndex = naiveAiChoose(availableBasicPokemon)

game.players['SYLVIA'].activePokemon = game.players['SYLVIA'].hand.pop(availableBasicPokemonIndexes[chosenActivePokemonIndex])

for i in range(5):
  if game.players['SYLVIA'].hand[5 - i].cardType == CardType.Pokemon and game.players['SYLVIA'].hand[5 - i].stage == Stage.Basic:
    choose = naiveAiChoose([False, True])
    if choose:
      game.players['SYLVIA'].bench.append(game.players['SYLVIA'].hand.pop(5 - i))

game.players[player1Name].activePokemon = game.players[player1Name].hand.pop(pickActivePokemon(game))

for i in range(5):
  pickedPokemonIndex = pickBenchPokemon(game)
  if pickedPokemonIndex == None:
    break
  game.players[player1Name].bench.append(game.players[player1Name].hand.pop(pickedPokemonIndex))

printGameBoard(game)

while game.winner == None:
  doTurn(game)

if game.winner == game.player1Name:
  print(f'\nCongratulations {player1Name}! You won!')
elif game.winner == game.player2Name:
  print(f'\nI won! Better luck next time {player1Name}!')
elif game.winner == 'tie':
  print('It\'s a tie!')
else:
  raise Exception('invalid win state!')
