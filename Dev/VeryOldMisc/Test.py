#import modules
from psychopy import *
from psychopy import sound
import numpy as num
from scipy import *
import time, copy 
from numpy.random import shuffle

#PARAMETERS


#present a dialogue box for changing params
params = {'Observer':'cs','eccentricity(deg)':0,'Crowding(deg)':0.8, 'Depth of surround(secs)':0,'StepSize(sec)':100}
paramsDlg2 = gui.DlgFromDict(params, title='StereoThresh', fixed=['date'])
if paramsDlg2.OK:
    print params
else: core.quit();print 'User Cancelled'



#Additional parameters

#for stereo AND ori:

params['SF']=6
params['No.Reps']=10
crowding=140*params['Crowding(deg)']# Pixels
if crowding==0:
    params['flankers']=0
else:
    params['flankers']=1
params['dateStr'] = time.strftime("%b_%d_%H%M", time.localtime())
params['date'] = time.strftime("%b_%d_%H%M", time.localtime())#add the current time
params['contrast']=0.99

params['centreSize(deg)']=0.6
params['surroundSize(deg)']=0.6

centresize=140*params['centreSize(deg)']# Pixels
surroundsize=140*params['surroundSize(deg)']# Pixels
eccentricity=140*params['eccentricity(deg)']# Pixels
SFpixels=params['SF']/140.00 #140=number of pixels in a degree - must put decimal points in here
pixel=25.0#How many secs of arc is 1 pixel shift?
#if STEREO:
params['RangeShift']=params['Depth of surround(secs)']


#CREATE MONITORS
DEBUG=False# If true we are in debug mode
# set up window to draw the stimuli
#(1680.0,1050.0) for stereolab monitors
if DEBUG:
    resX=800
    resY=600
    winL=visual.Window(size=(resX,resY), pos=[1000,0], monitor='testMonitor', units='pix', bitsMode=None, allowGUI=True, color=0.0,screen=0)
    winR=visual.Window(size=(resX,resY), pos=[0,0], monitor='testMonitor',units='pix', bitsMode=None, allowGUI=True, color=0.0,screen=0)
    winL.setGamma([1.0,1.0,1.0])
    winR.setGamma([1.0,1.0,1.0])

else:
    resX=1680
    resY=1050
    winL = visual.Window(size=(resX,resY), monitor='testMonitor', units='pix', bitsMode=None, fullscr=True, allowGUI=False, color=0.0,screen=0)
    winR = visual.Window(size=(resX,resY), monitor='testMonitor', units='pix', bitsMode=None, fullscr=True, allowGUI=False, color=0.0,screen=1)
    winL.setGamma([1.688,1.688,1.688])
    winR.setGamma([1.841,1.841,1.841])

# Get independent clocks
trialClock = core.Clock()

# set up sounds
corrSnd=sound.Sound(800,octave=6,secs=0.01)
corrSnd.setVolume(0.1)
incorrSnd = sound.Sound(300,octave=4,secs=0.1)
incorrSnd.setVolume(0.5)

# CREATE STIMULI and MESSAGES
MessageL= visual.TextStim(winL, text = u"Press any key to begin" , wrapWidth=1200, units='pix', height=100,color='midnightblue', pos=[-500, 0], alignHoriz='left',alignVert='bottom', bold=True) 
MessageR= visual.TextStim(winR, text = u"Press any key to begin" , wrapWidth=1200, units='pix', height=100,color='midnightblue', pos=[-500, 0], alignHoriz='left',alignVert='bottom', bold=True) 
warningMessageL= visual.TextStim(winL, text = u"Warning: Check crowding/eccentricity level" , wrapWidth=1200, units='pix', height=50,color='red', pos=[-500, 0], alignHoriz='left',alignVert='bottom', bold=True) 
warningMessageR= visual.TextStim(winR, text = u"Warning: Check crowding/eccentricity level" , wrapWidth=1200, units='pix', height=50,color='red', pos=[-500, 0], alignHoriz='left',alignVert='bottom', bold=True) 
warningMessage1L= visual.TextStim(winL, text = u"Warning: Timing error!" , wrapWidth=1200, units='pix', height=50,color='red', pos=[-500, 0], alignHoriz='left',alignVert='bottom', bold=True) 
warningMessage1R= visual.TextStim(winR, text = u"Warning: Timing error!" , wrapWidth=1200, units='pix', height=50,color='red', pos=[-500, 0], alignHoriz='left',alignVert='bottom', bold=True) 
#fusion lock
params['Fuse_Size']=600
fusionL = visual.RadialStim(winL,size=resY-5,angularCycles=25, color=-1,angularRes=35,units="pix")
maskL = visual.RadialStim(winL,color=[0,0,0],size=(resY-5)*0.95,angularCycles=25,angularRes=35,units="pix")
fusionR = visual.RadialStim(winR,size=resY-5,angularCycles=25, color=-1,angularRes=35,units="pix")
maskR = visual.RadialStim(winR,color=[0,0,0],size=(resY-5)*0.95,angularCycles=25,angularRes=35,units="pix")
#testR= visual.PatchStim(winR, tex='Fusion.png', units='pix',  size=(1680,1050))   
#testL=visual.PatchStim(winR, tex='Fusion.png', units='pix',  size=(1680,1050))   

if params['eccentricity(deg)'] <=3.5:
    # Fixation cross
    fixationL1 = visual.PatchStim(winL,color=-1,sf=0,size=(10,10),pos=(0.0,-eccentricity),mask='circle')
    fixationL2 = visual.PatchStim(winL,color=-1,sf=0,size=(10,10),pos=(0.0,-eccentricity),mask='circle')
    fixationR1 = visual.PatchStim(winR,color=-1,sf=0,size=(10,10),pos=(0.0,-eccentricity),mask='circle')
    fixationR2 = visual.PatchStim(winR,color=-1,sf=0,size=(10,10),pos=(0.0,-eccentricity),mask='circle')
else:
    eccentricity=140*3.5
    fixationL1 = visual.PatchStim(winL,color=-1,sf=0,size=(10,10),pos=(0.0,-eccentricity),mask='circle')
    fixationL2 = visual.PatchStim(winL,color=-1,sf=0,size=(10,10),pos=(0.0,-eccentricity),mask='circle')
    fixationR1 = visual.PatchStim(winR,color=-1,sf=0,size=(10,10),pos=(0.0,-eccentricity),mask='circle')
    fixationR2 = visual.PatchStim(winR,color=-1,sf=0,size=(10,10),pos=(0.0,-eccentricity),mask='circle')
#create nonius lines for alignment
def nonius():
    BoxL2 = visual.PatchStim(winL, tex='none', units='pix', color=0.0, pos=(0,0),ori=0, size=(300.0,300.0))   
    DotL = visual.PatchStim(winL, tex='none', units='pix', color=-1.0, pos=(0,0),ori=0, size=(20.0,20.0))
    BarTop = visual.PatchStim(winL, tex='none', units='pix', color=-1.0, pos=(0,150.0),ori=0, size=(20.0,226.0))
    BarLeft = visual.PatchStim(winL, tex='none', units='pix', color=-1.0, pos=(-150,0),ori=0, size=(226.0,20.0))
    #for right of screen
    BoxR2 = visual.PatchStim(winR, tex='none', units='pix', color=0.0, pos=(0,0),ori=0, size=(300,300.0))   
    DotR = visual.PatchStim(winR, tex='none', units='pix', color=-1.0, pos=(0,0),ori=0, size=(20.0,20.0))
    BarBottom = visual.PatchStim(winR, tex='none', units='pix', color=-1.0, pos=(0,-150),ori=0, size=(20.0,226.0))
    BarRight = visual.PatchStim(winR, tex='none', units='pix', color=-1.0, pos=(150,0),ori=0, size=(226.0,20.0))
#    draw items
#    testR.draw()
#    testL.draw()
    fusionL.draw()
    maskL.draw()
    fusionR.draw()
    maskR.draw()
    BoxL2.draw()
    DotL.draw()
    BarTop.draw()
    BarLeft.draw()
    BoxR2.draw()
    DotR.draw()
    BarBottom.draw()
    BarRight.draw()
    winL.flip()
    winR.flip()



if params['eccentricity(deg)'] <=3.5:
    vertShift=0.0
else:
    vertShift=(140.0*params['eccentricity(deg)'])-(140.0*3.5)
#Centre
CentreL = visual.PatchStim(winL, tex=None, mask='gauss', units='pix',  contrast = params['contrast'], size= centresize, sf=[SFpixels,0.0], ori=0,pos=(0.0,vertShift))
CentreR = visual.PatchStim(winR, tex=None, mask='gauss', units='pix',  contrast = params['contrast'], size= centresize, sf=[SFpixels,0.0], ori=0,pos=(0.0,vertShift))

#Surround
surroundDisp=params['Depth of surround(secs)']/pixel

#some stuff for working out position of the oblique dots:
thetaDeg=30
thetaRad=thetaDeg*(pi/180)
vertPos=(cos(thetaRad)*crowding)
horizPos=(sin(thetaRad)*crowding)


    
Surround1L = visual.PatchStim(winL, tex=None, mask='gauss', units='pix', contrast = params['contrast'], size=surroundsize,sf=[SFpixels,0],pos=((-0.5*surroundDisp)+crowding,vertShift))
Surround2L = visual.PatchStim(winL, tex=None, mask='gauss', units='pix', contrast = params['contrast'], size=surroundsize,sf=[SFpixels,0],pos=((-0.5*surroundDisp)-crowding,vertShift))
Surround3L = visual.PatchStim(winL, tex=None, mask='gauss', units='pix', contrast = params['contrast'], size=surroundsize,sf=[SFpixels,0],pos=((-0.5*surroundDisp)+horizPos,vertPos+vertShift))
Surround4L = visual.PatchStim(winL, tex=None, mask='gauss', units='pix', contrast = params['contrast'], size=surroundsize,sf=[SFpixels,0],pos=((-0.5*surroundDisp)+horizPos,-vertPos+vertShift))
Surround5L = visual.PatchStim(winL, tex=None, mask='gauss', units='pix', contrast = params['contrast'], size=surroundsize,sf=[SFpixels,0],pos=((-0.5*surroundDisp)-horizPos,vertPos+vertShift))
Surround6L = visual.PatchStim(winL, tex=None, mask='gauss', units='pix', contrast = param