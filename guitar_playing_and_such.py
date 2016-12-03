import numpy as np
# import RPi.GPIO as GPIO # uncomment this when working on the Rasberry Pi

SOLENOIDS_PER_STRING = 4
NOTES_PER_STRING = SOLENOIDS_PER_STRING + 1
STRINGS = np.array(["E", "A", "D", "G", "B", "e"])

# Note: G4 == B0 so we don't have a solenoid for G4
GPIO_MAP = {"E0": None, "E1": [[18,"High"]], "E2": [[27,"High"]],"E3": [[22,"High"]],"E4": [[23,"High"]],
			"A0": None, "A1": [[24,"High"]], "A2": [[10,"High"]],"A3": [[9,"High"]] ,"A4": [[25,"High"]],
			"D0": None, "D1": [[11,"High"]], "D2": [[8,"High"]],"D3": [[7,"High"]],"D4": [[5,"High"]],
			"G0": None, "G1": [[6,"High"]] "G2": [12,"High"]],"G3": [[13,"High"]],"G4": None,
			"B0": None, "B1": [[19, "Low"], [16, "Low"], "B2": [[19, "High"], [16, "Low"]],
			"B3": [[19, "Low"], [16, "High"]],"B4": [[19, "High"], [16, "High"]],
			"e0": None, "e1": [26, "Low"], [20, "Low"], "32": [[26, "High"], [20, "Low"]],
			"e3": [[26, "Low"], [20, "High"]],"e4": [[26, "High"], [20, "High"]]}

DAY_TRIPPER_NOTES = {"E0","E3", "E4", "A2", "D2", "D0", "A2", "D4", "A2", "D0", "D2",
					 "E0","E3", "E4", "A2", "D2", "D0", "A2", "D4", "A2", "D0", "D2",
					 "E0","E3", "E4", "A2", "D2", "D0", "A2", "D4", "A2", "D0", "D2",
					 "E0","E3", "E4", "A2", "D2", "D0", "A2", "D4", "A2", "D0", "D2",
					 "E0","E3", "E4", "A2", "D2", "D0", "A2", "D4", "A2", "D0", "D2",
					 "E0","E3", "E4", "A2", "D2", "D0", "A2", "D4", "A2", "D0", "D2",
					 "E0","E3", "E4", "A2", "D2", "D0", "A2", "D4", "A2", "D0", "D2",
					 "A0","A3", "A4", "D2", "G2", "G0", "D2", "G4", "D2", "G0", "G2",
					 "E0","E3", "E4", "A2", "D2", "D0", "A2", "D4", "A2", "D0", "D2",
					 "E2+A4", "E2+A4","E2+A4","E2+A4","E2+A4","E2+A4","E2+A4","E2+A4",
					 "E2+A4","E2+A4","E2+A4","E2+A4","E2+A4","E2+A4","E2+A4","E2+A4",
					 "E7+A7", "E7+A7","E7+A7","E7+A7","E2+A6","E2+A6","E2+A6","E2+A6",
					 "A4+D6","A4+D6","A4+D6","A4+D6","A2+D4","A2+D4","A2+D4","A2+D4",
					 "A2+D4+G4","A5","A6","D4","G4","G2","D4","G6","D4","G2","G4",
					 "E0","E3", "E4", "A2", "D2", "D0", "A2", "D4", "A2", "D0", "D2"}

#### This only works for the bottom 3 strings for now
def valid_equivalent_note(note):
    """
    Given a single input note, this function will output
    a note that can be played by one of the solenoids on
    our guitar.

    Parameter
    ---------
    note : String
        A note given from a guitar tab

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
    if note == None or note == "":
        print("'None' or "" is not a valid note")
    else:
        if isPlayable(note):
            string_letter, fret = note[0], int(note[1])
            next_string_dist = int(np.floor(fret / NOTES_PER_STRING))
            next_fret = fret % NOTES_PER_STRING
            curr_string_loc = np.where(STRINGS == string_letter)[0][0]
            next_string = STRINGS[curr_string_loc + next_string_dist]
            return next_string + str(next_fret)
    return None

def isPlayable(note):
    """ Determines whether the input note is playable with the number of solenoids on the guitar """

    string_letter, fret = note[0], int(note[1])
    distance_to_farthest_string = (len(STRINGS) - 1) - np.where(STRINGS == string_letter)[0][0]
    distance_to_next_string = np.floor(fret / SOLENOIDS_PER_STRING)

    if distance_to_next_string > distance_to_farthest_string:
        print('Error: Cannot play that note')
        return False
    return True

def convert2RawArrays(notes):
    note_arrays = []
    for note in notes:
        note_arrays += [note.split("+")]
    return note_arrays

def convert_notes(raw_notes):
    raw_note_arrays = convert2RawArrays(raw_notes)
    converted_notes = []
    for raw_note_arr in raw_note_arrays:
        sub_notes = []
        for raw_note in raw_note_arr:
            sub_notes += [valid_equivalent_note(raw_note)]
        converted_notes += [sub_notes]
    print(raw_note_arrays)
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

########## Attempt at making this Object Oriented ###########
# class MechaGuitar(object):
# 	""" A guitar with a given number of solenoids on each fret

# 	Attributes
# 	----------
# 		solenoids_per_string:
# 		notes_per_string:
# 		song: the notes to be played
# 	"""
# 	def __init__(self, num_sols, song=None):
# 		self.solenoids_per_string = num_sols
# 		self.notes_per_string = num_sols + 1
# 		self.songs = np.array(song)

# 	def addSong(self, song):
# 		self.songs.append(song)

# 	def playSong(self):
# 		# This will just print the song for now
# 		return None
	
# 	def playFaster(self):
# 		# This will print the song with the 
# 		return None

# 	def playSlower(self):
# 		return None


# class Song(object):
# 	""" Any tab along with the associated delays 

# 	Attributes
# 	----------
# 		title: the title of the song
# 		frets: A tab converted to an array of String arrays
# 		note_types: An array of note types (e.g. [quarter, eighth])
# 		tempo: the tempo of a song (beats/min)
# 	"""
# 	def __init__(self, title = None, frets=None, note_types=None, tempo=None):
# 		self.title = title
# 		self.frets = frets
# 		self.delays = delays
# 		self.tempo = tempo

# 	def parseFrets(self):
# 		"""Returns array of Note arrays """
# 		return None

# 	def note_durations(self):
# 		quarter_dur = 60 / tempo # 60 (sec/min) / tempo (beats/min) = beats/sec
# 		eighth_dur = quarter_dur / 2
# 		sixteenth_dur = quarter_dur / 4
# 		half_dur = quarter_dur * 2
# 		full_dur = quarter * 4

# class Note(object):
# 	def __init__(self, note_string):
# 		self.action = ""
# 		self.string = ""
# 		self.fret = 0
# 		self.duration = 0 
#############################################################