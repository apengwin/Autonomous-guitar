import guitar_playing_and_such
import Song
import songs
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

WORDS = ["Pi", "example", "google"]

def handle(text, mic, profile):
	if bool(re.search("Pi", text, re.IGNORECASE)):
		print("How can I help you?")
		command = mic.activeListen()
		


	if bool(re.search("Play", text, re.IGNORECASE)):
		print("OK")


def isValid(text):
	cond1 = bool(re.search("Pi", text, re.IGNORECASE))
	cond2 = bool(re.search(r'\bPi\b', text, re.IGNORECASE))
	return cond1 or cond2


print(isValid("Pi"))