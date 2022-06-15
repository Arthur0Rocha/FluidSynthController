from general.constants import *
from general import aseq, context
from general.eventlib import change_event_paramenter

def noteon(event):
    split = context.get('split_note')
    data = event[7]
    key_note = data[1]
    for voice in range(context.get('voices_active')):
        zone = context.get_voices_zones(voice)
        if zone == ZONE_FULL \
            or (zone == ZONE_LOWER and key_note <= split) \
            or (zone == ZONE_HIGHER and key_note > split):
            sound_note = key_note + context.get_voice_offset(voice)
            channel = context.get_voice_channel(voice)
            event = change_event_paramenter(event, channel=channel, param_note=sound_note)
            aseq.noteon(event=event, key_note=key_note)

def noteoff(event):
    aseq.noteoff(event)

def damper(event):
    aseq.damper(event)

def other(event):
    for voice in range(context.get('voices_active')):
        channel = context.get_voice_channel(voice)
        event = change_event_paramenter(event, channel=channel)
        aseq.send(event)