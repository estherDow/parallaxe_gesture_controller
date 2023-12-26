import copy
import itertools

from src.application.application_mode import ApplicationMode
from src.application.keypoint_logger import log_point_history, log_key_points


def log_data(mode: ApplicationMode, number: int, point_history_list, pre_processed_landmark_list):
    if 0 <= number <= 9:
        match mode:
            case ApplicationMode.LEARN_POINT_HISTORY:
                log_point_history(number, point_history_list)

            case ApplicationMode.LEARN_KEY_POINTS:
                log_key_points(number, pre_processed_landmark_list)
