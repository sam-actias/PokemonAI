from game import Game
from enums import Stage, EnergyType, CardType
from naiveAI import naiveAiChoose

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
  print(f'\n{game.player1Name}')
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

# def doTurn(game):
#   if (game.goesFirst == 'SYLVIA' and game.players['SYLVIA'].activeTurn == 
#       game.players[game.player1Name].activeTurn) or (game.goesFirst == game.player1Name and 
#       game.players['SYLVIA'].activeTurn < game.players[game.player1Name].activeTurn):
    

def determineTurnOptions(game, player):
  turnOptions = []

  for move in list(game.players[player].activePokemon.moves.keys()):
    if (game.energyForAttackCheck(game.players[player].activePokemon.attachedEnergy, game.players[player].activePokemon.moves[move]) 
            and move['canDo'](game, player)):
      turnOptions.append(move)

def pickActivePokemon(game):
  print('\nPick a Basic Pokemon from your hand to be your active Pokemon.\n')
  availableBasicPokemon = []
  availableBasicPokemonIndexes = []

  for index, card in enumerate(game.players[player1Name].hand):
    if card.cardType == CardType.Pokemon and card.stage == Stage.Basic:
      availableBasicPokemon.append(card)
      availableBasicPokemonIndexes.append(index)

  for index, pokemon in enumerate(availableBasicPokemon):
    print(f'{index}   {pokemon.name}')

  print('\nCommands:')
  print('details {x}: card details')
  print('pick {x}: pick a card\n')

  text = input()
  
  text = text.split()

  if text[0] == 'details':
    printPokemon(availableBasicPokemon[int(text[1])])
    pickActivePokemon(game)
  elif text[0] == 'pick':
    return availableBasicPokemonIndexes[int(text[1])]
  else:
    print('What?\n')
    pickActivePokemon(game)

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

def printPokemon(pokemon):
  print(f'\nName: {pokemon.name}')
  print('Card Type: Pokemon')
  print(f'Stage: {pokemon.stage.name}')
  if pokemon.evolvesFrom:
    print(f'Evolves From: {pokemon.evolvesFrom}')
  print(f'Current HP: {pokemon.hp}')
  print(f'Max HP: {pokemon.startHp}')
  print(f'Type: {pokemon.type.name}')
  if pokemon.weakness:
    print(f'Weakness: {pokemon.weakness.name} x{pokemon.weaknessFactor}')
  if pokemon.resistance:
    print(f'Resistance: {pokemon.resistance.name} -{pokemon.resistanceFactor}')
  print(f'Retreat Cost: {pokemon.retreatCost}')
  if pokemon.hasRuleBox:
    print('Rule Box: Yes')
  print(f'Prizes When Knocked Out: {pokemon.prizesWhenKnockedOut}')
  if pokemon.isV:
    print('V: yes')
  if pokemon.fusionStrike:
    print('Fusion Strike: Yes')
  if pokemon.ability:
    print(f'Ability Name: {pokemon.ability['name']}')
    print(f'Ability Text: {pokemon.ability['text']}')
  for moveKey in list(pokemon.moves.keys()):
    print(f'Move Name: {pokemon.moves[moveKey]['name']}')
    if pokemon.moves[moveKey]['energyRequirement'][EnergyType.Colorless]:
      print(f'Required Energy Colorless: {pokemon.moves[moveKey]['energyRequirement'][EnergyType.Colorless]}')
    if pokemon.moves[moveKey]['energyRequirement'][EnergyType.Psychic]:
      print(f'Required Energy Psychic: {pokemon.moves[moveKey]['energyRequirement'][EnergyType.Psychic]}')
    if pokemon.moves[moveKey]['energyRequirement'][EnergyType.Metal]:
      print(f'Required Energy Metal: {pokemon.moves[moveKey]['energyRequirement'][EnergyType.Metal]}')
    if pokemon.moves[moveKey]['energyRequirement'][EnergyType.Fire]:
      print(f'Required Energy Fire: {pokemon.moves[moveKey]['energyRequirement'][EnergyType.Fire]}')
    print(f'Move Text: {pokemon.moves[moveKey]['text']}')
  if pokemon.attachedEnergy[EnergyType.FusionStrikeEnergy]:
    print(f'Attached Energy Fusion Strike: {pokemon.attachedEnergy[EnergyType.FusionStrikeEnergy]}')
  if pokemon.attachedEnergy[EnergyType.DoubleTurboEnergy]:
    print(f'Attached Energy Double Turbo: {pokemon.attachedEnergy[EnergyType.DoubleTurboEnergy]}')
  if pokemon.attachedEnergy[EnergyType.Water]:
    print(f'Attached Energy Water: {pokemon.attachedEnergy[EnergyType.Water]}')
  if pokemon.tool:
    print(f'Tool Name: {pokemon.tool.name}')
    print(f'Tool Text: {pokemon.tool.text}')

player2Name = 'SYLVIA'

print(f'Hi? I\'m {player2Name}. What\'s your name?')

player1Name = input()

print(f'\nHi {player1Name}! Want to play Pokemon cards?')

input()

print('\nOkay, let\'s start')

game = Game(player1Name, player2Name)

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