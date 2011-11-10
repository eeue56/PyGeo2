import pygeo.base.abstract_elements_complex as Complex
import pygeo.base.abstract_elements_usphere as USphere
from pygeo.base.abstract_elements_real import method_get
from pygeo.base.pygeoexceptions import Argument_Type_Error

from pygeo.base.pygeomath import *
from pygeo.base.pygeoconstants import *
from pygeo.base.pygeoopts import *

import cmath


zLinePencilClasses = ['zLinePencil']

zLinePencilDef = ['zLineArray']


__all__ = zLinePencilClasses + zLinePencilDef

class zLinePencil(Complex._zLineArray):
   """
:constructors: 

     - zLineArray(zpoint)
     - zLinePencil(zpoint)

:returns:  array of equidistant lines on the `complex plane`_ and through the given point    
:site ref: http://mathworld.wolfram.com/Pencil.html
   """
   def __init__(self,zpoint,**kws):
      Complex._zLineArray.__init__(self,*[zpoint],**kws)
      self.zpoint=zpoint
      self.adelta=2*PI/self.density
      self.update()

   def _findSelf(self):
      zpoint=self.zpoint
      for i, zline in enumerate(self.zlines):
          angle=i*self.adelta
          zline.p1.set(zpoint)
          zline.p2.set(complex(0,1)*(math_E**complex(0,angle))+zpoint)
          zline.set_hermitian_from_points()
      return True



def zLineArray(*args,**kws):
   """
:constructors: 

   - zLineArray(zpoint); calls: `class zLinePencil`_

:returns: An instance of an object derived from the `_zLineArray`_ abstract class,
          representing an array infinite lines of the `complex plane`_
   """
   __sigs__=[[Complex._zPoint]]
   t,i = method_get(__sigs__,args)
   if t is None:
      raise Argument_Type_Error(__sigs__,args)
   else:
      if i==0:
         return zLinePencil(t[0],**kws)
      else:
         raise Argument_Type_Error(__sigs__,args)
