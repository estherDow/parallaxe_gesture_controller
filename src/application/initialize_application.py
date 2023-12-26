from src.application.application_mode import ApplicationMode
from src.domain.BookKeeper import BookKeeper
from src.infrastructure.argument_parser import get_arguments
from src.infrastructure.mediapipe.HandsReader import HandsReader
from src.domain.GestureReader import GestureReader
from src.infrastructure.openCV.video_capture.VideoCaptor import VideoCapture
from src.utils import CvFpsCalc


def initialize_application() -> [VideoCapture, CvFpsCalc, HandsReader, GestureReader, ApplicationMode]:
    arguments = get_arguments()
    use_static_image = False
    return VideoCapture(arguments), CvFpsCalc(buffer_len=10), \
        HandsReader(use_static_image,
                    arguments.min_detection_confidence,
                    arguments.min_tracking_confidence), \
        GestureReader(BookKeeper()), \
        ApplicationMode.DEBUG
