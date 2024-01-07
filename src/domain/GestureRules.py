from dataclasses import dataclass
from typing import Tuple

from src.domain.Action import Action
from src.domain.Hands import Chirality, Gesture
from src.domain.Labels import HandSignLabel


def get_first_by_chirality(gestures) -> tuple[Gesture| None, Gesture | None]:
    left = None
    right = None
    for gesture in gestures:
        if gesture.handedness == Chirality.LEFT:
            left = gesture
        elif gesture.handedness == Chirality.RIGHT:
            right = gesture
    return left, right

@dataclass
class RulesError:
    error_type: str


def apply_rules(gestures: list[Gesture]) -> Action | RulesError:
    if len(gestures) != 2:
        return RulesError(f"Not two hands: {len(gestures)}")

    left, right = get_first_by_chirality(gestures)

    if left is None or right is None:
        RulesError("Not left and right hand")
    if left.hand_sign == HandSignLabel.G1 and right.hand_sign == HandSignLabel.G1:
        return Action.START_PAUSE_TRACK_1

    if left.hand_sign == HandSignLabel.G1 and right.hand_sign == HandSignLabel.G2:
        return Action.START_PAUSE_TRACK_2

    if left.hand_sign == HandSignLabel.G1 and right.hand_sign == HandSignLabel.G3:
        return Action.START_PAUSE_TRACK_3

    if left.hand_sign == HandSignLabel.G2 and right.hand_sign == HandSignLabel.G1:
        return Action.RECORD_TRACK_1

    if left.hand_sign == HandSignLabel.G2 and right.hand_sign == HandSignLabel.G2:
        return Action.RECORD_TRACK_2

    if left.hand_sign == HandSignLabel.G2 and right.hand_sign == HandSignLabel.G3:
        return Action.RECORD_TRACK_3

    if left.hand_sign == HandSignLabel.G3 and right.hand_sign == HandSignLabel.G1:
        return Action.CLEAR_TRACK_1

    if left.hand_sign == HandSignLabel.G3 and right.hand_sign == HandSignLabel.G2:
        return Action.CLEAR_TRACK_2

    if left.hand_sign == HandSignLabel.G3 and right.hand_sign == HandSignLabel.G3:
        return Action.CLEAR_TRACK_3

    else:
        return RulesError("No rule")
