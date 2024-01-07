from enum import Enum


class HandSignLabel(Enum):
    G1 = 0
    G2 = 1
    G3 = 2
    G4 = 3
    G5 = 4


class FingerGestureLabel(Enum):
    STOP = 0
    CLOCKWISE = 1
    COUNTER_CLOCKWISE = 2
    MOVE = 3
