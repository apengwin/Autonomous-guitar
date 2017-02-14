from __future__ import division
import numpy as np
from Song import *
from static.lib import *
import time

import RPi.GPIO as GPIO # uncomment this when working on the Rasberry Pi
 
# This is to be used on the Raspberry Pi
GPIO.setmode(GPIO.BOARD)
chan_list = [3,5,7,8,10,11,12,13,15,16,18,19,21,22,23,24,26,29,31,32,33,35,36,37,38,40]
GPIO.setup(chan_list, GPIO.OUT, initial=GPIO.LOW)
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

class Guitar(object):
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
    def __init__(self, solenoids_per_string=0):
        self.base_strings = np.array(["E", "A", "D", "G", "B", "e"])
        self.solenoids_per_string = solenoids_per_string
        self.notes_per_string = 23
        self.songs_dict = dict()
        self.set_songs_dict()
        self.GPIO_list = np.array([[], [12], [13],[15],[16],
            [], [18], [19],[21],[22],
            [],[23],[24],[26],[29],
            [],[31],[32],[33],[],
            [],[35],[36], [35,36],[37],
            [],[38],[40],[38,40]])
        self.GPIO_dict = dict()
        self.setGPIO_dict()
	self.chan_list = [3,5,7,8,10,11,12,13,15,16,18,19,21,22,23,24,26,29,31,32,33,35,36,37,38,40]
    
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
               if string == "e" and i == 4:
		   continue
	       fret = string[0] + str(i)
               self.GPIO_dict[fret] = self.GPIO_list[j]
               j += 1
        return self.GPIO_dict
    
    def add_song(self, title, frets, durations, tempo):
        """ This assumes the user has not formatted the song in any way
        """
        valid_frets = convert_notes(frets, self)
        valid_song = Song(title, valid_frets, durations, tempo=tempo)
        self.songs_dict[title] = valid_song.get_song()
    
    def set_songs_dict(self):
        self.songs_dict = dict()
        self.add_song("LANDSLIDE", LANDSLIDE_FRETS, LANDSLIDE_DURATIONS, 144)
        self.add_song("DAY TRIPPER", DAY_TRIPPER_FRETS, DAY_TRIPPER_DURATION, 142)
        self.add_song("HOTEL CALIFORNIA", hotel_frets, HOTEL_LENGTH, 73)
	self.add_song("SEVEN NATION ARMY", SEVEN_NATION_ARMY_FRETS, SEVEN_NATION_ARMY_DURATION, 120)
        return self.songs_dict

    def get_songs_dict(self):
        return self.songs_dict
    
    def get_GPIO_dict(self):
        return self.GPIO_dict
    
    def get_notes_per_string(self):
        return self.notes_per_string
    
    def get_base_strings(self):
        return self.base_strings
    
    def play(self, song_name, speed):
        actual_song = self.songs_dict[song_name]
        print "Playing %s, at %s speed" % (song_name, speed)
        tempo_multiplier = 1
        if speed == "fast":
            tempo_multiplier = 0.5
        elif speed == "slow":
            tempo_multiplier = 1.5
         
        print actual_song   
        for note in actual_song:
            if note[-1] == "rest":
                duration = tempo_multiplier * note[1]
                #print "rest for " + str(duration) + " seconds"
                time.sleep(duration)
            elif note[-1] == "strum":
                self.strum(note, tempo_multiplier)

    def cleanup(self):
        GPIO.output(self.chan_list, GPIO.LOW)
        GPIO.cleanup()
    
    def setup(self):
	GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.chan_list, GPIO.OUT, initial=GPIO.LOW)

    def strum(self,note, tempo_multiplier):
        frets = note[0]
	open_string_to_gpio = {"E": 3, "A":5, "D":7, "G":8, "B":10, "e":11}
        gpio_frets = []
        index = 0
        found_e3 = False
        for fret in frets:
            gpio_frets += self.GPIO_dict[fret]
            if fret == "e3":
                found_e3 = True
                break
            index += 1
	#print gpio_frets
        gpio_strings = [open_string_to_gpio[fret[0]] for fret in frets]
        delay = note[1]
        curr_time = time.clock()
        GPIO.output(gpio_frets, GPIO.HIGH) # set the gpio_fret high
        counter = 0
        for string in gpio_strings:
            if not (found_e3 and counter == index):
                GPIO.output(string, GPIO.HIGH)
         #       print string
          #      print "plucking " + str(string) 
                time.sleep(EPSILON)
	        GPIO.output(string, GPIO.LOW)
            else:
                time.sleep(EPSILON)
            counter += 1
            #if (len(gpio_strings) > 1):
	#time.sleep(epsilon)
        #gpio.output(gpio_strings, gpio.low)
        #print "turning off string plucking solenoids"
        while time.clock() < curr_time + delay: pass
        GPIO.output(gpio_frets, GPIO.LOW)
#        print "turning off fret solenoids"

    def other_strum(self, note, tempo_multiplier):	
        frets = note[0]
	open_string_to_gpio = {"E": 3, "A":5, "D":7, "G":8, "B":10, "e":11}
        gpio_frets = []
        open_frets = []
        hammer_frets = []
        for fret in frets:
            if fret[-1] == "0":
                gpio_frets += [open_string_to_gpio[fret[0]]]
            else:
            	gpio_frets += self.GPIO_dict[fret]
	print gpio_frets
        delay = note[1]

        curr_time = time.clock()
        for string in gpio_frets:
             GPIO.output(string, GPIO.HIGH)
             print string
             print "plucking " + str(string) 
             time.sleep(EPSILON)
             GPIO.output(string, GPIO.LOW)
        #time.sleep(epsilon)
        #gpio.output(gpio_strings, gpio.low)
        #print "turning off string plucking solenoids"
        while time.clock() < curr_time + delay:
		pass
        #GPIO.output(gpio_frets, GPIO.LOW)
        #print "turning off fret solenoids"

