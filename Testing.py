import re

"""
A nice file for testing Jasper's abilities
"""

WORDS = ["Blargh"] 

def handle(text, mic, profile):
	print("How can I help you?")

def isValid(text):
	return bool(re.search("blargh", text, re.IGNORECASE))

