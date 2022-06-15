import alsaseq

from .constants import *
from .eventlib import *
from . import context

def init_client(client_name):
    alsaseq.client(client_name, 1, 1, False)
    print(f"Started ALSA Client: {client_name}")

################################# OUTPUT #################################

def panic():
    for chan in range(16):
        send(create_CC_event(chan, CC_PANIC, 0))

def noteon(event, key_note=None):
    evtype = event[0]
    if evtype != NOTEON_CODE:
        print("Called note on in wrong event!")
        return
    if key_note is None:
        key_note = event[7][1]
    context.noteon(event, key_note)
    send(event)

def noteoff(event):
    if event[0] != NOTEOFF_CODE:
        print("Called note off in wrong event!")
        return
    event_list = context.noteoff(event)
    for event in event_list:
        send(event)

def damper(event):
    if event[0] != CC_CODE or event[7][4] != CC_DAMPER:
        print("Called context damper in wrong event!")
        return
    event_list = context.damper(event)
    for event in event_list:
        send(event)

########################### ALSA INTERFACE ##############################

def has_new_event():
    return alsaseq.inputpending()

def read_event():
    return alsaseq.input()

def send(event):
    alsaseq.output(event)