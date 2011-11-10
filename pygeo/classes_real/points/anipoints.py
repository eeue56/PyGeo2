

import pygeo.base.abstract_elements_real as Real
from pygeo.base.abstract_elements_real import method_get


from pygeo.base.pygeoexceptions import Argument_Type_Error
from pygeo.base.pygeoconstants import *
from pygeo.base.pygeomath import *
from pygeo.base.pygeoprimitives import *
from pygeo.base.element import Element
from pygeo.base.position3 import Position3



from pygeo.base.pygeoopts import *

AniPointClasses = [ 'CirclingPoint', 'SlidingPoint']

AniPointDef = ['AniPoint']

__all__= AniPointClasses + AniPointDef



class CirclingPoint(Real._Point):
   """
:constructors:

    - AniPoint(circle,<rate=integer>,<angle=numeric>)
    - CirclingPoint(circle,<rate=integer>,<angle=numeric>)

 :returns: a point which moves around the circumference of the given circle, at a rate
           determined by the 'rate' keyword, and initial position as determined by
           the 'angle' keyword. See CircumPoint_

:site ref:  http://mathworld.wolfram.com/Circumference.html
   """
   __opts__= Real._Point.__opts__[:] + ["rate","angle"]

   def __init__(self,circle,**kws):
      self.circle=circle
      self.rate=kws.get("rate",360)
      self.rad=2.*PI/(self.rate)
      self.angle=kws.get("angle",0)
      self.delta=0
      Real._Point.__init__(self, *[circle],**kws)
      self.update()

   def _findSelf(self):
      self.delta=self.delta+self.rad
      self.set((self.circle._s*self.circle._radius).rotate(self.delta,self.circle._u))
      self+=self.circle._center
      return True

   def init(self):
      self.set(self.circle._cpoint)
      Element.init(self)



class SlidingPoint(Real._Point):
   """
:constructors:

    - AniPoint(line, <rate=integer>,<ratio=numeric>)
    - SlidingPoint(line, <rate=integer>,<ratio=numeric>)

 :returns: a point which moves along the given line, at a rate
           determined by the 'rate' keyword, and initial position as determined by
           the 'ratio' keyword. See LineDivider_

:site ref:  http://mathworld.wolfram.com/Line.html
   """
   __opts__= Real._Point.__opts__[:] + ["rate","ratio"]

   def __init__(self,line,**kws):
      self.line=line
      self.rate=kws.get('rate',36)
      self.ratio=kws.get('ratio',0)
      self.xdelta=1.0/self.rate
      self.delta=self.ratio
      Real._Point.__init__(self, *[line],**kws)
      self.update()

   def _findSelf(self):
      if self.line .seg:
         self.toInterpolated(self.line.p1,self.line.p2,self.delta)
      else:
          self.maxplus.set(MAX*self.line.getDirection()+self.line.p2)
          self.maxminus.set(-MAX*self.line.getDirection()+self.line.p1)
          self.toInterpolated(self.maxplus,self.maxminus,self.delta)
      self.delta+=self.xdelta
      return True

   def init(self):
      if self.line .seg:
         self.toInterpolated(self.line.p1,self.line.p2,self.ratio)
      else:
         self.maxplus=Position3(MAX*self.line.getDirection()+self.line.p2)
         self.maxminus=Position3(-MAX*self.line.getDirection()+self.line.p1)
         self.toInterpolated(self.maxplus,self.maxminus,self.ratio)
      Element.init(self)


def AniPoint(*args,**kws):
   """
:constructors:


  - AniPoint(circle,<rate=integer>,<angle=numeric>); calls `class CirclingPoint`_
  - AniPoint(line, <rate=integer>,<ratio=numeric>); calls `class CirclingPoint`_

:returns: a point which moves constrained to a given geometric object at each
          display update cycle.
   """
   __sigs__ = [[Real._Circle],[Real._Line]]
   t,i = method_get(__sigs__,args)
   if t is None:
      raise Argument_Type_Error(__sigs__,args)
   else:
      if i == 0:
         return CirclingPoint(t[0],**kws)
      elif i == 1:
         return SlidingPoint(t[0],**kws)
      else:
         raise Argument_Type_Error(__sigs__,args)
