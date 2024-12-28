def crossFusionStrike(game, player):
  benchedFusionStrikeIndexes = []
  benchedFusionStrikeMoves = []

  for index, pokemon in game.players[player].bench:
    if pokemon.fusionStrike == True:
      for move in list(pokemon.moves.keys()):
        if move['canDo'] == True:
          benchedFusionStrikeIndexes.append(index)
          benchedFusionStrikeMoves.append(move)

  print('Which move from a Fusion Strike Pokemon on your bench do you want to use?')

  for index in benchedFusionStrikeBenchIndexes:



turnOptions = {
  'crossFusionStrike': 
}