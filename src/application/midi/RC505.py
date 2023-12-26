from dataclasses import dataclass
from enum import Enum

from src.infrastructure.midi.Midi import Midi, ControllerData


class TrackState(Enum):
    PLAY = "play"
    STOP = "stop"
    RECORD = "record"


class MachineState(Enum):
    PLAY = "play"
    STOP = "stop"


@dataclass
class Track:
    state: TrackState


class RC505:
    play_pause_messages = [1, 2, 3, 4, 5]
    record_messages = [6, 7, 8, 9, 10]
    clear_messages = [11, 12, 13, 14, 15]

    def __init__(self, midi: Midi):
        self.midi = midi
        self.global_state = MachineState.STOP
        self.tracks = [Track(TrackState.STOP), Track(TrackState.STOP), Track(TrackState.STOP)]

    def play_all(self):
        self.midi.send_system_realtime_message(0xFA)

    def stop_all(self):
        self.midi.send_system_realtime_message(0xFC)

    def select_bank(self, number: int):
        self.midi.send_program_change(number)
        # todo use program channge 1-99 to set phrase memory

    def record(self, track: int):
            self.midi.send_control_change(ControllerData(self.record_messages[track-1], 127))
            # todo: i have doubts if it just records until stop

    def play(self, track: int):
            self.midi.send_control_change(ControllerData(self.play_pause_messages[track - 1], 127))

    def clear(self, track: int):
            self.midi.send_control_change(ControllerData(self.clear_messages[track - 1], 127))

    def fx_on(self, track: int):
        self.midi.send_control_change(ControllerData(track, 0x03))

    def fx_off(self, track: int):
        self.midi.send_control_change(ControllerData(track, 0x04))

    def fx_inc(self, track: int):
        self.midi.send_control_change(ControllerData(track, 0x05))

# we can use e “CC#1–#31, CC#64–#95”  to set different functions.
