class Player:
  def __init__(self, deck):
      self.deck = deck
      self.activePokemon = None
      self.bench = []
      self.hand =  []
      self.discardPile = []
      self.lostZone = []
      self.prizes = []
      self.activePokemonCantAttack = 0
      self.canUseSupporterFlag = True
      self.canPlayStadiumFlag = True
      self.canUseVstarPower = True
      self.activeTurn = 0
      self.playedPowerTabletFlag = False
      self.stadium = None
      self.canRetreat = True
      self.canAttachEnergy = True