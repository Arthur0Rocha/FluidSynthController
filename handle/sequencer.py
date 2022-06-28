import re

from general.constants import *
from general.music import *

l = lambda f, lis: list(map(f, lis))

class TokenReader:
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = 0
    def next(self):
        token = self.tokens[self.index]
        self.index += 1
        return token
    def next_int(self):
        token = int(self.tokens[self.index])
        self.index += 1
        return token

def read_song_pattern_from_str(content: str):
    seq_dict = {}

    tr = TokenReader(re.sub(r"(^ )|( $)", "", re.sub(r"(\s|\n|\t)+", " ", content)).split(" "))

    seq_dict['bar_signature'] = tr.next_int()
    seq_dict['tempo'] = tr.next_int()
    seq_dict['key'] = tr.next()

    token = tr.next()

    if token == 'D':
        pass
    elif token == 'B':
        pass
    else: # Cnum
        pass

    print(seq_dict)

def play_hello():

    SIGN = 4
    QUANT = 4
    BPM = 79
    KEY = 'Fm'

    BEGIN_OF_BAR = 0

    # Drum Notes
    bass_drum_note = BassDrumNote()
    snare_note = SnareDrumNote()
    ring_note = SnareRingNote()
    hihat_closed = ClosedHiHatNote()
    hihat_open = OpenHiHatNote()
    crash = Crash1DrumNote()
    tom1 = Tom1Note()
    tom2 = Tom2Note()

    # Bass Notes
    c1_quarterdot = Note(Duration.QUARTER_DOT, NOTES_DICT['C1'], Loudness.FFF)
    cs1_half_eight = Note(DurationLegatto([Duration.HALF, Duration.EIGHTH]), NOTES_DICT['C#1'], Loudness.FF)
    cs1_whole_quarter = Note(DurationLegatto([Duration.WHOLE, Duration.QUARTER]), NOTES_DICT['C#1'], Loudness.FF)
    ds1_quarterdot = Note(Duration.QUARTER_DOT, NOTES_DICT['D#1'], Loudness.FF)
    ds1_half_eight = Note(DurationLegatto([Duration.HALF, Duration.EIGHTH]), NOTES_DICT['D#1'], Loudness.FF)
    f1_quarterdot = Note(Duration.QUARTER_DOT, NOTES_DICT['F1'], Loudness.FF)
    f1_whole = Note(Duration.WHOLE, NOTES_DICT['F1'], Loudness.FF)
    gs1_half_eight = Note(DurationLegatto([Duration.HALF, Duration.EIGHTH]), NOTES_DICT['G#1'], Loudness.FF)
    gs1_quarterdot = Note(Duration.QUARTER_DOT, NOTES_DICT['G#1'], Loudness.FF)

    # EP Harmonies
    ep_Cm_quarterdot = Harmony(Duration.QUARTER_DOT, [  NOTES_DICT['C2' ], 
                                                        NOTES_DICT['G2' ],
                                                        NOTES_DICT['C3' ],
                                                        NOTES_DICT['D#3'],
                                                        NOTES_DICT['G3' ]], Loudness.PP)
    ep_CS_half_eight    = Harmony(DurationLegatto([Duration.HALF, Duration.EIGHTH]), [  NOTES_DICT['C#2'], 
                                                                                        NOTES_DICT['G#2'],
                                                                                        NOTES_DICT['C#3'],
                                                                                        NOTES_DICT['F3' ],
                                                                                        NOTES_DICT['G#3']], Loudness.PP)
    ep_CS_whole_quarter = Harmony(DurationLegatto([Duration.WHOLE, Duration.QUARTER]),[NOTES_DICT['C#2'], 
                                                                                        NOTES_DICT['G#2'],
                                                                                        NOTES_DICT['C#3'],
                                                                                        NOTES_DICT['F3' ],
                                                                                        NOTES_DICT['G#3']], Loudness.PP)
    ep_DS_quarterdot    = Harmony(Duration.QUARTER_DOT, [   NOTES_DICT['D#2'], 
                                                            NOTES_DICT['A#2'],
                                                            NOTES_DICT['D#3'],
                                                            NOTES_DICT['G3' ],
                                                            NOTES_DICT['A#3']], Loudness.PP)
    ep_DS_half_eight    = Harmony(DurationLegatto([Duration.HALF, Duration.EIGHTH]), [ NOTES_DICT['D#2'], 
                                                                                        NOTES_DICT['A#2'],
                                                                                        NOTES_DICT['D#3'],
                                                                                        NOTES_DICT['G3' ],
                                                                                        NOTES_DICT['A#3']], Loudness.PP)
    ep_Fm_quarterdot    = Harmony(Duration.QUARTER_DOT, [  NOTES_DICT['F2' ], 
                                                            NOTES_DICT['C3' ],
                                                            NOTES_DICT['F3' ],
                                                            NOTES_DICT['G#3'],
                                                            NOTES_DICT['C4' ]], Loudness.PP)
    ep_Fm_whole         = Harmony(Duration.WHOLE, [NOTES_DICT['F2' ], 
                                                    NOTES_DICT['C3' ],
                                                    NOTES_DICT['F3' ],
                                                    NOTES_DICT['G#3'],
                                                    NOTES_DICT['C4' ]], Loudness.PP)
    ep_GS_half_eight    = Harmony(DurationLegatto([Duration.HALF, Duration.EIGHTH]), [ NOTES_DICT['G#2'], 
                                                                                        NOTES_DICT['D#3'],
                                                                                        NOTES_DICT['G#3'],
                                                                                        NOTES_DICT['C4'],
                                                                                        NOTES_DICT['D#4']], Loudness.PP)
    ep_GS_quarterdot    = Harmony(Duration.QUARTER_DOT, [  NOTES_DICT['G#2'], 
                                                            NOTES_DICT['D#3'],
                                                            NOTES_DICT['G#3'],
                                                            NOTES_DICT['C4'],
                                                            NOTES_DICT['D#4']], Loudness.PP)

    # Drum Patterns Arrays
    precount = [(hihat_closed, n * QUANT) for n in range(3)] + [(hihat_open, 3 * QUANT)]
    bass_drum_1_25 = [(bass_drum_note, int(n * SIGN * QUANT)) for n in [BEGIN_OF_BAR, Duration.QUARTER_DOT.value]]
    bass_drum_35 = [(bass_drum_note, int(n * SIGN * QUANT)) for n in [DurationLegatto([Duration.HALF, Duration.EIGHTH]).value()]]
    chihat_1_2_3_4 = [(hihat_closed, n * QUANT) for n in range(4)]
    chihat_7 = [(hihat_closed, round(n/2 * QUANT)) for n in range(1,8)]
    chihat_8 = [(hihat_closed, round(n/2 * QUANT)) for n in range(8)]
    chihat_2_4 = [(hihat_closed.mp(), n * QUANT) for n in [1,3]]
    snare_2_4 = [(snare_note, n * QUANT) for n in [1,3]]
    ring_2_4 = [(ring_note, n * QUANT) for n in [1,3]]
    snare_var = [(snare_note, round(n * QUANT)) for n in [1, 3, 3.25]] + [(tom1, round(3.5 * QUANT)), (tom2, round(3.75 * QUANT))]
    crash_1 = [(crash, 0)]
    
    # Silent Bar
    silent_bar = Bar(SIGN, QUANT, [])
    # Drum Bars
    pre_count_bar = Bar(SIGN, QUANT, precount)
    verse_drum_01 = Bar(SIGN, QUANT, chihat_2_4)
    verse_drum_02_A = Bar(SIGN, QUANT, chihat_1_2_3_4 + bass_drum_1_25 + ring_2_4)
    verse_drum_02_B = Bar(SIGN, QUANT, chihat_1_2_3_4 + bass_drum_1_25 + bass_drum_35 + ring_2_4)
    chorus_drum_01_A = Bar(SIGN, QUANT, bass_drum_1_25 + chihat_2_4)
    chorus_drum_01_B = Bar(SIGN, QUANT, bass_drum_1_25 + bass_drum_35 + chihat_2_4)
    chorus_drum_02_A_crash = Bar(SIGN, QUANT, crash_1 + chihat_7 + snare_2_4 + bass_drum_1_25)
    chorus_drum_02_B = Bar(SIGN, QUANT, chihat_8 + snare_2_4 + bass_drum_1_25 + bass_drum_35)
    chorus_drum_02_C = Bar(SIGN, QUANT, chihat_8 + snare_2_4 + bass_drum_1_25)
    chorus_drum_02_D = Bar(SIGN, QUANT, chihat_8 + snare_var + bass_drum_1_25 + bass_drum_35)
    end_drums_A = Bar(SIGN, QUANT, crash_1 + chihat_2_4 + bass_drum_1_25)
    end_drums_B = Bar(SIGN, QUANT, chihat_2_4 + bass_drum_1_25 + bass_drum_35)
    end_drums_C = Bar(SIGN, QUANT, [(hihat_open, 0)])
    # Bass Bars
    verse_bass_A  = Bar(SIGN, QUANT, [(f1_quarterdot, BEGIN_OF_BAR), 
                                      (gs1_half_eight, round(Duration.QUARTER_DOT.value * SIGN * QUANT))])
    verse_bass_B  = Bar(SIGN, QUANT, [(ds1_quarterdot, BEGIN_OF_BAR), 
                                      (cs1_half_eight, round(Duration.QUARTER_DOT.value * SIGN * QUANT))])
    bridge_bass_A = Bar(SIGN, QUANT, [(f1_quarterdot, BEGIN_OF_BAR), 
                                      (ds1_half_eight, round(Duration.QUARTER_DOT.value * SIGN * QUANT))])
    bridge_bass_B = Bar(SIGN, QUANT, [(c1_quarterdot, BEGIN_OF_BAR), 
                                      (cs1_half_eight, round(Duration.QUARTER_DOT.value * SIGN * QUANT))])
    bridge_bass_C = Bar(SIGN, QUANT, [(f1_quarterdot, BEGIN_OF_BAR), 
                                      (ds1_quarterdot, round(Duration.QUARTER_DOT.value * SIGN * QUANT)), 
                                      (cs1_whole_quarter, round(Duration.HALF_DOT.value * SIGN * QUANT))])
    chorus_bass_A = Bar(SIGN, QUANT, [(f1_quarterdot.fff(), BEGIN_OF_BAR),
                                      (cs1_half_eight.fff(), round(Duration.QUARTER_DOT.value * SIGN * QUANT))])
    chorus_bass_B = Bar(SIGN, QUANT, [(gs1_quarterdot.fff(), BEGIN_OF_BAR),
                                      (ds1_half_eight.fff(), round(Duration.QUARTER_DOT.value * SIGN * QUANT))])
    end_bass = Bar(SIGN, QUANT, [(f1_whole , BEGIN_OF_BAR)])      
    # EP Bars
    verse_EP_A  = Bar(SIGN, QUANT, [(ep_Fm_quarterdot, BEGIN_OF_BAR), 
                                      (ep_GS_half_eight, round(Duration.QUARTER_DOT.value * SIGN * QUANT))])
    verse_EP_B  = Bar(SIGN, QUANT, [(ep_DS_quarterdot, BEGIN_OF_BAR), 
                                      (ep_CS_half_eight, round(Duration.QUARTER_DOT.value * SIGN * QUANT))])
    bridge_EP_A = Bar(SIGN, QUANT, [(ep_Fm_quarterdot, BEGIN_OF_BAR), 
                                      (ep_DS_half_eight, round(Duration.QUARTER_DOT.value * SIGN * QUANT))])
    bridge_EP_B = Bar(SIGN, QUANT, [(ep_Cm_quarterdot, BEGIN_OF_BAR), 
                                      (ep_CS_half_eight, round(Duration.QUARTER_DOT.value * SIGN * QUANT))])
    bridge_EP_C = Bar(SIGN, QUANT, [(ep_Fm_quarterdot, BEGIN_OF_BAR), 
                                      (ep_DS_quarterdot, round(Duration.QUARTER_DOT.value * SIGN * QUANT)), 
                                      (ep_CS_whole_quarter, round(Duration.HALF_DOT.value * SIGN * QUANT))])
    chorus_EP_A = Bar(SIGN, QUANT, [(ep_Fm_quarterdot, BEGIN_OF_BAR),
                                      (ep_CS_half_eight, round(Duration.QUARTER_DOT.value * SIGN * QUANT))])
    chorus_EP_B = Bar(SIGN, QUANT, [(ep_GS_quarterdot, BEGIN_OF_BAR),
                                      (ep_DS_half_eight, round(Duration.QUARTER_DOT.value * SIGN * QUANT))])
    end_EP = Bar(SIGN, QUANT, [(ep_Fm_whole , BEGIN_OF_BAR)])                                
    

    # Instruments
    drum = DrumLine([
        (pre_count_bar, 1), # 1 
        (verse_drum_01, 18+4), # 18 + 4
        ([chorus_drum_01_A, chorus_drum_01_B], 8), # 16
        (verse_drum_01, 2), # 2
        ([verse_drum_02_A, verse_drum_02_B], 4), # 8
        (verse_drum_01, 4), # 4
        ([chorus_drum_02_A_crash, chorus_drum_02_B, chorus_drum_02_C, chorus_drum_02_D], 10),
        ([end_drums_A, end_drums_B, end_drums_C], 1),
    ])
    bass = Bass([
        (silent_bar, 1), # 1                                                        # Counting
        ([verse_bass_A, verse_bass_B], 1+8), # 18                                   # Verse  1
        ([bridge_bass_A, bridge_bass_B, bridge_bass_C, silent_bar], 1), # 4         # Bridge 1
        ([chorus_bass_A, chorus_bass_B], 8), # 16                                   # Chorus 1
        ([verse_bass_A, verse_bass_B], 1+4), # 2 + 8                                # Verse  2
        ([bridge_bass_A, bridge_bass_B, bridge_bass_C, silent_bar], 1), # 4         # Bridge 2
        ([chorus_bass_A, chorus_bass_B], 8+4+8), # 40                               # Chorus 2, Chorus Variation, Chorus 3
        ([verse_bass_A, verse_bass_B, end_bass], 1), # 3                            # Ending
    ])
    ep = OtherInstrument([
        (silent_bar, 1), # 1                                                        # Counting
        ([verse_EP_A, verse_EP_B], 1+8), # 18                                   # Verse  1
        ([bridge_EP_A, bridge_EP_B, bridge_EP_C, silent_bar], 1), # 4         # Bridge 1
        ([chorus_EP_A, chorus_EP_B], 8), # 16                                   # Chorus 1
        ([verse_EP_A, verse_EP_B], 1+4), # 2 + 8                                # Verse  2
        ([bridge_EP_A, bridge_EP_B, bridge_EP_C, silent_bar], 1), # 4         # Bridge 2
        ([chorus_EP_A, chorus_EP_B], 8+4+8), # 40                               # Chorus 2, Chorus Variation, Chorus 3
        ([verse_EP_A, verse_EP_B, end_EP], 1), # 3                            # Ending
    ], EP_CHANNEL)

    # Sequencer
    PlaySequencer(BPM, SIGN, KEY, Instruments(drum, bass, [ep])).play()

def play_dont_dream_its_over():
    
    SIGN = 4
    QUANT = 4
    BPM = 80
    KEY = 'D#'

    BEGIN_OF_BAR = 0

    # Drum Notes
    bass_drum_note = BassDrumNote()
    snare_note = SnareDrumNote()
    ring_note = SnareRingNote()
    hihat_closed = ClosedHiHatNote()
    hihat_open = OpenHiHatNote()
    crash = Crash1DrumNote()
    tom1 = Tom1Note()
    tom2 = Tom2Note()

    # Bass Notes
    g1_half        = Note(Duration.HALF, NOTES_DICT['G1'], Loudness.FF)
    g1_quarterdot  = Note(Duration.QUARTER_DOT, NOTES_DICT['G1'], Loudness.FF)
    g1_quarter     = Note(Duration.QUARTER, NOTES_DICT['G1'], Loudness.FF)
    g1_eighth      = Note(Duration.EIGHTH, NOTES_DICT['G1'], Loudness.FF)
    gs1_half       = Note(Duration.HALF, NOTES_DICT['G#1'], Loudness.FF)
    gs1_quarterdot = Note(Duration.QUARTER_DOT, NOTES_DICT['G#1'], Loudness.FF)
    gs1_quarter    = Note(Duration.QUARTER, NOTES_DICT['G#1'], Loudness.FF)
    gs1_eighth     = Note(Duration.EIGHTH, NOTES_DICT['G#1'], Loudness.FF)
    as1_half       = Note(Duration.HALF, NOTES_DICT['A#1'], Loudness.FF)
    as1_quarterdot = Note(Duration.QUARTER_DOT, NOTES_DICT['A#1'], Loudness.FF)
    as1_quarter    = Note(Duration.QUARTER, NOTES_DICT['A#1'], Loudness.FF)
    as1_eighth     = Note(Duration.EIGHTH, NOTES_DICT['A#1'], Loudness.FF)
    c2_half        = Note(Duration.HALF, NOTES_DICT['C2'], Loudness.FF)
    c2_quarterdot  = Note(Duration.QUARTER_DOT, NOTES_DICT['C2'], Loudness.FF)
    c2_quarter     = Note(Duration.QUARTER, NOTES_DICT['C2'], Loudness.FF)
    c2_eighth      = Note(Duration.EIGHTH, NOTES_DICT['C2'], Loudness.FF)
    cs2_half        = Note(Duration.HALF, NOTES_DICT['C#2'], Loudness.FF)
    cs2_quarterdot  = Note(Duration.QUARTER_DOT, NOTES_DICT['C#2'], Loudness.FF)
    cs2_quarter     = Note(Duration.QUARTER, NOTES_DICT['C#2'], Loudness.FF)
    cs2_eighth      = Note(Duration.EIGHTH, NOTES_DICT['C#2'], Loudness.FF)
    ds2_whole        = Note(Duration.WHOLE, NOTES_DICT['D#2'], Loudness.FF)
    ds2_half       = Note(Duration.HALF, NOTES_DICT['D#2'], Loudness.FF)
    ds2_quarterdot = Note(Duration.QUARTER_DOT, NOTES_DICT['D#2'], Loudness.FF)
    ds2_quarter    = Note(Duration.QUARTER, NOTES_DICT['D#2'], Loudness.FF)
    ds2_eighth     = Note(Duration.EIGHTH, NOTES_DICT['D#2'], Loudness.FF)
    

    # EP Harmonies
    ep_Cm_half = Harmony(Duration.HALF, [ NOTES_DICT['C2' ], 
                                                NOTES_DICT['G2' ],
                                                NOTES_DICT['C3' ],
                                                NOTES_DICT['D#3'],
                                                NOTES_DICT['G3' ]], Loudness.PP)
    ep_DS_half = Harmony(Duration.HALF, [ NOTES_DICT['D#2'], 
                                                NOTES_DICT['A#2' ],
                                                NOTES_DICT['D#3' ],
                                                NOTES_DICT['G3'],
                                                NOTES_DICT['A#3' ]], Loudness.PP)
    ep_GS_half    = Harmony(Duration.HALF, [ NOTES_DICT['G#2'], 
                                                                                        NOTES_DICT['D#3'],
                                                                                        NOTES_DICT['G#3'],
                                                                                        NOTES_DICT['C4'],
                                                                                        NOTES_DICT['D#4']], Loudness.PP)
    ep_AS_half    = Harmony(Duration.HALF, [ NOTES_DICT['A#2'], 
                                            NOTES_DICT['F3'],
                                            NOTES_DICT['A#3'],
                                            NOTES_DICT['D4'],
                                            NOTES_DICT['F4']], Loudness.PP)
    ep_GD_half    = Harmony(Duration.HALF, [ NOTES_DICT['G2'], 
                                            NOTES_DICT['D3'],
                                            NOTES_DICT['G3'],
                                            NOTES_DICT['B4'],
                                            NOTES_DICT['D4']], Loudness.PP)


    # Drum Patterns Arrays
    precount = [(hihat_closed, n * QUANT) for n in range(3)] + [(hihat_open, 3 * QUANT)]
    bass_drum_verse = [(bass_drum_note, round(n * QUANT)) for n in [0, 1.5, 2, 3.5]]
    ring_2_4 = [(ring_note, n*QUANT) for n in [1,3]]
    
    # Silent Bar
    silent_bar = Bar(SIGN, QUANT, [])
    # Drum Bars
    pre_count_bar = Bar(SIGN, QUANT, precount)
    verse_drum_bar = Bar(SIGN, QUANT, bass_drum_verse + ring_2_4 + precount)
    drum_end = Bar(SIGN, QUANT, [(hihat_open, BEGIN_OF_BAR)])
    
    # Bass Bars
    intro = Bar(SIGN, QUANT, [(ds2_quarter, BEGIN_OF_BAR), 
                                      (ds2_eighth, round(Duration.QUARTER_DOT.value * SIGN * QUANT)),
                                      (ds2_quarter, round(DurationLegatto([Duration.QUARTER_DOT, Duration.EIGHTH]).value() * SIGN * QUANT)),
                                      (ds2_eighth, round(DurationLegatto([Duration.QUARTER_DOT, Duration.QUARTER_DOT, Duration.EIGHTH]).value() * SIGN * QUANT)),
                                    ])

    verse_bass_DS  = Bar(SIGN, QUANT, [(ds2_quarter, BEGIN_OF_BAR), 
                                      (ds2_eighth, round(Duration.QUARTER_DOT.value * SIGN * QUANT)),
                                      (ds2_quarter, round(DurationLegatto([Duration.QUARTER_DOT, Duration.EIGHTH]).value() * SIGN * QUANT)),
                                    ])
    verse_bass_C  = Bar(SIGN, QUANT, [(c2_quarter, BEGIN_OF_BAR), 
                                      (c2_eighth, round(Duration.QUARTER_DOT.value * SIGN * QUANT)),
                                      (c2_quarter, round(DurationLegatto([Duration.QUARTER_DOT, Duration.EIGHTH]).value() * SIGN * QUANT)),
                                    ])
    verse_bass_GS  = Bar(SIGN, QUANT, [(gs1_quarter, BEGIN_OF_BAR), 
                                      (gs1_eighth, round(Duration.QUARTER_DOT.value * SIGN * QUANT)),
                                      (gs1_quarter, round(DurationLegatto([Duration.QUARTER_DOT, Duration.EIGHTH]).value() * SIGN * QUANT)),
                                    ])
    verse_bass_GD  = Bar(SIGN, QUANT, [(g1_quarter, BEGIN_OF_BAR), 
                                      (g1_eighth, round(Duration.QUARTER_DOT.value * SIGN * QUANT)),
                                      (g1_quarter, round(DurationLegatto([Duration.QUARTER_DOT, Duration.EIGHTH]).value() * SIGN * QUANT)),
                                    ])
    chorus_bass_A  = Bar(SIGN, QUANT, [(gs1_quarter, BEGIN_OF_BAR), 
                                      (gs1_eighth, round(Duration.QUARTER_DOT.value * SIGN * QUANT)),
                                      (as1_quarter, round(DurationLegatto([Duration.QUARTER_DOT, Duration.EIGHTH]).value() * SIGN * QUANT)),
                                      (as1_eighth, round(DurationLegatto([Duration.QUARTER_DOT, Duration.QUARTER_DOT, Duration.EIGHTH]).value() * SIGN * QUANT)),
                                    ])                                
    chorus_bass_B  = Bar(SIGN, QUANT, [(ds2_quarter, BEGIN_OF_BAR), 
                                      (ds2_eighth, round(Duration.QUARTER_DOT.value * SIGN * QUANT)),
                                      (c2_quarter, round(DurationLegatto([Duration.QUARTER_DOT, Duration.EIGHTH]).value() * SIGN * QUANT)),
                                      (c2_eighth, round(DurationLegatto([Duration.QUARTER_DOT, Duration.QUARTER_DOT, Duration.EIGHTH]).value() * SIGN * QUANT)),
                                    ])                                                                
    solo_bass_A  = Bar(SIGN, QUANT, [(ds2_quarter, BEGIN_OF_BAR), 
                                      (ds2_eighth, round(Duration.QUARTER_DOT.value * SIGN * QUANT)),
                                      (gs1_quarter, round(DurationLegatto([Duration.QUARTER_DOT, Duration.EIGHTH]).value() * SIGN * QUANT)),
                                      (gs1_eighth, round(DurationLegatto([Duration.QUARTER_DOT, Duration.QUARTER_DOT, Duration.EIGHTH]).value() * SIGN * QUANT)),
                                    ])                                
    solo_bass_B  = Bar(SIGN, QUANT, [(cs2_quarter, BEGIN_OF_BAR), 
                                      (cs2_eighth, round(Duration.QUARTER_DOT.value * SIGN * QUANT)),
                                      (cs2_quarter, round(DurationLegatto([Duration.QUARTER_DOT, Duration.EIGHTH]).value() * SIGN * QUANT)),
                                    ])
    bass_end = Bar(SIGN, QUANT, [(ds2_whole, BEGIN_OF_BAR)])

                    
    # verse_bass_B  = Bar(SIGN, QUANT, [(c1_quarter, BEGIN_OF_BAR), 
    #                                     (c1_quarter, round(Duration.QUARTER.value * SIGN * QUANT)), 
    #                                     (c1_quarter, round(2 * Duration.QUARTER.value * SIGN * QUANT)), 
    #                                     (c1_quarter, round(3 * Duration.QUARTER.value * SIGN * QUANT)), 
                                      
    #                                 ])
    
    drum = DrumLine([
        (pre_count_bar, 1+4),
        (verse_drum_bar, 8 + 6+2 + 8 + 6+1 + 8+3+2 + 8 + 6+1 + 6+2),
        (drum_end, 1),
    ])
    bass = Bass([
        # Intro
        (silent_bar, 1), # 1 Counting
        ([intro, verse_bass_DS], 2), # 4 Intro
        # Verse 1
        ([verse_bass_DS, verse_bass_C, verse_bass_GS, verse_bass_GD], 2), # 8 
        # Chorus 1
        ([chorus_bass_A, chorus_bass_B], 3), # 6 
        (verse_bass_GS, 2), # 2 
        # Verse 2
        ([verse_bass_DS, verse_bass_C, verse_bass_GS, verse_bass_GD], 2), # 8 
        # Chorus 2
        ([chorus_bass_A, chorus_bass_B], 3), # 6 
        (verse_bass_GS, 1), # 1 
        # Solo
        ([verse_bass_DS, verse_bass_C, verse_bass_GS, verse_bass_GD], 2), # 8 Organ
        (solo_bass_A, 3), # 3 Guitar
        (solo_bass_B, 2), # 2 Guitar
        # Verse 3
        ([verse_bass_DS, verse_bass_C, verse_bass_GS, verse_bass_GD], 2), # 8 
        # Chorus 3 
        ([chorus_bass_A, chorus_bass_B], 3), # 6 
        (verse_bass_GS, 1), # 1 
        # Final 
        ([chorus_bass_A, chorus_bass_B], 3), # 6 
        (verse_bass_GS, 2), # 2 
        (bass_end, 1),
        
    ])

    # Sequencer
    PlaySequencer(BPM, SIGN, KEY, Instruments(drum, bass)).play()


def play():
    play_hello()
    # play_dont_dream_its_over()


if __name__ == "__main__":
    play()
    