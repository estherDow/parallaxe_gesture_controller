import itertools
from collections import deque
from dataclasses import dataclass
from enum import Enum


class Chirality(Enum):
    LEFT = "Left"
    RIGHT = "Right"


@dataclass
class Joint:
    x: float
    y: float
    z: float = 0.0


# https://developers.google.com/mediapipe/solutions/vision/hand_landmarker
class Hand:
    joints: list[Joint]
    handedness: Chirality

    # todo: move to bookKeeper
    history_length = 16
    point_history: deque = deque(maxlen=history_length)

    def __init__(self, joints: list[Joint], handedness: Chirality):
        self.joints = joints
        self.handedness = handedness

    def get_index(self) -> Joint:
        return self.joints[8]

    def get_base(self) -> Joint:
        return self.joints[0]

@dataclass
class Hands:
    hands_list: list[Hand]
