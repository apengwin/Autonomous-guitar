import numpy as np
from songs import *
# import RPi.GPIO as GPIO # uncomment this when working on the Rasberry Pi

STRINGS = np.array(["E", "A", "D", "G", "B", "e"])
NOTES = np.array(["A","A#","B","C","C#","D","D#","E","F","F#","G","G#"])

# Note: G4 == B0 so we don't have a solenoid for G4
GPIO_MAP = {"E0": None, "E1": [[18,"High"]], "E2": [[27,"High"]],"E3": [[22,"High"]],"E4": [[23,"High"]],
            "A0": None, "A1": [[24,"High"]], "A2": [[10,"High"]],"A3": [[9,"High"]] ,"A4": [[25,"High"]],
            "D0": None, "D1": [[11,"High"]], "D2": [[8,"High"]],"D3": [[7,"High"]],"D4": [[5,"High"]],
            "G0": None, "G1": [[6,"High"]], "G2": [[12,"High"]],"G3": [[13,"High"]],"G4": None,
            "B0": None, "B1": [[19, "Low"], [16, "Low"]], "B2": [[19, "High"], [16, "Low"]],
            "B3": [[19, "Low"], [16, "High"]],"B4": [[19, "High"], [16, "High"]],
            "e0": None, "e1": [[26, "Low"], [20, "Low"]], "32": [[26, "High"], [20, "Low"]],
            "e3": [[26, "Low"], [20, "High"]],"e4": [[26, "High"], [20, "High"]]}
                   
def all_notes():
    all_notes = []
    for string in STRINGS:
        string_notes = []
        string_start = np.where(NOTES == string.upper())[0][0]
        for i in range(23):
            next_note = (string_start + i) % len(NOTES)
            string_notes.append(NOTES[next_note])
        all_notes.append([string_notes])
    return all_notes

def frets2Notes_dict(all_strings):
    frets2Notes = {}
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
            frets2Notes[fret_str] = note
            i += 1
    return frets2Notes

def notes2ValidFrets_dict(all_strings):
    notes2ValidFrets = {}
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
            if note in notes2ValidFrets:
                notes2ValidFrets[note] += [fret_str]
            else:
                notes2ValidFrets[note] = [fret_str]
            i += 1
    return notes2ValidFrets

def frets2Values_dict():
    frets2Values = {}
    seen_E = False
    i = 0
    for string in STRINGS:
        letter = string[0][0]
        if letter == "E" and seen_E:
            letter = "e"
        elif letter == "E" and not seen_E:
            seen_E = True
            
        for j in range(23):
            frets2Values[string + str(j)] = i
            i += 1
    return frets2Values

def valid_equivalent_note(fret, frets2Notes, notes2ValidFrets):
    """
    Given a single input note, this function will output
    a note that can be played by one of the solenoids on
    our guitar.

    Parameter
    ---------
    fret : String
        A note given from a guitar tab
    frets2Notes : dict
        Mapping from every fret on the guitar to a note
    notes2ValidFrets : dict
        Mapping from every note to a playable fret

    Returns
    -------
    String
        If the note falls within the range of playable notes,
        this returns the equivalent note on a higher string.
        Otherwise, this returns None and prints an error message.

    Examples:
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
        valid_frets = notes2ValidFrets[frets2Notes[fret]]
        fret2Values = frets2Values_dict()
        for valid_fret in valid_frets:
            if fret2Values[fret] <= fret2Values[valid_fret]:
                return valid_fret
    print("Error: Cannot play that note")
    return None

def convert2RawArrays(notes):
    note_arrays = []
    for note in notes:
        note_arrays += [note.split("+")]
    return note_arrays

def convert_notes(raw_notes):
    all_strings = all_notes()
    frets2Notes = frets2Notes_dict(all_strings)
    notes2ValidFrets = notes2ValidFrets_dict(all_strings)
    
    raw_note_arrays = convert2RawArrays(raw_notes)
    converted_notes = []
    for raw_note_arr in raw_note_arrays:
        sub_notes = []
        for raw_note in raw_note_arr:
            sub_notes += [valid_equivalent_note(raw_note, frets2Notes, notes2ValidFrets)]
        converted_notes += [sub_notes]
    return converted_notes

def validNotes2GPIO(note_arrays):
    """
    Converts the notes to GPIO pins.

    The input notes are assumed to be valid (they are playable by the 
    machine).    

    Parameter
    ---------
    note_arrays : array of String arrays

    Returns
    -------
    array of GPIO arrays
    """
    return None

dayTripper = convert_notes(DAY_TRIPPER_NOTES)
print()
print(dayTripper)

########## Attempt at making this Object Oriented ###########
# class MechaGuitar(object):
#   """ A guitar with a given number of solenoids on each fret

#   Attributes
#   ----------
#       solenoids_per_string:
#       notes_per_string:
#       song: the notes to be played
#   """
#   def __init__(self, num_sols, song=None):
#       self.solenoids_per_string = num_sols
#       self.notes_per_string = num_sols + 1
#       self.songs = np.array(song)

#   def addSong(self, song):
#       self.songs.append(song)

#   def playSong(self):
#       # This will just print the song for now
#       return None
    
#   def playFaster(self):
#       # This will print the song with the 
#       return None

#   def playSlower(self):
#       return None


# class Song(object):
#   """ Any tab along with the associated delays 

#   Attributes
#   ----------
#       title: the title of the song
#       frets: A tab converted to an array of String arrays
#       note_types: An array of note types (e.g. [quarter, eighth])
#       tempo: the tempo of a song (beats/min)
#   """
#   def __init__(self, title = None, frets=None, note_types=None, tempo=None):
#       self.title = title
#       self.frets = frets
#       self.delays = delays
#       self.tempo = tempo

#   def parseFrets(self):
#       """Returns array of Note arrays """
#       return None

#   def note_durations(self):
#       quarter_dur = 60 / tempo # 60 (sec/min) / tempo (beats/min) = beats/sec
#       eighth_dur = quarter_dur / 2
#       sixteenth_dur = quarter_dur / 4
#       half_dur = quarter_dur * 2
#       full_dur = quarter * 4

# class Note(object):
#   def __init__(self, note_string):
#       self.action = ""
#       self.string = ""
#       self.fret = 0
#       self.duration = 0 
#############################################################