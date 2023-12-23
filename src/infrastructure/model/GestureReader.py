import itertools
from collections import deque, Counter

import numpy as np
from numpy import ndarray

from src.domain.BookKeeper import BookKeeper
from src.domain.Hands import Hand, Knuckle
from src.domain.Labels import HandSignLabel, FingerGestureLabel
from src.model.keypoint_classifier.keypoint_classifier import KeyPointClassifier
from src.model.point_history_classifier.point_history_classifier import PointHistoryClassifier


class GestureReader:

    def __init__(self,
                 book_keeper: BookKeeper,
                 key_point_model_path='src/model/keypoint_classifier/keypoint_classifier.tflite',
                 point_history_model_path='src/model/point_history_classifier/point_history_classifier.tflite',
                 ):
        self.book_keeper = book_keeper
        self.key_point_classifier = KeyPointClassifier(model_path=key_point_model_path)
        self.point_history_classifier = PointHistoryClassifier(model_path=point_history_model_path)

    def read(self, hand: Hand) -> tuple[HandSignLabel, FingerGestureLabel]:
        hand_sign = self.read_hand_sign(hand)
        self.append_point_history(hand, hand_sign)
        finger_gesture = self.read_finger_gesture(hand)
        return hand_sign, finger_gesture

    def read_hand_sign(self,
                       hand: Hand,
                       ) -> HandSignLabel:

        return self.key_point_classifier(hand.prepare_for_model())

    def append_point_history(self, hand, hand_sign):
        if hand_sign == HandSignLabel.POINTER:
            self.book_keeper.push_index_location(hand.get_index())
        else:
            self.book_keeper.push_index_location(Knuckle(0.0, 0.0))

    def read_finger_gesture(self, hand: Hand) -> FingerGestureLabel:
        finger_gesture_id = 0
        point_history_len = len(hand.point_history)
        if point_history_len == (hand.point_history.maxlen.real * 2):
            finger_gesture_id = self.point_history_classifier(
                hand.prepare_points_for_model())

        self.book_keeper.push_finger_gesture(finger_gesture_id)
        return FingerGestureLabel(Counter(self.book_keeper.finger_gesture_history).most_common()[0][0])
