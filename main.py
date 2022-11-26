import time

from general.constants import *
from general import context, aseq, aconnect_monitor, mvave
from handle import drumNbass as drum_n_bass, playsingle as sing, playcombi as comb, select, sequencer

def connect_devices():
    return aconnect_monitor.run()

def reset_all_connections():
    aconnect_monitor.disconnect_all()
    connect_devices()

def init():
    aseq.init_client('FSynth-Controller')
    context.init_context()
    connect_devices()

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
        elif param == CC_SW2: # All contexts
            context.set_SW2(value)
        elif param == CC_Y2:
            select.y2(value)
        elif param in MVAVE_REMAP_RANGE[2:]:
            # MVAVE incoming message from A to D switches // Avoiding E and F switches
            print( (param - MVAVE_REMAP_RANGE[2]) % 4 )
            

    
    if context.get_mode() == 'play_single':
        if evtype == CC_CODE:
            if param in CC_USER and value == HIGH:
                # CC_USER_1 TO CC_USER_4 ARE SEQUENTIAL IN VALUE
                sing.user(param - CC_USER_1)
            elif param == CC_FOOT_SW and value == HIGH:
                context.set_mode('play_combi')
            elif param == CC_PORTAMENTO_SW and value == HIGH:
                context.set_mode('drum_n_bass')
            else:
                pass # print("Ignoring CC event...")
    
    elif context.get_mode() == 'play_combi':
        if evtype == CC_CODE:
            if param == CC_FOOT_SW and value == HIGH:
                context.set_mode('drum_n_bass')
            elif param == CC_PORTAMENTO_SW and value == HIGH:
                context.set_mode('play_single')
            else:
                pass
        
    elif context.get_mode() == 'drum_n_bass':
        if evtype == CC_CODE:
            if param in CC_SW:
                context.update_drum_n_bass_config()
            if param == CC_FOOT_SW and value == HIGH:
                context.set_mode('play_single')
            elif param == CC_PORTAMENTO_SW and value == HIGH:
                context.set_mode('play_combi')
            else:
                pass # print("Ignoring CC event...")

    elif context.get_mode() == 'select':
        if evtype == CC_CODE:
            if param in CC_USER and value == HIGH:
                select.user(param - CC_USER_1)
            else:
                pass # print("Ignoring CC event...")
    
    else:
        pass # print("Attempt of context update in an undefined context mode...")

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
    elif context.get_mode() == 'drum_n_bass':
        if evtype == NOTEON_CODE:
            drum_n_bass.noteon(ev) # TODO
        elif evtype == NOTEOFF_CODE:
            drum_n_bass.noteoff(ev) # TODO
        elif evtype == CC_CODE and ev[7][4] == CC_DAMPER:
            drum_n_bass.damper(ev) # TODO
        else:
            drum_n_bass.other(ev) # TODO
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
        pass # print("Attempt of output event in an undefined context mode...")        

CONTEXT_UPDATE_CC_PARAM_VECTOR = \
    CC_SW + CC_USER + CC_FN + CC_Y + CC_2PEDALS + [CC_ATTACK] + MVAVE_REMAP_RANGE # + [CC_VOLUME]

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
                    manage_output_event(ev) # TODO or should be ignored?

            elif evtype == PGM_CHANGE_CODE:
                pass # print("Ignoring program change event...")

            else: # NOTES, AT, BEND
                manage_output_event(ev)

if __name__ == "__main__":
    try:
        init()
        loop()
        #sequencer.play()
    except KeyboardInterrupt:
        aseq.panic()
