from general.constants import *
from general import eventlib, aseq, context

BASS_OFFSET = -24
DRUM_OFFSET = -36
OCTAVE = 12

KICK = NOTES_DICT['B1']
DNB_SPLIT = NOTES_DICT['A#4']

def remap(drum_note):
    if drum_note == NOTES_DICT['C#2']:
        return NOTES_DICT['C#3']
    elif drum_note == NOTES_DICT['D#2']:
        return NOTES_DICT['D#3']
    elif drum_note == NOTES_DICT['C3']:
        return NOTES_DICT['E3']
    elif drum_note == NOTES_DICT['B2']:
        return NOTES_DICT['D3']
    elif drum_note == NOTES_DICT['A2']:
        return NOTES_DICT['C3']
    elif drum_note == NOTES_DICT['G2']:
        return NOTES_DICT['B2']
    elif drum_note == NOTES_DICT['F2']:
        return NOTES_DICT['A2']
    else:
        return drum_note

def noteon(event):
    key_note = event[7][1]
    if context.get('drum_n_bass_config') in [DRUM_N_BASS_COMB_CONFIG, DRUM_N_BASS_COMB_NOREMP]:
        if key_note > DNB_SPLIT:
            if context.get('drum_n_bass_config') == DRUM_N_BASS_COMB_NOREMP:
                event = eventlib.change_event_paramenter(event, DRUM_CHANNEL, key_note + DRUM_OFFSET) # TODO not tested
            else:
                event = eventlib.change_event_paramenter(event, DRUM_CHANNEL, remap(key_note+DRUM_OFFSET))
            aseq.noteon(event, key_note)

        else:
            event = eventlib.change_event_paramenter(event, BASS_CHANNEL, key_note + BASS_OFFSET)
            aseq.noteon(event, key_note)
        
    elif context.get('drum_n_bass_config') == DRUM_N_BASS_BASS_CONFIG:
        event = eventlib.change_event_paramenter(event, BASS_CHANNEL, key_note + BASS_OFFSET)
        aseq.noteon(event, key_note)
    elif context.get('drum_n_bass_config') == DRUM_N_BASS_DRUM_CONFIG:
        event = eventlib.change_event_paramenter(event, DRUM_CHANNEL, key_note + DRUM_OFFSET + OCTAVE)
        aseq.noteon(event, key_note)
    else:
        event = eventlib.change_event_paramenter(event, DRUM_CHANNEL, remap(key_note+DRUM_OFFSET+OCTAVE))
        aseq.noteon(event, key_note)

def noteoff(event):
    aseq.noteoff(event)

def damper(event):
    if context.get('drum_n_bass_config') != DRUM_N_BASS_BASS_CONFIG \
    and context.get('drum_n_bass_damper_behaviour') == 'kick':
        if event[7][5] == LOW:
            aseq.damper(event)
            event = eventlib.create_note_off_event(DRUM_CHANNEL, KICK)
            aseq.noteoff(event)
        else:
            event = eventlib.create_note_on_event(DRUM_CHANNEL, KICK, event[7][5])
            aseq.noteon(event)
    else:
        aseq.damper(event)

def other(event):
    aseq.send(event)