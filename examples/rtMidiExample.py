import time

from src.infrastructure.midi.Midi import Midi

midiout = Midi()
available_ports = midiout.list_ports()
print(available_ports)

if available_ports:
    midiout.open_midi_port(0)

note_on = [0x90, 60, 112]  # channel 1, middle C, velocity 112
note_off = [0x80, 60, 0]
for month in range(1, 13):
    midiout.send_channel_message(note_on)
    time.sleep(0.01)
    midiout.send_channel_message(note_off)
    time.sleep(0.01)

del midiout