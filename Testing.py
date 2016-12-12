import re

"""
A nice file for testing Jasper's abilities
"""

WORDS = ["Testing"] 

def handle(text, mic, profile):
	print("How can I help you?")

def isValid(text):
	return bool(re.search("Testing", text, re.IGNORECASE))

