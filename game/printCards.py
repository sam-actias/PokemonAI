from enums import EnergyType

def printNonPokemonCard(card):
  # combine with print pokemon
  print(f'\nName: {card.name}')
  print(f'Card Type: {card.cardType}')
  print(f'Text: {card.text}')

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