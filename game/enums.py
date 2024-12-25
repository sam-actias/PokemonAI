from enum import Enum

class EnergyType(Enum):
  Grass = 1
  Fire = 2
  Water = 3
  Lightning = 4
  Psychic = 5
  Fighting = 6
  Darkness = 7
  Metal = 8
  Fairy = 9
  Dragon = 10
  Colorless = 11
  FusionStrikeEnergy = 12
  DoubleTurboEnergy = 13

class CardType(Enum):
  Pokemon = 1
  Energy = 2
  Supporter = 3
  Stadium = 4
  Item = 5
  Tool = 6

class Stage(Enum):
  Basic = 1
  Vmax = 2