from enums import EnergyType, Stage, CardType
from player import Player
from cards import MewsRevenge, FusionStrikeEnergyFS244, DoubleTurboEnergyBS151
import random

class Game:
  def __init__(self, playerName1, player1Ai, playerName2, player2Ai):
    self.player1Name = playerName1
    self.player2Name = playerName2
    self.goesFirst = None
    self.winner = None
    self.players = {
      playerName1: Player(player1Ai, MewsRevenge()),
      playerName2: Player(player2Ai, MewsRevenge())
    }

  def activePokemonAttackChecks(self, player, opponent, attackAmt, mewVmaxCFS=False):
    doubleTurboEnergyAmt = self.players[player].activePokemon.attachedEnergy[EnergyType.DoubleTurboEnergy]

    doubleTurboEnergyReduction = doubleTurboEnergyAmt * 20

    attackAmt -= doubleTurboEnergyReduction

    if self.players[player]['playedPowerTabletFlag'] == True and self.players[player].activePokemon.fusionStrike == True:
      attackAmt += 30

    if (self.players[player].activePokemon.tool and self.players[player].activePokemon.tool.name == 'Choice Belt' 
              and self.players[opponent].activePokemon.isV == True):
      attackAmt += 30

    playerPokemonType = self.players[player].activePokemon.type

    if self.players[opponent].activePokemon.weakness == playerPokemonType:
      attackAmt *= self.players[opponent].activePokemon.weaknessFactor

    if self.players[opponent].activePokemon.resistance == playerPokemonType:
      attackAmt -= self.players[opponent].activePokemon.resitanceFactor

    oricorioFlag = False

    if self.players[opponent].activePokemon.fusionStrike:
      if self.players[opponent].activePokemon.name == 'Oricorio':
        oricorioFlag = True
      else:
        for pokemon in self.players[opponent].bench:
          if pokemon.name == 'Oricorio':
            oricorioFlag = True

    if oricorioFlag == True:
      attackAmt -= 20

    return attackAmt
  
  def shuffle(self, deck):
    deckSize = len(deck)

    shuffledDeck = []

    cardIndexes = list(range(0, deckSize))

    for i in range(deckSize):
      if len(cardIndexes) == 1:
        shuffledDeck.append(deck[cardIndexes[0]])
      else:
        index = cardIndexes.pop(random.randint(0, len(cardIndexes) - 1))
        shuffledDeck.append(deck[index])

    return shuffledDeck
  
  def energyForAttackCheck(self, energyAttached, energyRequirement):
    energyRequirementKeys = energyRequirement.keys()
    print(energyRequirementKeys)
    print(energyRequirement)

    canDoMoveFlag = True

    countingDoubleTurboEnergyFlag = False

    for key in list(energyRequirementKeys):
      for i in range(energyRequirement[key]):
        if energyAttached[key] > 0:
          energyAttached[key] -= 1
        elif energyAttached[EnergyType.DoubleTurboEnergy] > 0 and key == EnergyType.Colorless:
          if countingDoubleTurboEnergyFlag == False:
            countingDoubleTurboEnergyFlag = True
          else:
            countingDoubleTurboEnergyFlag = False
            energyAttached[EnergyType.DoubleTurboEnergy] -= 1
        elif key == EnergyType.Colorless:
          for energyType in [EnergyType.Grass, EnergyType.Fire, EnergyType.Water, EnergyType.Lightning, 
                  EnergyType.Psychic, EnergyType.Fighting, EnergyType.Darkness, EnergyType.Fairy,
                  EnergyType.Metal, EnergyType.Dragon]:
            if energyAttached[energyType] > 0:
              energyAttached[energyType] -= 1
              break
        elif energyAttached[EnergyType.FusionStrikeEnergy] > 0:
          energyAttached[EnergyType.FusionStrikeEnergy] -= 1
        else:
          canDoMoveFlag = False

    return canDoMoveFlag
  
  def putCardsAtBottomOfDeck(self, cards, deck):
    newDeck = []

    for card in cards:
      newDeck.append(card)

    for card in deck:
      newDeck.append(card)

    return newDeck
  
  def startGame(self):
    choose = random.randint(0, 1)

    if choose == 1:
      self.goesFirst = self.player1Name
    else:
      self.goesFirst = self.player2Name

    self.players[self.player1Name].deck = self.shuffle(self.players[self.player1Name].deck)
    self.players[self.player2Name].deck = self.shuffle(self.players[self.player2Name].deck)

    player1StartHand = []

    for i in range(7):
      player1StartHand.append(self.players[self.player1Name].deck.pop())

    player2StartHand = []

    for i in range(7):
      player2StartHand.append(self.players[self.player2Name].deck.pop())

    player1HasBasic = False

    for card in player1StartHand:
      if card.cardType == CardType.Pokemon and card.stage == Stage.Basic:
        player1HasBasic = True
        break

    player2HasBasic = False

    for card in player2StartHand:
      if card.cardType == CardType.Pokemon and card.stage == Stage.Basic:
        player2HasBasic = True
        break

    if (not player1HasBasic) and (not player2HasBasic):
      for card in player1StartHand:
        self.players[self.player1Name].deck.append(card)

      for card in player2StartHand:
        self.players[self.player2Name].deck.append(card)

      self.startGame()
    elif not player1HasBasic:
      player1StartHand, mulliganCount = self.mulligan(self.player1Name, player1StartHand)

      # maybe edit later so you can choose how many mulligan cards to draw? technically it is 'may'
      for i in range(mulliganCount):
        player2StartHand.append(self.players[self.player2Name].deck.pop())
    elif not player2HasBasic:
      player2StartHand, mulliganCount = self.mulligan(self.player2Name, player2StartHand)

      # maybe edit later so you can choose how many mulligan cards to draw? technically it is 'may'
      for i in range(mulliganCount):
        player1StartHand.append(self.players[self.player1Name].deck.pop())

    self.players[self.player1Name].hand = player1StartHand
    self.players[self.player2Name].hand = player2StartHand

    self.pickPrizeCards()

  def mulligan(self, player, previousHand, mulliganCount = 0):
    # show hand
    mulliganCount += 1

    for card in previousHand:
      self.players[player].deck.append(card)

    self.players[player].deck = self.shuffle(self.players[player].deck)

    playerNewHand = []

    for i in range(7):
      playerNewHand.append(self.players[player].deck.pop())

    hasBasic = False

    for card in playerNewHand:
      if card.cardType == CardType.Pokemon and card.stage == Stage.Basic:
        hasBasic = True
        break

    if hasBasic:
      return playerNewHand, mulliganCount
    else:
      return self.mulligan(player, playerNewHand, mulliganCount)
    
  def pickStartActivePokemon(self, player, handIndex):
    self.players[player].activePokemon = self.players[player].hand.pop(handIndex)

  def pickBenchPokemon(self, player, handIndex):
    self.players[player].bench.append(self.players[player].hand.pop(handIndex))

  def startTurn(self, player):
    self.players[player].activeTurn += 1

    self.players[player].hand.append(self.players[player].deck.pop())
  
  def playBasicPokemon(self, player, handIndex, playLocation):
    if playLocation == 'activePokemon' and self.players[player].activePokemon == None:
      self.players[player].activePokemon = self.players[player].hand.pop(handIndex)
    elif len(self.players[player].bench) < 5:
      self.players[player].bench.append(self.players[player].hand.pop(handIndex))
    else:
      raise Exception('can\'t play a pokemon there')
  
  def evolvePokemon(self, player, handIndex, formerPokemonLocation, formerPokemonIndex):
    if formerPokemonLocation == 'activePokemon':
      if self.players[player].activePokemon.name == self.players[player].hand[handIndex].evolvesFrom:
        self.players[player].activePokemon = self.players[player].hand.pop(handIndex)
    else:
      if self.players[player].bench[formerPokemonIndex].name == self.players[player].hand[handIndex].evolvesFrom:
        self.players[player].bench[formerPokemonIndex] = self.players[player].hand.pop(handIndex)

  def playItem(self, player, handIndex, effectParams):
    itemCard = self.players[player].hand[handIndex]

    self.players[player].hand[handIndex] = None

    self.updateSelf(itemCard.effect(self, player, **effectParams))

    self.players[player].discardPile.append(itemCard)

    self.players[player].hand = self.removeNullCards(self.players[player].hand)
  
  def playSupporter(self, player, handIndex, effectParams):
    if self.players[player].canUseSupporterFlag == True:
      supporterCard = self.players[player].hand[handIndex]

      self.players[player].hand[handIndex] = None

      self.updateSelf(supporterCard.effect(self, player, **effectParams))

      self.players[player].canUseSupporterFlag = False

      self.players[player].discardPile.append(supporterCard)

      self.players[player].hand = self.removeNullCards(self.players[player].hand)
    
    raise Exception('cannot play more than one supporter per turn')
    
  def playTool(self, player, handIndex, pokemonLocation, pokemonIndex = None):
    if pokemonLocation == 'activePokemon' and not self.players[player].activePokemon.tool:
      if self.players[player].activePokemon.isV == True or self.players[player].hand[handIndex].name != 'Path To The Peak':
        self.players[player].activePokemon.tool = self.players[player].hand[handIndex]
    elif not self.players[player].bench[pokemonIndex].tool:
      if self.players[player].bench[pokemonIndex].isV == True or self.players[player].hand[handIndex].name != 'Path To The Peak':
        self.players[player].bench[pokemonIndex].tool = self.players[player].hand[handIndex]
    else:
      raise Exception('Cannot add tool to Pokemon that already had a tool')
    
  def useToolEffect(self, player, opponent, effectParams, pokemonLocation, pokemonIndex = None):
    if pokemonLocation == 'activePokemon' and self.players[player].activePokemon.tool and self.players[player].activePokemon.tool.canUseEffect(self, player, opponent):
      self.players[player].activePokemon.tool.useEffect(self, player, **effectParams)
    elif self.players[player].bench[pokemonIndex].tool.canUseEffect(self, player, opponent):
      self.players[player].bench[pokemonIndex].tool.useEffect(self, player, **effectParams)
    else:
      raise Exception('Cannot use tool effect')

  def playStadium(self, player, opponent, handIndex):
    if self.players[player].canPlayStadiumFlag == True:
      if self.players[player].stadium:
        self.players[player].discardPile.append(self.players[player].stadium)
        self.players[player].stadium = None
      elif self.players[opponent].stadium:
        self.players[opponent].discardPile.append(self.players[opponent].stadium)
        self.players[opponent].stadium =None
      
      self.players[player].stadium = self.players[player].hand.pop(handIndex)

      self.players[player].canPlayStadiumFlag = False

    raise Exception('Can\'t play a Supporter more than once in a single turn')
  
  def useStadiumEffect(self, player, opponent, effectParams):
    if self.players[player].stadium:
      if effectParams == None:
        self.players[player].stadium.effect(self, player, opponent)
      else:
        self.players[player].stadium.effect(self, player, opponent, **effectParams)
    elif self.players[opponent].stadium:
      if effectParams == None:
        self.players[opponent].stadium.effect(self, player, opponent)
      else:
        self.players[opponent].stadium.effect(self, player, opponent, **effectParams)
    else:
      raise Exception('No stadium in play')
  
  def attachEnergy(self, player, energyHandIndex, pokemonLocation, pokemonIndex = None):
    energyCard = self.players[player].hand.pop(energyHandIndex)

    self = energyCard.attach(self, player, pokemonLocation, pokemonIndex)
  
  def usePokemonAbility(self, player, abilityParams, pokemonLocation, pokemonIndex = None):
    if pokemonLocation == 'activePokemon':
      self.updateSelf(self.players[player].activePokemon.ability['do'](self, player, **abilityParams))
    else:
      self.updateSelf(self.players[player].bench[pokemonIndex].ability['do'](self, player, **abilityParams))
  
  def attack(self, player, opponent, moveName, attackParams):
    boxOfDisasterAppliesToActivePokemon = False
    boxOfDisasterAppliesToBenchPokemon = []

    if (self.players[opponent].activePokemon.isV and self.players[opponent].activePokemon.tool.name == 'Box Of Disaster' and 
            self.players[opponent].activePokemon.hp == self.players[opponent].activePokemon.startHp):
      boxOfDisasterAppliesToActivePokemon = True

    for pokemon in self.players[opponent].bench:
      if pokemon.isV and pokemon.tool.name == 'Box Of Disaster' and pokemon.hp == pokemon.startHp:
        boxOfDisasterAppliesToBenchPokemon.append(True)
      else:
        boxOfDisasterAppliesToBenchPokemon.append(False)

    if not self.players[player].activePokemon.asleep and self.players[player].activePokemon.paralyzedCounter == 0 and self.players[player].activePokemonCantAttack == 0:
      self.updateSelf(self.players[player].activePokemon.moves[moveName]['do'](self, player, **attackParams))
    elif self.players[player].activePokemon.confused:
      coinFlip = random.randint(0, 1)

      if coinFlip:
        self.updateSelf(self.players[player].activePokemon.moves[moveName]['do'](self, player, **attackParams))
      else:
        self.players[player].activePokemon.hp -= 30
    else:
      raise Exception('this pokemon cannot attack')

    if self.players[player].activePokemon.hp <= 0:
      self.players[opponent].prizesToPick += self.players[player].activePokemon.prizesWhenKnockedOut

      if self.players[opponent].stadium.name == 'Lost City' or self.players[player].stadium.name == 'Lost City':
        self.players[player].lostZone.append(self.players[player].activePokemon)
      else:
        self.players[player].discardPile.append(self.players[player].activePokemon)
      
      self.players[player].activePokemon = None

    if self.players[opponent].activePokemon.hp <= 0:
      self.players[player].prizesToPick += self.players[opponent].activePokemon.prizesWhenKnockedOut

      if self.players[opponent].stadium.name == 'Lost City' or self.players[player].stadium.name == 'Lost City':
        self.players[opponent].lostZone.append(self.players[opponent].activePokemon)
      else:
        self.players[opponent].discardPile.append(self.players[opponent].activePokemon)
      
      self.players[opponent].activePokemon = None

    for index, pokemon in enumerate(self.players[player].bench):
      if pokemon.hp <= 0:
        self.players[opponent].prizesToPick += pokemon.prizesWhenKnockedOut

        if self.players[opponent].stadium.name == 'Lost City' or self.players[player].stadium.name == 'Lost City':
          self.players[player].lostZone.append(pokemon)
        else:
          self.players[player].discardPile.append(pokemon)
        
        self.players[player].bench[index] = None

    self.players[player].bench = self.removeNullCards(self.players[player].bench)

    for index, pokemon in enumerate(self.players[opponent].bench):
      if pokemon.hp <= 0:
        self.players[player].prizesToPick += pokemon.prizesWhenKnockedOut

    if self.players[player].prizesToPick >= len(self.players[player].prizes) and self.players[opponent].prizesToPick >= len(self.players[opponent].prizes):
      self.winner = 'tie'
    elif self.players[player].prizesToPick >= len(self.players[player].prizes):
      self.winner = player
    elif self.players[opponent].prizesToPick >= len(self.players[opponent].prizes):
      self.winner = opponent

    if boxOfDisasterAppliesToActivePokemon and self.players[opponent].activePokemon == None:
      self.players[player].activePokemon.hp -= 80

      if self.players[player].activePokemon.hp <= 0:
        self.players[opponent].prizesToPick += self.players[player].activePokemon.prizesWhenKnockedOut

        if self.players[opponent].prizesToPick >= len(self.players[opponent].prizes):
          self.winner = opponent

        if self.players[opponent].stadium.name == 'Lost City' or self.players[player].stadium.name == 'Lost City':
          self.players[player].lostZone.append(self.players[player].activePokemon)
        else:
          self.players[player].discardPile.append(self.players[player].activePokemon)
        
        self.players[player].activePokemon = None

    for index, pokemon in enumerate(self.players[opponent].bench):
      if pokemon.hp <= 0:
        if boxOfDisasterAppliesToBenchPokemon[index] == True:
          self.players[player].activePokemon.hp -= 80

          if self.players[player].activePokemon.hp <= 0:
            self.players[opponent].prizesToPick += self.players[player].activePokemon.prizesWhenKnockedOut

            if self.players[opponent].prizesToPick >= len(self.players[opponent].prizes):
              self.winner = opponent

            if self.players[opponent].stadium.name == 'Lost City' or self.players[player].stadium.name == 'Lost City':
              self.players[player].lostZone.append(self.players[player].activePokemon)
            else:
              self.players[player].discardPile.append(self.players[player].activePokemon)
            
            self.players[player].activePokemon = None

        if self.players[opponent].stadium.name == 'Lost City' or self.players[player].stadium.name == 'Lost City':
          self.players[opponent].lostZone.append(self.players[opponent].activePokemon)
        else:
          self.players[opponent].discardPile.append(self.players[opponent].activePokemon)
        
        self.players[player].bench[index] = None

    self.players[opponent].bench = self.removeNullCards(self.players[opponent].bench)

  
  def drawPrizes(self, player, prizeIndexes):
    for index in prizeIndexes:
      self.players[player].hand.append(self.players[player].prizes[index])

      self.players[player].prizes[index] = None

    self.players[player].prizes = self.removeNullCards(self.players[player].prizes)

  def retreat(self, player, newPokemonIndex, energyToDiscard):
    if self.players[player].activePokemon.asleep == True or self.players[player].activePokemon.paralyzedCounter > 0:
      raise Exception('Pokemon cannot retreat if asleep or paralyzed')

    if len(self.players[player].bench) > 0:
      for energy in energyToDiscard:
        if self.players[player].activePokemon.attachedEnergy[energy] > 0:
          self.players[player].activePokemon.attachedEnergy[energy] -= 1

          if energy == EnergyType.FusionStrikeEnergy:
            self.players[player].discardPile.append(FusionStrikeEnergyFS244())
          elif energy == EnergyType.DoubleTurboEnergy:
            self.players[player].discardPile.append(DoubleTurboEnergyBS151())
        
        raise Exception('cannot discard energy for retreat that isn\'t there')

      newPokemon = self.players[player].bench.pop(newPokemonIndex)

      self.players[player].activePokemon.burned = False

      self.players[player].activePokemon.poisoned = False

      self.players[player].activePokemon.confused = False

      self.players[player].bench.append(self.players[player].activePokemon)

      self.players[player].activePokemon = newPokemon

      self.players[player].canRetreat = False

      self.players[player].activePokemonCantAttack = 0

    raise Exception('cannot retreat if there are no benched Pokemon')
  
  def evolve(self, player, currentPokemonLocation, currentPokemonIndex, evolvedPokemonHandIndex):
    if currentPokemonLocation == 'activePokemon' and self.players[player].activePokemon.canEvolve:
      canEvolveToThisPokemon = False

      for pokemon in self.players[player].activePokemon.evolvesFrom:
        if pokemon.name == self.players[player].hand[evolvedPokemonHandIndex]:
          canEvolveToThisPokemon = True
          break
      
      if canEvolveToThisPokemon:
        self.players[player].hand[evolvedPokemonHandIndex].hp = (self.players[player].hand[evolvedPokemonHandIndex].startHp - 
            (self.players[player].activePokemon.startHp - self.players[player].activePokemon.hp))
        
        if self.players[player].activePokemon.tool:
          self.players[player].hand[evolvedPokemonHandIndex].tool = self.players[player].activePokemon.tool

        self.players[player].hand[evolvedPokemonHandIndex].attachedEnergy[EnergyType.FusionStrikeEnergy] = self.players[player].activePokemon.attachedEnergy[EnergyType.FusionStrikeEnergy]

        self.players[player].hand[evolvedPokemonHandIndex].attachedEnergy[EnergyType.DoubleStrikeEnergy] = self.players[player].activePokemon.attachedEnergy[EnergyType.DoubleStrikeEnergy]

        self.players[player].activePokemon = self.players[player].hand[evolvedPokemonHandIndex]

    elif self.players[player].bench[currentPokemonIndex].canEvolve:
      canEvolveToThisPokemon = False

      for pokemon in self.players[player].bench[currentPokemonIndex].evolvesFrom:
        if pokemon.name == self.players[player].hand[evolvedPokemonHandIndex]:
          canEvolveToThisPokemon = True
          break
        
      if canEvolveToThisPokemon:
        self.players[player].hand[evolvedPokemonHandIndex].hp = (self.players[player].hand[evolvedPokemonHandIndex].startHp - 
            (self.players[player].bench[currentPokemonIndex].startHp - self.players[player].bench[currentPokemonIndex].hp))
        
        if self.players[player].bench[currentPokemonIndex].tool:
          self.players[player].hand[evolvedPokemonHandIndex].tool = self.players[player].bench[currentPokemonIndex].tool

        self.players[player].hand[evolvedPokemonHandIndex].attachedEnergy[EnergyType.FusionStrikeEnergy] = self.players[player].bench[currentPokemonIndex].attachedEnergy[EnergyType.FusionStrikeEnergy]

        self.players[player].hand[evolvedPokemonHandIndex].attachedEnergy[EnergyType.DoubleStrikeEnergy] = self.players[player].bench[currentPokemonIndex].attachedEnergy[EnergyType.DoubleStrikeEnergy]

        self.players[player].bench[currentPokemonIndex] = self.players[player].hand[evolvedPokemonHandIndex]

  def startTurn(self, player):
    self.players[player].activeTurn += 1

    if self.players[player].activeTurn == 1 and player == self.goesFirst:
      self.players[player].canUseSupporterFlag = False

    print(f'{player} draws a card.')

    self.players[player].hand.append(self.players[player].deck.pop())

  def endTurn(self, player, opponent):
    # add print to narrate
    if self.players[player].activePokemon.poisoned:
      self.players[player].activePokemon += 10

      if self.players[player].activePokemon.hp <= 0:
        self.players[opponent].prizesToPick += self.players[player].activePokemon.prizesWhenKnockedOut

        if self.players[opponent].prizesToPick >= len(self.players[opponent].prizes):
          self.winner = opponent
          return

        if self.players[opponent].stadium.name == 'Lost City' or self.players[player].stadium.name == 'Lost City':
          self.players[player].lostZone.append(self.players[player].activePokemon)
        else:
          self.players[player].discardPile.append(self.players[player].activePokemon)
        
        self.players[player].activePokemon = None

    if self.players[player].activePokemon.burned:
      self.players[player].activePokemon += 20

      if self.players[player].activePokemon.hp <= 0:
        self.players[opponent].prizesToPick += self.players[player].activePokemon.prizesWhenKnockedOut

        if self.players[opponent].prizesToPick >= len(self.players[opponent].prizes):
          self.winner = opponent
          return
        
        if self.players[opponent].stadium.name == 'Lost City' or self.players[player].stadium.name == 'Lost City':
          self.players[player].lostZone.append(self.players[player].activePokemon)
        else:
          self.players[player].discardPile.append(self.players[player].activePokemon)
        
        self.players[player].activePokemon = None

    if self.players[player].activePokemon.asleep:
      coinFlip = random.randint(0, 1)

      if coinFlip:
        self.players[player].activePokemon.asleep = False
      
    if self.players[player].activePokemon.paralyzedCounter == 1:
      self.players[player].activePokemon.paralyzedCounter += 1
    if self.players[player].activePokemon.paralyzedCounter == 2:
      self.players[player].activePokemon.paralyzedCounter = 0

    if self.players[player].activePokemonCantAttack == 1:
      self.players[player].activePokemonCantAttack = 2
    if self.players[player].activePokemonCantAttack == 2:
      self.players[player].activePokemonCantAttack = 0

    self.players[player].canUseSupporterFlag = True
    self.players[player].canPlayStadiumFlag = True
    self.players[player].playedPowerTabletFlag = False
    self.players[player].canRetreat = True
    self.players[player].canAttachEnergy = True

    self.players[player].activePokemon.canEvolve = True

    for index in enumerate(self.players[player].bench):
      self.players[player].bench[index].canEvolve = True

  def pickNewActivePokemonFromBench(self, player, opponent, pokemonIndex):
    if len(self.players[player].bench) == 0:
      self.winner = opponent
      return
    
    self.players[player].activePokemon = self.players[player].bench.pop(pokemonIndex)

  def pickPrizeCards(self):
    for i in range(6):
      self.players[self.player1Name].prizes.append(self.players[self.player1Name].deck.pop())

    for i in range(6):
      self.players[self.player2Name].prizes.append(self.players[self.player2Name].deck.pop())

  def updateSelf(self, changedGame):
    self.players[self.player1Name] = changedGame[self.player1Name]
    self.players[self.player2Name] = changedGame[self.player2Name]

  def removeNullCards(self, cards):
      # used because sometimes multiple cards are removed and you don\'t want to affect indexes midway through
      for i in range(len(cards)):
        if cards[len(cards) - 1 - i] == None:
          cards.pop(len(cards) - 1 - i)

      return cards
  
  def discardPokemonAndAttachedCards(self, player, pokemonLocation, pokemonIndex):
    if pokemonLocation == 'activePokemon':
      if self.players[player].activePokemon.evolvesFrom:
        self.players[player].discardPile.append(self.players[player].activePokemon.evolvesFrom)

      if self.players[player].activePokemon.tool:
        self.players[player].discardPile.append(self.players[player].activePokemon.tool)
        self.players[player].activePokemon.tool = None

      if self.players[player].activePokemon.attachedEnergy[EnergyType.FusionStrikeEnergy] > 0:
        for i in range(self.players[player].activePokemon.attachedEnergy[EnergyType.FusionStrikeEnergy]):
          self.players[player].discardPile.append(FusionStrikeEnergyFS244())
        self.players[player].activePokemon.attachedEnergy[EnergyType.FusionStrikeEnergy] = 0

      if self.players[player].activePokemon.attachedEnergy[EnergyType.DoubleTurboEnergy] > 0:
        for i in range(self.players[player].activePokemon.attachedEnergy[EnergyType.DoubleTurboEnergy]):
          self.players[player].discardPile.append(DoubleTurboEnergyBS151())
        self.players[player].activePokemon.attachedEnergy[EnergyType.DoubleTurboEnergy] = 0

      self.players[player].activePokemon.hp = self.players[player].activePokemon.startHp
      self.players[player].activePokemon.burned = False
      self.players[player].activePokemon.poisoned = False
      self.players[player].activePokemon.paralyzed = False
      self.players[player].activePokemon.confused = False
      self.players[player].activePokemon.asleep = False

      self.players[player].discardPile.append(self.players[player].activePokemon)

      self.players[player].activePokemon = None

    else:
      if self.players[player].bench[pokemonIndex].evolvesFrom:
        self.players[player].discardPile.append(self.players[player].bench[pokemonIndex].evolvesFrom)

      if self.players[player].bench[pokemonIndex].tool:
        self.players[player].discardPile.append(self.players[player].bench[pokemonIndex].tool)
        self.players[player].bench[pokemonIndex].tool = None

      if self.players[player].bench[pokemonIndex].attachedEnergy[EnergyType.FusionStrikeEnergy] > 0:
        for i in range(self.players[player].bench[pokemonIndex].attachedEnergy[EnergyType.FusionStrikeEnergy]):
          self.players[player].discardPile.append(FusionStrikeEnergyFS244())
        self.players[player].bench[pokemonIndex].attachedEnergy[EnergyType.FusionStrikeEnergy] = 0

      if self.players[player].bench[pokemonIndex].attachedEnergy[EnergyType.DoubleTurboEnergy] > 0:
        for i in range(self.players[player].bench[pokemonIndex].attachedEnergy[EnergyType.DoubleTurboEnergy]):
          self.players[player].discardPile.append(DoubleTurboEnergyBS151())
        self.players[player].bench[pokemonIndex].attachedEnergy[EnergyType.DoubleTurboEnergy] = 0

      self.players[player].bench[pokemonIndex].hp = self.players[player].bench[pokemonIndex].startHp
      self.players[player].bench[pokemonIndex].burned = False
      self.players[player].bench[pokemonIndex].poisoned = False
      self.players[player].bench[pokemonIndex].paralyzed = False
      self.players[player].bench[pokemonIndex].confused = False
      self.players[player].bench[pokemonIndex].asleep = False

      self.players[player].discardPile.append(self.players[player].bench[pokemonIndex])

      self.players[player].bench.pop(pokemonIndex)

  def lostZonePokemonAndAttachedCard(self, player, pokemonLocation, pokemonIndex):
    if pokemonLocation == 'activePokemon':
      if self.players[player].activePokemon.evolvesFrom:
        self.players[player].lostZone.append(self.players[player].activePokemon.evolvesFrom)

      if self.players[player].activePokemon.tool:
        self.players[player].lostZone.append(self.players[player].activePokemon.tool)
        self.players[player].activePokemon.tool = None

      if self.players[player].activePokemon.attachedEnergy[EnergyType.FusionStrikeEnergy] > 0:
        for i in range(self.players[player].activePokemon.attachedEnergy[EnergyType.FusionStrikeEnergy]):
          self.players[player].lostZone.append(FusionStrikeEnergyFS244())
        self.players[player].activePokemon.attachedEnergy[EnergyType.FusionStrikeEnergy] = 0

      if self.players[player].activePokemon.attachedEnergy[EnergyType.DoubleTurboEnergy] > 0:
        for i in range(self.players[player].activePokemon.attachedEnergy[EnergyType.DoubleTurboEnergy]):
          self.players[player].lostZone.append(DoubleTurboEnergyBS151())
        self.players[player].activePokemon.attachedEnergy[EnergyType.DoubleTurboEnergy] = 0

      self.players[player].activePokemon.hp = self.players[player].activePokemon.startHp
      self.players[player].activePokemon.burned = False
      self.players[player].activePokemon.poisoned = False
      self.players[player].activePokemon.paralyzed = False
      self.players[player].activePokemon.confused = False
      self.players[player].activePokemon.asleep = False

      self.players[player].lostZone.append(self.players[player].activePokemon)

      self.players[player].activePokemon = None

    else:
      if self.players[player].bench[pokemonIndex].evolvesFrom:
        self.players[player].lostZone.append(self.players[player].bench[pokemonIndex].evolvesFrom)

      if self.players[player].bench[pokemonIndex].tool:
        self.players[player].lostZone.append(self.players[player].bench[pokemonIndex].tool)
        self.players[player].bench[pokemonIndex].tool = None

      if self.players[player].bench[pokemonIndex].attachedEnergy[EnergyType.FusionStrikeEnergy] > 0:
        for i in range(self.players[player].bench[pokemonIndex].attachedEnergy[EnergyType.FusionStrikeEnergy]):
          self.players[player].lostZone.append(FusionStrikeEnergyFS244())
        self.players[player].bench[pokemonIndex].attachedEnergy[EnergyType.FusionStrikeEnergy] = 0

      if self.players[player].bench[pokemonIndex].attachedEnergy[EnergyType.DoubleTurboEnergy] > 0:
        for i in range(self.players[player].bench[pokemonIndex].attachedEnergy[EnergyType.DoubleTurboEnergy]):
          self.players[player].lostZone.append(DoubleTurboEnergyBS151())
        self.players[player].bench[pokemonIndex].attachedEnergy[EnergyType.DoubleTurboEnergy] = 0

      self.players[player].bench[pokemonIndex].hp = self.players[player].bench[pokemonIndex].startHp
      self.players[player].bench[pokemonIndex].burned = False
      self.players[player].bench[pokemonIndex].poisoned = False
      self.players[player].bench[pokemonIndex].paralyzed = False
      self.players[player].bench[pokemonIndex].confused = False
      self.players[player].bench[pokemonIndex].asleep = False

      self.players[player].lostZone.append(self.players[player].bench[pokemonIndex])

      self.players[player].bench.pop(pokemonIndex)