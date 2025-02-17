#Import modules
from psychopy import *
import numpy as num
from scipy import *
import time, copy 
from numpy.random import shuffle

numTrials = 1

#Setup window
resX=1680
resY=1050
winL = visual.Window(size=(resX,resY), monitor='testMonitor', units='pix', bitsMode=None, fullscr=True, allowGUI=False, color=0.0,screen=0)

winL.setGamma([1.688,1.688,1.688])

#Create stimlui initial stimuli
fusionL = visual.RadialStim(winL,size=resY-5,angularCycles=25, color=-1,angularRes=35,units="pix", radialCycles = 0, contrast = 0.5)
maskL = visual.RadialStim(winL,color=[0,0,0],size=(resY-5)*0.745,angularCycles=25,angularRes=35,units="pix")

for x in range(numTrials):
#    Randomise location of trigger around annulus
    triggerStart = random.randint(0,359)
    triggerEnd = 45 + triggerStart
    triggerL = visual.RadialStim(winL,size=resY-5,angularCycles=25, color=-1,angularRes=35,units="pix", radialCycles = 0, visibleWedge = (triggerStart,triggerEnd))

#   Present stimuli
    fusionL.draw()
    maskL.draw()


    winL.flip()

    time.sleep(1)

#   Present trigger
    fusionL.draw()
    triggerL.draw()
    maskL.draw()


    winL.flip()

    winL.getMovieFrame()
    winL.saveMovieFrames('Left.png')
    event.waitKeys()

#    Clear Screen

    winL.flip()

    time.sleep(0.5)

#Close screen
winL.close()
