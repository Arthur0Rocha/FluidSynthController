import alsaseq

# Event structure: (evtype, flags, tag, queue, time stamp, source, destination, data)
# Event types -> 10: CC, 12: AT
# Event data CC -> [0]: channel, [4]: param, [5]: value
# Event data Note -> [0]: channel, [1]: note, [2]: velocity, [3]: off_velocity, [4]: duration
# In a client without queue, received events have no time information and are asigned dummy queue number 253
DUMMY_QUEUE_NUMBER = 253
DUMMY_FLAG = 1

# SYSTEM EVENTS 0 AND 1
# SND_SEQ_EVENT_SYSEX = 130
# CLIENT, PORT EVENTS FROM 60 TO 67

BASE_NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
NOTES_DICT = {'C-1': 0, 'C0': 12, 'A0': 21, 'B3': 59} # TODO create this (until G9?)
NOTES_LIST = []

HIGH = 127
LOW = 0

# NOTE EVENTS FROM 5 TO 8
NOTE_CODE = 5 # note on and off with duration
NOTEON_CODE = 6
NOTEOFF_CODE = 7
ATMONO_CODE = 8
# CONTROL EVENTS FROM 10 TO 13
CC_CODE = 10
PGM_CHANGE_CODE = 11
AT_CODE = 12
BEND_CODE = 13

CC_Y1 = 1
CC_Y2 = 2
CC_PEDAL = 4
CC_VOLUME = 7
CC_USER_1 = 26
CC_USER_2 = 27
CC_USER_3 = 28
CC_USER_4 = 29
CC_DAMPER = 64
CC_ATTACK = 73
CC_SW1 = 80
CC_SW2 = 81
CC_FOOT_SW = 82

CC_PANIC = 123

CC_F1_CUTOFF = 74
CC_F2_RESONANCE = 71
CC_F3_ENVELOPE = 79
CC_F4_RELEASE = 72
CC_F5_KUSER1 = 17
CC_F6_KUSER2 = 19
CC_F7_KUSER3 = 20
CC_F8_KUSER4 = 21

MAX_CHANNEL = 16

ZONE_FULL = 0
ZONE_LOWER = 1
ZONE_HIGHER = 2

initial_status = {
    'voices_channels': [0, 14, 9, 5],
    'voices_zones': [ZONE_HIGHER, ZONE_HIGHER, ZONE_LOWER, ZONE_FULL],
    'voices_offset': [0, 0, 0, 0],
    'voices_active': 1,
    'split_note': NOTES_DICT['B3'],
    'notes_hanging': [],
    'mode': 'play',
    'SW_active': [0, 0]
}

status = {
    'voices_channels': [0, 14, 9, 5],
    'voices_zones': [ZONE_HIGHER, ZONE_HIGHER, ZONE_LOWER, ZONE_FULL],
    'voices_offset': [0, 0, 0, 0],
    'voices_active': 4,
    'split_note': NOTES_DICT['B3'],
    'notes_hanging': [],
    'mode': 'play',
    'SW_active': [0, 0]
}

def manage_output_event(ev):
    evtype = ev[0]
    if evtype == NOTEON_CODE:
        split = status['split_note']
        data = ev[7]
        note = data[1]
        for voice in range(status['voices_active']):
            zone = status['voices_zones'][voice]
            if zone == ZONE_FULL \
                or (zone == ZONE_LOWER and note <= split) \
                or (zone == ZONE_HIGHER and note > split):
                out_note = note + status['voices_offset'][voice]
                channel = status['voices_channels'][voice]
                event = change_event_paramenter(ev, channel=channel, param_note=out_note)
                status['notes_hanging'].append( (channel, note, out_note) )
                alsaseq.output(event)

    elif evtype == NOTEOFF_CODE:
        leng = len(status['notes_hanging'])
        for index in reversed(range(leng)):
            channel, note, out_note = status['notes_hanging'][index]
            if note == ev[7][1]:
                event = create_note_off_event(channel, out_note)
                alsaseq.output(event)
                del status['notes_hanging'][index]

    # elif evtype == CC_CODE:
    #     pass # TODO handle sustain over multiple channels
    else:
        for voice in range(status['voices_active']):
            channel = status['voices_channels'][voice]
            event = change_event_paramenter(ev, channel=channel)
            alsaseq.output(event)
    
    return

def panic():
    for chan in range(16):
        alsaseq.output(create_CC_event(chan, CC_PANIC, 0))

def reset_status():
    panic()
    for key in initial_status:
        status[key] = initial_status[key]

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

def init():
    for octave in range(-1, 12):
        for ind, note in enumerate(BASE_NOTES):
            index = ind + 12 * (octave + 1)
            note += str(octave)
            NOTES_LIST.append(note)
            NOTES_DICT[note] = index
            
    alsaseq.client('FSynth-Controller', 1, 1, False)
    reset_status()

def loop():
    while True:
        if alsaseq.inputpending():
            ev = alsaseq.input()

            evtype = ev[0]
            data = ev[7]
            
            if evtype == CC_CODE:
                param = data[4]
                value = data[5]
                if param == CC_FOOT_SW and value == HIGH:
                    status['voices_channels'][0] = (status['voices_channels'][0] + 1) % MAX_CHANNEL
                elif param == CC_SW1:
                    status['SW_active'][0] = 1 if value == HIGH else 0
                elif param == CC_SW2:
                    status['SW_active'][1] = 1 if value == HIGH else 0
                elif param >= CC_USER_1 and param <= CC_USER_4 and value == HIGH:
                    chan = param - CC_USER_1 # CC_USER_1 TO CC_USER_4 ARE SEQUENTIAL IN VALUE
                    sw1, sw2 = status['SW_active']
                    status['voices_channels'][0] = chan + 4*sw1 + 8*sw2
                # elif param == CC_PEDAL:
                #     pass
                elif param == CC_PANIC:
                    alsaseq.output(ev) # Direct output disconsidering channel routing
                else:
                    manage_output_event(ev)

            # elif evtype == AT_CODE:
            #     pass

            # elif evtype == PGM_CHANGE_CODE:
            #     pass

            # elif evtype == NOTEON_CODE:
            #     pass

            # elif evtype == NOTEOFF_CODE:
            #     pass
            
            else:
                manage_output_event(ev)



if __name__ == "__main__":
    init()
    loop()
