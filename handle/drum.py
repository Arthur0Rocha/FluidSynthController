from general.constants import DRUM_CHANNEL, LOW, NOTES_DICT
from general import eventlib, aseq

def noteon(event):
    channel = DRUM_CHANNEL
    event = eventlib.change_event_paramenter(event, channel=channel)
    aseq.noteon(event)

def noteoff(event):
    aseq.noteoff(event)

def damper(event):
    if event[7][5] == LOW:
        event = eventlib.create_note_off_event(DRUM_CHANNEL, NOTES_DICT['B1'])
        aseq.noteoff(event)
    else:
        event = eventlib.create_note_on_event(DRUM_CHANNEL, NOTES_DICT['B1'], event[7][5])
        aseq.noteon(event)

def other(event):
    aseq.send(event)