#import copy

from pygeo.base.pygeoconstants import *
from pygeo.base.pygeomath import identity

elements=[]  #list of all Elements in scene with effect on dependencies
freepoints=[] #list of Elements that can be picked and moved - some have constraints

def register(element,args):
   import pygeo.base.abstract_elements_real as Real
   import pygeo.base.abstract_elements_complex as Complex
   import pygeo.base.abstract_elements_usphere as USphere
   for i in args:
     
      if  (isinstance(i,Real._FreePosition)
           or isinstance(i,Complex._zFreePosition)
           or isinstance(i,USphere._uFreePosition)) :
            i._add_dependant(element)
      
      
      if hasattr(i,'args'):
         register(element,i.args)

def get_args(args):
   e=[]
   for arg in args:
     if isinstance(arg,Element):
        e.append(arg)
   return e


class Element(object):
   """
:definition: the abstract class from which all PyGeo geometric objects derive

:keywords:

   ===========   ============================     =================  =====================
   Keyword       Definition                        Type               Default 
   ===========   ============================     =================  =====================
   color         drawn color of object            list of 3 numbers  [0,0,0] (BLACK) 
   level         visibility "level" - see GUI     integer            1
   trace         toggle for tracing function      boolean            False 
   texture       texture for Povray output        string             None
   ===========   ============================     =================  =====================
   """
   __opts__ = ["color","initcolor","trace","level",
              "texture","extend","povout","label","append","export"]
   def __init__(self,*args,**kws):
      """ class from which all geometric Elements are dervied."""


      # append to list of instances of classes derived from Element

      self.append = (kws.get("append",True))
      if self.append:
         elements.append(self)

      # all classes have an associated list ('__opt__') of valid keyword arguments
      # and we test that given named arguments are valid.

      for key in kws:
         if key not in self.__opts__:
            print 'WARNING "%s" not a valid keyword for initialization of %s' %(key,self.__class__.__name__)

      #we toggle this to 0 when a calculated point or an element dependent on such point
      #is unobtainable for 'real' space, i.e. it is an imaginary number

      self.Not_null=True

      # we toggle this to 0 when we want an elment used in the construction calculations,, but not
      # to be rendered

      self.show=True


      # the color in which is the screen representation of the object will be rendered

      self.color = (kws.get("color",BLACK))

      # we need this to be able to reset the rendering color to that which is selected
      # by script where it might be changed temporarily by interactivity, e.g.
      # to indicate that it has been interactively picked.

      self.initcolor = self.color

      # signify whether the inherited object is to be traced during an interactive session.
      # Used for rendering loci of points

      self.trace=kws.get("trace",False)

      # the visibility of elements can be controlled from the GUI based on its 'level' attribute
      # set to 1 by default

      self.level=kws.get("level",1)

      # certain elements can 'extend' other elements, e.g. a intersection point of
      # a line can extend the segment of the line rendered to the intersection point
      # this is a toggle

      self.extend=kws.get("extend",False)



      self.export=kws.get("export",True)


      # a Pov-Ray recognised texture can be associated with certain elements when
      # exported to Pov-Ray

      self.texture=kws.get("texture",None)

      #Perhaps unnecessary initialization.  Test.

      # list that holds the VPython rendering primitives associated with a class
      self.rend=[]


      #let's kept track whether the rendering is visible
      self.visible= True

      # list that holds secondary ('extended') VPython rendering primitives
      # associated with a class
      self.crend=[]

      # list that loci elements when doing tracing

      self.rtrace=[]
      
      # text label to be rendered with element

      self.label=kws.get("label", None)


      # flag indicating whether there has been a change in the Boolean return value
      # of the update calculation for an Element

      self.r_Flag=True


      # flag indicating whether there has been a change in status of an Element on which
      # it is depednant from real to imaginary, or imaginary to real

      self.n_Flag=True

      # flag indicating whether intial drawinf set-up has occurred

      self.init_draw=False
      
      self.args=get_args(args)
      
      if self.append:
         if self.level > 1:
            self.show=False
            if hasattr(self,'element_array'):
                for element in self.element_array:
                     element.show=False

         register(self,self.args)
         
      self.init()

   def __iter__(self):
       all = [self] + self.rtrace
       for a in all:
           yield a
         
   def __len__(self):
       all = [self] + self.rtrace
       return len(all)        
   
   def update(self):
      """Routine determines this Elements position based on scene change, e.g pick and drag of
      FreePoint."""
      if self.append:
         if not self.init_draw:
             self.draw()
      tflag =  self._findSelf()
      if tflag <> self.r_Flag:
        self._togglenull()
      self.setshow()
      self.r_Flag =tflag


   def _findSelf(self):
      return True

   def rmatrix(self):
      """each object has a 4x4 matrix associated with it, representing the object's axis of
      rotation and translation from the origin. Needed for the implementation of the
      Projection class.  Set to the identity matrix by default."""

      return identity(4).astype('d')


   # test whether any Elements on which there is a dependancy
   # have become 'null',.i.e. imaginary

   def _allreal(self):
     nflag = 0 not in [p.Not_null for p in self.args]
     if nflag <> self.n_Flag:
        if not nflag:
           if self.Not_null:
              self._setnull(True)
        else:
           self._setnull(False)
     self.n_Flag=nflag

   # check for change in visibiliy status and toggle
   # visibility as necessary, reset change flag to 0 on
   # effectuating change in visiblity

   def setshow(self):
      if self.Not_null and self.show:
         if not self.visible:
             for e in self:
                 for r in e.rend:
                     r.visible=True
             if self.label:
                 self.lab.visible=True
             for c in self.crend:
                 c.visible=True
             self.visible=True

      else:
         if self.visible:
            for e in self:
               for r in e.rend:
                   r.visible=False
            if self.label:
               self.lab.visible=False
            for c in self.crend:
                c.visible=False
            self.visible=False
      self._redraw()
      if self.extend:
         self.setext()

   def _togglenull(self):
      if self.Not_null:
         self._setnull(True)
      else:
         self._setnull(False)

   def _setnull(self,to_null=True):
      if to_null:
         if self.Not_null:
             self.Not_null=False
             for d in self.deps:
               d.Not_null=False
      else:
         if not self.Not_null:
            self.Not_null=True
            for d in self.deps:
               d.Not_null=True

   def setcolor(self,color):
      self.color=color

   def init(self):
      pass

   def reset(self):
      """Routine to return Element to intial position.
      Default is to run update routine"""
      self.update()

   def reset_trace(self):
      pass

   def reset_trace_curves(self):
      pass
