import pygeo.base.abstract_elements_complex as Complex
import pygeo.base.abstract_elements_usphere as USphere
import pygeo.base.abstract_elements_real as Real
from pygeo.base.position3 import Position3
from pygeo.base.abstract_elements_real import method_get
from pygeo.base.pygeoexceptions import Argument_Len_Error,Argument_Type_Error

from pygeo.base.pygeomath import *
from pygeo.base.pygeoconstants import *
from pygeo.base.pygeoopts import *

USphereClasses = ['uSphere','kSphere']


__all__ = USphereClasses


class uSphere(USphere._uSphere):
   """
:constructors: 

     - uSphere() 
 
:returns: an origin centered sphere of unit radius representing the `Riemann sphere`_
:site ref: http://mathworld.wolfram.com/RiemannSphere.html
   """
   def __init__(self,**kw):
      USphere._uSphere.__init__(self,**kw)
      self.update()


# the sphere centered at z=1 with radius = sqrt(2)
class kSphere(USphere._uSphere):
   """
:constructors: 

     - kSphere() 
 
:returns: a sphere of radius sqrt(2) centered at (0,0,1)
:site ref: http://mathworld.wolfram.com/InversionSphere.html
   """
   def __init__(self,**kw):
      self.color=kw.get("color",WHITE)
      USphere._uSphere.__init__(self,**kw)
      self._radiusSquared=2
      self._radius=sqrt(2)
      self._center=_rPoint(0,0,1,append=False)
      self.update()()

   def rmatrix(self):
      mat=Element.rmatrix(self)
      mat[3:]=array([[0.,1.,0.,1.0]])
      return mat
