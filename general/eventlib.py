from constants import *

def create_CC_event(channel, param, value):
    return (CC_CODE, DUMMY_FLAG, 0, DUMMY_QUEUE_NUMBER, (0, 0), (0, 0), (0, 0), (channel, 0, 0, 0, param, value))

def create_note_on_event(channel, note, velocity):
    return (NOTEON_CODE, DUMMY_FLAG, 0, DUMMY_QUEUE_NUMBER, (0, 0), (0, 0), (0, 0), (channel, note, velocity, 0, 0))

def create_note_off_event(channel, note):
    return (NOTEON_CODE, DUMMY_FLAG, 0, DUMMY_QUEUE_NUMBER, (0, 0), (0, 0), (0, 0), (channel, note, 0, 0, 0))

def change_event_paramenter(ev, channel=None, param_note=None, value_velocity=None):
    evtype, flags, tag, queue, time_stamp, source, destination, original_data = ev
    
    note_event = evtype == NOTEON_CODE or evtype == NOTEOFF_CODE or evtype == NOTE_CODE or evtype == ATMONO_CODE
    control_event = evtype == CC_CODE or evtype == AT_CODE or evtype == BEND_CODE or evtype == PGM_CHANGE_CODE

    if not (note_event or control_event):
        return ev
    
    if channel is None:
        channel = original_data[0]
    if param_note is None:
        param_note = original_data[1 if note_event else 4]
    if value_velocity is None:
        value_velocity = original_data[2 if note_event else 5]

    if note_event:
        data = (channel, param_note, value_velocity) + original_data[3:]
    else:
        data = (channel,) + original_data[1:4]+ (param_note, value_velocity)

    event = (evtype, flags, tag, queue, time_stamp, source, destination, data)
    return event