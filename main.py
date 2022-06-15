import time

from general.constants import *
from general import context, aseq
from handle import drum, playsingle as sing, playcombi as comb, select

def init():
    aseq.init_client('FSynth-Controller')
    context.init_context()

def reset_status():
    aseq.panic()
    context.reset_context()

def manage_context_update(ev):
    evtype = ev[0]
 
    if evtype == CC_CODE:
        param = ev[7][4]
        value = ev[7][5]
        if param == CC_SW1: # All contexts
            context.set_SW1(value)
            return
        elif param == CC_SW2: # All contexts
            context.set_SW2(value)
            return
        elif param == CC_Y2:
            select.y2(value)

    
    if context.get_mode() == 'play_single':
        if evtype == CC_CODE:
            if param == CC_FOOT_SW and value == HIGH:
                sing.set_next_channel()
            elif param in CC_USER and value == HIGH:
                # CC_USER_1 TO CC_USER_4 ARE SEQUENTIAL IN VALUE
                sing.user(param - CC_USER_1)
            else:
                print("Ignoring CC event...")
    
    elif context.get_mode() == 'play_combi':
        print("Still not implemented") # TODO
        
    elif context.get_mode() == 'drum':
        print("Still not implemented") # TODO

    elif context.get_mode() == 'select':
        if evtype == CC_CODE:
            if param in CC_USER and value == HIGH:
                select.user(param - CC_USER_1)
            else:
                print("Ignoring CC event...")
    
    else:
        print("Attempt of context update in an undefined context mode...")

def manage_output_event(ev):
    evtype = ev[0]
    if context.get_mode() == 'play_single':
        if evtype == NOTEON_CODE:
            sing.noteon(ev)
        elif evtype == NOTEOFF_CODE:
            sing.noteoff(ev)
        elif evtype == CC_CODE and ev[7][4] == CC_DAMPER:
            sing.damper(ev)
        else:
            sing.other(ev)
    elif context.get_mode() == 'play_combi':
        if evtype == NOTEON_CODE:
            comb.noteon(ev)
        elif evtype == NOTEOFF_CODE:
            comb.noteoff(ev)
        elif evtype == CC_CODE and ev[7][4] == CC_DAMPER:
            comb.damper(ev)
        else:
            comb.other(ev)
    elif context.get_mode() == 'drum':
        if evtype == NOTEON_CODE:
            drum.noteon(ev)
        elif evtype == NOTEOFF_CODE:
            drum.noteoff(ev)
        elif evtype == CC_CODE and ev[7][4] == CC_DAMPER:
            drum.damper(ev)
        else:
            drum.other(ev)
    elif context.get_mode() == 'select':
        if evtype == NOTEON_CODE:
            pass # Ignoring note on event on select mode
        elif evtype == NOTEOFF_CODE:
            select.noteoff(ev)
        elif evtype == CC_CODE and ev[7][4] == CC_DAMPER:
            select.damper(ev)
        else:
            pass # Ignoring other events
    else:
        print("Attempt of output event in an undefined context mode...")        

CONTEXT_UPDATE_CC_PARAM_VECTOR = \
    CC_SW + CC_USER + CC_FN + CC_Y + CC_2PEDALS + [CC_ATTACK, CC_VOLUME]

def loop():
    while True:
        time.sleep(0.001)
        while aseq.has_new_event():
            ev = aseq.read_event()
            evtype = ev[0]
            data = ev[7]
            
            if evtype == CC_CODE:
                param = data[4]
                if param == CC_PANIC:
                    # Direct output disconsidering channel routing
                    aseq.send(ev) 
                elif param in CONTEXT_UPDATE_CC_PARAM_VECTOR:
                    manage_context_update(ev)
                else:
                    manage_output_event(ev)

            elif evtype == PGM_CHANGE_CODE:
                print("Ignoring program change event...")

            else: # NOTES, AT, BEND
                manage_output_event(ev)

if __name__ == "__main__":
    init()
    loop()
