from src.domain.Labels import HandSignLabel, FingerGestureLabel
from src.infrastructure.openCV.draw.draw_debug_messages import draw_bounding_rectangle, draw_info_text, \
    calculate_bounding_rectangle, \
    draw_point_history, draw_statistics
from src.infrastructure.openCV.draw.draw_hand_landmarks import draw_landmarks

from src.infrastructure.openCV.video_capture.VideoCaptor import Image


def draw_overlays_with_landmarks(image: Image, hand_sign: HandSignLabel, chirality, landmark_list,
                                 finger_gesture: FingerGestureLabel,
                                 hand_landmarks) -> Image:
    bounding_rectangle = calculate_bounding_rectangle(image, hand_landmarks)

    image_with_rectangle = draw_bounding_rectangle(image.image, bounding_rectangle)
    image_with_landmarks = draw_landmarks(image_with_rectangle, landmark_list)
    image_with_info = draw_info_text(
        image_with_landmarks,
        bounding_rectangle,
        chirality,
        hand_sign.name,
        finger_gesture.name,
    )
    return Image(image_with_info)


def draw_overlays(image: Image, fps, mode, number, point_history):
    image_with_point_history = draw_point_history(image.image, point_history)
    image_with_statistics = draw_statistics(image_with_point_history, fps, mode, number)
    return Image(image_with_statistics)
