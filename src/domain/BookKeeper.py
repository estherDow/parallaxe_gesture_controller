from collections import deque

from src.domain.Hands import Knuckle
from src.domain.Labels import FingerGestureLabel, HandSignLabel


class BookKeeper:
    history_length = 16

    finger_gesture_history: deque = deque(maxlen=history_length)
    index_location_history: deque = deque(maxlen=history_length)
    hand_sign_history: deque = deque(maxlen=history_length)

    def push_index_location(self,knuckle: Knuckle):
        self.index_location_history.append(knuckle)

    def push_finger_gesture(self, gesture: FingerGestureLabel):
        self.finger_gesture_history.append(gesture)

    def push_hand_sign(self, sign: HandSignLabel):
        self.hand_sign_history.append(sign)
