from .constants import *
from .eventlib import create_CC_event

VERBOSE = False

def remap_input(event, invert_pedal=True):
    evtype = event[0]
    channel = event[7][0]

    if evtype not in [PGM_CHANGE_CODE, CC_CODE]:
        return event
    param, value = event[7][4:]
    if evtype == PGM_CHANGE_CODE:
        if value == 0:
            if VERBOSE:
                print("A")
            return create_CC_event(channel, CC_USER_1, HIGH) # A
        elif value == 1:
            if VERBOSE:
                print("B")
            return create_CC_event(channel, CC_USER_2, HIGH) # B
        elif value == 2:
            if VERBOSE:
                print("C")
            return create_CC_event(channel, CC_USER_3, HIGH) # C
        elif value == 3:
            if VERBOSE:
                print("D")
            return create_CC_event(channel, CC_USER_4, HIGH) # D
        else:
            if VERBOSE:
                print("W1")
            return event # Weird. This value shouldn't be accessible
    else:
        if param == CC_Y2:
            if VERBOSE:
                print("E")
            return create_CC_event(channel, CC_PORTAMENTO_SW, HIGH) # E
        elif param == CC_03:
            if VERBOSE:
                print("F")
            return create_CC_event(channel, CC_FOOT_SW, HIGH) # F
        elif param == CC_VOLUME:
            if invert_pedal:
                value = HIGH - value
            if VERBOSE:
                print(f"PEDAL - {value:03d}")
            return create_CC_event(channel, CC_PEDAL, value) # PEDAL
        else:
            if VERBOSE:
                print("W2")
            return event # Weird. This value shouldn't be accessible
