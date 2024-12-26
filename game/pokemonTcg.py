from game import Game
from enums import Stage, EnergyType, CardType

def printGameBoard(game):
  print('SYLVIA')
  player2PrizeAmt = len(game['SYLVIA'].prizes)
  print(f'Prizes: {player2PrizeAmt}')

def pickActivePokemon():
  print('Pick a Basic Pokemon from your hand to be your active Pokemon')
  availableBasicPokemon = []

  for card in game.players[player1Name].hand:
    print(card.name)
    if card.cardType == CardType.Pokemon and card.stage == Stage.Basic:
      availableBasicPokemon.append(card)

  for index, pokemon in enumerate(availableBasicPokemon):
    print(f'{index}   {pokemon.name}')

  print('Commands:')
  print('details {x}: card details')
  print('pick {x}: pick a card')

  text = input()
  
  text = text.split()

  if text[0] == 'details':
    printPokemon(availableBasicPokemon[int(text[1])])
    pickActivePokemon()
  elif text[0] == 'pick':
    # pick pokemon
    print('coming later')
  else:
    print('What?')

def printPokemon(pokemon):
  print(f'Name: {pokemon.name}')
  print('Card Type: Pokemon')
  print(f'Stage: {pokemon.stage}')
  if pokemon.evolvesFrom:
    print(f'Evolves From: {pokemon.evolvesFrom}')
  print(f'Current HP: {pokemon.hp}')
  print(f'Max HP: {pokemon.startHp}')
  print(f'Type: {pokemon.type}')
  if pokemon.weakness:
    print(f'Weakness: {pokemon.weakness} x{pokemon.weaknessFactor}')
  if pokemon.resistance:
    print(f'Resistance: {pokemon.resistance} -{pokemon.resistanceFactor}')
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

player2Name = 'SYLVIA'

print(f'Hi? I\'m {player2Name}. What\'s your name?')

player1Name = input()

print(f'Hi {player1Name}! Want to play Pokemon cards?')

input()

print('Okay, let\'s start')

game = Game(player1Name, player2Name)

game = game.startGame()

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

pickActivePokemon()