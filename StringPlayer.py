from guitar import *
import Song
import time
import re
from multiprocessing import Process
import sys

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
	guitar = Guitar(4)
	signal.signal(signal.SIGTERM, term_cleanup)
	print "Playing " + song_name +" at " + str(speed) + " speed."
	print guitar.play(song_name, speed) 

def handle(text, mic, profile):
        # make this more sophisticated
	song_name = " ".join(text.split()[1:])
	global guitar_process
        if text.split()[0] == "PLAY":
		print "Alright"
		print "How fast would you like to play? (slow/normal/fast)"
       #		print guitar.get_all_notes()
		time.sleep(1)
		speed = mic.activeListen()
		if speed == None:
			speed = "normal"
                guitar_process = Process(target=play, args=(song_name, speed))
                print "yeah"
                guitar_process.start()
        elif text.split()[0] == "STOP":
		if guitar_process != None:     
			print "attempting to stop guitar"
			guitar_process.terminate()
			guitar_process = None
	else:
		pass

def term_cleanup(signal, frame):
        print "stopping"
	frame.f_locals["guitar"].cleanup()
	sys.exit(1)

def isValid(text):
	print "Getting songs"
	cond1 = bool(re.search("play one", text, re.IGNORECASE))
	#cond2 = bool(re.search("play two", text, re.IGNORECASE))
	#cond3 = bool(re.search("play three", text, re.IGNORECASE))
	#return cond1 or cond2 or cond3
	return cond1
