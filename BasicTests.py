##########################################
#######    Basic Guitar Tests   ##########
#######       (so basic...)     ##########
##########################################

from guitar import *
from Song import *
import time
guitar = Guitar(4)

def OneFretTest():
    basic_frets = ['E0', 'A0','D0']
    #clean_basic_frets = convert_notes(basic_frets, guitar)
    #print clean_basic_frets
    basic_durations = ["eighth-note","quarter-note","eighth-note"]
    tempo = 120
    guitar.add_song("basic-one", basic_frets, basic_durations, tempo)
    print guitar.get_songs_dict()["basic-one"]
    guitar.play("basic-one", "normal")

def TwoFretTest():
    ### Tests two actuating 2 frets at the same time
    basic_frets = ["D0+A0"]
    #clean_basic_frets = convert_notes(basic_frets, guitar)
    basic_durations = ["quarter-note"]
    tempo = 120
    song = guitar.add_song("basic-two", basic_frets, basic_durations, tempo)
    #print(song.get_song())
    guitar.play("basic-two", "normal")

def ThreeFretTest():
    ### Tests two actuating 3 frets at the same time
    basic_frets = ["E0+A0+D0"]
    #clean_basic_frets = convert_notes(basic_frets, guitar)
    basic_durations = ["quarter-note"]
    tempo = 120
    song = guitar.add_song("basic-three", basic_frets, basic_durations, tempo)
    print guitar.get_songs_dict()["basic-three"]

    guitar.play("basic-three", "normal")

def FourFretTest():
    ### Tests two actuating 4 frets at the same time
    basic_frets = ["E2+A2+D2+G2"]
    clean_basic_frets = convert_notes(basic_frets, guitar)
    basic_durations = ["quarter-note"]
    tempo = 120
    song = guitar.add_song("basic-four", clean_basic_frets, basic_durations, tempo)
    #print(song.get_song())
    guitar.play("basic-four", "normal")

def FiveFretTest():
    ### Tests two actuating 5 frets at the same time
    basic_frets = ["E2+A2+D2+G2+B2"]
    clean_basic_frets = convert_notes(basic_frets, guitar)
    basic_durations = ["quarter-note"]
    tempo = 120
    song = guitar.add_song("basic-five", clean_basic_frets, basic_durations, tempo)
    #print(song.get_song())
    guitar.play("basic-five", "normal")

def SixFretTest():
    ### Tests two actuating 6 frets at the same time
    basic_frets = ["E2+A2+D2+G2+B2+e2"]
    clean_basic_frets = convert_notes(basic_frets, guitar)
    basic_durations = ["quarter-note"]
    tempo = 120
    song = guitar.add_song("basic-six", clean_basic_frets, basic_durations, tempo)
    #print(song.get_song())
    guitar.play("basic-six", "normal")

def TwoNoteSongTest():
    ### Tests a song with 2 notes and 1 rest in between
    basic_frets = ["E2","A2"]
    clean_basic_frets = convert_notes(basic_frets, guitar)
    basic_durations = ["quarter-note","quarter-rest", "quarter-note"]
    tempo = 120
    song = guitar.add_song("two-note", clean_basic_frets, basic_durations, tempo)
    #print(song.get_song())
    guitar.play("two-note", "normal") 

def testEachFret():
    ### Playing a sequence where every possible fret is played once
    all_frets = ["E0","E1","E2","E3","E4",
                 "A0","A1","A2","A3","A4",
                 "D0","D1","D2","D3","D4",
                 "G0","G1","G2","G3","G4",
                 "B0","B1","B2","B3","B4",
                 "e0","e1","e2","e3","e4"]
    clean_basic_frets = convert_notes(all_frets, guitar)
    basic_durations = ["quarter-note","quarter-note","quarter-note",
                       "quarter-note","quarter-note","quarter-note",
                       "quarter-note","quarter-note","quarter-note",
                       "quarter-note","quarter-note","quarter-note",
                       "quarter-note","quarter-note","quarter-note",
                       "quarter-note","quarter-note","quarter-note",
                       "quarter-note","quarter-note","quarter-note",
                       "quarter-note","quarter-note","quarter-note",
                       "quarter-note","quarter-note","quarter-note",
                       "quarter-note","quarter-note","quarter-note"]
    tempo = 120
    song = guitar.add_song("testEachFret", clean_basic_frets, basic_durations, tempo)
    #print(song.get_song())
    guitar.play("testEachFret", "normal")


############### Tests ##################

#OneFretTest()
#time.sleep(4)
TwoFretTest()
time.sleep(4)
ThreeFretTest()
#FourFretTest()
#FiveFretTest()
#SixFretTest()
#TwoNoteSongTest()
#testEachFret()








