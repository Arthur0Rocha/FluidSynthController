from .constants import *
from .eventlib import change_event_paramenter, create_note_off_event

all_modes = [
    'play_single', 
    'play_combi', 
    'drum', 
    'sequencer',
    'song_list',
    'edit', 
    'select', 
    ]

status = {}

initial_status = {
    # General
    'mode': 'play_single',
    'last_playable_mode': 'play_single',
    'SW_active': [0, 0],
    'using_damper': [1] * MAX_CHANNEL,
    'notes_hanging': [],
    # Play Mode
    # Single
    'channel_single': 0,
    # Combi
    'voices_active': 3,
    'split_note': NOTES_DICT['B3'],
    'voices_zones': [ZONE_LOWER, ZONE_HIGHER, ZONE_HIGHER, ZONE_FULL],
    'voices_channels': [BASS_CHANNEL, PIANO_CHANNEL, STRINGS_CHANNEL, EP_CHANNEL],
    'voices_offset': [-24, -12, 0, 0],
    'voices_volumes': [1., 1., 1., 1.],
    # SongList Mode
    'current_song_index': 0,
}

def init_context():
    reset_context()

def reset_context():
    for key in initial_status:
        status[key] = initial_status[key]

################################ GETTERS ################################

def get(key):
    return status[key]

def get_mode():
    return status['mode']

def get_voices_zones(index):
    return status['voices_zones'][index]

def get_voice_offset(index):
    return status['voices_offset'][index]

def get_voice_channel(index):
    return status['voices_channels'][index]

def get_channel_single():
    return status['channel_single']

def get_SW1():
    return status['SW_active'][0]

def get_SW2():
    return status['SW_active'][1]

################################ SETTERS ################################

def set_mode(value):
    if value not in all_modes:
        print('Wrong mode name. Ignored.')
        return
    if status['mode'] not in ['select', 'edit']:
        status['last_playable_mode'] = status['mode']
    status['mode'] = value

def switch_back_mode():
    status['mode'] = status['last_playable_mode']

def set_channel_single(channel):
    if channel < 0 or channel >= MAX_CHANNEL:
        print('Channel out of range. Not set.')
        return
    status['channel_single'] = channel

def set_next_channel_single():
    status['channel_single'] = (status['channel_single'] + 1) % MAX_CHANNEL

def set_SW1(value):
    if value == LOW:
        status['SW_active'][0] = 0
        return
    if value == HIGH or value == 1:
        status['SW_active'][0] = 1
        return
    print("Invalid value for SW")

def set_SW2(value):
    if value == LOW:
        status['SW_active'][1] = 0
        return
    if value == HIGH or value == 1:
        status['SW_active'][1] = 1
        return
    print("Invalid value for SW")

################################# EVENTS #################################

def noteon(event, query_note):
    channel = event[7][0]
    played_note = event[7][1]
    status['notes_hanging'].append( (channel, query_note, played_note) )

def noteoff(event):
    leng = len(status['notes_hanging'])
    noteoff_evn_list = []
    for index in reversed(range(leng)):
        channel, query_note, played_note = status['notes_hanging'][index]
        if query_note == event[7][1]:
            event = create_note_off_event(channel, played_note)
            noteoff_evn_list.append(event)
            del status['notes_hanging'][index]
    return noteoff_evn_list

def damper(event):
    event_list = []
    for chan in range(MAX_CHANNEL):
        if event[7][5] == LOW or status['using_damper'][chan] == 1:
            event = change_event_paramenter(event, channel=chan)
            event_list.append(event)
    return event_list
            