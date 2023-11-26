import unittest
from time import sleep

from src.application.midi.Rt505 import Rt505
from src.infrastructure.midi.Midi import Midi


class MyTestCase(unittest.TestCase):
    midi = Midi()
    rt505 = Rt505(midi)

    def test_rt505_should_show_as_available_device(self):
        actual_ports = self.midi.list_ports()
        expected_port = 'RC-505'
        self.assertIn(expected_port, actual_ports)
    def test_rt505_should_record_and_play_on_track(self):
        print(hex(0xB0 | 0x00))
        actual_ports = self.midi.list_ports()
        print(f"found ports: {actual_ports}")
        self.midi.open_midi_port(1)
        self.rt505.record(1)
        sleep(5)
        self.rt505.play(1)
        sleep(5)
        self.rt505.stop(1)

    def test_should_play_all(self):
        self.midi.open_midi_port(1)
        self.rt505.play_all()
    def test_rt505_should_play_then_pause_a_track(self):
        self.assertEqual(True, False)  # add assertion here

if __name__ == '__main__':
    unittest.main()
