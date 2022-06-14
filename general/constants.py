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
NOTES_DICT = {'C-1': 0, 'C0': 12, 'A0': 21, 'B3': 59} # This is being filled during init()
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

CC_BANK_MSB = 0
CC_BANK_LSB = 32

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

EP_CHANNEL = 0
STRINGS_CHANNEL = 1
PIANO_CHANNEL = 2
BASS_CHANNEL = 8
DRUM_CHANNEL = 9

ZONE_FULL = 0
ZONE_LOWER = 1
ZONE_HIGHER = 2

def init_notes():
    for octave in range(-1, 12):
        for ind, note in enumerate(BASE_NOTES):
            index = ind + 12 * (octave + 1)
            note += str(octave)
            NOTES_LIST.append(note)
            NOTES_DICT[note] = index