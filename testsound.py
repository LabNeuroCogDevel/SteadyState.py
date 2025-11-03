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
    snddata = AudioClip.load(file)
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
# # with snd.stop() out side of timer
# [0.00014257431030273438, 0.00039196014404296875, 0.00036835670471191406, 0.0003819465637207031, 0.0004181861877441406, 0.000396728515625, 0.00042366981506347656, 0.0003962516784667969, 0.0004794597625732422, 0.0004115104675292969, 0.0003654956817626953, 0.00041747093200683594, 0.00035858154296875, 0.0004210472106933594, 0.0003540515899658203, 0.0004036426544189453, 0.00038361549377441406, 0.0003590583801269531, 0.0003685951232910156, 0.00042128562927246094]

