import numpy as np
from guitar_playing_and_such import *

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
    def __init__(self, title, frets, tempo=0, note_types=None):
        self.title = title
        self.frets = frets
        self.delays = delays
        self.tempo = tempo
    
    def getTitle(self):
        return title
    
    def getSong(self):
        return (frets, delays)
    
    def getDelays(self):
        return delays
    
    def getFrets(self):
        return frets

class ValidSong(Song):
    """ A song that can be played by a given instrument 
    """
    def __init__(self, frets, instrument):
        self.instrument = instrument
        self.frets = frets
        self.frets2Notes = None
        self.notes2ValidFrets = None
        self.frets2Values = None

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
    if note == None or note == "":
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
        print(raw_note_arrays)
        return converted_notes