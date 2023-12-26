import unittest

from src.domain.BookKeeper import BookKeeper
from src.domain.Labels import HandSignLabel
from src.infrastructure.model.GestureReader import GestureReader
from test.HandsStub import should_create_hands


class GestureReaderTest(unittest.TestCase):
    key_point_model_path = '../src/model/keypoint_classifier/keypoint_classifier.tflite'
    point_history_model_path = '../src/model/point_history_classifier/point_history_classifier.tflite'
    gesture_reader = GestureReader(BookKeeper(), key_point_model_path,
                                   point_history_model_path)

    def test_should_read_gesture(self):
        given_hands = should_create_hands()
        expected_gesture = HandSignLabel.OPEN
        actual_gesture = self.gesture_reader.read_hand_sign(given_hands.hands_list[0])
        self.assertEqual(expected_gesture, actual_gesture)  # add assertion here


if __name__ == '__main__':
    unittest.main()
