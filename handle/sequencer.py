import re

from general.constants import *
from general.music import *

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

def play():
    bd = BassDrumNote(Loudness.MP)
    sd = SnareDrumNote(Loudness.MP)
    hh = ClosedHiHatNote(Loudness.MP)
    

    bar = Bar(4, 4, [   (bd,0), 
                        (bd,8),
                        (bd,10),
                        (sd,4),
                        (sd.var(2),12),
                        (hh,0),
                        (hh,2),
                        (hh,4),
                        (hh,6),
                        (hh,8),
                        (hh,10),
                        (hh,12),
                        (hh.var(0),14),
                    ]
            )

    fim = Bar(4, 4, [(hh.var(2),0)])

    drum = DrumLine([(bar,4), (fim, 1)])

    insts = Instruments(drum)

    seq = PlaySequencer(120, 4, 'C', insts)

    seq.play()


if __name__ == "__main__":
    play()
    