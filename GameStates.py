from enum import Enum

class GameStates(Enum):
    Intro           = 0
    Menu            = 1
    Running         = 2
    Paused          = 4
    Dificuldades    = 8
    Ranking         = 16
    Exit            = 512