import unittest
import cv2 as cv

from src.application.opencv.Image import Image
from src.domain.BookKeeper import BookKeeper
from src.domain.Labels import HandSignLabel
from src.domain.GestureReader import GestureReader
from test.HandsStub import should_create_hands


class GestureReaderTest(unittest.TestCase):
    key_point_model_path = '../src/model/keypoint_classifier/keypoint_classifier.tflite'
    point_history_model_path = '../src/model/point_history_classifier/point_history_classifier.tflite'
    gesture_reader = GestureReader(BookKeeper(), key_point_model_path,
                                   point_history_model_path)

    def test_should_read_gesture(self):
        test_image = Image(cv.imread('open hand.jpg'))
        given_hands = should_create_hands()
        expected_hand_sign = HandSignLabel.G1
        actual_gesture = self.gesture_reader.read(given_hands, test_image)
        self.assertEqual(expected_hand_sign, actual_gesture[0].hand_sign)


if __name__ == '__main__':
    unittest.main()
