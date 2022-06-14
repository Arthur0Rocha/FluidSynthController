from ..general import context, eventlib

def noteon(event):
    channel = get_channel()
    note = event[7][1]
    event = eventlib.change_event_paramenter(event, channel=channel)
    context.noteon(event=event, query_note=note)
    

def noteoff(event):
    context.noteoff(event)

def other(event):
    channel = get_channel()
    event = eventlib.change_event_paramenter(event, channel=channel)
    context.send(event)
    
def get_channel():
    return context.get_channel_single()

def set_next_channel():
    context.set_next_channel_single()

def set_channel(channel):
    context.set_channel_single(channel)

def user(value):
    sw1, sw2 = context.get_SW1(), context.get_SW2()
    set_channel(value + 4*sw1 + 8*sw2)