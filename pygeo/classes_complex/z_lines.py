
import pygeo.base.abstract_elements_complex as Complex
#import pygeo.base.abstract_elements_usphere as USphere
from pygeo.base.abstract_elements_real import method_get
from pygeo.base.pygeoexceptions import Argument_Type_Error

from pygeo.base.pygeomath import *
from pygeo.base.pygeoconstants import *
from pygeo.base.pygeoopts import *

import cmath


ZLineClasses = [ 'zLineFromPoints','zBiChord']

ZLineDef = ['zLine']


__all__ = ZLineClasses + ZLineDef


class zLineFromPoints(Complex._zLine):
   """
:constructors: 

     - zLine(point1,point2)
     - zLinefromPoints(point1,point2)

:returns:  the line_ of the `complex plane`_ through the point_ arguments

:site ref: http://mathworld.wolfram.com/Line.html
   """
   def __init__(self,p1,p2,**kws):
      Complex._zLine.__init__(self,*[p1,p2],**kws)
      self.p1=p1
      self.p2=p2
      self.update()

class zBiChord(Complex._zLine):
   """
:constructors: 

     - zLine(zcircle1,zcircle2)
     - zBiChord(zcircle1,zcircle2)

:returns:  the radical axis determined by the 'complex circle'_ arguments
:site ref: http://mathworld.wolfram.com/RadicalLine.html
   """
   def __init__(self,circle1,circle2,**kw):
      Complex._zLine.__init__(self,*[circle1,circle2],**kw)
      self.zCircle1=circle1
      self.zCircle2=circle2
      self.deps=[self.p1,self.p2]
      self.update()

   def _findSelf(self):
      v=self.zCircle2._center-self.zCircle1._center
      d=mod(v)
      a = (self.zCircle1._radiusSquared - self.zCircle2._radiusSquared + d**2 ) / (2*d)
      P2 = self.zCircle1._center + a * ( v) / d
      h = abs(self.zCircle1._radius - a**2)
      m1=v/d*h
      m2=v/d*-h
      self.p1.set(complex(-m1.imag+P2.real,m1.real+P2.imag))
      self.p2.set(complex(-m2.imag+P2.real,m2.real+P2.imag))
      self.set_hermitian_from_points()
      return True

def zLine(*args,**kws):
   """
:constructors: 

   - zLine(zpoint1,zpoint2); calls: `class zLinefromPoints`_
   - zLine(zcircle1,zcircle2); calls: `class zBiChord`_
   
:returns: the line_ of the `complex plane`_ uniquely determined by its arguments
   """
   __sigs__=[[Complex._zPoint,Complex._zPoint],
             [Complex._zCircle,Complex._zCircle]]
   t,i = method_get(__sigs__,args)
   if t is None:
      raise Argument_Type_Error(__sigs__,args)
   else:
      if i==0:
         return zLineFromPoints(t[0],t[1],**kws)
      elif i==1:
         return zBiChord(t[0],t[1],**kws)
      else:
         raise Argument_Type_Error(__sigs__,args)
