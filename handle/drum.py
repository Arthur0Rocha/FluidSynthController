from ..general.constants import DRUM_CHANNEL, LOW, NOTES_DICT
from ..general import context, eventlib

def noteon(event):
    channel = DRUM_CHANNEL
    note = event[7][1]
    event = eventlib.change_event_paramenter(event, channel=channel)
    context.noteon(channel=channel, note=note, out_note=note)

def noteoff(event):
    context.noteoff(event)

def damper(event):
    if event[7][5] == LOW:
        event = eventlib.create_note_off_event(DRUM_CHANNEL, NOTES_DICT['B1'])
        context.noteoff(event)
    else:
        event = eventlib.create_note_on_event(DRUM_CHANNEL, NOTES_DICT['B1'], event[7][5])
        context.noteon(event)
