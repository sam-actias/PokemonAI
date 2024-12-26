from enums import EnergyType, Stage
from player import Player
from cards import MewsRevenge, FusionStrikeEnergyFS244, DoubleTurboEnergyBS151
import random

class Game:
  def __init__(self, playerName1, playerName2):
    self.player1Name = playerName1
    self.player2Name = playerName2
    self.goesFirst = None
    self[playerName1] = Player(MewsRevenge())
    self[playerName2] = Player(MewsRevenge())

  def activePokemonAttackChecks(self, player, opponent, attackAmt, mewVmaxCFS=False):
    doubleTurboEnergyAmt = self[player].activePokemon.attachedEnergy[EnergyType.DoubleTurboEnergy]

    doubleTurboEnergyReduction = doubleTurboEnergyAmt * 20

    attackAmt -= doubleTurboEnergyReduction

    if self[player]['playedPowerTabletFlag'] == True and self[player].activePokemon.fusionStrike == True:
      attackAmt += 30

    if (self[player].activePokemon.tool and self[player].activePokemon.tool.name == 'ChoiceBeltPE176' 
              and self[opponent].activePokemon.isV == True):
      attackAmt += 30

    playerPokemonType = self[player].activePokemon.type

    if self[opponent].activePokemon.weakness == playerPokemonType:
      attackAmt *= self[opponent].activePokemon.weaknessFactor

    if self[opponent].activePokemon.resistance == playerPokemonType:
      attackAmt -= self[opponent].activePokemon.resitanceFactor

    oricorioFlag = False

    if self[opponent].activePokemon.fusionStrike:
      if self[opponent].activePokemon.name == 'OricorioFS42':
        oricorioFlag = True
      else:
        for pokemon in self[opponent].bench:
          if pokemon.name == 'OricorioFS42':
            oricorioFlag = True

    if oricorioFlag == True:
      attackAmt -= 20

    return attackAmt
  
  def shuffle(self, deck):
    deckSize = len(deck)

    shuffledDeck = []

    cardIndexes = list(range(0, deckSize))

    for cardIndex in cardIndexes:
      if len(cardIndexes) == 1:
        shuffledDeck.append(deck[cardIndexes[0]])
      else:
        index = cardIndex.pop(random.randInt(0, len(cardIndexes) - 1))
        shuffledDeck.append(deck[index])

    return shuffledDeck
  
  def energyForAttackCheck(self, energyAttached, energyRequirement):
    energyRequirementKeys = energyRequirement.keys()

    canDoMoveFlag = True

    countingDoubleTurboEnergyFlag = False

    for key in energyRequirementKeys:
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
    self[self.player1Name].deck = self.shuffle(self[self.player1Name].deck)
    self[self.player2Name].deck = self.shuffle(self[self.player2Name].deck)

    player1StartHand = []

    for i in range(7):
      player1StartHand.append(self[self.player1Name].deck.pop())

    player2StartHand = []

    for i in range(7):
      player2StartHand.append(self[self.player2Name].deck.pop())

    player1HasBasic = False

    for card in player1StartHand:
      if card.stage == Stage.Basic:
        player1HasBasic = True
        break

    player2HasBasic = False

    for card in player2StartHand:
      if card.stage == Stage.Basic:
        player2HasBasic = True
        break

    if not player1HasBasic and not player2HasBasic:
      self.startGame()
    elif not player1HasBasic:
      player1StartHand, mulliganCount = self.mulligan(self.player1Name, player1StartHand)

      # maybe edit later so you can choose how many mulligan cards to draw? technically it is 'may'
      for i in range(mulliganCount):
        player2StartHand.append(self[self.player2Name].deck.pop())
    elif not player2HasBasic:
      player2StartHand, mulliganCount = self.mulligan(self.player2Name, player2StartHand)

      # maybe edit later so you can choose how many mulligan cards to draw? technically it is 'may'
      for i in range(mulliganCount):
        player1StartHand.append(self[self.player1Name].deck.pop())

    self[self.player1Name].hand = player1StartHand
    self[self.player2Name].hand = player2StartHand

    return self

  def mulligan(self, player, previousHand, mulliganCount = 0):
    # show hand

    mulliganCount += 1

    for card in previousHand:
      self[player].deck.append(card)

    self[player].deck = self.shuffle(self[player].deck)

    playerNewHand = []

    for i in range(7):
      playerNewHand.append(self[player].deck.pop())

    hasBasic = False

    for card in playerNewHand:
      if card.stage == Stage.Basic:
        hasBasic = True
        break

    if hasBasic:
      return { playerNewHand, mulliganCount }
    else:
      return self.mulligan(player, playerNewHand, mulliganCount)
    
  def pickStartActivePokemon(self, player, handIndex):
    self[player].activePokemon = self[player].hand.pop(handIndex)

  def pickBenchPokemon(self, player, handIndex):
    self[player].bench.append(self[player].hand.pop(handIndex))

  def doTurn(self, player):
    self[player].activeTurn += 1

    # if len(self[player].deck) == 0:
      # insert lose actions

    self[player].hand.append(self[player].deck.pop())

    return self
  
  def playBasicPokemon(self, player, handIndex, playLocation):
    if playLocation == 'activePokemon' and self[player].activePokemon == None:
      self[player].activePokemon = self[player].hand.pop(handIndex)
    elif len(self[player].bench) < 5:
      self[player].bench.append(self[player].hand.pop(handIndex))
    else:
      raise Exception('can\'t play a pokemon there')
    
    return self
  
  def evolvePokemon(self, player, handIndex, formerPokemonLocation, formerPokemonIndex):
    if formerPokemonLocation == 'activePokemon':
      if self[player].activePokemon.name == self[player].hand[handIndex].evolvesFrom:
        self[player].activePokemon = self[player].hand.pop(handIndex)
    else:
      if self[player].bench[formerPokemonIndex].name == self[player].hand[handIndex].evolvesFrom:
        self[player].bench[formerPokemonIndex] = self[player].hand.pop(handIndex)

    return self

  def playItem(self, player, handIndex, effectParams):
    itemCard = self[player].hand[handIndex]

    self[player].hand[handIndex] = None

    self.updateSelf(itemCard.effect(self, player, **effectParams))

    self[player].discardPile.append(itemCard)

    self[player].hand = self.removeNullCards(self[player].hand)

    return self
  
  def playSupporter(self, player, handIndex, effectParams):
    if self[player].canUseSupporterFlag == True:
      supporterCard = self[player].hand[handIndex]

      self[player].hand[handIndex] = None

      self.updateSelf(supporterCard.effect(self, player, **effectParams))

      self[player].canUseSupporterFlag = False

      self[player].discardPile.append(supporterCard)

      self[player].hand = self.removeNullCards(self[player].hand)

      return self
    
    raise Exception('cannot play more than one supporter per turn')
    
  def playTool(self, player, handIndex, pokemonLocation, pokemonIndex = None):
    if pokemonLocation == 'activePokemon' and not self[player].activePokemon.tool:
      if self[player].activePokemon.isV == True or self[player].hand[handIndex].name != 'PathToThePeakCR148':
        self[player].activePokemon.tool = self[player].hand[handIndex]
    elif not self[player].bench[pokemonIndex].tool:
      if self[player].bench[pokemonIndex].isV == True or self[player].hand[handIndex].name != 'PathToThePeakCR148':
        self[player].bench[pokemonIndex].tool = self[player].hand[handIndex]
    else:
      raise Exception('Cannot add tool to Pokemon that already had a tool')
    
    return self
    
  def useToolAbility(self, player, effectParams, pokemonLocation, pokemonIndex = None):
    if pokemonLocation == 'activePokemon' and self[player].activePokemon.tool:
      self[player].activePokemon.tool.useAbility(self, player, **effectParams)
    else:
      self[player].bench[pokemonIndex].tool.useAbility(self, player, **effectParams)

  def playStadium(self, player, opponent, handIndex):
    if self[player].stadium:
      self[player].discardPile.append(self[player].stadium)
      self[player].stadium = None
    elif self[opponent].stadium:
      self[opponent].discardPile.append(self[opponent].stadium)
      self[opponent].stadium =None

    self[player].stadium = self[player].hand.pop(handIndex)

    return self
  
  def usePokemonAbility(self, player, abilityParams, pokemonLocation, pokemonIndex = None):
    if pokemonLocation == 'activePokemon':
      self.updateSelf(self[player].activePokemon.ability['do'](self, player, **abilityParams))
    else:
      self.updateSelf(self[player].bench[pokemonIndex].ability['do'](self, player, **abilityParams))

    return self
  
  def attack(self, player, opponent, moveName, attackParams):
    if not self[player].activePokemon.asleep and self[player].activePokemon.paralyzedCounter == 0:
      self.updateSelf(self[player].activePokemon.moves[moveName]['do'](self, player, **attackParams))
    elif self[player].activePokemon.confused:
      coinFlip = random.randint(0, 1)

      if coinFlip:
        self.updateSelf(self[player].activePokemon.moves[moveName]['do'](self, player, **attackParams))
      else:
        self[player].activePokemon.hp -= 30
    else:
      raise Exception('this pokemon cannot attack')

    if self[player].activePokemon.hp <= 0:
      self[opponent].prizesToPick += self[player].activePokemon.prizesWhenKnockedOut

    if self[opponent].activePokemon.hp <= 0:
      self[player].prizesToPick += self[opponent].activePokemon.prizesWhenKnockedOut

    if self[player].prizesToPick >= len(self[player].prizes) and self[opponent].prizesToPick >= len(self[opponent].prizes):
      self.winner = 'tie'
    elif self[player].prizesToPick >= len(self[player].prizes):
      self.winner = player
    elif self[opponent].prizesToPick >= len(self[opponent].prizes):
      self.winner = opponent

    return self
  
  def drawPrizes(self, player, prizeIndexes):
    for index in prizeIndexes:
      self[player].hand.append(self[player].prizes[index])

      self[player].prizes[index] = None

    self[player].prizes = self.removeNullCards(self[player].prizes)

    return self

  def retreat(self, player, newPokemonIndex, energyToDiscard):
    if self[player].activePokemon.asleep == True or self[player].activePokemon.paralyzedCounter > 0:
      raise Exception('Pokemon cannot retreat if asleep or paralyzed')

    if len(self[player].bench) > 0:
      for energy in energyToDiscard:
        if self[player].activePokemon.attachedEnergy[energy] > 0:
          self[player].activePokemon.attachedEnergy[energy] -= 1

          if energy == EnergyType.FusionStrikeEnergy:
            self[player].discardPile.append(FusionStrikeEnergyFS244())
          elif energy == EnergyType.DoubleTurboEnergy:
            self[player].discardPile.append(DoubleTurboEnergyBS151())
        
        raise Exception('cannot discard energy for retreat that isn\'t there')

      newPokemon = self[player].bench.pop(newPokemonIndex)

      self[player].activePokemon.burned = False

      self[player].activePokemon.poisoned = False

      self[player].activePokemon.confused = False

      self[player].bench.append(self[player].activePokemon)

      self[player].activePokemon = newPokemon

    raise Exception('cannot retreat if there are no benched Pokemon')
  
  def endTurn(self, player, opponent, opponentNewActivePokemonIndex = None, playerAttackPrizeIndexes = None):
    if self[player].activePokemon.poisoned:
      self[player].activePokemon += 10

      if self[player].activePokemon.hp <= 0:
        self[opponent].prizesToPick += self[player].activePokemon.prizesWhenKnockedOut

      if self[opponent].prizesToPick >= len(self[opponent].prizes):
        self.winner = opponent
        return self
    
    if self[player].activePokemon.burned:
      self[player].activePokemon += 20

      if self[player].activePokemon.hp <= 0:
        self[opponent].prizesToPick += self[player].activePokemon.prizesWhenKnockedOut

      if self[opponent].prizesToPick >= len(self[opponent].prizes):
        self.winner = opponent
        return self

    if self[player].activePokemon.asleep:
      coinFlip = random.randint(0, 1)

      if coinFlip:
        self[player].activePokemon.asleep = False
      
    if self[player].activePokemon.paralyzedCounter == 1:
      self[player].activePokemon.paralyzedCounter += 1
    if self[player].activePokemon.paralyzedCounter == 2:
      self[player].activePokemon.paralyzedCounter = 0

    return self

  def pickNewActivePokemonFromBench(self, player, opponent, pokemonIndex):
    if len(self[player].bench) == 0:
      self.winner = opponent
      return self
    
    self[player].activePokemon = self[player].bench.pop(pokemonIndex)

    return self

  def updateSelf(self, changedGame):
    self[self.player1Name] = changedGame[self.player1Name]
    self[self.player2Name] = changedGame[self.player2Name]

  def removeNullCards(self, cards):
      # used because sometimes multiple cards are removed and you don\'t want to affect indexes midway through
      for i in range(len(cards)):
        if cards[len(cards) - 1 - i] == None:
          cards.pop(len(cards) - 1 - i)

      return cards