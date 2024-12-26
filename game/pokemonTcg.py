from game import Game
from enums import Stage

player2Name = 'SYLVIA'

print('Hi? I\'m {player2Name}. What\s your name?')

player1Name = input()

print('Hi {player1Name}! Want to play Pokemon cards?')

input()

print('Okay, let\'s start')

game = Game(player1Name, player2Name)

game = game.startGame()

if game.goesFirst == player1Name:
  print('You go first.')
else:
  print('I go first.')

# TODO logic for showing hand to opponent during a mulligan

if len(game[player1Name].hand > 7):
  extraCards = len(game[player1Name].hand) - 7

  print('You drew {extraCards} extra card(s) because of my mulligans')
elif len(game['SYLVIA'].hand > 7):
  extraCards = len(game['SYLVIA'].hand) - 7

  print('I drew {extraCards} extra card(s) because of your mulligans')

def printGameBoard(game):
  print('SYLVIA')
  player2PrizeAmt = len(game['SYLVIA'].prizes)
  print('Prizes: {player2PrizeAmt}')

def pickActivePokemon():
  print('Pick a Basic Pokemon from your hand to be your active Pokemon')

  availableBasicPokemon = []

  for card in game[player1Name].hand:
    if card.stage == Stage.Basic:
      availableBasicPokemon.append(card)

  for index, pokemon in enumerate(availableBasicPokemon):
    print('{index}   {pokemon.name}')

  print('Commands:')
  print('details \{x\}: card details')
  print('pick \{x\}: pick a card')

def printPokemon(pokemon):
  print('Card Type: Pokemon')
  print('Stage: {pokemon.stage}')
  print('Current HP: {pokemon.hp}')
  print('Max HP: {pokemon.stageHp}')
  print('Type: {pokemon.type}')
  