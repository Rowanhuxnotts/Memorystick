#Import modules
from psychopy import *
from scipy import *
import time, copy 
from datetime import datetime
from numpy import random
import csv

#--------------------------------------
#              Initialisation
#--------------------------------------

#Experiment params
NumTrials = 60

# Get Date and start time
now = datetime.now()
Date = now.strftime('%d%m%y_%H%M')

#present a dialogue box for changing params
params = {'Observer':'', 'Run(1/2)':''}
paramsDlg2 = gui.DlgFromDict(params, title='Reaction Time', fixed=['date'])

ConditionList = [
        {'Condition': 'Baseline'}
        ]
Exp = data.TrialHandler(ConditionList, NumTrials, method='random', dataTypes=None, extraInfo=None,seed=None,originPath=None)


#Setup window
resX=1680
resY=1050
winL = visual.Window(size=(resX,resY), monitor='testMonitor', units='pix', bitsMode=None, fullscr=True, allowGUI=False, color=0.0,screen=0)
winR = visual.Window(size=(resX,resY), monitor='testMonitor', units='pix', bitsMode=None, fullscr=True, allowGUI=False, color=0.0,screen=1)

# Are these needed???
winL.setGamma([1.688,1.688,1.688])
winR.setGamma([1.841,1.841,1.841])

# Clock
clock = core.Clock()

#--------------------------------------
#            Create stimlui 
#--------------------------------------

#Create stimlui initial stimuli
RadL = visual.RadialStim(winL,size=resY-350,angularCycles=25, color=-1,angularRes=35,units="pix", radialCycles = 0, contrast = 0.7)
maskL = visual.RadialStim(winL,color=[0,0,0],size=(resY-350)*0.745,angularCycles=25,angularRes=35,units="pix")
RadR = visual.RadialStim(winR,size=resY-350,angularCycles=25, color=-1,angularRes=35,units="pix", radialCycles = 0, contrast = 0.7)
maskR = visual.RadialStim(winR,color=[0,0,0],size=(resY-350)*0.76,angularCycles=25,angularRes=35,units="pix")

# Trigger
triggerR = visual.RadialStim(winR,size=resY-350,angularCycles=0, color=-1,angularRes=35,units="pix", radialCycles = 8, 
        visibleWedge = (170,210))

# End location

EndLocL2 = visual.PatchStim(winL, tex='None', units='pix', pos=[-140,-420], size=(7,60), color=[-1,-1,-1], ori=200)
EndLocL1 = visual.PatchStim(winL, tex='None', units='pix', pos=[0,-440], size=(7,60), color=[-1,-1,-1], ori=0)
EndLocR2 = visual.PatchStim(winR, tex='None', units='pix', pos=[-140,-420], size=(7,60), color=[-1,-1,-1], ori=200)
EndLocR1 = visual.PatchStim(winR, tex='None', units='pix', pos=[0,-440], size=(7,60), color=[-1,-1,-1], ori=0)

#Create fixation and fusion lock
#Dot
fixationL = visual.PatchStim(winL, texRes=512, tex='None', mask="circle",units='pix',rgb=-1, pos=[0,0], size=(20.0,20.0))
fixationR = visual.PatchStim(winR, texRes=512, tex='None', mask="circle",units='pix',rgb=-1, pos=[0,0], size=(20.0,20.0))

#Spokes
# to the right window    
BarTop = visual.PatchStim(winR, tex='none', units='pix', rgb=1.0, pos=(0,85),ori=0, size=(15,100))
BarLeft = visual.PatchStim(winR, tex='none', units='pix', rgb=1.0, pos=(-85,0),ori=0, size=(100,15))

# to the left window    
BarBottom = visual.PatchStim(winL, tex='none', units='pix', rgb=-1.0, pos=(-0,-85),ori=0, size=(15,100))
BarRight = visual.PatchStim(winL, tex='none', units='pix', rgb=-1.0, pos=(85,0),ori=0, size=(100,15))

#Fusion lock
LockSize=512
array = zeros([LockSize,LockSize])
for n in range(0, LockSize+1, 32):
    array[n:16+n,0:16]=1
    array[n-16:16+n-16,0:16]=-1
    array[n:16+n,LockSize-16:LockSize]=-1
    array[n-16:16+n-16,LockSize-16:LockSize]=1
    
    array[0:16,n:16+n]=1
    array[0:16, n-16:16+n-16]=-1
    array[LockSize-16:LockSize,n:16+n]=-1
    array[LockSize-16:LockSize, n-16:16+n-16]=1

fusionL = visual.PatchStim(winL, tex=array, 
    size=(1050,1050), units='pix',
    interpolate=False,
    autoLog=True)
fusionR = visual.PatchStim(winR, tex=array, 
    size=(1050,1050), units='pix',
    interpolate=False,
    autoLog=True) 

Fixation = [fixationL, fixationR, BarBottom, BarTop, BarLeft, BarRight, EndLocL1, EndLocL2, EndLocR1, EndLocR2]

#--------------------------------------
#                 Messages
#--------------------------------------

# Inscructions = 
IntroMsgL = visual.TextStim(winL, 'Instructions:\nFixate on the cross and press the space bar when the concentric wedge appears.\nPress space to begin.', pos=(0,250),  
    flipHoriz=True, height=40, wrapWidth=1000)
IntroMsgR = visual.TextStim(winR, 'Instructions:\nFixate on the cross and press the space bar when the concentric wedge appears.\nPress space to begin.', pos=(0,250),  
    flipHoriz=True, height=40, wrapWidth=1000)

# Check stimuli is fusing
FixationMsgL = visual.TextStim(winL, 'Please ensure stimuli is fusing. ', pos=(0,250),  
    flipHoriz=True, height=40, wrapWidth=1000)
FixationMsgR = visual.TextStim(winR, 'Please ensure stimuli is fusing.', pos=(0,250),  
    flipHoriz=True, height=40, wrapWidth=1000)

#--------------------------------------
#           Presentation Loop
#--------------------------------------

IntroMsgL.draw()
IntroMsgR.draw()
winL.flip()
winR.flip()
event.waitKeys()

#Check fusion
fusionL.draw()
fusionR.draw()
for x in Fixation:
    x.draw()
FixationMsgL.draw()
FixationMsgR.draw()
winL.flip()
winR.flip()
event.waitKeys()

# Initialise lists that will store output data
Direction = []
ResponseTime = []

for x in Exp:
# Set new wait time
    WaitTime = random.rand() * 2 + 1 
# Present initial stimuli
    fusionL.draw()
    fusionR.draw()
    RadL.draw()
    RadR.draw()
    maskL.draw()
    maskR.draw()
    for x in Fixation:
        x.draw()
    winL.flip()
    winR.flip()
    time.sleep(WaitTime)
# Present response wedge
    fusionL.draw()
    fusionR.draw()
    RadL.draw()
    RadR.draw()
    triggerR.draw()
    maskL.draw()
    maskR.draw()
    for x in Fixation:
        x.draw()
    winL.flip()
    winR.flip()
    clock.reset()
# Wait for response and save response time
    Keys = event.waitKeys()
    RT = clock.getTime()
    Exp.addData('RT', RT)
# Add data from trial
    RespTime = clock.getTime()
    ResponseTime.append(RespTime)
    Keys = Keys[0]
    Keys = Keys.strip("[']")
    Direction.append(Keys)
    
# Clear screen and wait for next run 
    fusionL.draw()
    fusionR.draw()
    for x in Fixation:
        x.draw()
    winL.flip()
    winR.flip()
    time.sleep(1)

#--------------------------------------
#              End/Cleanup
#--------------------------------------

#Output reaction times in csv

if params['Observer'] == 'z':
    pass
else:
    #Output responses in csv
    FileName = './data/RT_' + params['Observer'] + '_' + params['Run(1/2)'] + '_' + Date + '.csv'
    #, newline=''     ./data/
    with open(FileName, 'w') as csvfile:
        Writer = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        Writer.writerow(["ParticipantID", "Direction", "ResponseTime"])
        for x in range(len(ResponseTime)):
            Writer.writerow([params['Observer'], Direction[x], ResponseTime[x]])

#Close screen
winL.close()
winR.close()