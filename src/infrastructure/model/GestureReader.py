import itertools
from collections import deque, Counter

from src.application.opencv.Image import Image
from src.domain.BookKeeper import BookKeeper
from src.domain.Hands import Hand, Joint
from src.domain.Labels import HandSignLabel, FingerGestureLabel
from src.model.keypoint_classifier.keypoint_classifier import KeyPointClassifier
from src.model.point_history_classifier.point_history_classifier import PointHistoryClassifier


def to_vector_relative_to_image(joint: Joint, base: Joint, image_width: int, image_height: int) -> list:
    return [(joint.x - base.x) / image_width, (joint.y - base.y) / image_height]


def convert_to_coordinates_relative_to_screen(temp_point_history: deque[Joint], image_width, image_height) -> list:
    base = temp_point_history[0]
    relative_point_history = []
    for index, joint in enumerate(temp_point_history):
        relative_point_history.append([(joint.x - base.x) / image_width, (joint.y - base.y) / image_height])
    return relative_point_history


def convert_to_relative_coordinates(hand: Hand) -> list:
    base = hand.get_base()
    relative_joint_list: list = []
    for index, joint in enumerate(hand.joints):
        relative_joint_list.append([joint.x - base.x, joint.y - base.y])
    return relative_joint_list


def flatten_list(knuckle_list) -> list:
    return list(itertools.chain.from_iterable(knuckle_list))


def normalize(knuckle_list) -> list:
    max_value = max(list(map(abs, knuckle_list)))

    def normalize_(n):
        return n / max_value

    return list(map(normalize_, knuckle_list))


def prepare_for_model(hand: Hand) -> list:
    return normalize(flatten_list(convert_to_relative_coordinates(hand)))


def prepare_points_for_model(index_location_history: deque[Joint], image: Image) -> list:
    return flatten_list(convert_to_coordinates_relative_to_screen(index_location_history, image.width(), image.height()))


class GestureReader:

    def __init__(self,
                 book_keeper: BookKeeper,
                 key_point_model_path='src/model/keypoint_classifier/keypoint_classifier.tflite',
                 point_history_model_path='src/model/point_history_classifier/point_history_classifier.tflite',
                 ):
        self.book_keeper = book_keeper
        self.key_point_classifier = KeyPointClassifier(model_path=key_point_model_path)
        self.point_history_classifier = PointHistoryClassifier(model_path=point_history_model_path)

    def read(self, hand: Hand, image: Image) -> tuple[HandSignLabel, FingerGestureLabel]:
        hand_sign = self.read_hand_sign(hand)
        self.append_point_history(hand, hand_sign)
        finger_gesture = self.read_finger_gesture(image)
        return hand_sign, finger_gesture

    def read_hand_sign(self,
                       hand: Hand,
                       ) -> HandSignLabel:

        return self.key_point_classifier(prepare_for_model(hand))

    def append_point_history(self, hand, hand_sign: HandSignLabel):
        if hand_sign == HandSignLabel.POINTER:
            self.book_keeper.push_index_location(hand.get_index())
        else:
            self.book_keeper.push_index_location(Joint(0.0, 0.0))

    def read_finger_gesture(self, image: Image) -> FingerGestureLabel:
        finger_gesture_id = 0
        point_history_len = len(self.book_keeper.index_location_history)
        if point_history_len == (self.book_keeper.index_location_history.maxlen.real * 2):
            finger_gesture_id = self.point_history_classifier(
                prepare_points_for_model(self.book_keeper.index_location_history, image))
        self.book_keeper.push_finger_gesture(finger_gesture_id)

        return FingerGestureLabel(Counter(self.book_keeper.finger_gesture_history).most_common()[0][0])
