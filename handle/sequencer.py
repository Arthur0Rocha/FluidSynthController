import re
import time

from general.constants import *
from general import eventlib, aseq


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

class BassDrumPattern:
    def __init__(self, quantization=16, positions=[0, 8, 10], durations=[4, 2, 4], velocities=[90, 90, 90]):
        self.quant = quantization
        self.midi = [[] for _ in range(self.quant)]
        self.pos = positions
        self.dur = durations
        self.vel = velocities
        for i in range(self.quant):
            if i in self.pos:
                self.midi[i].append(eventlib.create_note_on_event(DRUM_CHANNEL, BASS_DRUM_NOTE, self.vel[self.pos.index(i)]))
                off_index = (i + self.dur[self.pos.index(i)]) % self.quant
                self.midi[off_index].append(eventlib.create_note_off_event(DRUM_CHANNEL, BASS_DRUM_NOTE))
    def get_midi(self, position: int):
        return self.midi[position]

class SnareDrumPattern:
    def __init__(self, quantization=16, positions=[4, 12], durations=[4, 4], velocities=[90, 90]):
        self.quant = quantization
        self.midi = [[] for _ in range(self.quant)]
        self.pos = positions
        self.dur = durations
        self.vel = velocities
        for i in range(self.quant):
            if i in self.pos:
                self.midi[i].append(eventlib.create_note_on_event(DRUM_CHANNEL, SNARE_DRUM_NOTE, self.vel[self.pos.index(i)]))
                off_index = (i + self.dur[self.pos.index(i)]) % self.quant
                self.midi[off_index].append(eventlib.create_note_off_event(DRUM_CHANNEL, SNARE_DRUM_NOTE))
    def get_midi(self, position: int):
        return self.midi[position]

class OvertopDrumPattern:
    def __init__(self, quantization=16, positions=[0, 2, 4, 6, 8, 10, 12, 14], durations=[2, 2, 2, 2, 2, 2, 2, 2], velocities=[90, 90, 90, 90, 90, 90, 90, 90]):
        self.quant = quantization
        self.midi = [[] for _ in range(self.quant)]
        self.pos = positions
        self.dur = durations
        self.vel = velocities
        for i in range(self.quant):
            if i in self.pos:
                self.midi[i].append(eventlib.create_note_on_event(DRUM_CHANNEL, CLOSED_HIHAT_NOTE, self.vel[self.pos.index(i)]))
                off_index = (i + self.dur[self.pos.index(i)]) % self.quant
                self.midi[off_index].append(eventlib.create_note_off_event(DRUM_CHANNEL, CLOSED_HIHAT_NOTE))
    def get_midi(self, position: int):
        return self.midi[position]

class DrumPattern:
    def __init__(self, quantization=16, bass_drum_pattern=None, snare_pattern=None, overtop_pattern=None):
        self.quant = quantization
        self.bass_drum_pattern = bass_drum_pattern
        if self.bass_drum_pattern is None:
            self.bass_drum_pattern = BassDrumPattern()
        self.snare_pattern = snare_pattern
        if self.snare_pattern is None:
            self.snare_pattern = SnareDrumPattern()
        self.overtop_pattern = overtop_pattern
        if self.overtop_pattern is None:
            self.overtop_pattern = OvertopDrumPattern()

        self.midi = []
        for i in range(self.quant):
            self.midi.append(self.bass_drum_pattern.get_midi(i) + self.snare_pattern.get_midi(i) + self.overtop_pattern.get_midi(i))
    def get_midi(self, position: int):
        return self.midi[position]

class BassPattern:
    def __init__(self):
        pass
    def get_midi(self):
        return []

class OtherPattern:
    def __init__(self, channel):
        self.channel = channel
    def get_midi(self):
        return []

class PiecePattern:
    def __init__(self, quantization=16):
        self.quant = quantization
        self.instruments = []
        self.midi = [[] for _ in range(self.quant)]
    def add_instrument_pattern(self, instrument_pattern):
        self.instruments.append(instrument_pattern)
        for i in range(self.quant):
            self.midi[i] = self.midi[i] + instrument_pattern.get_midi(i)
    def get_midi(self, position):
        return self.midi[position]

class SongPattern:
    def __init__(self, tempo=120, signature=4, key='C', quantization=16): # quantization should be a multiple of the signature
        self.tempo = tempo
        self.sign = signature
        self.key = key
        self.quant = quantization
        self.time_between_quants_ms = int(1000. * 60 * self.sign / (self.tempo * self.quant))
        self.piece_patterns = []
    def add_piece_pattern(self, piece_pattern: PiecePattern):
        self.piece_patterns.append(piece_pattern)
    def play(self):
        assert len(self.piece_patterns) > 0
        self.current_piece_pattern = 0
        self.current_quant_position = 0
    def next_pattern(self):
        self.current_piece_pattern = (self.current_piece_pattern + 1) % len(self.piece_patterns)
    def get_midi(self):
        call_me_back_in_ms = self.time_between_quants_ms
        output = (self.piece_patterns[self.current_piece_pattern].get_midi(self.current_quant_position), call_me_back_in_ms)
        self.current_quant_position = (self.current_quant_position + 1) % self.quant
        return output

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
    song = SongPattern()
    piece = PiecePattern()
    song.add_piece_pattern(piece)
    piece.add_instrument_pattern(DrumPattern())
    song.play()

    while True:
        midi, t = song.get_midi()
        for m in midi:
            aseq.send(m)
        time.sleep(t/1000.)

if __name__ == "__main__":
    play()