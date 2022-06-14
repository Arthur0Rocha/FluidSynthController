from ..general.constants import *
from ..general import context
from ..general.eventlib import change_event_paramenter

def noteon(event):
    split = context.get('split_note')
    data = event[7]
    note = data[1]
    for voice in range(context.get('voices_active')):
        zone = context.get_voices_zones(voice)
        if zone == ZONE_FULL \
            or (zone == ZONE_LOWER and note <= split) \
            or (zone == ZONE_HIGHER and note > split):
            out_note = note + context.get_voice_offset(voice)
            channel = context.get_voice_channel(voice)
            event = change_event_paramenter(event, channel=channel, param_note=out_note)
            context.noteon(event=event, query_note=note)

def noteoff(event):
    context.noteoff(event)

def other(event):
    for voice in range(context.get('voices_active')):
        channel = context.get_voice_channel(voice)
        event = change_event_paramenter(event, channel=channel)
        context.send(event)