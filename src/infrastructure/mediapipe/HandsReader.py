import itertools
from collections import deque

import mediapipe as mp

from src.application.opencv.Image import Image
from src.domain.Hands import Hands, Hand, Chirality, Joint


class HandsReader:
    max_num_hands = 2

    def __init__(
            self,
            use_static_image_mode: bool,
            min_detection_confidence: float,
            min_tracking_confidence: float,

    ):
        self.hands = mp.solutions.hands.Hands(
            static_image_mode=use_static_image_mode,
            max_num_hands=self.max_num_hands,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence,
        )

    def get_hands(self, image: Image) -> Hands | None:
        frame = self.hands.process(image.image)
        hands_list = []
        if frame.multi_hand_landmarks is None:
            return None
        for hand_landmarks, handednness in zip(frame.multi_hand_landmarks, frame.multi_handedness):
            hands_list.append(
                Hand(
                    list(map(
                        lambda n: Joint(x=min(int(n.x * image.width()), image.width() - 1),
                                        y=min(int(n.y * image.height()), image.height() - 1)),
                        hand_landmarks.landmark)),
                    Chirality(handednness.classification[0].label[0:])
                )
            )
        return Hands(hands_list)
