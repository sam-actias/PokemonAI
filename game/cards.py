from enums import EnergyType, CardType, Stage

class MewVmaxFS268:
  def __init__(self):
    self.cardType = CardType.Pokemon
    self.name = 'MewVmaxFS268'
    self.stage = Stage.Vmax
    self.hp = 310
    self.startHp = 310
    self.type = EnergyType.Psychic
    self.weakness = EnergyType.Darkness
    self.weaknessFactor = 2
    self.resistance = EnergyType.Fighting
    self.resistanceFactor = 30
    self.retreatCost = 0
    self.hasRuleBox = True
    self.prizesWhenKnockedOut = 3
    self.evolvesFrom = 'MewVFS250'
    self.fusionStrike = True
    self.isV = True
    self.moves = {
      'crossFusionStrike': {
        'do': self.crossFusionStrike,
        'energyRequirement': {
          EnergyType.Colorless: 2
        },
        'text': 'Choose 1 of your Benched Fusion Strike Pokémon\'s attacks and use it as this attack.'
      },
      'maxMiracle': {
        'do': self.maxMiracle,
        'energyRequirement': {
          EnergyType.Psychic: 2
        },
        'text': 'This attack\'s damage isn\'t affected by any effects on your opponent\'s Active Pokémon.'
      }
    }
    self.attachedEnergy = {
      EnergyType.FusionStrikeEnergy: 0,
      EnergyType.DoubleTurboEnergy: 0,
      EnergyType.Water: 0
    }

  def crossFusionStrike(self, game, player, benchedPokemonIndex, moveIndex, moveInput):
    if not game.energyForAttackCheck(game[player].activePokemon.attachedEnergy, self.moves['crossFusionStrike']['energyRequirement']):
      raise Exception('Not enough energy for move Cross Fusion Strike')

    return game[player].bench[benchedPokemonIndex].moves[moveIndex].do(**moveInput)
  
  def maxMiracle(self, game, player, opponent):
    if not game.energyForAttackCheck(game[player].activePokemon.attachedEnergy, self.moves['maxMiracle']['energyRequirement']):
      raise Exception('Not enough energy for move Max Miracle')

    # no damage effects on this attack from effects on opponent's active Pokemon

    game[opponent].activePokemon.hp -= game.activePokemonAttackChecks(player, opponent, 130, True)

    return game
  
class MewVFS250:
  def __init__(self):
    self.cardType = CardType.Energy
    self.name = 'MewVFS250'
    self.stage = Stage.Basic
    self.hp = 180
    self.startHp = 180
    self.type = EnergyType.Psychic
    self.weakness = EnergyType.Darkness
    self.weaknessFactor = 2
    self.resistance = EnergyType.Fighting
    self.resistanceFactor = 30
    self.retreatCost = 0
    self.hasRuleBox = True
    self.prizesWhenKnockedOut = 2
    self.fusionStrike = True
    self.isV = True
    self.moves = {
      'energyMix': {
        'do': self.energyMix,
        'energyRequirement': {
          EnergyType.Psychic: 1
        },
        'text': 'Search your deck for an Energy card and attach it to 1 of your Fusion Strike Pokémon. Then, shuffle your deck.'
      },
      'psychicLeap': {
        'name': 'Psychic Leap',
        'do': self.psychicLeap,
        'energyRequirement': {
          EnergyType.Psychic: 1,
          EnergyType.Colorless: 1
        },
        'text': 'You may shuffle this Pokémon and all attached cards into your deck.'
      }
    }
    self.attachedEnergy = {
      EnergyType.FusionStrikeEnergy: 0,
      EnergyType.DoubleTurboEnergy: 0,
      EnergyType.Water: 0
    }

  def energyMix(self, game, player, deckIndex, pokemonIndex):
    if not game.energyForAttackCheck(game[player].activePokemon.attachedEnergy, self.moves['energyMix']['energyRequirement']):
      raise Exception('Not enough energy for move Energy Mix')
    # provide an index for the energy card in the deck
    # provide a location and index (if needed) of the chosen Fusion Strike Pokemon

    card = game[player].deck.pop(deckIndex)

    if pokemonIndex < 6:
      if game[player].bench[pokemonIndex].fusionStrike:
        game[player].bench[pokemonIndex].attachedEnergy[card.energyType] += 1
      else:
        raise Exception('cannot use Mew V\'s Energy Mix on a non-Fusion Strike Pokemon')
    else:
      if game[player].activePokemon.fusionStrike:
        game[player].activePokemon.attachedEnergy[card.energyType] += 1
      else:
        raise Exception('cannot use Mew V\'s Energy Mix on a non-Fusion Strike Pokemon')
      
    return game
      
  def psychicLeap(self, game, player, opponent, shuffleIn, newActivePokemonIndex):
    if not game.energyForAttackCheck(game[player].activePokemon.attachedEnergy, self.moves['psychicLeap']['energyRequirement']):
      raise Exception('Not enough energy for move Psychic Leap')
    # provide a shuffleIn boolean

    game[opponent].activePokemon.hp -= game.activePokemonAttackChecks(player, opponent, 70)

    if (shuffleIn & newActivePokemonIndex):
      if len(game[player].bench) < 1:
        raise Exception('can\'t do move Psychic Leap if no Pokemon on bench')
      else:
        if game[player].activePokemon.tool:
          game[player].deck.append(game[player].activePokemon.tool)
        
        if len(game[player].activePokemon.attachedEnergy) > 0:
          for card in game[player].activePokemon.attachedEnergy:
            game[player].deck.append(card)

        game[player].activePokemon.tool = None

        game[player].activePokemon.hp = game[player].activePokemon.startHp

        game[player].activePokemon.attachedEnergy = []

        game[player].activePokemon.burned = False

        game[player].activePokemon.paralyzedCounter = 0

        game[player].activePokemon.poisoned = False

        game[player].activePokemon.asleep = False

        game[player].activePokemon.confused = False

        game[player].deck.append(game[player].activePokemon)

        game[player].deck = game.shuffle(game[player].deck)

        game[player].activePokemon = game[player].bench.pop(newActivePokemonIndex)
    elif ((shuffleIn and not newActivePokemonIndex) or (not shuffleIn and newActivePokemonIndex)):
      raise Exception('can\'t do move Psychic Leap without both shuffleIn and newActivePokemonIndex')
    
    return game
  
class GenesectVFS255:
  def __init__(self):
    self.cardType = CardType.Pokemon
    self.name = 'GenesectVFS255'
    self.stage = Stage.Basic
    self.hp = 190
    self.startHp = 190
    self.type = EnergyType.Metal
    self.weakness = EnergyType.Fire
    self.weaknessFactor = 2
    self.resistance = EnergyType.Grass
    self.resistanceFactor = 30
    self.retreatCost = 2
    self.hasRuleBox = True
    self.prizesWhenKnockedOut = 2
    self.fusionStrike = True
    self.isV = True
    self.ability = {
      'name': 'FusionStrikeSystem',
      'do': self.fusionStrikeSystem,
      'usedFlag': False,
      'text': 'Once during your turn, you may draw cards until you have as many cards in your hand as you have Fusion Strike Pokémon in play.'
    }
    self.moves = {
      'technoBlast': {
        'do': self.technoBlast,
        'EnergyRequirement': {
          EnergyType.Metal: 2,
          EnergyType.Colorless: 1
        },
        'text': 'During your next turn, this Pokémon can\'t attack.'
      }
    }
    self.attachedEnergy = {
      EnergyType.FusionStrikeEnergy: 0,
      EnergyType.DoubleTurboEnergy: 0,
      EnergyType.Water: 0
    }

  def fusionStrikeSystem(self, game, player):
    if (game[player].stadium == None and  game[player].stadium == None) or (game[player].stadium 
                          != 'PathToThePeakCR148' and game[player].stadium  != 'PathToThePeakCR148'):
      fusionStrikePokemonInPlay = 0

      if game[player].activePokemon.fusionStrike:
        fusionStrikePokemonInPlay += 1

      for pokemon in game[player].bench:
        if pokemon.fusionStrike:
          fusionStrikePokemonInPlay += 1

      if fusionStrikePokemonInPlay > len(game[player].hand):
        amtToDraw = fusionStrikePokemonInPlay - len(game[player].hand)

        for i in range(amtToDraw):
          game[player].hand.append(game[player].deck.pop())

      self.ability.usedFlag = True

      return game
    
    raise Exception("Cannot use ability Fusion Strike System while Path To The Peak is the stadium in play")
  
  def technoBlast(self, game, player, opponent):
    if not game.energyForAttackCheck(game[player].activePokemon.attachedEnergy, self.moves['technoBlast']['energyRequirement']):
      raise Exception('Not enough energy for move Techno Blast')
    
    if game[player].activePokemonCantAttack == 0:
      game[opponent].activePokemon.hp -= game.activePokemonAttackChecks(player, opponent, 210)

      game[player].activePokemonCantAttack = 2
    else:
      raise Exception('Genesect V cannot attack right now due to the rules of a move')
    
    return game
    
class MeloettaFS124:
  def __init__(self):
    self.cardType = CardType.Pokemon
    self.name = 'MeloettaFS124'
    self.stage = Stage.Basic
    self.hp = 90
    self.startHp = 90
    self.type = EnergyType.Psychic
    self.weakness = EnergyType.Darkness
    self.weaknessFactor = 2
    self.resistance = EnergyType.Fighting
    self.resistanceFactor = 30
    self.retreatCost = 1
    self.prizesWhenKnockedOut = 1
    self.fusionStrike = True
    self.moves = {
      'melodiouEcho': {
        'do': self.melodiousEcho,
        'EnergyRequirement': {
          EnergyType.Psychic: 1,
          EnergyType.Colorless: 1
        },
        'text': 'This attack does 70 damage for each Fusion Strike Energy attached to all of your Pokémon.'
      }
    }
    self.attachedEnergy = {
      EnergyType.FusionStrikeEnergy: 0,
      EnergyType.DoubleTurboEnergy: 0,
      EnergyType.Water: 0
    }

  def melodiousEcho(self, game, player, opponent):
    if not game.energyForAttackCheck(game[player].activePokemon.attachedEnergy, self.moves['melodiousBlast']['energyRequirement']):
      raise Exception('Not enough energy for move Melodious Blast')

    fusionStrikeEnergyAmt = 0

    fusionStrikeEnergyAmt += self.attachedEnergy[EnergyType.FusionStrikeEnergy]

    for pokemon in game[player].bench:
      fusionStrikeEnergyAmt += pokemon.attachedEnergy[EnergyType.FusionStrikeEnergy]

    game[opponent].activePokemon.hp -= game.activePokemonAttackChecks(player, opponent, 70 * fusionStrikeEnergyAmt)

    return game

class OricorioFS42:
  def __init__(self):
    self.cardType = CardType.Pokemon
    self.name = 'OricorioFS42'
    self.stage = Stage.Basic
    self.hp = 90
    self.startHp = 90
    self.type = EnergyType.Fire
    self.weakness = EnergyType.Water
    self.weaknessFactor = 2
    self.retreatCost = 1
    self.prizesWhenKnockedOut = 1
    self.fusionStrike = True
    self.ability = {
      'name': 'LessonInZeal',
      'text': 'All of your Fusion Strike Pokémon take 20 less damage from attacks from your opponent\'s Pokémon (after applying Weakness and Resistance). You can\'t apply more than 1 Lesson in Zeal Ability at a time.'
    }
    self.moves = {
      'glisteningDroplets': {
        'do': self.glisteningDroplets,
        'EnergyRequirement': {
          EnergyType.Fire: 1,
          EnergyType.Colorless: 1
        },
        'text': 'Put 5 damage counters on your opponent\'s Pokémon in any way you like.'
      }
    }
    self.attachedEnergy = {
      EnergyType.FusionStrikeEnergy: 0,
      EnergyType.DoubleTurboEnergy: 0,
      EnergyType.Water: 0
    }

  def glisteningDroplets(self, game, player, opponent, howToPutDamageCounters):
    if not game.energyForAttackCheck(game[player].activePokemon.attachedEnergy, self.moves['glisteningDroplets']['energyRequirement']):
      raise Exception('Not enough energy for move Glistening Droplets')
    
    # howToPutDamageCounters is a list containing dictionaries with keys pokemonLocation, pokemonIndex, and damageAmt

    howToDamageAmt = 0

    for howTo in howToPutDamageCounters:
      howToDamageAmt += howTo.damageAmt

      if howTo.pokemonLocation == "activePokemon":
        game[opponent][howTo.pokemonLocation].hp -= howTo.damageAmt
      else:
        game[opponent][howTo.pokemonLocation][howTo.pokemonIndex].hp -= howTo.damageAmt

    if not howToDamageAmt == 5:
      raise Exception('Damage amount for Glistening Droplets does not equal exactly 5')
    
    return game
  
class BosssOrdersGhetsisPE265:
  def __init__(self):
    self.cardType = CardType.Supporter
    self.name = 'BosssOrdersGhetsisPE265'
    self.text = 'Switch in 1 of your opponent\'s Benched Pokémon to the Active Spot.'

  def effect(self, game, player, opponent, benchedPokemonIndex):
    if game[player].canUseSupporter == True:
      if len(game[opponent].bench) > 0:
        pokemon = game[opponent].bench.pop(benchedPokemonIndex)

        game[opponent].activePokemon.burned = False

        game[opponent].activePokemon.paralyzedCounter = 0

        game[opponent].activePokemon.poisoned = False

        game[opponent].activePokemon.asleep = False

        game[opponent].activePokemon.confused = False

        game[opponent].bench.append(game[opponent].activePokemon)

        game[opponent].activePokemon = pokemon

      game[player].canUseSupporter = False

      return game
    
    raise Exception("Can't play Boss\'s Order Ghetsis if player has already played a Supporter card this turn")
  
class ElesasSparkleFS260:
  def __init__(self):
    self.cardType = CardType.Supporter
    self.name = 'ElesasSparkleFS260'
    self.text = 'Choose up to 2 of your Fusion Strike Pokémon. For each of those Pokémon, search your deck for a Fusion Strike Energy card and attach it to that Pokémon. Then, shuffle your deck.'

  def effect(self, game, player, pokemon1Location, pokemon1Index = None, pokemon2Location = None, pokemon2Index = None):
    if game[player].canUseSupporter == True:
      for index, card in enumerate(game[player].deck):
        if card.name == 'FusionStrikeEnergyFS244':
          if pokemon1Location == 'activePokemon':
            game[player].activePokemon.attachedEnergy[EnergyType.FusionStrikeEnergy] += 1
            game[player].deck.pop(index)
            break
          else:
            game[player].bench[pokemon1Index].attachedEnergy[EnergyType.FusionStrikeEnergy] += 1
            game[player].deck.pop(index)
            break
      
      if pokemon2Location:
        for index, card in enumerate(game[player].deck):
          if card.name == 'FusionStrikeEnergyFS244':
            if pokemon2Location == 'activePokemon':
              game[player].activePokemon.attachedEnergy[EnergyType.FusionStrikeEnergy] += 1
              game[player].deck.pop(index)
              break
            else:
              game[player].bench[pokemon2Index].attachedEnergy[EnergyType.FusionStrikeEnergy] += 1
              game[player].deck.pop(index)
              break

      game[player].deck = game.shuffle(game[player].deck)

      game[player].canUseSupporter = False

      return game
    
    raise Exception("Can't play Elesa\'s Sparkle if player has already played a Supporter card this turn")

class IonoPE269:
  def __init__(self):
    self.cardType = CardType.Supporter
    self.name = 'IonoPE269'
    self.text = 'Each player shuffles their hand and puts it on the bottom of their deck. If either player put any cards on the bottom of their deck in this way, each player draws a card for each of their remaining Prize cards.'

  def effect(self, game, player, opponent):
    if game[player].canUseSupporter == True:
      if len(game[player].hand) > 0:
        playerShuffledHand = game.shuffle(game[player].hand)

        game[player].deck = game.putCardsAtBottomOfDeck(playerShuffledHand, game[player].deck)

        for card in game[player].prizes:
          game[player].hand.append(game[player].deck.pop())

      if len(game[opponent].hand) > 0:
        opponentShuffledHand = game.shuffle(game[opponent].hand)

        game[opponent].deck = game.putCardsAtBottomOfDeck(opponentShuffledHand, game[opponent].deck)

        for card in game[opponent].prizes:
          game[opponent].hand.append(game[opponent].deck.pop())

      game[player].canUseSupporter = False

      return game
  
    raise Exception("Can't play Iono if player has already played a Supporter card this turn")  

class JudgeSAV176:
  def __init__(self):
    self.cardType = CardType.Supporter
    self.name = 'JudgeSAV176'
    self.text = 'Each player shuffles their hand into their deck and draws 4 cards.'

  def effect(self, game, player, opponent):
    if game[player].canUseSupporter == True:
      for card in game[player].hand:
        game[player].deck.append(card)

      game[player].deck = game.shuffle(game[player].deck)

      game[player].hand = []

      for i in range(4):
        game[player].hand.append(game[player].deck.pop())

      for card in game[opponent].hand:
        game[opponent].deck.append(card)

      game[opponent].deck = game.shuffle(game[opponent].deck)

      game[opponent].hand = []

      for i in range(4):
        game[opponent].hand.append(game[opponent].deck.pop())

      game[player].canUseSupporter = False

      return game

    raise Exception("Can't play Judge if player has already played a Supporter card this turn") 

class LostCityLO161:
  def __init__(self):
    self.cardType = CardType.Stadium
    self.name = 'LostCityLO161'
    self.text = 'Whenever a Pokémon (either yours or your opponent\'s) is Knocked Out, put that Pokémon in the Lost Zone instead of the discard pile. (Discard all attached cards.)'

class CrystalCaveES230:
  def __init__(self):
    self.cardType = CardType.Stadium
    self.name = 'CrystalCaveES230'
    self.text = 'Once during each player\'s turn, that player may heal 30 damage from each of their Metal Pokémon and Dragon Pokémon.'

  def effect(self, game, player):
    if game[player].activePokemon.type == EnergyType.Metal or game[player].activePokemon.type == EnergyType.Dragon:
      game[player].activePokemon.hp += 30

      if game[player].activePokemon.hp > game[player].activePokemon.startHp:
        game[player].activePokemon.hp = game[player].activePokemon.startHp

    for index, pokemon in enumerate(game[player].bench):
      if pokemon.type == EnergyType.Metal or game[player].activePokemon.type == EnergyType.Dragon:
        game[player].bench[index].hp += 30

        if game[player].bench[index].hp > game[player].bench[index].startHp:
          game[player].bench[index].hp = game[player].bench[index].startHp

    return game

class PathToThePeakCR148:
  def __init__(self):
    self.cardType = CardType.Stadium
    self.name = 'PathToThePeakCR148'
    self.text = 'Pokémon with a Rule Box in play (both yours and your opponent\'s) have no Abilities. (Pokémon V, Pokémon-GX, etc. have Rule Boxes.)'

class BattleVipPassFS225:
  def __init__(self):
    self.cardType = CardType.Item
    self.name = 'BattleVipPassFS225'

  def effect(self, game, player, pokemon1Index = None, pokemon2Index = None):
    if game[player].activeTurn == 1:
      # check that pokemon are basic
      if game[player].deck[pokemon1Index].stage != Stage.Basic or game[player].deck[pokemon2Index].stage != Stage.Basic:
        raise Exception('cannot pick non-Basic pokemon with Battle VIP Pass')

      # if 2 pokemon are being picked, special logic so that the higher index card gets taken out of the deck first
      if pokemon2Index and len(game[player].bench) <= 3:
        if pokemon1Index > pokemon2Index:
          game[player].bench.append(game[player].deck.pop(pokemon1Index))
          game[player].bench.append(game[player].deck.pop(pokemon2Index))
        else:
          game[player].bench.append(game[player].deck.pop(pokemon2Index))
          game[player].bench.append(game[player].deck.pop(pokemon1Index))
      elif len(game[player].bench) <= 4:
        game[player].bench.append(game[player].deck.pop(pokemon1Index))
      
      game[player].deck = game.shuffle(game[player].deck)

      return game
    
    raise Exception('cannot play Battle VIP Pass on any turn but a player\'s first turn')
  
class CramomaticFS229:
  def __init__(self):
    self.cardType = CardType.Item
    self.name = 'CramomaticFS229'

  def effect(self, game, player, discardItemIndex, heads, deckCardIndex):
    if game[player].hand[discardItemIndex].cardType == CardType.Item:
      game[player].discardPile.append(game[player].hand.pop(discardItemIndex))

      if heads:
        game[player].hand.append(game[player].deck.pop(deckCardIndex))

        game[player].deck = game.shuffle(game[player].deck)

      return game
    
    raise Exception('item discarded in ordeer to play Cram-O-Matic must be an Item')
  
class PowerTabletFS281:
  def __init__(self):
    self.cardType = CardType.Item
    self.name = 'PowerTabletFS281'

  def effect(self, game, player):
    game[player].playedPowerTabletFlag = True

    return game
  
class UltraBallSAV196:
  def __init__(self):
    self.cardType = CardType.Item
    self.name = 'UltraBallSAV196'

  def effect(self, game, player, discardCard1Index, discardCard2Index, pokemonDeckIndex = None):
    if discardCard1Index > discardCard2Index:
      game[player].discardPile.append(game[player].hand.pop(discardCard1Index))
      game[player].discardPile.append(game[player].hand.pop(discardCard2Index))
    else:
      game[player].discardPile.append(game[player].hand.pop(discardCard2Index))
      game[player].discardPile.append(game[player].hand.pop(discardCard1Index))

    if pokemonDeckIndex:
      if game[player].deck[pokemonDeckIndex].type != CardType.Pokemon:
        raise Exception('cannot pull card that isn\'t a pokemon from deck with Ultra Ball')
      
      game[player].hand.append(game[player].deck.pop(pokemonDeckIndex))

    game[player].deck = game.shuffle(game[player].deck)

    return game
  
class LostVacuumLO217:
  def __init__(self):
    self.cardType = CardType.Item
    self.name = 'LostVacuumLO217'

  def effect(self, game, player, entryFeeLostZoneCardIndex, lostZoneCardOwner, lostZoneCardStadium = False, lostZoneCardToolLocation = None, lostZoneCardToolIndex = None):
    game[player].lostZone.append(game[player].hand.pop(entryFeeLostZoneCardIndex))

    if lostZoneCardStadium:
      game[lostZoneCardOwner].lostZone.append(game[lostZoneCardOwner].stadium)
      game[lostZoneCardOwner].stadium = None
    elif lostZoneCardToolLocation == "activePokemon":
      game[lostZoneCardOwner].lostZone.append(game[lostZoneCardOwner].activePokemon.tool)
      game[lostZoneCardOwner].activePokemon.tool = None
    else:
      game[lostZoneCardOwner].lostZone.append(game[lostZoneCardOwner].bench[lostZoneCardToolIndex])
      game[lostZoneCardOwner].bench[lostZoneCardToolIndex] = None

    return game
  
class NestBallSAV255:
  def __init__(self):
    self.cardType = CardType.Item
    self.name = 'NestBallSAV255'
    
  def effect(self, game, player, pokemonDeckIndex):
    if game[player].deck[pokemonDeckIndex].stage == Stage.Basic:
      if len(game[player].bench) <= 4:
        game[player].bench.append(game[player].deck.pop(pokemonDeckIndex))

        game[player].deck = game.shuffle(game[player].deck)

      return game
    
    raise Exception('cannot pull a card other than a Basic Pokemon from deck with Nest Ball')
  
class SwitchCartAR154:
  def __init__(self):
    self.cardType = CardType.Item
    self.name = 'SwitchCartAR154'

  def effect(self, game, player, benchPokemonIndex):
    game[player].activePokemon.hp += 30

    if game[player].activePokemon.hp > game[player].activePokemon.startHp:
      game[player].activePokemon.hp = game[player].activePokemon.startHp

    pokemonFromBench = game[player].bench.pop(benchPokemonIndex)

    game[player].activePokemon.burned = False

    game[player].activePokemon.paralyzedCounter = 0

    game[player].activePokemon.poisoned = False

    game[player].activePokemon.asleep = False

    game[player].activePokemon.confused = False

    game[player].bench.append(game[player].activePokemon)

    game[player].activePokemon = pokemonFromBench

    return game
  
class EscapeRopeBS125:
  def __init__(self):
    self.cardType = CardType.Item
    self.name = 'EscapeRopeBS125'

  def effect(self, game, player, opponent, playerBenchIndex = None, opponentBenchIndex = None):
    if playerBenchIndex:
      playerPokemonFromBench = game[player].bench.pop(playerBenchIndex)

      game[player].activePokemon.burned = False

      game[player].activePokemon.paralyzedCounter = 0

      game[player].activePokemon.poisoned = False

      game[player].activePokemon.asleep = False

      game[player].activePokemon.confused = False

      game[player].bench.append(game[player].activePokemon)

      game[player].activePokemon = playerPokemonFromBench
    
    if opponentBenchIndex:
      opponentPokemonFromBench = game[opponent].bench.pop(opponentBenchIndex)

      game[opponent].activePokemon.burned = False

      game[opponent].activePokemon.paralyzedCounter = 0

      game[opponent].activePokemon.poisoned = False

      game[opponent].activePokemon.asleep = False

      game[opponent].activePokemon.confused = False

      game[opponent].bench.append(game[opponent].activePokemon)

      game[opponent].activePokemon = opponentPokemonFromBench

    return game
  
class PalPadSAV182:
  def __init__(self):
    self.cardType = CardType.Item
    self.name = 'PalPadSAV182'

  def effect(self, game, player, discardPileIndex1, discardPileIndex2 = None):
    if discardPileIndex2:
      if (game[player].discardPile[discardPileIndex1].cardType == CardType.Supporter 
            and game[player].discardPile[discardPileIndex2].cardType == CardType.Supporter):
        if discardPileIndex1 > discardPileIndex2:
          game[player].deck.append(game[player].discardPile.pop(discardPileIndex1))
          game[player].deck.append(game[player].discardPile.pop(discardPileIndex2))
        else:
          game[player].deck.append(game[player].discardPile.pop(discardPileIndex2))
          game[player].deck.append(game[player].discardPile.pop(discardPileIndex1))
      else:
        raise Exception('cannot take a card that is not a Supporter out of discard pile with Pal Pad')
    else:
      if game[player].discardPile[discardPileIndex1].cardType != CardType.Supporter:
        raise Exception('cannot take a card that is not a Supporter out of discard pile with Pal Pad')
      
      game[player].deck.append(game[player].discardPile.pop(discardPileIndex1))

    game[player].deck = game.shuffle(game[player].deck)

    return game

class ForestSealStoneST156:
  def __init__(self):
    self.cardType = CardType.Tool
    self.name = 'ForestSealStoneST156'

  def useAbility(self, game, player, opponent, cardDeckIndex):
    if game[player].canUseVstarPower == True:
      if (game[player].stadium and game[player].stadium.name == 'PathToThePeakCR148') or (game[opponent].stadium 
                                                          and game[opponent].stadium.name == 'PathToThePeakCR148'):
        raise Exception('because of stadium Path to the Peak, this Pokemon V has no abilities')
      
      game[player].canUseVstarPower = False

      game[player].hand.append(game[player].deck.pop(cardDeckIndex))

      game[player].deck = game.shuffle(game[player].deck)

      return game
    
    raise Exception('cannot use Forest Seal Stone\s Ability because player has already used a Vstar Power this game')
  
class ChoiceBeltPE176:
  def __init__(self):
    self.cardType = CardType.Tool
    self.name = 'ChoiceBeltPE176'

class BoxOfDisasterLO214:
  def __init__(self):
    self.cardType = CardType.Tool
    self.name = 'BoxOfDisasterLO214'

class FusionStrikeEnergyFS244:
  def __init__(self):
    self.cardType = CardType.Energy
    self.name = 'FusionStrikeEnergyFS244'

  def attach(self, game, player, pokemonLocation, pokemonIndex = None):
    if pokemonLocation == 'activePokemon' and game[player].activePokemon.fusionStrike:
      game[player].activePokemon.attachedEnergy[EnergyType.FusionStrikeEnergy] += 1
    elif game[player].bench[pokemonIndex].fusionStrike:
      game[player].bench[pokemonIndex].attachedEnergy[EnergyType.FusionStrikeEnergy] += 1
    else:
      game[player].discardPile.append(self)

    return game
  
  def detach(self, game, player, pokemonLocation, pokemonIndex = None):
    if pokemonLocation == 'activePokemon':
      game[player].activePokemon.attachedEnergy[EnergyType.FusionStrikeEnergy] -= 1

      if game[player].activePokemon.attachedEnergy[EnergyType.FusionStrikeEnergy] < 0:
        raise Exception('cannot remove nonexistent Fusion Strike Energy from Pokemon')
      
      game[player].discardPile.append(self)
    else:
      game[player].bench[pokemonIndex].attachedEnergy[EnergyType.FusionStrikeEnergy] -= 1

      if game[player].bench[pokemonIndex].attachedEnergy[EnergyType.FusionStrikeEnergy] < 0:
        raise Exception('cannot remove nonexistent Fusion Strike Energy from Pokemon')
      
      game[player].discardPile.append(self)

    return game
  
class DoubleTurboEnergyBS151:
  def __init__(self):
    self.cardType = CardType.Energy
    self.name = 'DoubleTurboEnergyBS151'

  def attach(self, game, player, pokemonLocation, pokemonIndex = None):
    if pokemonLocation == 'activePokemon':
      game[player].activePokemon.attachedEnergy[EnergyType.DoubleTurboEnergy] += 1
    else:
      game[player].bench[pokemonIndex].attachedEnergy[EnergyType.DoubleTurboEnergy] += 1

  def detach(self, game, player, pokemonLocation, pokemonIndex = None):
    if pokemonLocation == 'activePokemon':
      game[player].activePokemon.attachedEnergy[EnergyType.DoubleTurboEnergy] -= 1

      if game[player].activePokemon.attachedEnergy[EnergyType.DoubleTurboEnergy] < 0:
        raise Exception('cannot remove nonexistent Double Turbo Energy from Pokemon')
      
      game[player].discardPile.append(self)
    else:
      game[player].bench[pokemonIndex].attachedEnergy[EnergyType.DoubleTurboEnergy] -= 1

      if game[player].bench[pokemonIndex].attachedEnergy[EnergyType.DoubleTurboEnergy] < 0:
        raise Exception('cannot remove nonexistent Double Turbo Energy from Pokemon')
      
      game[player].discardPile.append(self)

    return game

# DECKS

def MewsRevenge():
  deck = []

  for i in range(3):
    deck.append(MewVmaxFS268())

  for i in range(4):
    deck.append(MewVFS250())

  for i in range(4):
    deck.append(GenesectVFS255())

  deck.append(MeloettaFS124())

  deck.append(OricorioFS42())

  for i in range(2):
    deck.append(BosssOrdersGhetsisPE265())

  for i in range(2):
    deck.append(ElesasSparkleFS260())

  deck.append(IonoPE269())

  deck.append(JudgeSAV176())

  for i in range(2):
    deck.append(LostCityLO161())

  deck.append(CrystalCaveES230())

  deck.append(PathToThePeakCR148())

  for i in range(4):
    deck.append(BattleVipPassFS225())

  for i in range(4):
    deck.append(CramomaticFS229())

  for i in range(4):
    deck.append(PowerTabletFS281())

  for i in range(4):
    deck.append(UltraBallSAV196())

  for i in range(2):
    deck.append(LostVacuumLO217)

  for i in range(2):
    deck.append(NestBallSAV255())

  for i in range(2):
    deck.append(SwitchCartAR154())

  deck.append(EscapeRopeBS125())

  deck.append(PalPadSAV182())

  for i in range(3):
    deck.append(ForestSealStoneST156())

  for i in range(2):
    deck.append(ChoiceBeltPE176())

  deck.append(BoxOfDisasterLO214())

  for i in range(4):
    deck.append(FusionStrikeEnergyFS244())

  for i in range(3):
    deck.append(DoubleTurboEnergyBS151())

  if len(deck) != 60:
    raise Exception('Mew\s Revenge does not have exactly 60 cards.')
  
  return deck