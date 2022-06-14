from general.constants import *
from general import context
from handle import drum, playsingle as sing, playcombi as comb

# TODO # Modes: Play (Single and Combi), SongList, Edit, Drum(nBass), Sequencer

def manage_output_event(ev):
    evtype = ev[0]
    if evtype == NOTEON_CODE:
        if context.get_mode() == 'drum':
            drum.noteon(ev)
        elif context.get_mode() == 'play_single':
            sing.noteon(ev)
        elif context.get_mode() == 'play_combi':
            comb.noteon(ev)
        else:
            context.noteon(event=ev, query_note=ev[7][1]) 

    elif evtype == NOTEOFF_CODE:
        context.noteoff(ev)

    elif evtype == CC_CODE and ev[7][4] == CC_DAMPER:
        if context.get_mode() == 'drum':
            drum.damper(ev)
        else:
            context.damper(ev)

    else:
        if context.get_mode() == 'play_single':
            sing.other(ev)
        elif context.get_mode() == 'play_combi':
            comb.other(ev)
        else:
            context.send(ev)
    
    return

def reset_status():
    context.panic()
    context.reset_context()

def init():
    context.init_context('FSynth-Controller')
    init_notes()

def loop():
    while True:
        if context.has_new_event():
            ev = context.read_event()

            evtype = ev[0]
            data = ev[7]
            
            if evtype == CC_CODE:
                param = data[4]
                value = data[5]
                if param == CC_SW1:
                    context.set_SW1(value)
                elif param == CC_SW2:
                    context.set_SW2(value)
                if context.get_mode() == 'play_single':
                    if param == CC_FOOT_SW and value == HIGH:
                        sing.set_next_channel()
                    elif param >= CC_USER_1 and param <= CC_USER_4 and value == HIGH:
                        sing.user(param - CC_USER_1) # CC_USER_1 TO CC_USER_4 ARE SEQUENTIAL IN VALUE
                    else:
                        manage_output_event(ev)
                # elif param == CC_PEDAL:
                #     pass
                elif param == CC_PANIC:
                    context.send(ev) # Direct output disconsidering channel routing
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
