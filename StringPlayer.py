from guitar import *
import Song
import time
import re
from multiprocessing import Process

""" 
File that will use Jasper API to control the robot

Key API elements
----------------
WORDS : string array
	Set of words Jasper should recognize
isValid : bool function
	Function that determines if the input text is within WORDS
handle : function
	A funtion that performs actions when the text is valid
"""

WORDS = ["PLAY"]#, "PLAY TWO","PLAY THREE"]
guitar_process = None

def test():
        guitar = Guitar(4)

def play(song_name, speed):
	print "Playing " + song_name +" at " + str(speed) + " speed."
	print guitar.play(song_name, speed) 

def handle(text, mic, profile):
	guitar = Guitar(4)
        # make this more sophisticated
	song_name = text.split()[1:]
	global guitar_process
        if song_name[0] == "PLAY":
		print "Alright"
		print "How fast would you like to play? (slow/normal/fast)"
       		print guitar.get_all_notes()
		time.sleep(1)
		speed = mic.activeListen()
		if speed == None:
			speed = "normal"
                guitar_process = Process(target=play, args=(song_name, speed)
                guitar_process.start()
        if song_name[0] == "STOP":
		if guitar_process != None:     
			print "attempting to stop guitar"
			guitar_process.terminate()
			guitar_process = None

def isValid(text):
	print "Getting songs"
	cond1 = bool(re.search("play one", text, re.IGNORECASE))
	#cond2 = bool(re.search("play two", text, re.IGNORECASE))
	#cond3 = bool(re.search("play three", text, re.IGNORECASE))
	#return cond1 or cond2 or cond3
	return cond1
