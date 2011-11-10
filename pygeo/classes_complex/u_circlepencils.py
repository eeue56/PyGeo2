import cmath
import pygeo.base.abstract_elements_complex as Complex
import pygeo.base.abstract_elements_usphere as USphere
import pygeo.base.abstract_elements_real as Real
from pygeo.base.abstract_elements_real import method_get
from pygeo.base.pygeoexceptions import Argument_Type_Error

from pygeo.base.pygeomath import *
from pygeo.base.pygeoconstants import *
from pygeo.base.pygeoopts import *

UCirclePencilClasses = ['uSphereSlices', 'z_to_uCirclePencil']

UCirclePencilDef = ['uCirclePencil']


__all__ = UCirclePencilClasses + UCirclePencilDef

#pencil of circles on the unit sphere
class uSphereSlices(USphere._uCirclePencil):
   """
:constructors: 

     - uCirclePencil(planearray) 
     - uSphereSlices(planearray) 
 
:returns: `spheric sections`_ of the `Riemann sphere`_ formed by the intersection of  
          planes of the given plane array with the `Riemann sphere`_ .
:site ref: http://mathworld.wolfram.com/SphericSection.html
   """
   def __init__(self,pencil,**kws):
       self.pencil=pencil
       USphere._uCirclePencil.__init__(self,*[pencil],**kws)
       self.density=self.pencil.density
       self.update()

   def _findSelf(self):
      for i,circle in enumerate(self.circles):
         plane=self.pencil.planes[i]
         circle._center.set(vector(0,0,0))
         circle._u.set(plane._u)
         circle._d= d = plane._d
         u=circle._u
         circle.set_s_from_u(u)
         pt=homogenous(-u)
         equat=array([u.x,u.y,u.z,-d])
         mat= multiply.outer(equat,pt)
         k=matrixmultiply(pt,equat)
         for i in range(4):
             mat[i,i]-=k
         circle._center.to_3d(matrixmultiply(circle._center.homogenous(),mat))
         rsqr = 1.0-circle._center.mag2
         if rsqr < 0:
             rsqr = 0
         circle._cpoint.set(circle._s*sqrt(rsqr)+circle._center)
         circle._radiusSquared=circle._center.distanceSquared(circle._cpoint)
         circle._radius=sqrt(circle._radiusSquared)
      return True

class z_to_uCirclePencil(USphere._uCirclePencil):
   """
:constructors: 

     - uCircle(zCirclePencil)
     - z_to_uCirclePencil(zCirclePencil) 
 
:returns: the `stereographic projection`_ to the `Riemann sphere`_  of an array of `complex circle`_ `s 
          of the `complex plane`_
:site ref: http://www.math.ubc.ca/~cass/courses/m309-01a/montero/math309project.html
   """
   def __init__(self,zpencil,**kw):
      self.zpencil=zpencil
      self.density=self.zpencil.density
      USphere._uCirclePencil.__init__(self,*[zpencil],**kw)
      self.update()

   def _findSelf(self):
      for zCircle, uCircle in zip(self.zpencil,self.circles):
         zCircle.to_uSphere(uCircle)
      return True

def uCirclePencil(*args,**kws):
   """
:constructors: 

  - uCirclePencil(planearray);  calls: `class uSphereSlices`_
  - uCircle(zCirclePencil);  calls: `class z_to_uCirclePencil`_
  
:returns: an array of `_uCircle`_ s
          
:site ref: http://mathworld.wolfram.com/SphericSection.html
   """
   __sigs__=[[Real._PlaneArray],
            [Complex._zCirclePencil]]
   t,i = method_get(__sigs__,args)
   if t is None:
      raise Argument_Type_Error(__sigs__,args)
   else:
      if i==0:
         return uSphereSlices(t[0],**kws)
      elif i==1:
         return z_to_uCirclePencil(t[0],**kws)
      else:
         raise Argument_Type_Error(__sigs__,args)

