from enums import EnergyType, Stage, CardType
from player import Player
from cards import MewsRevenge, FusionStrikeEnergyFS244, DoubleTurboEnergyBS151
import random

class Game:
  def __init__(self, playerName1, playerName2):
    self.player1Name = playerName1
    self.player2Name = playerName2
    self.goesFirst = None
    self.players = {
      playerName1: Player(MewsRevenge()),
      playerName2: Player(MewsRevenge())
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

    if not player1HasBasic and not player2HasBasic:
      for card in player1StartHand:
        self.players[self.player1Name].deck.append(card)

      for card in player2StartHand:
        self.players[self.player2Name].deck.append(card)

      return self.startGame()
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

    return self

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

  def doTurn(self, player):
    self.players[player].activeTurn += 1

    # if len(self.players[player].deck) == 0:
      # insert lose actions

    self.players[player].hand.append(self.players[player].deck.pop())

    return self
  
  def playBasicPokemon(self, player, handIndex, playLocation):
    if playLocation == 'activePokemon' and self.players[player].activePokemon == None:
      self.players[player].activePokemon = self.players[player].hand.pop(handIndex)
    elif len(self.players[player].bench) < 5:
      self.players[player].bench.append(self.players[player].hand.pop(handIndex))
    else:
      raise Exception('can\'t play a pokemon there')
    
    return self
  
  def evolvePokemon(self, player, handIndex, formerPokemonLocation, formerPokemonIndex):
    if formerPokemonLocation == 'activePokemon':
      if self.players[player].activePokemon.name == self.players[player].hand[handIndex].evolvesFrom:
        self.players[player].activePokemon = self.players[player].hand.pop(handIndex)
    else:
      if self.players[player].bench[formerPokemonIndex].name == self.players[player].hand[handIndex].evolvesFrom:
        self.players[player].bench[formerPokemonIndex] = self.players[player].hand.pop(handIndex)

    return self

  def playItem(self, player, handIndex, effectParams):
    itemCard = self.players[player].hand[handIndex]

    self.players[player].hand[handIndex] = None

    self.updateSelf(itemCard.effect(self, player, **effectParams))

    self.players[player].discardPile.append(itemCard)

    self.players[player].hand = self.removeNullCards(self.players[player].hand)

    return self
  
  def playSupporter(self, player, handIndex, effectParams):
    if self.players[player].canUseSupporterFlag == True:
      supporterCard = self.players[player].hand[handIndex]

      self.players[player].hand[handIndex] = None

      self.updateSelf(supporterCard.effect(self, player, **effectParams))

      self.players[player].canUseSupporterFlag = False

      self.players[player].discardPile.append(supporterCard)

      self.players[player].hand = self.removeNullCards(self.players[player].hand)

      return self
    
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
    
    return self
    
  def useToolAbility(self, player, effectParams, pokemonLocation, pokemonIndex = None):
    if pokemonLocation == 'activePokemon' and self.players[player].activePokemon.tool:
      self.players[player].activePokemon.tool.useAbility(self, player, **effectParams)
    else:
      self.players[player].bench[pokemonIndex].tool.useAbility(self, player, **effectParams)

  def playStadium(self, player, opponent, handIndex):
    if self.players[player].stadium:
      self.players[player].discardPile.append(self.players[player].stadium)
      self.players[player].stadium = None
    elif self.players[opponent].stadium:
      self.players[opponent].discardPile.append(self.players[opponent].stadium)
      self.players[opponent].stadium =None

    self.players[player].stadium = self.players[player].hand.pop(handIndex)

    return self
  
  def usePokemonAbility(self, player, abilityParams, pokemonLocation, pokemonIndex = None):
    if pokemonLocation == 'activePokemon':
      self.updateSelf(self.players[player].activePokemon.ability['do'](self, player, **abilityParams))
    else:
      self.updateSelf(self.players[player].bench[pokemonIndex].ability['do'](self, player, **abilityParams))

    return self
  
  def attack(self, player, opponent, moveName, attackParams):
    if not self.players[player].activePokemon.asleep and self.players[player].activePokemon.paralyzedCounter == 0:
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

    if self.players[opponent].activePokemon.hp <= 0:
      self.players[player].prizesToPick += self.players[opponent].activePokemon.prizesWhenKnockedOut

    if self.players[player].prizesToPick >= len(self.players[player].prizes) and self.players[opponent].prizesToPick >= len(self.players[opponent].prizes):
      self.winner = 'tie'
    elif self.players[player].prizesToPick >= len(self.players[player].prizes):
      self.winner = player
    elif self.players[opponent].prizesToPick >= len(self.players[opponent].prizes):
      self.winner = opponent

    return self
  
  def drawPrizes(self, player, prizeIndexes):
    for index in prizeIndexes:
      self.players[player].hand.append(self.players[player].prizes[index])

      self.players[player].prizes[index] = None

    self.players[player].prizes = self.removeNullCards(self.players[player].prizes)

    return self

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

    raise Exception('cannot retreat if there are no benched Pokemon')
  
  def endTurn(self, player, opponent, opponentNewActivePokemonIndex = None, playerAttackPrizeIndexes = None):
    if self.players[player].activePokemon.poisoned:
      self.players[player].activePokemon += 10

      if self.players[player].activePokemon.hp <= 0:
        self.players[opponent].prizesToPick += self.players[player].activePokemon.prizesWhenKnockedOut

      if self.players[opponent].prizesToPick >= len(self.players[opponent].prizes):
        self.winner = opponent
        return self
    
    if self.players[player].activePokemon.burned:
      self.players[player].activePokemon += 20

      if self.players[player].activePokemon.hp <= 0:
        self.players[opponent].prizesToPick += self.players[player].activePokemon.prizesWhenKnockedOut

      if self.players[opponent].prizesToPick >= len(self.players[opponent].prizes):
        self.winner = opponent
        return self

    if self.players[player].activePokemon.asleep:
      coinFlip = random.randint(0, 1)

      if coinFlip:
        self.players[player].activePokemon.asleep = False
      
    if self.players[player].activePokemon.paralyzedCounter == 1:
      self.players[player].activePokemon.paralyzedCounter += 1
    if self.players[player].activePokemon.paralyzedCounter == 2:
      self.players[player].activePokemon.paralyzedCounter = 0

    return self

  def pickNewActivePokemonFromBench(self, player, opponent, pokemonIndex):
    if len(self.players[player].bench) == 0:
      self.winner = opponent
      return self
    
    self.players[player].activePokemon = self.players[player].bench.pop(pokemonIndex)

    return self

  def updateSelf(self, changedGame):
    self.players[self.player1Name] = changedGame[self.player1Name]
    self.players[self.player2Name] = changedGame[self.player2Name]

  def removeNullCards(self, cards):
      # used because sometimes multiple cards are removed and you don\'t want to affect indexes midway through
      for i in range(len(cards)):
        if cards[len(cards) - 1 - i] == None:
          cards.pop(len(cards) - 1 - i)

      return cards