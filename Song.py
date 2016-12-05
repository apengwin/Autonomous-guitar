import numpy as np
from guitar_playing_and_such import *

PREFIX_LIST = ["large","long","breve","whole","half","quarter",
             "eighth","sixteenth","thirtysecond"]
MULTIPLIER_LIST = [32, 16, 8, 4, 2, 1, 1/2, 1/4, 1/8]
POSTFIX_LIST = ["dotted"]
NOTE_LIST = [prefix + "-note" for prefix in PREFIX_LIST]
NOTE_LIST = NOTE_LIST + [note +"-"+ postfix for postfix in POSTFIX_LIST for note in NOTE_LIST]
REST_LIST = [prefix + "-rest" for prefix in PREFIX_LIST]
REST_LIST = REST_LIST + [rest + "-" + postfix for postfix in POSTFIX_LIST for rest in REST_LIST]

def prefix_to_multiplier_dict():
    i = 0
    prefix2Multiplier = {}
    for prefix in PREFIX_LIST:
        prefix2Multiplier[prefix] = MULTIPLIER_LIST[i]
        i += 1
    return prefix2Multiplier
    
    
class Song(object):
    """ Any tab along with the associated delays 

    Attributes
    ----------
    title : String
        the title of the song
    frets : array of String arrays
        A tab converted to an array of String arrays
    note_types : array of float arrays
        An array of note types corresponding to the frets (e.g. quarter, half)
    tempo : int
        the tempo of a song (beats/min)
    """
    def __init__(self, title, frets, note_types, tempo=0):
        self.title = title
        self.frets = frets
        self.tempo = tempo
        self.note_types = note_types
        self.durations = self.find_durations(note_types, tempo)
        self.song = self.make_song()
    
    def get_title(self):
        return self.title
    
    def get_note_types(self):
        return self.note_types
    
    def get_song(self):
        return self.song
    
    def get_durations(self):
        return self.durations
    
    def get_tempo(self):
        return self.tempo
        
    def get_frets(self):
        return self.frets

    def note_to_delay_dict(self,note_names, tempo, prefix_to_multiplier):
        quarter_note_time = 60 / tempo
        note2Delay = {}
        for note_name in note_names:
            split_note = note_name.split("-")
            delay = prefix_to_multiplier[split_note[0]] * quarter_note_time
            if split_note[-1] == "dotted":
                delay = delay + (0.5 * delay)
            note2Delay[note_name] = delay
        return note2Delay

    def find_durations(self, note_names, tempo):
        """
        Given an input of note names (e.g. quarter-note, half-rest), this converts
        the notes into numerical durations

        Attributes
        ----------
        note_names : String array
        tempo : int
            quarter notes / min
        """
        durations = []
        prefix2Multiplier = prefix_to_multiplier_dict()
        note2Delay = self.note_to_delay_dict(NOTE_LIST+REST_LIST, tempo, prefix2Multiplier)
        for note in note_names:
            durations.append(note2Delay[note])
        return durations
    
    def find_actions(self, note_list):
        actions = []
        for note in note_list:
            note_or_rest = note.split("-")[1]
            if note_or_rest == "note":
                actions.append("strum")
            elif note_or_rest == "rest":
                actions.append("rest")
            else:
                print("Input " + note_or_rest + " is not actionable.")
                return None
        return actions

    def make_song(self):
        actions = self.find_actions(self.note_types)
        durations = self.durations
        song_actions = []
        i = 0 # counter for frets
        j = 0 # counter for durations
        for action in actions:
            if action == "strum":
                song_actions.append([self.frets[i], durations[j], action])
                i += 1
            elif action == "rest":
                song_actions.append([None, durations[j], action])
            j += 1  
        return song_actions


############################################################################
############# Helper Methods (mostly dictionary constructors) ##############
############################################################################

def frets_to_notes_dict(all_strings):
    frets_to_notes = {}
    seen_E = False
    for string in all_strings:
        i = 0
        letter = string[0][0]
        if letter == "E" and seen_E:
            letter = "e"
        elif letter == "E" and not seen_E:
            seen_E = True

        for note in string[0]:
            fret_str = letter + str(i) 
            frets_to_notes[fret_str] = note
            i += 1
    return frets_to_notes

def notes_to_valid_frets_dict(all_strings):
    notes_to_valid_frets = {}
    seen_E = False
    for string in all_strings:
        i = 0
        letter = string[0][0]
        if letter == "E" and seen_E:
            letter = "e"
        elif letter == "E" and not seen_E:
            seen_E = True

        for note in string[0][:5]:
            fret_str = letter + str(i) 
            if note in notes_to_valid_frets:
                notes_to_valid_frets[note] += [fret_str]
            else:
                notes_to_valid_frets[note] = [fret_str]
            i += 1
    return notes_to_valid_frets

def frets_to_values_dict(instrument):
    frets_to_values = {}
    seen_E = False
    i = 0
    for string in instrument.get_base_strings():
        letter = string[0][0]
        if letter == "E" and seen_E:
            letter = "e"
        elif letter == "E" and not seen_E:
            seen_E = True

        for j in range(instrument.get_notes_per_string()):
            frets_to_values[string + str(j)] = i
            i += 1
    return frets_to_values

def valid_equivalent_note(fret, instrument, frets_to_notes, notes_to_valid_frets):
    """
    Given a single input note, this function will output
    a note that can be played by one of the solenoids on
    our guitar.

    Parameter
    ---------
    fret : String
        A note given from a guitar tab
    frets_to_notes : dict
        Mapping from every fret on the guitar to a note
    notes_to_valid_frets : dict
        Mapping from every note to a playable fret

    Returns
    -------
    String
        If the note falls within the range of playable notes,
        this returns the equivalent note on a higher string.
        Otherwise, this returns None and prints an error message.

    Examples (for guitar):
    >>> valid_equivalent_note("A2")
    'A2'
    >>> valid_equivalent_note("E7")
    'A2'
    >>> valid_equivalent_note("G6")
    'B2'
    >>> valid_equivalen_note("B10")
    'Error: Cannot play that note'
    """
    if fret == None or fret == "":
        print("'None' or "" is not a valid note")
    else:
        valid_frets = notes_to_valid_frets[frets_to_notes[fret]]
        fret2Values = frets_to_values_dict(instrument)
        for valid_fret in valid_frets:
            if fret2Values[fret] <= fret2Values[valid_fret]:
                return valid_fret
    print("Error: Cannot play that note")
    return None

def convert_to_raw_arrays(notes):
    note_arrays = []
    for note in notes:
        note_arrays += [note.split("+")]
    return note_arrays

def convert_notes(raw_notes, instrument):
    all_strings = instrument.get_all_notes()
    frets_to_notes = frets_to_notes_dict(all_strings)
    notes_to_valid_frets = notes_to_valid_frets_dict(all_strings)
    raw_note_arrays = convert_to_raw_arrays(raw_notes)
    converted_notes = []
    
    for raw_note_arr in raw_note_arrays:
        sub_notes = []
        for raw_note in raw_note_arr:
            sub_notes += [valid_equivalent_note(raw_note, instrument, frets_to_notes, notes_to_valid_frets)]
        converted_notes += [sub_notes]
    return converted_notes