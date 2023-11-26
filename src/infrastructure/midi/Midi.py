import dataclasses
import threading
from multiprocessing import Process

import rtmidi
from dataclasses import dataclass

import schedule as schedule
from rtmidi.midiconstants import NOTE_OFF, NOTE_ON, CONTROL_CHANGE, PROGRAM_CHANGE, SONG_START, SONG_STOP, \
    ACTIVE_SENSING, TIMING_CLOCK


@dataclass
class Status:
    message_type: int
    channel: int


@dataclass
class Data:
    first: int
    second: int = None


class Midi:

    def __init__(self):
        self.midi_out = rtmidi.MidiOut()
        self.channel = 1

    def set_channel(self, new_channel: int) -> None:
        self.channel = new_channel

    def list_ports(self) -> list[str]:
        return self.midi_out.get_ports()

    def open_midi_port(self, port_number: int) -> None:
        self.midi_out.open_port(port_number)

    def send_channel_message(self, status, data1=None, data2=None, ch=None):
        """Send a MIDI channel mode message."""
        msg = [(status & 0xF0) | ((ch if ch else self.channel) - 1 & 0xF)]

        if data1 is not None:
            msg.append(data1 & 0x7F)

            if data2 is not None:
                msg.append(data2 & 0x7F)

        self.midi_out.send_message(msg)

    def send_control_change(self, cc=0, value=127, ch=None):
        """Send a 'Control Change' message."""
        self.send_channel_message(CONTROL_CHANGE, cc, value, ch=ch)

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
