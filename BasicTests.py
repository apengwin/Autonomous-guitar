##########################################
#######    Basic Guitar Tests   ##########
#######       (so basic...)     ##########
##########################################

from guitar import *
from Song import *
import time
#guitar = Guitar(4)


##################################
######### String Tests #############
##################################
def allStringTest():
    basic_frets = ['E0','A0','D0','G0','B0','e0']
    basic_durations = ["quarter-note","quarter-note","quarter-note","triplet-note","triplet-note","triplet-note"]
    tempo = 120
    guitar.add_song("all-strings", basic_frets, basic_durations, tempo)
    guitar.play("all-strings", "normal")

def OneStringTest():
    basic_frets =  ['E2', 'E3', 'E4' ]
    basic_durations = [ "quarter-note", 'quarter-note', 'quarter-note']
    tempo = 120
    guitar.add_song("basic-one", basic_frets, basic_durations, tempo)
    #print guitar.get_songs_dict()["basic-one"]
    guitar.play("basic-one", "normal")

def TwoStringTest():
    ### Tests two actuating 2 frets at the same time
    basic_frets = ["D0"]
    basic_durations = ["quarter-note"]
    tempo = 120
    guitar.add_song("basic-two", basic_frets, basic_durations, tempo)
    #print(song.get_song())
    guitar.play("basic-two", "normal")

def ThreeStringTest():
    ### Tests two actuating 3 frets at the same time
    basic_frets = ["E0+A0+D0"]
    basic_durations = ["quarter-note"]
    tempo = 120
    guitar.add_song("basic-three", basic_frets, basic_durations, tempo)
    #print guitar.get_songs_dict()["basic-three"]
    guitar.play("basic-three", "normal")

##################################
######### Fret Tests #############
##################################
def OneFretTest():
    basic_frets = ['E3']
    basic_durations = ["quarter-note"]
    print "hello"
    tempo = 120
    guitar.add_song("fret-one", basic_frets, basic_durations, tempo)
    guitar.play("fret-one", "normal")

def TwoFretTest():
    basic_frets = ['E1','e1']
    basic_durations = ["quarter-note","quarter-note" ]
    tempo = 120
    guitar.add_song("fret-two", basic_frets, basic_durations, tempo)
    guitar.play("fret-two", "normal")

def ThreeFretTest():
    basic_frets = ['E2', 'A1','D4']
    basic_durations = ["eighth-note","quarter-note","eighth-note"]
    tempo = 120
    guitar.add_song("fret-three", basic_frets, basic_durations, tempo)
    #print guitar.get_songs_dict()["basic-one"]
    guitar.play("fret-three", "normal")

def TwoAtOnceFret():
    basic_frets = ["E1+A3"]
    basic_durations = ["quarter-note"]
    tempo = 120
    guitar.add_song("two-for-one", basic_frets,basic_durations,tempo)
    guitar.play("two-for-one", "normal")

def ThreeAtOnceFret():
    basic_frets = ["E1+A3+B2"]
    basic_durations = ["quarter-note"]
    tempo = 120
    guitar.add_song("three-for-one", basic_frets,basic_durations,tempo)
    guitar.play("three-for-one", "normal")

def FourAtOnceFret():
    basic_frets = ["E1+A3+B2+D1"]
    basic_durations = ["quarter-note"]
    tempo = 120
    guitar.add_song("four-for-one", basic_frets,basic_durations,tempo)
    guitar.play("four-for-one","normal")

def FiveAtOnceFret():
    basic_frets = ["E1+A1+D1+G1+B1"]
    basic_durations = ["quarter-note"]
    tempo = 120
    guitar.add_song("four-for-one", basic_frets,basic_durations,tempo)
    guitar.play("four-for-one","normal")

def testEachFret():
    ### Playing a sequence where every possible fret is played once
    all_frets = ["E0","E1","E2","E3","E4",
                 "A0","A1","A2","A3","A4",
                 "D0","D1","D2","D3","D4",
                 "G0","G1","G2","G3","G4",
                 "B0","B1","B2","B3","B4",
                 "e0","e1","e2","e3"]
    basic_durations = ["quarter-note","quarter-note","quarter-note",
                       "quarter-note","quarter-note","quarter-note",
                       "quarter-note","quarter-note","quarter-note",
                       "quarter-note","quarter-note","quarter-note",
                       "quarter-note","quarter-note","quarter-note",
                       "quarter-note","quarter-note","quarter-note",
                       "quarter-note","quarter-note","quarter-note",
                       "quarter-note","quarter-note","quarter-note",
                       "quarter-note","quarter-note","quarter-note",
                       "quarter-note","quarter-note"]
    tempo = 120
    song = guitar.add_song("testEachFret", all_frets, basic_durations, tempo)
    #print(song.get_song())
    guitar.play("testEachFret", "normal")



def FourFretTest():
    ### Tests two actuating 4 frets at the same time
    basic_frets = ["E2+A2+D2+G2"]
    basic_durations = ["quarter-note"]
    tempo = 120
    song = guitar.add_song("basic-four",basic_frets, basic_durations, tempo)
    #print(song.get_song())
    guitar.play("basic-four", "normal")

def FiveFretTest():
    ### Tests two actuating 5 frets at the same time
    basic_frets = ["E2+A2+D2+G2+B2"]
    basic_durations = ["quarter-note"]
    tempo = 120
    guitar.add_song("basic-five", basic_frets, basic_durations, tempo)
    #print(song.get_song())
    guitar.play("basic-five", "normal")

def SixFretTest():
    ### Tests two actuating 6 frets at the same time
    basic_frets = ["E2+A2+D2+G2+B2+e2"]
    basic_durations = ["quarter-note"]
    tempo = 120
    guitar.add_song("basic-six", clean_basic_frets, basic_durations, tempo)
    #print(song.get_song())
    guitar.play("basic-six", "normal")

def TwoNoteSongTest():
    ### Tests a song with 2 notes and 1 rest in between
    basic_frets = ["E2","A2"]
    basic_durations = ["quarter-note","quarter-rest", "quarter-note"]
    tempo = 120
    guitar.add_song("two-note", clean_basic_frets, basic_durations, tempo)
    #print(song.get_song())
    guitar.play("two-note", "normal") 

def test_DAYTRIPPER():
    guitar.play("DAY TRIPPER", "normal")
############### Tests ##################
#allStringTest()
#time.sleep(2)
#OneStringTest()
#time.sleep(4)
#TwoStringTest()
#time.sleep(4)
#OneFretTest()
#ThreeFretTest()
#FourFretTest()
#FiveFretTest()
#SixFretTest()
#TwoNoteSongTest()
#testEachFret()
#test_DAYTRIPPER()
#guitar.play("HOTEL CALIFORNIA", "normal")
#guitar.play("LANDSLIDE", "normal")




#guitar.play("SEVEN NATION ARMY", "normal")


#allStringTest()



#test_DAYTRIPPER()
