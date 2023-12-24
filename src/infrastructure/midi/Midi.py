import dataclasses

import rtmidi
from dataclasses import dataclass
from rtmidi.midiconstants import NOTE_OFF, NOTE_ON, CONTROL_CHANGE, PROGRAM_CHANGE, SONG_START, SONG_STOP


@dataclass
class Status:
    message_type: int
    channel: int


@dataclass
class Data:
    first: int
    second: int = None


class ControllerData(Data):
    def __init__(self, number: int, value: int):
        self.first = number
        self.second = value


class Midi:

    def __init__(self):
        self.midi_out = rtmidi.MidiOut()
        self.channel = 0x0

    def set_channel(self, new_channel: int) -> None:
        self.channel = new_channel

    def list_ports(self) -> list[str]:
        return self.midi_out.get_ports()

    def open_midi_port(self, port_number: int) -> None:
        self.midi_out.open_port(port_number)

    def send_channel_message(self, status: Status, data: Data = None) -> None:
        msg = [status.message_type | status.channel, data.first]
        if data.second is not None:
            msg.append(data.second)
        print(msg)

        self.midi_out.send_message(
            msg
        )

    def send_control_change(self, data: ControllerData) -> None:
        self.send_channel_message(
            Status(CONTROL_CHANGE, self.channel),
            data,
        )

    def send_program_change(self, program: int) -> None:
        self.send_channel_message(
            Status(PROGRAM_CHANGE, self.channel),
            Data(program)
        )

    def send_system_realtime_message(self, message: int) -> None:
        self.midi_out.send_message([message])

    def start_song(self) -> None:
        self.send_system_realtime_message(SONG_START)

    def stop_song(self) -> None:
        self.send_system_realtime_message(SONG_STOP)
