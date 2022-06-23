import random
import time
from typing import Union, List, Tuple
from enum import Enum

from .constants import  *
from . import eventlib, aseq

# TODO This lib cannot handle different bar slot sizes for now

HUMAN_FACTOR_AMPLITUDE = 5

class Duration(Enum):
    WHOLE = 1
    HALF = 1/2
    QUARTER = 1/4
    EIGHTH = 1/8
    SIXTEENTH = 1/16
    
    HALF_DOT = HALF + QUARTER
    QUARTER_DOT = QUARTER + EIGHTH
    EIGHTH_DOT = EIGHTH + SIXTEENTH

class DurationLegatto:
    def __init__(self, legatto_list: List[Duration]) -> None:
        self.__leg = legatto_list
    def value(self):
        return sum([l.value for l in self.__leg])

class Loudness(Enum):
    SILENT = 0
    PPP = 21
    PP = 36
    P = 51
    MP = 66
    MF = 81
    F = 96
    FF = 111
    FFF = 126

def loudness_to_velocity(loud: Loudness):
    return max(LOW,min(HIGH,int(random.gauss(loud.value, HUMAN_FACTOR_AMPLITUDE))))

class Note:
    def __init__(self, duration: Union[Duration, DurationLegatto], pitch: int, loudness: Loudness) -> None:
        self.__duration = duration
        self.__dur = duration.value if isinstance(duration, Duration) else duration.value()
        self.__pit = pitch
        self.__loud = loudness
    def get_velocity(self):
        return loudness_to_velocity(self.__loud)
    def to_midi_note(self, channel, bar_slots):
        return MIDINote(channel=channel, note=self.__pit, velocity=self.get_velocity(), duration_slots=round(bar_slots*self.__dur))
    def fff(self):
        return Note(self.__duration, self.__pit, Loudness.FFF)
    def ff(self):
        return Note(self.__duration, self.__pit, Loudness.FF)
    def f(self):
        return Note(self.__duration, self.__pit, Loudness.F)
    def mf(self):
        return Note(self.__duration, self.__pit, Loudness.MF)
    def mp(self):
        return Note(self.__duration, self.__pit, Loudness.MP)
    def p(self):
        return Note(self.__duration, self.__pit, Loudness.P)
    def pp(self):
        return Note(self.__duration, self.__pit, Loudness.PP)
    def ppp(self):
        return Note(self.__duration, self.__pit, Loudness.PPP)

class BassDrumNote(Note):
    def __init__(self, loudness: Loudness = Loudness.F) -> None:
        super().__init__(Duration.EIGHTH, BASS_DRUM_NOTE, loudness)

class SnareDrumNote(Note):
    def __init__(self, loudness: Loudness = Loudness.F) -> None:
        super().__init__(Duration.EIGHTH, SNARE_DRUM_NOTE, loudness)
    def var(self, num: int = 0, loudness: Union[Loudness, None] = None):
        if loudness is None:
            loudness = self._Note__loud
        options = [ 
                    SnareRingNote,
                    Tom1Note,
                    Tom2Note,
                    Tom3Note,
                    Tom4Note,
                    Floor1Note,
                    Floor2Note
                  ]
        if num < 0 or num >= len(options):
            num = 0
        return options[num](loudness=loudness)

class SnareRingNote(Note):
    def __init__(self, loudness: Loudness = Loudness.F) -> None:
        super().__init__(Duration.EIGHTH, SNARE_RING_NOTE, loudness)

class Tom1Note(Note):
    def __init__(self, loudness: Loudness = Loudness.F) -> None:
        super().__init__(Duration.EIGHTH, TOM1_NOTE, loudness)

class Tom2Note(Note):
    def __init__(self, loudness: Loudness = Loudness.F) -> None:
        super().__init__(Duration.EIGHTH, TOM2_NOTE, loudness)

class Tom3Note(Note):
    def __init__(self, loudness: Loudness = Loudness.F) -> None:
        super().__init__(Duration.EIGHTH, TOM3_NOTE, loudness)

class Tom4Note(Note):
    def __init__(self, loudness: Loudness = Loudness.F) -> None:
        super().__init__(Duration.EIGHTH, TOM4_NOTE, loudness)

class Floor1Note(Note):
    def __init__(self, loudness: Loudness = Loudness.F) -> None:
        super().__init__(Duration.EIGHTH, FLOOR1_NOTE, loudness)

class Floor2Note(Note):
    def __init__(self, loudness: Loudness = Loudness.F) -> None:
        super().__init__(Duration.EIGHTH, FLOOR2_NOTE, loudness)

class ClosedHiHatNote(Note):
    def __init__(self, loudness: Loudness = Loudness.F) -> None:
        super().__init__(Duration.EIGHTH, CLOSED_HIHAT_NOTE, loudness)
    def var(self, num: int = 0, loudness: Union[Loudness, None] = None):
        if loudness is None:
            loudness = self._Note__loud
        options = [ 
                    OpenHiHatNote,
                    RideDrumNote,
                    Crash1DrumNote,
                    Crash2DrumNote
                  ]
        if num < 0 or num >= len(options):
            num = 0
        return options[num](loudness=loudness)

class OpenHiHatNote(Note):
    def __init__(self, loudness: Loudness = Loudness.F) -> None:
        super().__init__(Duration.EIGHTH, OPEN_HIHAT_NOTE, loudness)

class Crash1DrumNote(Note):
    def __init__(self, loudness: Loudness = Loudness.F) -> None:
        super().__init__(Duration.EIGHTH, CRASH1_NOTE, loudness)

class Crash2DrumNote(Note):
    def __init__(self, loudness: Loudness = Loudness.F) -> None:
        super().__init__(Duration.EIGHTH, CRASH2_NOTE, loudness)

class RideDrumNote(Note):
    def __init__(self, loudness: Loudness = Loudness.F) -> None:
        super().__init__(Duration.EIGHTH, RIDE_NOTE, loudness)

class Harmony:
    def __init__(self, duration: Union[Duration, DurationLegatto], notes_pitch: List[int], loudness: Loudness) -> None:
        self.__duration = duration
        self.__dur = duration.value if isinstance(duration, Duration) else duration.value()
        self.__notes_pitch = notes_pitch
        self.__loud = loudness
    def get_velocity(self):
        return loudness_to_velocity(self.__loud)
    def to_note_list(self):
        return [Note(self.__duration, pit, self.__loud) for pit in self.__notes_pitch]
    def to_midi_note_list(self, channel, bar_slots):
        return [Note(self.__duration, pit, self.__loud).to_midi_note(channel, bar_slots) for pit in self.__notes_pitch]

MusicalElement = Union[Note, Harmony]

class Bar:
    def __init__(self, signature: int, # Signature is the # of Quarter notes in the bar. Assuming bars are X/4
                       quantization: int, # Number of divisions of the quarter note. Quantization of 4 in a 4/4 bar means 16 position slots
                       elements: List[Tuple[MusicalElement, int]] # List of pair of musical elements and positions (ranges from 0 to signature*quantization-1)
                ) -> None:
        self.__sign = signature
        self.__quant = quantization
        self.__el: List[MusicalElement] = [[] for _ in range(self.slots())]
        for el, pos in elements:
            self.__el[pos].append(el)
        self.__autoread_position = 0
    def slots(self):
        return self.__sign * self.__quant
    def signature(self):
        return self.__sign
    def quantization(self):
        return self.__quant
    def elements(self, position) -> List[Note]:
        output = []
        for el in self.__el[position]:
            if isinstance(el, Harmony):
                output += el.to_note_list()
            else:
                output += [el]
        return output
    def reset_autoread(self):
        self.__autoread_position = 0
    def next_element(self):
        output = self.elements(self.__autoread_position)
        self.__autoread_position = (self.__autoread_position + 1) % self.slots()
        return output
    def is_last_position(self):
        return self.__autoread_position == self.slots() - 1

class BarS:
    def __init__(self, 
                    bar_list: List[Tuple[Union[Bar,List[Bar]],int]] # List of pairs of Bars (or list of Bars) and how many times should it be repeated
                ) -> None:
        self.__barlist: List[Bar] = []
        for el, rep in bar_list:
            if isinstance(el, Bar):
                el = [el]
            for _ in range(rep):
                for b in el:
                    self.__barlist.append(b)
        assert max([el.slots() for el in self.__barlist]) == min([el.slots() for el in self.__barlist])
        self.__slots = self.__barlist[0].slots()
        self.__autoread_position = 0
        self.__current_bar_index = 0
    def slots(self):
        return self.__slots
    def reset_autoread(self):
        self.__autoread_position = 0
        self.__current_bar_index = 0
    def get_elements(self, bar_index, bar_position) -> List[Note]:
        return self.__barlist[bar_index].elements(bar_position)
    def next_elements(self):
        output = self.get_elements(self.__current_bar_index, self.__autoread_position)
        self.__autoread_position = self.__autoread_position + 1
        if self.__autoread_position >= len(self.__barlist[self.__current_bar_index]):
            self.__autoread_position = 0
            self.__autoread_position = (self.__autoread_position + 1) % len(self.__barlist)
        return output
    def ended(self, position):
        bar_index = int(position / self.slots())
        return bar_index >= len(self.__barlist)

class DrumLine(BarS):
    def __init__(self, bar_list: List[Tuple[Union[Bar, List[Bar]], int]]) -> None:
        super().__init__(bar_list)
    def get_midi_list(self, absolute_position):
        bar_index = int(absolute_position / self.slots())
        pos = absolute_position % self.slots()
        return [el.to_midi_note(DRUM_CHANNEL, self.slots()) for el in self.get_elements(bar_index, pos)]

class DrumLoop:
    def __init__(self) -> None:
        pass

class Bass(BarS):
    def __init__(self, bar_list: List[Tuple[Union[Bar, List[Bar]], int]]) -> None:
        super().__init__(bar_list)
    def get_midi_list(self, absolute_position):
        bar_index = int(absolute_position / self.slots())
        pos = absolute_position % self._BarS__slots
        return [el.to_midi_note(BASS_CHANNEL, self.slots()) for el in self.get_elements(bar_index, pos)]

class OtherInstrument(BarS):
    def __init__(self, bar_list: List[Tuple[Union[Bar, List[Bar]], int]], channel) -> None:
        super().__init__(bar_list)
        self.__channel = channel
    def get_midi_list(self, absolute_position):
        bar_index = int(absolute_position / self.slots())
        pos = absolute_position % self._BarS__slots
        return [el.to_midi_note(self.__channel, self.slots()) for el in self.get_elements(bar_index, pos)]

class Instruments:
    def __init__(self,  drums: DrumLine = None,
                        bass: Bass = None,
                        other: List[OtherInstrument] = []
                ) -> None:
        self.__insts : List[Union[DrumLine,Bass,OtherInstrument]] = []
        if drums is not None:
            self.__insts.append(drums)
        if bass is not None:
            self.__insts.append(bass)
        self.__insts += other
    def get_midi_list(self, absolute_position):
        out = []
        for inst in self.__insts:
            if not inst.ended(absolute_position):
                out += inst.get_midi_list(absolute_position)
        return out
    def get_slots(self):
        return self.__insts[0].slots()
    def all_ended(self, position):
        return all([inst.ended(position) for inst in self.__insts])
        
class LoopJam:
    def __init__(self,  drums: DrumLoop = None,
                        bass: Bass = None,
                        other: List[OtherInstrument] = []
                ) -> None:
        pass

class PlaySequencer:
    def __init__(self, 
                    tempo: int, 
                    signature: int, 
                    key: str, 
                    instruments: Instruments, # Union[Instruments, LoopJam],
                    loop: bool = False
                ) -> None:
        self.__tempo = tempo
        self.__sign = signature
        self.__key = key
        self.__loop = loop
        self.__intruments = instruments
        self.__bar_slots = self.__intruments.get_slots()
        self.__time_sleep = 60. / (self.__tempo * 4)
        self.__current_position = 0
        self.__offQ = MIDIOffQueue()
    def play(self):
        while not self.__intruments.all_ended(self.__current_position) or not self.__offQ.isempty():
            notes = self.__intruments.get_midi_list(self.__current_position)
            for n in notes:
                aseq.send(n.on())
            self.__offQ.add_list(notes)
            for n in self.__offQ.get_next():
                aseq.send(n)
            self.__current_position += 1
            time.sleep(self.__time_sleep)
            



# ============================================ MIDI ============================================ #


class MIDINote:
    def __init__(self, channel, note, velocity, duration_slots):
        self.__on = eventlib.create_note_on_event(channel, note, velocity)
        self.__off = eventlib.create_note_off_event(channel, note)
        self.__dur = duration_slots
    def on(self):
        return self.__on
    def off(self):
        return self.__off
    def duration(self):
        return self.__dur

class MIDIOffQueue:
    def __init__(self):
        self.__queue = []
    def add_midi(self, midi: MIDINote):
        dur = midi.duration()
        while dur >= len(self.__queue):
            self.__queue.append([])
        self.__queue[dur].append(midi)
    def add_list(self, l):
        for el in l:
            self.add_midi(el)
    def get_next(self):
        if len(self.__queue) == 0:
            return []
        out = list(map(lambda x: x.off(), self.__queue[0]))
        del self.__queue[0]
        return out
    def isempty(self):
        return len(self.__queue) == 0
