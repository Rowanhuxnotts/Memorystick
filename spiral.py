from psychopy import visual
class spiralStim(visual.PatchStim):
    """Stimulus object for drawing spiral stimuli, like an annulus, a rotating wedge,
    a checkerboard etc...
    Built upon the radialStim class.

    Ideal for fMRI retinotopy stimuli!

    Many of the capabilities are built on top of the PatchStim.

    This stimulus is still relatively new and I'm finding occasional gliches. it also takes longer to draw
    than a typical PatchStim, so not recommended for tasks where high frame rates are needed.
    """
    def __init__(self,
                 win,
                 tex     ="sqrXsqr",
                 mask    ="none",
                 units   ="",
                 pos     =(0.0,0.0),
                 size    =(1.0,1.0),
                 radialCycles=3,
                 angularCycles=4,
                 radialPhase=0,
                 angularPhase=0,
                 ori     =0.0,
                 texRes =64,
                 angularRes=100,
                 visibleWedge=(0, 360),
                 rgb   =None,
                 color=(1.0,1.0,1.0),
                 colorSpace='rgb',
                 dkl=None,
                 lms=None,
                 contrast=1.0,
                 opacity=1.0,
                 depth=0,
                 rgbPedestal = (0.0,0.0,0.0),
                 interpolate=False,
                 name='', autoLog=True,
                 carrier=False):
        """
        :Parameters:

            win :
                a :class:`~psychopy.visual.Window` object (required)
            tex :
                The texture forming the image

                - 'sqrXsqr', 'sinXsin', 'sin','sqr',None
                - or the name of an image file (most formats supported)
                - or a numpy array (1xN, NxNx1, NxNx3) ranging -1:1

            mask :
                Unlike the mask in the PatchStim, this is a 1-D mask dictating the behaviour
                from the centre of the stimulus to the surround.
            units : **None**, 'norm', 'cm', 'deg' or 'pix'
                If None then the current units of the :class:`~psychopy.visual.Window` will be used.
                See :ref:`units` for explanation of other options.
            pos :
                a tuple (0.0,0.0) or a list [0.0,0.0] for the x and y of the centre of the stimulus.
                Stimuli can be position beyond the window!
            size :
                a tuple (0.5,0.5) or a list [0.5,0.5] for the x and y
                OR a single value (which will be applied to x and y).
                Sizes can be negative and stimuli can extend beyond the window.
            ori :
                orientation of stimulus in degrees.
            texRes : (default= *128* )
                resolution of the texture (if not loading from an image file)
            angularRes : (default= *100* )
                100, the number of triangles used to make the sti
            radialPhase :
                the phase of the texture from the centre to the perimeter
                of the stimulus
            angularPhase :
                the phase of the texture around the stimulus

            color:

                Could be a:

                    - web name for a color (e.g. 'FireBrick');
                    - hex value (e.g. '#FF0047');
                    - tuple (1.0,1.0,1.0); list [1.0,1.0, 1.0]; or numpy array.

                If the last three are used then the color space should also be given
                See :ref:`colorspaces`

            colorSpace:
                the color space controlling the interpretation of the `color`
                See :ref:`colorspaces`
            contrast : (default= *1.0* )
                How far the stimulus deviates from the middle grey.
                Contrast can vary -1:1 (this is a multiplier for the
                values given in the color description of the stimulus)
            opacity :
                1.0 is opaque, 0.0 is transparent
            depth:
                The depth argument is deprecated and may be removed in future versions.
                Depth is controlled simply by drawing order.
            name : string
                The name of the object to be using during logged messages about
                this stim
        """
        _BaseVisualStim.__init__(self, win, units=units, name=name, autoLog=autoLog)

        if win._haveShaders: self._useShaders=True#by default, this is a good thing
        else: self._useShaders=False

        self.ori = float(ori)
        self.texRes = texRes #must be power of 2
        self.angularRes = angularRes
        self.radialPhase = radialPhase
        self.radialCycles = radialCycles
        self.maskRadialPhase = 0
        self.visibleWedge = visibleWedge
        self.angularCycles = angularCycles
        self.angularPhase = angularPhase
        self.contrast = float(contrast)
        self.opacity = opacity
        self.pos = numpy.array(pos, float)
        self.interpolate=interpolate

        #these are defined by the PatchStim but will just cause confusion here!
        self.setSF = None
        self.setPhase = None
        self.setSF = None

        self.colorSpace=colorSpace
        if rgb!=None:
            log.warning("Use of rgb arguments to stimuli are deprecated. Please use color and colorSpace args instead")
            self.setColor(rgb, colorSpace='rgb')
        elif dkl!=None:
            log.warning("Use of dkl arguments to stimuli are deprecated. Please use color and colorSpace args instead")
            self.setColor(dkl, colorSpace='dkl')
        elif lms!=None:
            log.warning("Use of lms arguments to stimuli are deprecated. Please use color and colorSpace args instead")
            self.setColor(lms, colorSpace='lms')
        else:
            self.setColor(color)

        if type(rgbPedestal)==float or type(rgbPedestal)==int: #user may give a luminance val
            self.rgbPedestal=numpy.array((rgbPedestal,rgbPedestal,rgbPedestal), float)
        else:
            self.rgbPedestal = numpy.asarray(rgbPedestal, float)

        self.depth=depth
        if depth!=0:#deprecated in 1.64.00
            log.warning("The depth argument is deprecated and may be removed. Depth is controlled simply by drawing order")

        #size
        if type(size) in [tuple,list]:
            self.size = numpy.array(size,float)
        else:
            self.size = numpy.array((size,size),float)#make a square if only given one dimension
        #initialise textures for stimulus
        if self.win.winType=="pyglet":
            self.texID=GL.GLuint()
            GL.glGenTextures(1, ctypes.byref(self.texID))
            self.maskID=GL.GLuint()
            GL.glGenTextures(1, ctypes.byref(self.maskID))
        else:
            (self.texID, self.maskID) = GL.glGenTextures(2)
        self.setTex(tex)
        self.setMask(mask)

        #
        self._triangleWidth = pi*2/self.angularRes
        self._angles = numpy.arange(0,pi*2, self._triangleWidth, dtype='float64')
        #which vertices are visible?
        self._visible = (self._angles>=(self.visibleWedge[0]*pi/180))#first edge of wedge
        self._visible[(self._angles+self._triangleWidth)*180/pi>(self.visibleWedge[1])] = False#second edge of wedge
        self._nVisible = numpy.sum(self._visible)*3

        #do the scaling to the window coordinate system
        self._calcPosRendered()
        self._calcSizeRendered()#must be done BEFORE _updateXY

        self._updateTextureCoords()
        self._updateMaskCoords()
        self._updateXY()
        if not self._useShaders:
            #generate a displaylist ID
            self._listID = GL.glGenLists(1)
            self._updateList()#ie refresh display list

    def setSize(self, value, operation=''):
        self._set('size', value, operation)
        self._calcSizeRendered()
        self._updateXY()
        self.needUpdate=True
    def setAngularCycles(self,value,operation=''):
        """set the number of cycles going around the stimulus"""
        self._set('angularCycles', value, operation)
        self._updateTextureCoords()
        self.needUpdate=True
    def setRadialCycles(self,value,operation=''):
        """set the number of texture cycles from centre to periphery"""
        self._set('radialCycles', value, operation)
        self._updateTextureCoords()
        self.needUpdate=True
    def setAngularPhase(self,value, operation=''):
        """set the angular phase of the texture"""
        self._set('angularPhase', value, operation)
        self._updateTextureCoords()
        self.needUpdate=True
    def setRadialPhase(self,value, operation=''):
        """set the radial phase of the texture"""
        self._set('radialPhase', value, operation)
        self._updateTextureCoords()
        self.needUpdate=True

    def draw(self, win=None):
        """
        Draw the stimulus in its relevant window. You must call
        this method after every MyWin.flip() if you want the
        stimulus to appear on that frame and then update the screen
        again.

        If win is specified then override the normal window of this stimulus.
        """
        #set the window to draw to
        if win==None: win=self.win
        if win.winType=='pyglet': win.winHandle.switch_to()

        #work out next default depth
        if self.depth==0:
            thisDepth = self.win._defDepth
            self.win._defDepth += _depthIncrements[self.win.winType]
        else:
            thisDepth=self.depth

        #do scaling
        GL.glPushMatrix()#push before the list, pop after
        #scale the viewport to the appropriate size
        self.win.setScale(self._winScale)
        #move to centre of stimulus and rotate
        GL.glTranslatef(self._posRendered[0],self._posRendered[1],thisDepth)
        GL.glRotatef(-self.ori,0.0,0.0,1.0)

        if self._useShaders:
            #setup color
            desiredRGB = (self.rgb*self.contrast+1)/2.0#RGB in range 0:1 and scaled for contrast
            if numpy.any(desiredRGB>1.0) or numpy.any(desiredRGB<0):
                log.warning('Desired color %s (in RGB 0->1 units) falls outside the monitor gamut. Drawing blue instead'%desiredRGB) #AOH
                desiredRGB=[0.0,0.0,1.0]

            GL.glColor4f(desiredRGB[0],desiredRGB[1],desiredRGB[2], self.opacity)

            #assign vertex array
            if self.win.winType=='pyglet':
                GL.glVertexPointer(2, GL.GL_DOUBLE, 0, self._visibleXY.ctypes)
            else:
                GL.glVertexPointerd(self._visibleXY)#must be reshaped in to Nx2 coordinates

            #then bind main texture
            GL.glActiveTexture(GL.GL_TEXTURE0)
            GL.glBindTexture(GL.GL_TEXTURE_2D, self.texID)
            GL.glEnable(GL.GL_TEXTURE_2D)
            #and mask
            GL.glActiveTexture(GL.GL_TEXTURE1)
            GL.glBindTexture(GL.GL_TEXTURE_1D, self.maskID)
            GL.glDisable(GL.GL_TEXTURE_2D)
            GL.glEnable(GL.GL_TEXTURE_1D)

            #setup the shaderprogram
            GL.glUseProgram(self.win._progSignedTexMask1D)
            GL.glUniform1i(GL.glGetUniformLocation(self.win._progSignedTexMask1D, "texture"), 0) #set the texture to be texture unit 0
            GL.glUniform1i(GL.glGetUniformLocation(self.win._progSignedTexMask1D, "mask"), 1)  # mask is texture unit 1

            #set pointers to visible textures
            GL.glClientActiveTexture(GL.GL_TEXTURE0)
            if self.win.winType=='pyglet':
                GL.glTexCoordPointer(2, GL.GL_DOUBLE, 0, self._visibleTexture.ctypes)
            else:
                GL.glTexCoordPointerd(self._visibleTexture)
            GL.glEnableClientState(GL.GL_TEXTURE_COORD_ARRAY)

            #mask
            GL.glClientActiveTexture(GL.GL_TEXTURE1)
            if self.win.winType=='pyglet':
                GL.glTexCoordPointer(1, GL.GL_DOUBLE, 0, self._visibleMask.ctypes)
            else:
                GL.glTexCoordPointerd(self._visibleMask)
            GL.glEnableClientState(GL.GL_TEXTURE_COORD_ARRAY)

            #do the drawing
            GL.glEnableClientState(GL.GL_VERTEX_ARRAY)
            GL.glDrawArrays(GL.GL_TRIANGLES, 0, self._nVisible)

            #unbind the textures
            GL.glClientActiveTexture(GL.GL_TEXTURE1)
            GL.glBindTexture(GL.GL_TEXTURE_2D, 0)
            #main texture
            GL.glClientActiveTexture(GL.GL_TEXTURE0)
            GL.glBindTexture(GL.GL_TEXTURE_2D, 0)
            GL.glDisable(GL.GL_TEXTURE_2D)
            #disable set states
            GL.glDisableClientState(GL.GL_VERTEX_ARRAY)
            GL.glDisableClientState(GL.GL_TEXTURE_COORD_ARRAY)

            GL.glUseProgram(0)
        else:
            #the list does the texture mapping
            if self.needUpdate: self._updateList()
            GL.glCallList(self._listID)

        #return the view to previous state
        GL.glPopMatrix()

    def _updateXY(self):
        """Update if the SIZE changes
        Update AFTER _calcSizeRendered"""
        #triangles = [trisX100, verticesX3, xyX2]
        self._XY = numpy.zeros([self.angularRes, 3, 2])
        self._XY[:,1,0] = numpy.sin(self._angles)*self._sizeRendered[0]/2 #x position of 1st outer vertex
        self._XY[:,1,1] = numpy.cos(self._angles)*self._sizeRendered[1]/2#y position of 1st outer vertex
        self._XY[:,2,0] = numpy.sin(self._angles+self._triangleWidth)*self._sizeRendered[0]/2#x position of 2nd outer vertex
        self._XY[:,2,1] = numpy.cos(self._angles+self._triangleWidth)*self._sizeRendered[1]/2#y position of 2nd outer vertex

        self._visibleXY = self._XY[self._visible,:,:]
        self._visibleXY = self._visibleXY.reshape(self._nVisible,2)

    def _updateTextureCoords(self):
        #calculate texture coordinates if angularCycles or Phase change
        self._textureCoords = numpy.zeros([self.angularRes, 3, 2])
        if self.carrier == False:
           self._textureCoords[:, 0, 0] = ((self._angles + self._triangleWidth/2) *
               self.angularCycles / pi2 + self.angularPhase+10)
        else:
           self._textureCoords[:, 0, 0] = ((self._angles + self._triangleWidth/2) *
               self.angularCycles / pi2 + self.angularPhase-10)
        #self._textureCoords[:,0,0] = (self._angles+self._triangleWidth/2)*self.angularCycles/(2*pi)+self.angularPhase #x position of inner vertex
        self._textureCoords[:,0,1] = 0.25+-self.radialPhase #y position of inner vertex
        self._textureCoords[:,1,0] = (self._angles)*self.angularCycles/(2*pi)+self.angularPhase #x position of 1st outer vertex
        self._textureCoords[:,1,1] = 0.25+self.radialCycles-self.radialPhase#y position of 1st outer vertex
        self._textureCoords[:,2,0] = (self._angles+self._triangleWidth)*self.angularCycles/(2*pi)+self.angularPhase#x position of 2nd outer vertex
        self._textureCoords[:,2,1] = 0.25+self.radialCycles-self.radialPhase#y position of 2nd outer vertex
        self._visibleTexture = self._textureCoords[self._visible,:,:].reshape(self._nVisible,2)

    def _updateMaskCoords(self):
        #calculate mask coords
        self._maskCoords = numpy.zeros([self.angularRes,3]) + self.maskRadialPhase
        self._maskCoords[:,1:] = 1 + self.maskRadialPhase#all outer points have mask value of 1
        self._visibleMask = self._maskCoords[self._visible,:]


    def _updateListShaders(self):
        """
        The user shouldn't need this method since it gets called
        after every call to .set() Basically it updates the OpenGL
        representation of your stimulus if some parameter of the
        stimulus changes. Call it if you change a property manually
        rather than using the .set() command
        """
        self.needUpdate=0
        GL.glNewList(self._listID,GL.GL_COMPILE)

        #assign vertex array
        if self.win.winType=='pyglet':
            arrPointer = self._visibleXY.ctypes.data_as(ctypes.POINTER(ctypes.c_float))
            GL.glVertexPointer(2, GL.GL_FLOAT, 0, arrPointer)
        else:
            GL.glVertexPointerd(self._visibleXY)#must be reshaped in to Nx2 coordinates

        #setup the shaderprogram
        GL.glUseProgram(self.win._progSignedTexMask1D)
        GL.glUniform1i(GL.glGetUniformLocation(self.win._progSignedTexMask1D, "texture"), 0) #set the texture to be texture unit 0
        GL.glUniform1i(GL.glGetUniformLocation(self.win._progSignedTexMask1D, "mask"), 1)  # mask is texture unit 1

        #set pointers to visible textures
        GL.glClientActiveTexture(GL.GL_TEXTURE0)
        if self.win.winType=='pyglet':
            arrPointer = self._visibleTexture.ctypes.data_as(ctypes.POINTER(ctypes.c_float))
            GL.glTexCoordPointer(2, GL.GL_FLOAT, 0, arrPointer)
        else:
            GL.glTexCoordPointerd(self._visibleTexture)
        GL.glEnableClientState(GL.GL_TEXTURE_COORD_ARRAY)
        #then bind main texture
        GL.glActiveTexture(GL.GL_TEXTURE0)
        GL.glBindTexture(GL.GL_TEXTURE_2D, self.texID)
        GL.glEnable(GL.GL_TEXTURE_2D)

        #mask
        GL.glClientActiveTexture(GL.GL_TEXTURE1)
        if self.win.winType=='pyglet':
            arrPointer = self._visibleMask.ctypes.data_as(ctypes.POINTER(ctypes.c_float))
            GL.glTexCoordPointer(1, GL.GL_FLOAT, 0, arrPointer)
        else:
            GL.glTexCoordPointerd(self._visibleMask)
        GL.glEnableClientState(GL.GL_TEXTURE_COORD_ARRAY)
        #and mask
        GL.glActiveTexture(GL.GL_TEXTURE1)
        GL.glBindTexture(GL.GL_TEXTURE_1D, self.maskID)
        GL.glDisable(GL.GL_TEXTURE_2D)
        GL.glEnable(GL.GL_TEXTURE_1D)

        #do the drawing
        GL.glEnableClientState(GL.GL_VERTEX_ARRAY)
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, self._nVisible*3)
        #disable set states
        GL.glDisableClientState(GL.GL_VERTEX_ARRAY)
        GL.glDisableClientState(GL.GL_TEXTURE_COORD_ARRAY)
        GL.glDisable(GL.GL_TEXTURE_2D)

        GL.glUseProgram(0)
        #setup the shaderprogram
        GL.glEndList()

    def _updateListNoShaders(self):
        """
        The user shouldn't need this method since it gets called
        after every call to .set() Basically it updates the OpenGL
        representation of your stimulus if some parameter of the
        stimulus changes. Call it if you change a property manually
        rather than using the .set() command
        """
        self.needUpdate=0
        GL.glNewList(self._listID,GL.GL_COMPILE)
        GL.glColor4f(1.0,1.0,1.0,1.0)#glColor can interfere with multitextures

        #assign vertex array
        if self.win.winType=='pyglet':
            GL.glVertexPointer(2, GL.GL_DOUBLE, 0, self._visibleXY.ctypes)
        else:
            GL.glVertexPointerd(self._visibleXY)#must be reshaped in to Nx2 coordinates
        GL.glEnableClientState(GL.GL_VERTEX_ARRAY)

        #bind and enable textures
        #main texture
        GL_multitexture.glActiveTextureARB(GL_multitexture.GL_TEXTURE0_ARB)
        GL.glBindTexture(GL.GL_TEXTURE_2D, self.texID)
        GL.glEnable(GL.GL_TEXTURE_2D)
        #mask
        GL_multitexture.glActiveTextureARB(GL_multitexture.GL_TEXTURE1_ARB)
        GL.glBindTexture(GL.GL_TEXTURE_1D, self.maskID)
        GL.glDisable(GL.GL_TEXTURE_2D)
        GL.glEnable(GL.GL_TEXTURE_1D)

        #set pointers to visible textures
        #mask
        GL_multitexture.glClientActiveTextureARB(GL_multitexture.GL_TEXTURE1_ARB)
        if self.win.winType=='pyglet':
            GL.glTexCoordPointer(2, GL.GL_DOUBLE, 0, self._visibleMask.ctypes)
        else:
            GL.glTexCoordPointerd(self._visibleMask)
        GL.glEnableClientState(GL.GL_TEXTURE_COORD_ARRAY)
        #texture
        GL_multitexture.glClientActiveTextureARB(GL_multitexture.GL_TEXTURE0_ARB)
        if self.win.winType=='pyglet':
            GL.glTexCoordPointer(2, GL.GL_DOUBLE, 0,self._visibleTexture.ctypes)
        else:
            GL.glTexCoordPointerd(self._visibleTexture)
        GL.glEnableClientState(GL.GL_TEXTURE_COORD_ARRAY)

        #do the drawing
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, self._nVisible)

        #disable set states
        GL.glDisableClientState(GL.GL_VERTEX_ARRAY)
        GL_multitexture.glActiveTextureARB(GL_multitexture.GL_TEXTURE0_ARB)
        GL.glDisableClientState(GL.GL_TEXTURE_COORD_ARRAY)
        GL_multitexture.glActiveTextureARB(GL_multitexture.GL_TEXTURE1_ARB)
        GL.glDisableClientState(GL.GL_TEXTURE_COORD_ARRAY)

        GL.glEndList()

    def setTex(self,value):
        self._texName = value
        createTexture(value, id=self.texID, pixFormat=GL.GL_RGB, stim=self, res=self.texRes)
    def setMask(self,value):
        """
        """
        self._maskName = value
        res = self.texRes#resolution of texture - 128 is bearable
        step = 1.0/res
        rad = numpy.arange(0,1+step,step)
        if type(self._maskName) == numpy.ndarray:
            #handle a numpy array
            intensity = 255*self._maskName.astype(float)
            res = len(intensity)
            fromFile=0
        elif type(self._maskName) == list:
            #handle a numpy array
            intensity = 255*numpy.array(self._maskName, float)
            res = len(intensity)
            fromFile=0
        elif self._maskName == "circle":
            intensity = 255.0*(rad<=1)
            fromFile=0
        elif self._maskName == "gauss":
            sigma = 1/3.0;
            intensity = 255.0*numpy.exp( -rad**2.0 / (2.0*sigma**2.0) )#3sd.s by the edge of the stimulus
            fromFile=0
        elif self._maskName == "radRamp":#a radial ramp
            intensity = 255.0-255.0*rad
            intensity = numpy.where(rad<1, intensity, 0)#half wave rectify
            fromFile=0
        elif self._maskName in [None,"none","None"]:
            res=4
            intensity = 255.0*numpy.ones(res,float)
            fromFile=0
        else:#might be a filename of a tiff
            try:
                im = Image.open(self._maskName)
                im = im.transpose(Image.FLIP_TOP_BOTTOM)
                im = im.resize([max(im.size), max(im.size)],Image.BILINEAR)#make it square
            except IOError, (details):
                log.error("couldn't load mask...%s: %s" %(value,details))
                return
            res = im.size[0]
            im = im.convert("L")#force to intensity (in case it was rgb)
            intensity = numpy.asarray(im)

        data = intensity.astype(numpy.uint8)
        mask = data.tostring()#serialise

        #do the openGL binding
        if self.interpolate: smoothing=GL.GL_LINEAR
        else: smoothing=GL.GL_NEAREST
        GL.glBindTexture(GL.GL_TEXTURE_1D, self.maskID)
        GL.glTexImage1D(GL.GL_TEXTURE_1D, 0, GL.GL_ALPHA,
                        res, 0,
                        GL.GL_ALPHA, GL.GL_UNSIGNED_BYTE, mask)
        GL.glTexParameteri(GL.GL_TEXTURE_1D,GL.GL_TEXTURE_WRAP_S,GL.GL_REPEAT) #makes the texture map wrap (this is actually default anyway)
        GL.glTexParameteri(GL.GL_TEXTURE_1D,GL.GL_TEXTURE_MAG_FILTER,smoothing)     #linear smoothing if texture is stretched
        GL.glTexParameteri(GL.GL_TEXTURE_1D,GL.GL_TEXTURE_MIN_FILTER,smoothing)
        GL.glTexEnvi(GL.GL_TEXTURE_ENV, GL.GL_TEXTURE_ENV_MODE, GL.GL_MODULATE)
        GL.glEnable(GL.GL_TEXTURE_1D)

        self.needUpdate=True

    def __del__(self):
        self.clearTextures()#remove textures from graphics card to prevent crash

    def clearTextures(self):
        """
        Clear the textures associated with the given stimulus.
        As of v1.61.00 this is called automatically during garbage collection of
        your stimulus, so doesn't need calling explicitly by the user.
        """
        #only needed for pyglet
        if self.win.winType=='pyglet':
            GL.glDeleteTextures(1, self.texID)
            GL.glDeleteTextures(1, self.maskID)