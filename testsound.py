#!/usr/bin/env python3
#import psychtoolbox.audio
#from psychopy import prefs
import time
from psychopy.core import wait
from psychopy.sound.audioclip import AudioClip
#prefs.hardware["audioLib"] = ["PTB", "pyo", "pygame"]
#prefs.hardware["audioLib"] = ["pygame"]
from psychopy.sound import Sound

# https://www.psychopy.org/api/sound/audioclip.html
snd = Sound()
def loadsnd(file): 
    snddata = AudioClip.load('click-20HzTrain.wav')
    snddata.resample(snd.sampleRate)
    return snddata

clips = {'20': loadsnd('click-20HzTrain.wav'),
         '30': loadsnd('click-30HzTrain.wav')}

def timemark(msg):
    t = time.time()
    print(f"{t:0.5f}\t{msg}")
    return t

diffs = []
for i in range(10):
    b=timemark("set20")
    snd.setSound(clips['20'])
    timemark("play20")
    snd.play()
    e=timemark("wait20")
    diffs.append(e-b)
    wait(clips['30'].duration)
    # !!NB!! w/o stop, setSound will take 10ms instead of .1ms
    snd.stop()

    b=timemark("set30")
    snd.setSound(clips['30'])
    timemark("play30")
    snd.play()
    e=timemark("wait30")
    wait(clips['30'].duration)
    snd.stop()
    diffs.append(e-b)
    timemark("done")
print(diffs)
#print("playing 20")
#s20.play()
#wait(.5)
#print("playing 30")
#s30.play()
#wait(.5)
#
