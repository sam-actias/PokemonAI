from enums import EnergyType, CardType, Stage

class MewVmaxFS268:
  def __init__(self):
    self.cardType = CardType.Pokemon
    self.name = 'Mew VMAX'
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
    self.evolvesFrom = [ MewVFS250() ]
    self.canEvolve = False
    self.fusionStrike = True
    self.isV = True
    self.tool = None
    self.burned = False
    self.poisoned = False
    self.paralyzed = False
    self.confused = False
    self.asleep = False
    self.moves = {
      'crossFusionStrike': {
        'name': 'Cross Fusion Strike',
        'do': self.crossFusionStrike,
        'canDo': self.canDoCrossFusionStrike,
        'energyRequirement': {
          EnergyType.Colorless: 2,
          EnergyType.Psychic: 0,
          EnergyType.Metal: 0,
          EnergyType.Fire: 0
        },
        'text': 'Choose 1 of your Benched Fusion Strike Pokémon\'s attacks and use it as this attack.'
      },
      'maxMiracle': {
        'name': 'Max Miracle',
        'do': self.maxMiracle,
        'canDo': self.canDoMaxMiracle,
        'energyRequirement': {
          EnergyType.Colorless: 0,
          EnergyType.Psychic: 2,
          EnergyType.Metal: 0,
          EnergyType.Fire: 0
        },
        'text': 'This attack\'s damage isn\'t affected by any effects on your opponent\'s Active Pokémon.'
      }
    }
    self.attachedEnergy = {
      EnergyType.FusionStrikeEnergy: 0,
      EnergyType.DoubleTurboEnergy: 0,
      EnergyType.Water: 0
    }

  def crossFusionStrike(self, game, player, benchedPokemonIndex, move, moveInput):
    if not game.energyForAttackCheck(game.players[player].activePokemon.attachedEnergy, self.moves['crossFusionStrike']['energyRequirement']):
      raise Exception('Not enough energy for move Cross Fusion Strike')

    return game.players[player].bench[benchedPokemonIndex].moves[move].do(**moveInput)
  
  def canDoCrossFusionStrike(self, game, player):
    canDo = False

    for pokemone in game.players[player].bench:
      if pokemone.fusionStrike == True:
        canDo = True
        break
    
    return canDo
  
  def maxMiracle(self, game, player, opponent):
    if not game.energyForAttackCheck(game.players[player].activePokemon.attachedEnergy, self.moves['maxMiracle']['energyRequirement']):
      raise Exception('Not enough energy for move Max Miracle')

    # no damage effects on this attack from effects on opponent's active Pokemon

    game.players[opponent].activePokemon.hp -= game.activePokemonAttackChecks(player, opponent, 130, True)

    return game
  
  def canDoMaxMiracle():
    return True
  
class MewVFS250:
  def __init__(self):
    self.cardType = CardType.Energy
    self.name = 'Mew V'
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
    self.evolvesFrom = []
    self.canEvolve = False
    self.fusionStrike = True
    self.isV = True
    self.tool = None
    self.burned = False
    self.poisoned = False
    self.paralyzed = False
    self.confused = False
    self.asleep = False
    self.moves = {
      'energyMix': {
        'name': 'Energy Mix',
        'do': self.energyMix,
        'canDo': self.canDoEnergyMix,
        'energyRequirement': {
          EnergyType.Colorless: 0,
          EnergyType.Psychic: 1,
          EnergyType.Metal: 0,
          EnergyType.Fire: 0
        },
        'text': 'Search your deck for an Energy card and attach it to 1 of your Fusion Strike Pokémon. Then, shuffle your deck.'
      },
      'psychicLeap': {
        'name': 'Psychic Leap',
        'do': self.psychicLeap,
        'energyRequirement': {
          EnergyType.Colorless: 1,
          EnergyType.Psychic: 1,
          EnergyType.Metal: 0,
          EnergyType.Fire: 0

        },
        'text': 'You may shuffle this Pokémon and all attached cards into your deck.'
      }
    }
    self.attachedEnergy = {
      EnergyType.FusionStrikeEnergy: 0,
      EnergyType.DoubleTurboEnergy: 0,
      EnergyType.Water: 0
    }

  def energyMix(self, game, player, deckIndex, pokemonLocation, pokemonIndex):
    if not game.energyForAttackCheck(game.players[player].activePokemon.attachedEnergy, self.moves['energyMix']['energyRequirement']):
      raise Exception('Not enough energy for move Energy Mix')
    # provide an index for the energy card in the deck
    # provide a location and index (if needed) of the chosen Fusion Strike Pokemon

    card = game.players[player].deck.pop(deckIndex)

    if pokemonLocation != 'activePokemon':
      if game.players[player].bench[pokemonIndex].fusionStrike:
        game.players[player].bench[pokemonIndex].attachedEnergy[card.energyType] += 1
      else:
        raise Exception('cannot use Mew V\'s Energy Mix on a non-Fusion Strike Pokemon')
    else:
      if game.players[player].activePokemon.fusionStrike:
        game.players[player].activePokemon.attachedEnergy[card.energyType] += 1
      else:
        raise Exception('cannot use Mew V\'s Energy Mix on a non-Fusion Strike Pokemon')
      
    return game
  
  def canDoEnergyMix(game, player):
    return True
      
  def psychicLeap(self, game, player, opponent, shuffleIn, newActivePokemonIndex = None):
    if not game.energyForAttackCheck(game.players[player].activePokemon.attachedEnergy, self.moves['psychicLeap']['energyRequirement']):
      raise Exception('Not enough energy for move Psychic Leap')
    # provide a shuffleIn boolean

    game.players[opponent].activePokemon.hp -= game.activePokemonAttackChecks(player, opponent, 70)

    if (shuffleIn & newActivePokemonIndex):
      if len(game.players[player].bench) < 1:
        raise Exception('can\'t do move Psychic Leap and shuffle Mew V into deck if no Pokemon on bench')
      else:
        if game.players[player].activePokemon.evolvesFrom:
          game.players[player].deck.append(game.players[player].activePokemon.evolvesFrom)

        if game.players[player].activePokemon.tool:
          game.players[player].deck.append(game.players[player].activePokemon.tool)
        
        if game.players[player].activePokemon.attachedEnergy[EnergyType.FusionStrikeEnergy] > 0:
          for i in range(game.players[player].activePokemon.attachedEnergy[EnergyType.FusionStrikeEnergy]):
            game.players[player].deck.append(FusionStrikeEnergyFS244())

        if game.players[player].activePokemon.attachedEnergy[EnergyType.DoubleTurboEnergy] > 0:
          for i in range(game.players[player].activePokemon.attachedEnergy[EnergyType.DoubleTurboEnergy]):
            game.players[player].deck.append(DoubleTurboEnergyBS151())

        game.players[player].activePokemon.tool = None

        game.players[player].activePokemon.hp = game.players[player].activePokemon.startHp

        game.players[player].activePokemon.attachedEnergy = []

        game.players[player].activePokemon.burned = False

        game.players[player].activePokemon.paralyzedCounter = 0

        game.players[player].activePokemon.poisoned = False

        game.players[player].activePokemon.asleep = False

        game.players[player].activePokemon.confused = False

        game.players[player].deck.append(game.players[player].activePokemon)

        game.players[player].deck = game.shuffle(game.players[player].deck)

        game.players[player].activePokemon = game.players[player].bench.pop(newActivePokemonIndex)
    elif ((shuffleIn and not newActivePokemonIndex) or (not shuffleIn and newActivePokemonIndex)):
      raise Exception('can\'t do move Psychic Leap without both shuffleIn and newActivePokemonIndex')
    
    return game
  
  def canDoPsychicLeap():
    return True
  
class GenesectVFS255:
  def __init__(self):
    self.cardType = CardType.Pokemon
    self.name = 'Genesect V'
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
    self.evolvesFrom = []
    self.canEvolve = False
    self.fusionStrike = True
    self.isV = True
    self.tool = None
    self.burned = False
    self.poisoned = False
    self.paralyzed = False
    self.confused = False
    self.asleep = False
    self.ability = {
      'name': 'Fusion Strike System',
      'do': self.fusionStrikeSystem,
      'canDo': self.canDoFusionStrikeSystem,
      'usedFlag': False,
      'text': 'Once during your turn, you may draw cards until you have as many cards in your hand as you have Fusion Strike Pokémon in play.'
    }
    self.moves = {
      'technoBlast': {
        'name': 'Techno Blast',
        'do': self.technoBlast,
        'canDo': self.canDoTechnoBlast,
        'energyRequirement': {
          EnergyType.Colorless: 1,
          EnergyType.Psychic: 0,
          EnergyType.Metal: 2,
          EnergyType.Fire: 0
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
    if (game.players[player].stadium == None and  game.players[player].stadium == None) or (game.players[player].stadium 
                          != 'PathToThePeakCR148' and game.players[player].stadium  != 'PathToThePeakCR148'):
      fusionStrikePokemonInPlay = 0

      if game.players[player].activePokemon.fusionStrike:
        fusionStrikePokemonInPlay += 1

      for pokemon in game.players[player].bench:
        if pokemon.fusionStrike:
          fusionStrikePokemonInPlay += 1

      if fusionStrikePokemonInPlay > len(game.players[player].hand):
        amtToDraw = fusionStrikePokemonInPlay - len(game.players[player].hand)

        for i in range(amtToDraw):
          game.players[player].hand.append(game.players[player].deck.pop())

      self.ability.usedFlag = True

      return game
    
    raise Exception("Cannot use ability Fusion Strike System while Path To The Peak is the stadium in play")
  
  def canDoFusionStrikeSystem(game, player):
    fusionStrikePokemonAmt = 0

    if game.players[player].activePokemon.fusionStrike:
      fusionStrikePokemonAmt += 1

    for pokemon in game.players[player].bench:
      if pokemon.fusionStrike:
        fusionStrikePokemonAmt += 1

    if fusionStrikePokemonAmt > len(game.players[player].hand):
      return True
    
    return False

  def technoBlast(self, game, player, opponent):
    if not game.energyForAttackCheck(game.players[player].activePokemon.attachedEnergy, self.moves['technoBlast']['energyRequirement']):
      raise Exception('Not enough energy for move Techno Blast')
    
    if game.players[player].activePokemonCantAttack == 0:
      game.players[opponent].activePokemon.hp -= game.activePokemonAttackChecks(player, opponent, 210)

      game.players[player].activePokemonCantAttack = 2
    else:
      raise Exception('Genesect V cannot attack right now due to the rules of a move')
    
    return game
  
  def canDoTechnoBlast():
    return True
    
class MeloettaFS124:
  def __init__(self):
    self.cardType = CardType.Pokemon
    self.name = 'Meloetta'
    self.stage = Stage.Basic
    self.hp = 90
    self.startHp = 90
    self.type = EnergyType.Psychic
    self.weakness = EnergyType.Darkness
    self.weaknessFactor = 2
    self.resistance = EnergyType.Fighting
    self.resistanceFactor = 30
    self.retreatCost = 1
    self.hasRuleBox = False
    self.prizesWhenKnockedOut = 1
    self.evolvesFrom = []
    self.canEvolve = False
    self.fusionStrike = True
    self.isV = False
    self.tool = None
    self.burned = False
    self.poisoned = False
    self.paralyzed = False
    self.confused = False
    self.asleep = False
    self.moves = {
      'melodiouEcho': {
        'name': 'Melodious Echo',
        'do': self.melodiousEcho,
        'canDo': self.canDoMelodiousEcho,
        'energyRequirement': {
          EnergyType.Colorless: 1,
          EnergyType.Psychic: 1,
          EnergyType.Metal: 0,
          EnergyType.Fire: 0
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
    if not game.energyForAttackCheck(game.players[player].activePokemon.attachedEnergy, self.moves['melodiousBlast']['energyRequirement']):
      raise Exception('Not enough energy for move Melodious Blast')

    fusionStrikeEnergyAmt = 0

    fusionStrikeEnergyAmt += self.attachedEnergy[EnergyType.FusionStrikeEnergy]

    for pokemon in game.players[player].bench:
      fusionStrikeEnergyAmt += pokemon.attachedEnergy[EnergyType.FusionStrikeEnergy]

    game.players[opponent].activePokemon.hp -= game.activePokemonAttackChecks(player, opponent, 70 * fusionStrikeEnergyAmt)

    return game
  
  def canDoMelodiousEcho():
    return True

class OricorioFS42:
  def __init__(self):
    self.cardType = CardType.Pokemon
    self.name = 'Oricorio'
    self.stage = Stage.Basic
    self.hp = 90
    self.startHp = 90
    self.type = EnergyType.Fire
    self.weakness = EnergyType.Water
    self.weaknessFactor = 2
    self.resistance = EnergyType.Fighting
    self.resistanceFactor = 30
    self.retreatCost = 1
    self.hasRuleBox = False
    self.prizesWhenKnockedOut = 1
    self.evolvesFrom = []
    self.canEvolve = False
    self.fusionStrike = True
    self.isV = False
    self.tool = None
    self.burned = False
    self.poisoned = False
    self.paralyzed = False
    self.confused = False
    self.asleep = False
    self.ability = {
      'name': 'Lesson In Zeal',
      'canDo': self.canDoLessonInZeal(),
      'text': 'All of your Fusion Strike Pokémon take 20 less damage from attacks from your opponent\'s Pokémon (after applying Weakness and Resistance). You can\'t apply more than 1 Lesson in Zeal Ability at a time.'
    }
    self.moves = {
      'glisteningDroplets': {
        'name': 'Glistening Droplets',
        'do': self.glisteningDroplets,
        'canDo': self.canDoGlisteningDroplets,
        'energyRequirement': {
          EnergyType.Colorless: 1,
          EnergyType.Psychic: 0,
          EnergyType.Metal: 0,
          EnergyType.Fire: 1
        },
        'text': 'Put 5 damage counters on your opponent\'s Pokémon in any way you like.'
      }
    }
    self.attachedEnergy = {
      EnergyType.FusionStrikeEnergy: 0,
      EnergyType.DoubleTurboEnergy: 0,
      EnergyType.Water: 0
    }

  def canDoLessonInZeal():
    return False

  def glisteningDroplets(self, game, player, opponent, howToPutDamageCounters):
    if not game.energyForAttackCheck(game.players[player].activePokemon.attachedEnergy, self.moves['glisteningDroplets']['energyRequirement']):
      raise Exception('Not enough energy for move Glistening Droplets')
    
    # howToPutDamageCounters is a list containing dictionaries with keys pokemonLocation and pokemonIndex for each damage counter

    if len(howToPutDamageCounters) != 5:
      raise Exception('Damage amount for Glistening Droplets does not equal exactly 5')

    for howTo in howToPutDamageCounters:
      if howTo.pokemonLocation == "activePokemon":
        game.players[opponent][howTo.pokemonLocation].hp -= 10
      else:
        game.players[opponent][howTo.pokemonLocation][howTo.pokemonIndex].hp -= 10

    return game
  
  def canDoGlisteningDroplets():
    return True
  
class BosssOrdersGhetsisPE265:
  def __init__(self):
    self.cardType = CardType.Supporter
    self.name = 'Boss\'s Orders (Ghetsis)'
    self.text = 'Switch in 1 of your opponent\'s Benched Pokémon to the Active Spot.'

  def effect(self, game, player, opponent, benchedPokemonIndex):
    if game.players[player].canUseSupporter == True:
      if len(game.players[opponent].bench) > 0:
        pokemon = game.players[opponent].bench.pop(benchedPokemonIndex)

        game.players[opponent].activePokemon.burned = False

        game.players[opponent].activePokemon.paralyzedCounter = 0

        game.players[opponent].activePokemon.poisoned = False

        game.players[opponent].activePokemon.asleep = False

        game.players[opponent].activePokemon.confused = False

        game.players[opponent].bench.append(game.players[opponent].activePokemon)

        game.players[opponent].activePokemon = pokemon

        game.players[opponent].activePokemonCantAttack = 0

      game.players[player].canUseSupporter = False

      return game
    
    raise Exception("Can't play Boss\'s Order Ghetsis if player has already played a Supporter card this turn")
  
  def canPlay(self, game, player, opponent):
    if len(game.players[opponent].bench) > 0 and game.players[player].canUseSupporterFlag:
      return True
    
    return False
  
class ElesasSparkleFS260:
  def __init__(self):
    self.cardType = CardType.Supporter
    self.name = 'Elesa\'s Sparkle'
    self.text = 'Choose up to 2 of your Fusion Strike Pokémon. For each of those Pokémon, search your deck for a Fusion Strike Energy card and attach it to that Pokémon. Then, shuffle your deck.'

  def effect(self, game, player, pokemon1Location, pokemon1Index = None, pokemon2Location = None, pokemon2Index = None):
    if game.players[player].canUseSupporter == True:
      for index, card in enumerate(game.players[player].deck):
        if card.name == 'Fusion Strike Energy':
          if pokemon1Location == 'activePokemon':
            game.players[player].activePokemon.attachedEnergy[EnergyType.FusionStrikeEnergy] += 1
            game.players[player].deck.pop(index)
            break
          else:
            game.players[player].bench[pokemon1Index].attachedEnergy[EnergyType.FusionStrikeEnergy] += 1
            game.players[player].deck.pop(index)
            break
      
      if pokemon2Location:
        for index, card in enumerate(game.players[player].deck):
          if card.name == 'Fusion Strike Energy':
            if pokemon2Location == 'activePokemon':
              game.players[player].activePokemon.attachedEnergy[EnergyType.FusionStrikeEnergy] += 1
              game.players[player].deck.pop(index)
              break
            else:
              game.players[player].bench[pokemon2Index].attachedEnergy[EnergyType.FusionStrikeEnergy] += 1
              game.players[player].deck.pop(index)
              break

      game.players[player].deck = game.shuffle(game.players[player].deck)

      game.players[player].canUseSupporter = False

      return game
    
    raise Exception("Can't play Elesa\'s Sparkle if player has already played a Supporter card this turn")

  def canPlay(self, game, player, opponent):
    if game.players[player].canUseSupporterFlag:
      if game.players[player].activePokemon.fusionStrike:
        return True
      
      for pokemon in game.players[player].bench:
        if pokemon.fusionStrike:
          return True
      
    return False

class IonoPE269:
  def __init__(self):
    self.cardType = CardType.Supporter
    self.name = 'Iono'
    self.text = 'Each player shuffles their hand and puts it on the bottom of their deck. If either player put any cards on the bottom of their deck in this way, each player draws a card for each of their remaining Prize cards.'

  def effect(self, game, player, opponent):
    if game.players[player].canUseSupporter == True:
      if len(game.players[player].hand) > 0:
        playerShuffledHand = game.shuffle(game.players[player].hand)

        game.players[player].deck = game.putCardsAtBottomOfDeck(playerShuffledHand, game.players[player].deck)

        for card in game.players[player].prizes:
          game.players[player].hand.append(game.players[player].deck.pop())

      if len(game.players[opponent].hand) > 0:
        opponentShuffledHand = game.shuffle(game.players[opponent].hand)

        game.players[opponent].deck = game.putCardsAtBottomOfDeck(opponentShuffledHand, game.players[opponent].deck)

        for card in game.players[opponent].prizes:
          game.players[opponent].hand.append(game.players[opponent].deck.pop())

      game.players[player].canUseSupporter = False

      return game
  
    raise Exception("Can't play Iono if player has already played a Supporter card this turn")

  def canPlay(self, game, player, opponent):
    if game.players[player].canUseSupporterFlag:
      return True

class JudgeSAV176:
  def __init__(self):
    self.cardType = CardType.Supporter
    self.name = 'Judge'
    self.text = 'Each player shuffles their hand into their deck and draws 4 cards.'

  def effect(self, game, player, opponent):
    if game.players[player].canUseSupporter == True:
      for card in game.players[player].hand:
        game.players[player].deck.append(card)

      game.players[player].deck = game.shuffle(game.players[player].deck)

      game.players[player].hand = []

      for i in range(4):
        game.players[player].hand.append(game.players[player].deck.pop())

      for card in game.players[opponent].hand:
        game.players[opponent].deck.append(card)

      game.players[opponent].deck = game.shuffle(game.players[opponent].deck)

      game.players[opponent].hand = []

      for i in range(4):
        game.players[opponent].hand.append(game.players[opponent].deck.pop())

      game.players[player].canUseSupporter = False

      return game

    raise Exception("Can't play Judge if player has already played a Supporter card this turn") 

  def canPlay(self, game, player, opponent):
    if game.players[player].canUseSupporterFlag:
      return True

class LostCityLO161:
  def __init__(self):
    self.cardType = CardType.Stadium
    self.name = 'Lost City'
    self.text = 'Whenever a Pokémon (either yours or your opponent\'s) is Knocked Out, put that Pokémon in the Lost Zone instead of the discard pile. (Discard all attached cards.)'

  def canPlay(self, game, player, opponent):
    if game.players[player].canPlayStadiumFlag and (game.players[player].stadium == None or 
                                                game.players[player].stadium.name != self.name): 
      return True
    
class CrystalCaveES230:
  def __init__(self):
    self.cardType = CardType.Stadium
    self.name = 'Crystal Cave'
    self.text = 'Once during each player\'s turn, that player may heal 30 damage from each of their Metal Pokémon and Dragon Pokémon.'

  def effect(self, game, player):
    if game.players[player].activePokemon.type == EnergyType.Metal or game.players[player].activePokemon.type == EnergyType.Dragon:
      game.players[player].activePokemon.hp += 30

      if game.players[player].activePokemon.hp > game.players[player].activePokemon.startHp:
        game.players[player].activePokemon.hp = game.players[player].activePokemon.startHp

    for index, pokemon in enumerate(game.players[player].bench):
      if pokemon.type == EnergyType.Metal or game.players[player].activePokemon.type == EnergyType.Dragon:
        game.players[player].bench[index].hp += 30

        if game.players[player].bench[index].hp > game.players[player].bench[index].startHp:
          game.players[player].bench[index].hp = game.players[player].bench[index].startHp

    return game
  
  def canPlay(self, game, player, opponent):
    if game.players[player].canPlayStadiumFlag and (game.players[player].stadium == None or 
                                                game.players[player].stadium.name != self.name): 
      return True

class PathToThePeakCR148:
  def __init__(self):
    self.cardType = CardType.Stadium
    self.name = 'Path To The Peak'
    self.text = 'Pokémon with a Rule Box in play (both yours and your opponent\'s) have no Abilities. (Pokémon V, Pokémon-GX, etc. have Rule Boxes.)'

  def canPlay(self, game, player, opponent):
    if game.players[player].canPlayStadiumFlag and (game.players[player].stadium == None or 
                                                game.players[player].stadium.name != self.name): 
      return True

class BattleVipPassFS225:
  def __init__(self):
    self.cardType = CardType.Item
    self.name = 'Battle VIP Pass'
    self.text = 'You can use this card only during your first turn. Search your deck for up to 2 Basic Pokémon and put them onto your Bench. Then, shuffle your deck.'

  def effect(self, game, player, pokemon1Index = None, pokemon2Index = None):
    if game.players[player].activeTurn == 1:
      # check that pokemon are basic
      if game.players[player].deck[pokemon1Index].stage != Stage.Basic or game.players[player].deck[pokemon2Index].stage != Stage.Basic:
        raise Exception('cannot pick non-Basic pokemon with Battle VIP Pass')

      # if 2 pokemon are being picked, special logic so that the higher index card gets taken out of the deck first
      if pokemon2Index and len(game.players[player].bench) <= 3:
        if pokemon1Index > pokemon2Index:
          game.players[player].bench.append(game.players[player].deck.pop(pokemon1Index))
          game.players[player].bench.append(game.players[player].deck.pop(pokemon2Index))
        else:
          game.players[player].bench.append(game.players[player].deck.pop(pokemon2Index))
          game.players[player].bench.append(game.players[player].deck.pop(pokemon1Index))
      elif len(game.players[player].bench) <= 4:
        game.players[player].bench.append(game.players[player].deck.pop(pokemon1Index))
      
      game.players[player].deck = game.shuffle(game.players[player].deck)

      return game
    
    raise Exception('cannot play Battle VIP Pass on any turn but a player\'s first turn')
  
  def canPlay(self, game, player, opponent):
    if game.players[player].activeTurn == 1 and len(game.players[player].bench) < 5 and len(game.players[player].deck) > 0:
      return True
    
    return False

class CramomaticFS229:
  def __init__(self):
    self.cardType = CardType.Item
    self.name = 'Cram-O-Matic'
    self.text = 'You can use this card only if you discard another Item card from your hand. Flip a coin. If heads, search your deck for a card and put it into your hand. Then, shuffle your deck.'

  def effect(self, game, player, discardItemIndex, heads, deckCardIndex = None):
    if game.players[player].hand[discardItemIndex].cardType == CardType.Item:
      game.players[player].discardPile.append(game.players[player].hand.pop(discardItemIndex))

      if heads:
        game.players[player].hand.append(game.players[player].deck.pop(deckCardIndex))

        game.players[player].deck = game.shuffle(game.players[player].deck)

      return game
    
    raise Exception('item discarded in ordeer to play Cram-O-Matic must be an Item')
  
  def canPlay(self, game, player, opponent):
    if len(game.players[player].deck) > 0:
      itemAmtInHand = 0

      for card in game.players[player].hand:
        if card.cardType == CardType.Item:
          itemAmtInHand += 1
          if itemAmtInHand == 2:
            return True
          
      return False
  
class PowerTabletFS281:
  def __init__(self):
    self.cardType = CardType.Item
    self.name = 'Power Tablet'
    self.text = 'During this turn, your Fusion Strike Pokémon\'s attacks do 30 more damage to your opponent\'s Active Pokémon (before applying Weakness and Resistance).'

  def effect(self, game, player):
    game.players[player].playedPowerTabletFlag = True

    return game
  
  def canPlay(self, game, player, opponent):
    return True
  
class UltraBallSAV196:
  def __init__(self):
    self.cardType = CardType.Item
    self.name = 'Ultra Ball'
    self.text = 'You can use this card only if you discard 2 other cards from your hand. Search your deck for a Pokémon, reveal it, and put it into your hand. Then, shuffle your deck.'

  def effect(self, game, player, discardCard1Index, discardCard2Index, pokemonDeckIndex = None):
    if discardCard1Index > discardCard2Index:
      game.players[player].discardPile.append(game.players[player].hand.pop(discardCard1Index))
      game.players[player].discardPile.append(game.players[player].hand.pop(discardCard2Index))
    else:
      game.players[player].discardPile.append(game.players[player].hand.pop(discardCard2Index))
      game.players[player].discardPile.append(game.players[player].hand.pop(discardCard1Index))

    if pokemonDeckIndex:
      if game.players[player].deck[pokemonDeckIndex].type != CardType.Pokemon:
        raise Exception('cannot pull card that isn\'t a pokemon from deck with Ultra Ball')
      
      game.players[player].hand.append(game.players[player].deck.pop(pokemonDeckIndex))

    game.players[player].deck = game.shuffle(game.players[player].deck)

    return game
  
  def canPlay(self, game, player, opponent):
    if len(game.players[player].hand) >= 3:
      return True
    
    return False
  
class LostVacuumLO217:
  def __init__(self):
    self.cardType = CardType.Item
    self.name = 'Lost Vacuum'
    self.text = 'You can use this card only if you put another card from your hand in the Lost Zone. Choose a Pokémon Tool attached to any Pokémon, or any Stadium in play, and put it in the Lost Zone.'

  def effect(self, game, player, entryFeeLostZoneCardIndex, lostZoneCardOwner, lostZoneCardStadium = False, lostZoneCardToolLocation = None, lostZoneCardToolIndex = None):
    game.players[player].lostZone.append(game.players[player].hand.pop(entryFeeLostZoneCardIndex))

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
  
  def canPlay(self, game, player, opponent):
    if len(game.players[player].hand) >= 3:
      if game.players[player].activePokemon.tool != None:
        return True
      
      if game.players[opponent].activePokemon.tool != None:
        return True
      
      if game.players[player].stadium != None:
        return True
      
      if game.players[opponent].stadium != None:
        return True
      
      for pokemon in game.players[player].bench:
        if pokemon.tool != None:
          return True

      for pokemon in game.players[opponent].bench:
        if pokemon.tool != None:
          return True
        
    return False
  
class NestBallSAV255:
  def __init__(self):
    self.cardType = CardType.Item
    self.name = 'Nest Ball'
    self.text = 'Search your deck for a Basic Pokémon and put it onto your Bench. Then, shuffle your deck.'
    
  def effect(self, game, player, pokemonDeckIndex):
    if game.players[player].deck[pokemonDeckIndex].stage == Stage.Basic:
      if len(game.players[player].bench) <= 4:
        game.players[player].bench.append(game.players[player].deck.pop(pokemonDeckIndex))

        game.players[player].deck = game.shuffle(game.players[player].deck)

      return game
    
    raise Exception('cannot pull a card other than a Basic Pokemon from deck with Nest Ball')

  def canPlay(self, game, player, opponent):
    return True

class SwitchCartAR154:
  def __init__(self):
    self.cardType = CardType.Item
    self.name = 'Switch Cart'
    self.text = 'Switch your Active Basic Pokémon with 1 of your Benched Pokémon. If you do, heal 30 damage from the Pokémon you moved to your Bench.'

  def effect(self, game, player, benchPokemonIndex):
    game.players[player].activePokemon.hp += 30

    if game.players[player].activePokemon.hp > game.players[player].activePokemon.startHp:
      game.players[player].activePokemon.hp = game.players[player].activePokemon.startHp

    pokemonFromBench = game.players[player].bench.pop(benchPokemonIndex)

    game.players[player].activePokemon.burned = False

    game.players[player].activePokemon.paralyzedCounter = 0

    game.players[player].activePokemon.poisoned = False

    game.players[player].activePokemon.asleep = False

    game.players[player].activePokemon.confused = False

    game.players[player].bench.append(game.players[player].activePokemon)

    game.players[player].activePokemon = pokemonFromBench

    game.players[player].activePokemonCantAttack = 0

    return game
  
  def canPlay(self, game, player, opponent):
    if len(game.players[player].bench) > 0:
      return True
    
    return False
  
class EscapeRopeBS125:
  def __init__(self):
    self.cardType = CardType.Item
    self.name = 'Escape Rope'
    self.text = 'Each player switches their Active Pokémon with 1 of their Benched Pokémon. Your opponent switches first. (If a player does not have a Benched Pokémon, they don\'t switch Pokémon.)'

  def effect(self, game, player, opponent, playerBenchIndex = None, opponentBenchIndex = None):
    if playerBenchIndex:
      playerPokemonFromBench = game.players[player].bench.pop(playerBenchIndex)

      game.players[player].activePokemon.burned = False

      game.players[player].activePokemon.paralyzedCounter = 0

      game.players[player].activePokemon.poisoned = False

      game.players[player].activePokemon.asleep = False

      game.players[player].activePokemon.confused = False

      game.players[player].bench.append(game.players[player].activePokemon)

      game.players[player].activePokemon = playerPokemonFromBench

      game.players[player].activePokemonCantAttack = 0
    
    if opponentBenchIndex:
      opponentPokemonFromBench = game.players[opponent].bench.pop(opponentBenchIndex)

      game.players[opponent].activePokemon.burned = False

      game.players[opponent].activePokemon.paralyzedCounter = 0

      game.players[opponent].activePokemon.poisoned = False

      game.players[opponent].activePokemon.asleep = False

      game.players[opponent].activePokemon.confused = False

      game.players[opponent].bench.append(game.players[opponent].activePokemon)

      game.players[opponent].activePokemon = opponentPokemonFromBench

      game.players[opponent].activePokemonCantAttack = 0

    return game
  
  def canPlay(self, game, player, opponent):
    if len(game.players[player].bench) > 0 or len(game.players[opponent].bench) > 0:
      return True
    
    return False
  
class PalPadSAV182:
  def __init__(self):
    self.cardType = CardType.Item
    self.name = 'Pal Pad'
    self.text = 'Shuffle up to 2 Supporter cards from your discard pile into your deck.'

  def effect(self, game, player, discardPileIndex1, discardPileIndex2 = None):
    if discardPileIndex2:
      if (game.players[player].discardPile[discardPileIndex1].cardType == CardType.Supporter 
            and game.players[player].discardPile[discardPileIndex2].cardType == CardType.Supporter):
        if discardPileIndex1 > discardPileIndex2:
          game.players[player].deck.append(game.players[player].discardPile.pop(discardPileIndex1))
          game.players[player].deck.append(game.players[player].discardPile.pop(discardPileIndex2))
        else:
          game.players[player].deck.append(game.players[player].discardPile.pop(discardPileIndex2))
          game.players[player].deck.append(game.players[player].discardPile.pop(discardPileIndex1))
      else:
        raise Exception('cannot take a card that is not a Supporter out of discard pile with Pal Pad')
    else:
      if game.players[player].discardPile[discardPileIndex1].cardType != CardType.Supporter:
        raise Exception('cannot take a card that is not a Supporter out of discard pile with Pal Pad')
      
      game.players[player].deck.append(game.players[player].discardPile.pop(discardPileIndex1))

    game.players[player].deck = game.shuffle(game.players[player].deck)

    return game
  
  def canPlay(self, game, player, opponent):
    for card in game.players[player].discardPile:
      if card.cardType == CardType.Supporter:
        return True
    
    return False

class ForestSealStoneST156:
  def __init__(self):
    self.cardType = CardType.Tool
    self.name = 'Forest Seal Stone'
    self.text = 'VSTAR Power: The Pokémon V this card is attached to can use the VSTAR Power on this card. ABILITY Star Alchemy: During your turn, you may search your deck for a card and put it into your hand. Then, shuffle your deck.(You can\'t use more than 1 VSTAR Power in a game.)'

  def useAbility(self, game, player, opponent, cardDeckIndex):
    if game.players[player].canUseVstarPower == True:
      if (game.players[player].stadium and game.players[player].stadium.name == 'Path To The Peak') or (game.players[opponent].stadium 
                                                          and game.players[opponent].stadium.name == 'PathToThePeakCR148'):
        raise Exception('because of stadium Path to the Peak, this Pokemon V has no abilities')
      
      game.players[player].canUseVstarPower = False

      game.players[player].hand.append(game.players[player].deck.pop(cardDeckIndex))

      game.players[player].deck = game.shuffle(game.players[player].deck)

      return game
    
    raise Exception('cannot use Forest Seal Stone\'s Ability because player has already used a Vstar Power this game')
  
  def canPlay(self, game, player, opponent):
    if game.players[player].activePokemon.isV and game.players[player].activePokemon.tool == None:
      return True
    
    for pokemon in game.players[player].bench:
      if pokemon.isV and pokemon.tool == None:
        return True
      
    return False
  
class ChoiceBeltPE176:
  def __init__(self):
    self.cardType = CardType.Tool
    self.name = 'Choice Belt'
    self.text = 'The attacks of the Pokémon this card is attached to do 30 more damage to your opponent\'s Active Pokémon V (before applying Weakness and Resistance).'

  def canPlay(self, game, player, opponent):
    if game.players[player].activePokemon.tool == None:
      return True
    
    for pokemon in game.players[player].bench:
      if pokemon.tool == None:
        return True
      
    return False
  
class BoxOfDisasterLO214:
  def __init__(self):
    self.cardType = CardType.Tool
    self.name = 'Box Of Disaster'
    self.text = 'If the Pokémon V this card is attached to has full HP and is Knocked Out by damage from an attack from your opponent\'s Pokémon, put 8 damage counters on the Attacking Pokémon.'

  def canPlay(self, game, player, opponent):
    if game.players[player].activePokemon.tool == None:
      return True
    
    for pokemon in game.players[player].bench:
      if pokemon.tool == None:
        return True
      
    return False

class FusionStrikeEnergyFS244:
  def __init__(self):
    self.cardType = CardType.Energy
    self.name = 'Fusion Strike Energy'
    self.text = 'This card can only be attached to a Fusion Strike Pokémon. If this card is attached to anything other than a Fusion Strike Pokémon, discard this card. As long as this card is attached to a Pokémon, it provides every type of Energy but provides only 1 Energy at a time. Prevent all effects of your opponent\'s Pokémon\'s Abilities done to the Pokémon this card is attached to.'

  def attach(self, game, player, pokemonLocation, pokemonIndex = None):
    if pokemonLocation == 'activePokemon' and game.players[player].activePokemon.fusionStrike:
      game.players[player].activePokemon.attachedEnergy[EnergyType.FusionStrikeEnergy] += 1
    elif game.players[player].bench[pokemonIndex].fusionStrike:
      game.players[player].bench[pokemonIndex].attachedEnergy[EnergyType.FusionStrikeEnergy] += 1
    else:
      game.players[player].discardPile.append(self)

    return game
  
  def detach(self, game, player, pokemonLocation, pokemonIndex = None):
    if pokemonLocation == 'activePokemon':
      game.players[player].activePokemon.attachedEnergy[EnergyType.FusionStrikeEnergy] -= 1

      if game.players[player].activePokemon.attachedEnergy[EnergyType.FusionStrikeEnergy] < 0:
        raise Exception('cannot remove nonexistent Fusion Strike Energy from Pokemon')
      
      game.players[player].discardPile.append(self)
    else:
      game.players[player].bench[pokemonIndex].attachedEnergy[EnergyType.FusionStrikeEnergy] -= 1

      if game.players[player].bench[pokemonIndex].attachedEnergy[EnergyType.FusionStrikeEnergy] < 0:
        raise Exception('cannot remove nonexistent Fusion Strike Energy from Pokemon')
      
      game.players[player].discardPile.append(self)

    return game
  
  def canPlay(self, game, player, opponent):
    if game.players[player].activePokemon.fusionStrike:
      return True
    
    for pokemon in game.players[player].bench:
      if pokemon.fusionStrike:
        return True
    
    return False
  
class DoubleTurboEnergyBS151:
  def __init__(self):
    self.cardType = CardType.Energy
    self.name = 'Double Turbo Energy'
    self.text = 'As long as this card is attached to a Pokémon, it provides 2 Colorless Energy. The attacks of the Pokémon this card is attached to do 20 less damage to your opponent\'s Pokémon (before applying Weakness and Resistance).'

  def attach(self, game, player, pokemonLocation, pokemonIndex = None):
    if pokemonLocation == 'activePokemon':
      game.players[player].activePokemon.attachedEnergy[EnergyType.DoubleTurboEnergy] += 1
    else:
      game.players[player].bench[pokemonIndex].attachedEnergy[EnergyType.DoubleTurboEnergy] += 1

  def detach(self, game, player, pokemonLocation, pokemonIndex = None):
    if pokemonLocation == 'activePokemon':
      game.players[player].activePokemon.attachedEnergy[EnergyType.DoubleTurboEnergy] -= 1

      if game.players[player].activePokemon.attachedEnergy[EnergyType.DoubleTurboEnergy] < 0:
        raise Exception('cannot remove nonexistent Double Turbo Energy from Pokemon')
      
      game.players[player].discardPile.append(self)
    else:
      game.players[player].bench[pokemonIndex].attachedEnergy[EnergyType.DoubleTurboEnergy] -= 1

      if game.players[player].bench[pokemonIndex].attachedEnergy[EnergyType.DoubleTurboEnergy] < 0:
        raise Exception('cannot remove nonexistent Double Turbo Energy from Pokemon')
      
      game.players[player].discardPile.append(self)

    return game
  
  def canPlay(self, game, player, opponent):
    return True

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
    deck.append(LostVacuumLO217())

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
    raise Exception('Mew\'s Revenge does not have exactly 60 cards.')
  
  return deck