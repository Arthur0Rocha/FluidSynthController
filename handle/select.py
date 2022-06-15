from general.constants import *
from general import aseq, context

def y2(value):
    if value >= Y2_VALUE_SUPERIOR_THRESHOLD:
        context.set_mode('select')
    elif value <= Y2_VALUE_INFERIOR_THRESHOLD:
        context.switch_back_mode()
    else:
        context.set_mode('edit')

def user(value):
    if value == 0:
        context.set_mode('play_single')
    elif value == 1:
        context.set_mode('play_combi')
    elif value == 2:
        context.set_mode('drum_n_bass')
    elif value == 3:
        context.set_mode('sequencer')
    else:
        print("Wrong user value!")

def noteoff(event):
    aseq.noteoff(event)

def damper(event):
    aseq.damper(event)