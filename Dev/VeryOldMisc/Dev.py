#Import modules
from psychopy import *
#import numpy as num
from scipy import *
import time, copy 
from datetime import datetime
from numpy.random import shuffle

resX=1680
resY=1050
winL = visual.Window(size=(resX,resY), monitor='testMonitor', units='pix', bitsMode=None, fullscr=True, allowGUI=False, color=0.0,screen=0)
winR = visual.Window(size=(resX,resY), monitor='testMonitor', units='pix', bitsMode=None, fullscr=True, allowGUI=False, color=0.0,screen=1)


RadL = visual.RadialStim(winL,size=resY-350,angularCycles=25, color=-1,angularRes=35,units="pix", radialCycles = 0, contrast = 0.7)
BlockL = visual.PatchStim(winL, tex='None', units='pix', pos=[-300,0], size=(600,resY), color=[0, 0, 0])

RadL.draw()
BlockL.draw()
winL.flip()
time.sleep(2)