#Import modules
from psychopy import *
#import numpy as num
from scipy import *
import time, copy 
from datetime import datetime
from numpy.random import shuffle

#Setup window
resX=1680
resY=1050
winL = visual.Window(size=(resX,resY), monitor='testMonitor', units='pix', bitsMode=None, fullscr=True, allowGUI=False, color=0.0,screen=0)
winR = visual.Window(size=(resX,resY), monitor='testMonitor', units='pix', bitsMode=None, fullscr=True, allowGUI=False, color=0.0,screen=1)

#Create stimlui initial stimuli
RadL = visual.RadialStim(winL,size=resY*2, pos=[110,110], angularCycles=25, color=-1,angularRes=35,units="pix", radialCycles = 0, contrast = 0.7)
MaskL = visual.RadialStim(winL,color=[0,0,0],size=(resY-350)*0.745,angularCycles=25,angularRes=35,units="pix")
MaskOutsideL = visual.PatchStim(winL,color=[0,0,0],size=(resY-2500)*0.745,units="pix", mask="circle")

RadL.draw()
MaskL.draw()
MaskOutsideL.draw()
winL.flip()
core.wait(2)
