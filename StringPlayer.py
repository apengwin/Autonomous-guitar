from guitar_playing_and_such import *
import Song
import time
import re

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

WORDS = ["PLAY ONE"]#, "PLAY TWO","PLAY THREE"]

def handle(text, mic, profile):
	guitar = Guitar(n=4)
	song_name = text.split(" ")[1]
	print "Alright"
	print "How fast would you like to play? (slow/normal/fast)"
	time.sleep(1)
	speed = mic.activeListen()
	if speed == None:
		speed = "normal"
	print "Playing " + song_name +" at " + str(speed) + " speed."
	print guitar.play_song(song_name, speed) 

def isValid(text):
	print "Getting songs"
	cond1 = bool(re.search("play one", text, re.IGNORECASE))
	#cond2 = bool(re.search("play two", text, re.IGNORECASE))
	#cond3 = bool(re.search("play three", text, re.IGNORECASE))
	#return cond1 or cond2 or cond3
	return cond1
