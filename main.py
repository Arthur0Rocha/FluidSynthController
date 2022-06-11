import alsaseq
import os

# Event structure: (evtype, flags, tag, queue, time stamp, source, destination, data)
# Event types -> 10: CC, 12: AT
# Event data CC -> [0]: channel, [4]: param, [5]: value
# Event data Note -> [0]: channel, [1]: note, [2]: velocity, [3]: off_velocity, [4]: duration
# In a client without queue, received events have no time information and are asigned dummy queue number 253

# SYSTEM EVENTS 0 AND 1
# SND_SEQ_EVENT_SYSEX = 130
# CLIENT, PORT EVENTS FROM 60 TO 67

NOTES = {'C-1': 0, 'C0': 12, 'A0': 21, 'B3': 59} # TODO create this (until G9?)

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

# 74 71 79 72 | 17 19 20 21 

status = {
    'layers_channels': [],
    'layers_offset': [],
    'layers_active': 0,
    'split_note': 0,
    'notes_hanging': [],
    'mode': '',
}

def panic():
    for chan in range(16):
        pass # send PANIC (123) event
    return # TODO implement this

def reset_status():
    panic()
    status['layers_channels'] = [0]
    status['layers_offset'] = [0]
    status['layers_active'] = 1
    status['split_note'] = NOTES['B3']
    status['mode'] = 'play'

def create_CC_event():
    return

def send_ev():
    event = ()
    alsaseq.output(event)

def check_connections_fail():
    return False # TODO implement this function

def connect_devices():
    reset_status()
    return # TODO implement this function
#     Port 0 is input, port 1 is output. Connect ALSA client 129 (could be a musical keyboard or Virtual Keyboard) to the input port, and connect output port to ALSA client 130 (a MIDI to sound converter like Timidity):
#       >>> alsaseq.connectfrom( 0, 129, 0 )
#       >>> alsaseq.connectto( 1, 130, 0 )

def init():
    reset_status()
    alsaseq.client('FSynth-Controller', 1, 1, False)

def loop():
    while True:
        if check_connections_fail():
            print("Connections Failed...")
            connect_devices()

        if alsaseq.inputpending():
            ev = alsaseq.input()

            evtype = ev[0]
            data = ev[7]
            channel = data[0]

            if evtype == CC_CODE:
                param = data[4]
                value = data[5]
                if param == CC_FOOT_SW and value == HIGH:
                    print(f"CC: FOOT SW - {param} {value} - Channel {channel}")
                    pass # CC 82 (Foot SW) HIGH
                elif param >= CC_USER_1 and param <= CC_USER_4 and value == HIGH:
                    print(f"CC: USER - {param} {value} - Channel {channel}")
                    pass # CC 26 <=> 29 HIGH
                elif param == CC_PEDAL:
                    print(f"CC: Pedal - {param} {value} - Channel {channel}")
                    pass # CC 04 (Pedal)
                else:
                    print(f"CC: {param} {value} - Channel {channel}")

            elif evtype == AT_CODE:
                param = data[4]
                value = data[5]
                print(f"AT: {param} {value} - Channel {channel}")
                pass # AT

            elif evtype == PGM_CHANGE_CODE:
                param = data[4]
                value = data[5]
                print(f"PGM CHNG: {param} {value} - Channel {channel}")
                pass

            elif evtype == NOTEON_CODE:
                note, velocity, off_velocity, duration = data[1:]
                print(f"NOTE ON: {note} {velocity} {off_velocity} {duration} - Channel {channel}")
                pass

            elif evtype == NOTEOFF_CODE:
                note, velocity, off_velocity, duration = data[1:]
                print(f"NOTE OFF: {note} {velocity} {off_velocity} {duration} - Channel {channel}")
                pass



if __name__ == "__main__":
    init()
    loop()
