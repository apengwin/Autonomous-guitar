import numpy as np
from Song import *
from songs import *
# import RPi.GPIO as GPIO # uncomment this when working on the Rasberry Pi

NOTES = np.array(["A","A#","B","C","C#","D","D#","E","F","F#","G","G#"])

class StringInstrument(object):
    """ A general string instrument
    
    Attributes
    ----------
    base_strings : String NumPy Array
        The open notes of the instrument ordered from lowest to highest
    solenoids_per_string : int
        duh.
    songs_dict : dict
        Dictionary of songs.  Mapping from song title to song actions (frets + durations)
    GPIO_dict : dict
        Mapping from playable frets to GPIO pins + output (High or Low)
    GPIO_list : list
        List of GPIO pins + output for the instrument to actuate a given fret.
        This is ordered in ascending order so that the lowest open note of the
        instrument corresponds to the first item of the list, and the highest
        playable fret of the highest string is the last item of the list.
    
    """
    def __init__(self, base_strings=None, solenoids_per_string=0):
        self.base_strings = base_strings
        self.solenoids_per_string = solenoids_per_string
        self.songs_dict = dict()
        self.GPIO_dict = dict()
        self.GPIO_list = [None, [[18,"High"]], [[27,"High"]],[[22,"High"]],[[23,"High"]],
            None, [[24,"High"]], [[10,"High"]],[[9,"High"]] ,[[25,"High"]],
            None,[[11,"High"]],[[8,"High"]],[[7,"High"]],[[5,"High"]],
            None,[[6,"High"]],[[12,"High"]],[[13,"High"]], None,
            None,[[19, "Low"], [16, "Low"]],[[19, "High"], [16, "Low"]],
            [[19, "Low"], [16, "High"]],[[19, "High"], [16, "High"]],
            None,[[26, "Low"], [20, "Low"]],[[26, "High"], [20, "Low"]],
            [[26, "Low"], [20, "High"]],[[26, "High"], [20, "High"]]]
    
    def playSong(self, song):
        return None
    
    def get_all_notes(self):
        all_notes = []
        for string in self.base_strings():
            string_notes = []
            string_start = np.where(NOTES == string.upper())[0][0]
            for i in range():
                next_note = (string_start + i) % len(NOTES)
                string_notes.append(NOTES[next_note])
            all_notes.append([string_notes])
        return all_notes
    
    def setGPIO_dict(self):
        j = 0
        for string in self.base_strings:
            for i in range(self.solenoids_per_string + 1):
                fret = string[0] + str(i)
                self.GPIO_dict[fret] = self.GPIO_list[j]
                j += 1
    
    def makeValidSong(self, song):
        valid_song = ValidSong(song, self).convert_notes()
        
        return
        
    def addSong(self, song):
        song_dict[song.getTitle()] = song.getSong()
    
    def get_GPIO_dict(self):
        return self.GPIO_dict
    
    def get_base_strings(self):
        return self.base_strings
    
        
class Guitar(StringInstrument): 
    def __init__(self, n=0):
        strs = np.array(["E", "A", "D", "G", "B", "e"])
        StringInstrument.__init__(self,base_strings=strs, solenoids_per_string=n)
        self.setGPIO_dict()


class Ukulele(StringInstrument):
    def __init__(self,n=0):
        strs = np.array(["G", "C", "E", "A"])
        StringInstrument.__init__(self,base_strings=strs, solenoids_per_string=n)
        self.setGPIO_dict()
        



PREFIX_LIST = ["large","long","breve","whole","half","quarter",
             "eighth","sixteenth","thirtysecond"]
MULTIPLIER_LIST = [32, 16, 8, 4, 2, 1, 1/2, 1/4, 1/8]
POSTFIX_LIST = ["dotted"]
NOTE_LIST = [prefix + "-note" for prefix in PREFIX_LIST]
NOTE_LIST = NOTE_LIST + [note +"-"+ postfix for postfix in POSTFIX_LIST for note in NOTE_LIST]
REST_LIST = [prefix + "-rest" for prefix in PREFIX_LIST]
REST_LIST = REST_LIST + [rest + "-" + postfix for postfix in POSTFIX_LIST for rest in REST_LIST]

def prefix2Multiplier_dict():
    i = 0
    prefix2Multiplier = {}
    for prefix in PREFIX_LIST:
        prefix2Multiplier[prefix] = MULTIPLIER_LIST[i]
        i += 1
    return prefix2Multiplier

def note2Delay_dict(note_names, tempo, prefix2Multiplier):
    quarter_note_time = 60 / tempo
    note2Delay = {}
    for note_name in note_names:
        split_note = note_name.split("-")
        delay = prefix2Multiplier[split_note[0]] * quarter_note_time
        if split_note[-1] == "dotted":
            delay = delay + (0.5 * delay)
        note2Delay[note_name] = delay
    return note2Delay
            
def findDelays(note_names, tempo):
    """
    Given an input of note names (e.g. quarter-note, half-rest), this converts
    the notes into numerical delays
    
    Attributes
    ----------
    note_names : String array
    tempo : int
        quarter notes / min
    """
    delays = []
    prefix2Multiplier = prefix2Multiplier_dict()
    note2Delay = note2Delay_dict(NOTE_LIST+REST_LIST, tempo, prefix2Multiplier)
    for note in note_names:
        delays.append(note2Delay[note])
    return delays

# This is to be used on the Raspberry Pi
# 
# chan_list = [18,27,22,23,24,10,9,25,6,12,13,19,16,26,20]
# GPIO.setup(chan_list, GPIO.OUT)
# ##### Example of setting pins HIGH #######
# ##### ---------------------------- #######
# GPIO.output(chan_list[0], GPIO.HIGH)
# # Can set every channel HIGH/LOW by doing this
# GPIO.output(chan_list, GPIO.HIGH)
# # Could also set multiple channels by doing this
# GPIO.output(chan_list[0:3], (GPIO.HIGH, GPIO.LOW, GPIO.HIGH))

# GPIO.cleanup() # This should be put at the end of the script 
# 