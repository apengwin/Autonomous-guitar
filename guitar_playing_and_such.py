import numpy as np
from Song import *
# import RPi.GPIO as GPIO # uncomment this when working on the Rasberry Pi
 
# This is to be used on the Raspberry Pi
# 
# chan_list = [18,27,22,23,24,10,9,25,6,12,13,19,16,26,20]
# GPIO.setup(chan_list, GPIO.OUT)
# """
# ##### Example of setting pins HIGH #######
# ##### ---------------------------- #######
# GPIO.output(chan_list[0], GPIO.HIGH)
# # Can set every channel HIGH/LOW by doing this
# GPIO.output(chan_list, GPIO.HIGH)
# # Could also set multiple channels by doing this
# GPIO.output(chan_list[0:3], (GPIO.HIGH, GPIO.LOW, GPIO.HIGH))

# GPIO.cleanup() # This should be put at the end of the script 
# """

EPSILON = 1e-2
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
    def __init__(self, base_strings=None, notes_per_string=0, solenoids_per_string=0):
        self.base_strings = base_strings
        self.solenoids_per_string = solenoids_per_string
        self.notes_per_string = notes_per_string
        self.songs_dict = dict()
        self.GPIO_list = np.array([None, [[18,"High"]], [[27,"High"]],[[22,"High"]],[[23,"High"]],
            None, [[24,"High"]], [[10,"High"]],[[9,"High"]] ,[[25,"High"]],
            None,[[11,"High"]],[[8,"High"]],[[7,"High"]],[[5,"High"]],
            None,[[6,"High"]],[[12,"High"]],[[13,"High"]], None,
            None,[[19, "Low"], [16, "Low"]],[[19, "High"], [16, "Low"]],
            [[19, "Low"], [16, "High"]],[[19, "High"], [16, "High"]],
            None,[[26, "Low"], [20, "Low"]],[[26, "High"], [20, "Low"]],
            [[26, "Low"], [20, "High"]],[[26, "High"], [20, "High"]]])
        self.GPIO_dict = self.setGPIO_dict()
    
    def get_all_notes(self):
        all_notes = []
        for string in self.base_strings:
            string_notes = []
            string_start = np.where(NOTES == string.upper())[0][0]
            for i in range(self.notes_per_string):
                next_note = (string_start + i) % len(NOTES)
                string_notes.append(NOTES[next_note])
            all_notes.append([string_notes])
        return all_notes
    
    def setGPIO_dict(self):
        self.GPIO_dict = dict()
        j = 0
        for string in self.base_strings:
            for i in range(self.solenoids_per_string + 1):
                fret = string[0] + str(i)
                self.GPIO_dict[fret] = self.GPIO_list[j]
                j += 1
    
    def add_song(self, song):
        """ This assumes the user has not formatted the song in any way
        """
        valid_frets = convert_notes(song.get_frets(), self)
        title = song.get_title()
        tempo = song.get_tempo()
        note_types = song.get_note_types()
        valid_song = Song(title, valid_frets, note_types, tempo) 
        self.songs_dict[title] = valid_song
    
    def get_songs_dict(self):
        return self.songs_dict
    
    def get_GPIO_dict(self):
        return self.GPIO_dict
    
    def get_notes_per_string(self):
        return self.notes_per_string
    
    def get_base_strings(self):
        return self.base_strings
    
    def play(self, song_name, speed):
	actual_song = songs_dict[song_name]
	tempo_multiplier = 1
	if speed == "faster":
		tempo_multiplier = 0.5
	elif speed == "slower":
		tempo_multiplier = 1.5

        for note in actual_song:
            if note[-1] == "rest":
                duration = tempo_multiplier * note[1]
		print(str(note[0]) + ", " + str(duration) + ", " + (note[2:]))
                time.sleep(duration)
            elif note[-1] == "strum":
                strum(note, GPIO_dict, tempo_multiplier)
            
    def strum(self,note, GPIO_dict, tempo_multiplier):
        delay = tempo_multiplier * note[1]
        frets = note[0]
        open_strings = fret[0]
        GPIO_frets = [GPIO_dict[fret] for fret in frets]
        GPIO_strings = [GPIO_dict[open_string] for string in open_strings]

        curr_time = time.clock()
        GPIO.output(GPIO_frets, GPIO.HIGH) # set the GPIO_fret HIGH
        time.sleep(0.05) # this gives time for the fret to be compressed before strumming
        if len(GPIO_strings) > 1:
            for string in GPIO_strings:
                GPIO.output(string, GPIO.HIGH)
                time.sleep(EPSILON)
        else:
           GPIO.output(GPIO_strings, GPIO.HIGH) 
        time.sleep(0.05)
        GPIO.output(GPIO_strings, GPIO.LOW)
        while time.clock() < curr_time + delay: {}
        GPIO.output(GPIO_frets, GPIO.LOW)
    
        
class Guitar(StringInstrument): 
    def __init__(self, n=0):
        strs = np.array(["E", "A", "D", "G", "B", "e"])
        super(Guitar, self).__init__(base_strings=strs, notes_per_string=23,solenoids_per_string=n)
        self.setGPIO_dict()


class Ukulele(StringInstrument):
    def __init__(self,n=0):
        strs = np.array(["G", "C", "E", "A"])
        StringInstrument.__init__(self,base_strings=strs, notes_per_string=17,solenoids_per_string=n)
        self.setGPIO_dict()
    

