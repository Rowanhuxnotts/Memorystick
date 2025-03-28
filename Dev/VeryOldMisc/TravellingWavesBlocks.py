# Basic travalling wave experiment 
# LEFT AND RIGHT ARE REVERSED

#To do: Current- set up stimuli types and change presentation to account for these
#    Flash Suppression
#    Target zone
#    Restrict trigger to cardinal directions  (Or maybe just top?)
#    functions for a lot of this stuff
#    Some kind of randomisation of trials?
#    Wait for button press at start of experiment
#    wait for button response 
#    note button response w/ timing
#    write output to file
#    remove trigger after its shown for a brief period
#    Messages intro

#--------------------------------------
#              Initialisation
#--------------------------------------

#Import modules
from psychopy import *
import numpy as num
from scipy import *
import time, copy 
from numpy.random import shuffle

numTrials = 5
Trials = [0,1]  # 0 = left carrier, 1 = right carrier
NumBlocks = 2

#Setup window
resX=1680
resY=1050
winL = visual.Window(size=(resX,resY), monitor='testMonitor', units='pix', bitsMode=None, fullscr=True, allowGUI=False, color=0.0,screen=0)
winR = visual.Window(size=(resX,resY), monitor='testMonitor', units='pix', bitsMode=None, fullscr=True, allowGUI=False, color=0.0,screen=1)
winL.setGamma([1.688,1.688,1.688])
winR.setGamma([1.841,1.841,1.841])

#--------------------------------------
#                  Functions
#--------------------------------------


#--------------------------------------
#            Create stimlui 
#--------------------------------------

StimSize = resY - 20
fixationL = visual.TextStim(winL,'+')
fixationR= visual.TextStim(winR, '+')

# Concentric Left
ConL = visual.RadialStim(winL,size=StimSize*0.80,angularCycles=25, color=-1,angularRes=35,units="pix", radialCycles = 0, contrast = 0.7)
RadR = visual.RadialStim(winR,size=StimSize*0.80,angularCycles=0, color=-1,angularRes=35,units="pix", radialCycles= 8, ori=300, contrast = 0.7)

# Concentric right
RadL = visual.RadialStim(winL,size=StimSize*0.80,angularCycles=25, color=-1,angularRes=35,units="pix", radialCycles = 0, contrast = 0.7)
ConR = visual.RadialStim(winR,size=StimSize*0.80,angularCycles=0, color=-1,angularRes=35,units="pix", radialCycles= 8, ori=300, contrast = 0.7)


# Masks
maskL = visual.RadialStim(winL,color=[0,0,0],size=StimSize*0.60,angularCycles=25,angularRes=35,units="pix")
maskR = visual.RadialStim(winR,color=[0,0,0],size=StimSize*0.60,angularCycles=25,angularRes=35,units="pix")

#--------------------------------------
#                 Messages
#--------------------------------------

# Inscructions = 

# Pause between trials
PauseMsgL = visual.TextStim(winL, 'Break in experiment \nPress any button to continue')
PauseMsgR = visual.TextStim(winR, 'Break in experiment \nPress any button to continue')

EndMsgL = visual.TextStim(winL, 'Experiment Over \nThanks for Participating!')
EndMsgR = visual.TextStim(winR, 'Experiment Over \nThanks for Participating!')

#--------------------------------------
#           Presentation Loop
#--------------------------------------

z = 1
for y in range(NumBlocks):
    for x in Trials:
        if x  == 0:
        #    Randomise location of trigger around annulus
            triggerStart = random.randint(0,359)
            triggerEnd = 45 + triggerStart
            triggerR = visual.RadialStim(winR,size=StimSize*0.80,angularCycles=0, color=-1,angularRes=35,units="pix", radialCycles = 8, visibleWedge = (triggerStart,triggerEnd))
    
            fixationL.draw()
            fixationR.draw()
            winL.flip()
            winR.flip()
            time.sleep(0.25)
    
    #    Flash suppression
            fusionR.draw()
            maskR.draw()
            fixationL.draw()
            fixationR.draw()
    
            winL.flip()
            winR.flip()
            time.sleep(1)
    
        #   Present stimuli
            fusionL.draw()
            maskL.draw()
            fusionR.draw()
            maskR.draw()
            fixationL.draw()
            fixationR.draw()
    
            winL.flip()
            winR.flip()
            time.sleep(1)
    
        #   Present trigger
            fusionL.draw()
            maskL.draw()
            fusionR.draw()
            triggerR.draw()
            maskR.draw()
            fixationL.draw()
            fixationR.draw()
    
            winL.flip()
            winR.flip()
            time.sleep(0.5)
    
    
        # Remove Trigger and wait for response
            fusionL.draw()
            maskL.draw()
            fusionR.draw()
            triggerR.draw()
            maskR.draw()
            fixationL.draw()
            fixationR.draw()
    
            winL.flip()
            winR.flip()
    
            event.waitKeys()
    
        #    Clear Screen
            fixationL.draw()
            fixationR.draw()
            winL.flip()
            winR.flip()
    
        elif x == 1:
            #    Randomise location of trigger around annulus
            triggerStart = random.randint(0,359)
            triggerEnd = 45 + triggerStart
            triggerL = visual.RadialStim(winL,size=StimSize*0.80,angularCycles=0, color=-1,angularRes=35,units="pix", radialCycles = 8, visibleWedge = (triggerStart,triggerEnd))
    
            fixationL.draw()
            fixationR.draw()
            winL.flip()
            winR.flip()
            time.sleep(0.25)
    
    #    Flash suppression
            fusionL.draw()
            maskL.draw()
            fixationL.draw()
            fixationR.draw()
    
            winL.flip()
            winR.flip()
            time.sleep(1)
    
        #   Present stimuli
            fusionL.draw()
            maskL.draw()
            fusionR.draw()
            maskR.draw()
            fixationL.draw()
            fixationR.draw()
    
            winL.flip()
            winR.flip()
            time.sleep(0.25)
    
        #   Present trigger
            fusionL.draw()
            maskL.draw()
            fusionR.draw()
            maskR.draw()
            triggerL.draw()
            fixationL.draw()
            fixationR.draw()
    
            winL.flip()
            winR.flip()
            time.sleep(0.5)
    
    
        # Remove Trigger and wait for response
            fusionL.draw()
            maskL.draw()
            fusionR.draw()
            triggerR.draw()
            maskR.draw()
            fixationL.draw()
            fixationR.draw()
    
            winL.flip()
            winR.flip()
    
            event.waitKeys()
    
        #    Clear Screen
            fixationL.draw()
            fixationR.draw()
            winL.flip()
            winR.flip()

        else:
            print('Error: Invalid trial number')
            winL.close()
            winR.close()

    if z != NumBlocks:
        PauseMsgL.draw()
        PauseMsgR.draw()
        winL.flip()
        winR.flip()
        z = z +1
        event.waitKeys()
        print(z)
    else:
        EndMsgL.draw()
        EndMsgR.draw()
        winL.flip()
        winR.flip()
        event.waitKeys()

#Close screen
winL.close()
winR.close()
