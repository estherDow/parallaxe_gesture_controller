from dataclasses import dataclass
from enum import Enum

from src.domain.Labels import HandSignLabel, FingerGestureLabel


class Chirality(Enum):
    LEFT = "Left"
    RIGHT = "Right"


@dataclass
class Joint:
    x: int
    y: int
    z: int = 0


# https://developers.google.com/mediapipe/solutions/vision/hand_landmarker
class Hand:
    joints: list[Joint]
    handedness: Chirality

    def __init__(self, joints: list[Joint], handedness: Chirality):
        self.joints = joints
        self.handedness = handedness

    def get_index(self) -> Joint:
        return self.joints[8]

    def get_base(self) -> Joint:
        return self.joints[0]


@dataclass
class Gesture:
    handedness: Chirality
    hand_sign: HandSignLabel = None
    finger_gesture: FingerGestureLabel = None


@dataclass
class Hands:
    hands_list: list[Hand]
