import pygeo.base.abstract_elements_complex as Complex
import pygeo.base.abstract_elements_usphere as USphere
from pygeo.base.abstract_elements_real import method_get
from pygeo.base.pygeoexceptions import Argument_Type_Error

from pygeo.base.pygeomath import *
from pygeo.base.pygeoconstants import *
from pygeo.base.pygeoopts import *

import cmath


zPointPencilClasses = ['zCirclePoints','zLinePoints']

zPointPencilDef = ['zPointArray']


__all__ = zPointPencilClasses + zPointPencilDef

class zCirclePoints(Complex._zPointArray):
   """
:constructors: 

     - zPointArray(zcircle)
     - zCirclePoints(zcircle)

:returns: array of equidistant `complex point`_ s on the given `complex circle`_

:site ref: http://mathworld.wolfram.com/CirclePointPicking.html
   """
   def __init__(self,circle,**kws):
      Complex._zPointArray.__init__(self,*[circle],**kws)
      self.circle=circle
      self.adelta=2*PI/self.density
      self.update()

   def _findSelf(self):
      circle=self.circle
      for i, zpoint in enumerate(self):
          angle=i*self.adelta
          zpoint.set(complex(0,1)*circle._radius*(math_E**complex(0,angle))+circle._center)
      return True

class zLinePoints(Complex._zPointArray):
   """
:constructors: 

     - zPointArray(zline)
     - zLinePoints(zline)

:returns: array of points equidistant on a given line of the `complex plane`_ 
:site ref: http://mathworld.wolfram.com/LineSegmentRange.html
   """
   def __init__(self,zline,**kws):
      self.zline=zline
      self.seg=kws.get('seg',False)
      Complex._zPointArray.__init__(self,*[zline],**kws)
      self.update()

   def _findSelf(self):
      zline =self.zline
      p= zline.direction()
      length=zMAX*2
      start = (p*-zMAX)+(zline.p1+zline.p2)/2
      steps=[length/float(self.density-1)*i for i in range(self.density)]
      for zpoint,step in zip(self,steps):
         zpoint.set(p*step+start)
      return True


def zPointArray(*args,**kws):
   """
:constructors: 

   - zPointArray(zcircle);              calls: `class zCirclePoints`_
   - zPointArray(zline);                calls: `class zLinePoints`_
   
:returns: An instance of an object derived from the `_zPointArray`_ abstract class,
          representing an array of points with determined positions 
          on the `complex plane`_
   """
   __sigs__=[[Complex._zCircle]]
   t,i = method_get(__sigs__,args)
   if t is None:
      raise Argument_Type_Error(__sigs__,args)
   else:
      if i==0:
         return zCirclePoints(t[0],**kws)
      else:
         raise Argument_Type_Error(__sigs__,args)
