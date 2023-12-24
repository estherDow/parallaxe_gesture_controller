import unittest
from time import sleep

from src.application.midi.RC505 import RC505
from src.infrastructure.midi.Midi import Midi


class RC505Test(unittest.TestCase):
    midi = Midi()
    rt505 = RC505(midi)

    def test_rt505_should_show_as_available_device(self):
        actual_ports = self.midi.list_ports()
        print(actual_ports)
        expected_port = 'RC-505'
        self.assertIn(expected_port, actual_ports)
    def test_rt505_should_record_and_play_on_track(self):
        actual_ports = self.midi.list_ports()
        print(f"found ports: {actual_ports}")
        self.midi.open_midi_port(0)
        n = 2
        print(f"Messages for track number: {n}")
        self.rt505.record(n)
        sleep(1)

        self.rt505.record(n)
        sleep(1)

        self.rt505.play(n)
        sleep(1)
        self.rt505.clear(n)
        sleep(1)
        self.midi.midi_out.close_port()
        self.midi.midi_out.delete()

    def test_should_play_all(self):
        self.midi.open_midi_port(1)
        self.rt505.play_all()
    def test_rt505_should_play_then_pause_a_track(self):
        self.assertEqual(True, False)  # add assertion here

if __name__ == '__main__':
    unittest.main()
