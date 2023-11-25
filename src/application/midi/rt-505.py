from dataclasses import dataclass
from enum import Enum

from src.infrastructure.midi.Midi import Midi, Data


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


class Rt505:
    play_messages = [0x00, 0x01, 0x02, 0x03, 0x04]
    record_messages = [0x05, 0x06, 0x07, 0x08, 0x09]
    stop_messages = [0x0A, 0x0B, 0x0C, 0x0D, 0x0E]
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
        if track <= len(self.tracks) and self.tracks[track].state != TrackState.RECORD:
            self.midi.send_control_change(Data(self.record_messages[track - 1]))
            self.tracks[track].state = TrackState.RECORD
            # todo: i have doubts if it just records until stop
    def play(self, track: int):
        if track <= len(self.tracks) and self.tracks[track].state != TrackState.PLAY:
            self.midi.send_control_change(Data(self.play_messages[track - 1]))
            self.tracks[track].state = TrackState.PLAY

    def stop(self, track: int):
        if track <= len(self.tracks) and self.tracks[track].state != TrackState.STOP:
            self.midi.send_control_change(Data(self.stop_messages[track - 1]))
            self.tracks[track].state = TrackState.STOP

    def clear(self, track: int):
        self.midi.send_control_change(Data(track, 0x02))

    def fx_on(self, track: int):
        self.midi.send_control_change(Data(track, 0x03))

    def fx_off(self, track: int):
        self.midi.send_control_change(Data(track, 0x04))

    def fx_inc(self, track: int):
        self.midi.send_control_change(Data(track, 0x05))

# we can use e “CC#1–#31, CC#64–#95”  to set different functions.
