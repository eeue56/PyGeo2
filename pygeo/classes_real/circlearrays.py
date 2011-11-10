import pygeo.base.abstract_elements_real as Real
from pygeo.base.abstract_elements_real import method_get

from pygeo.base.pygeoexceptions import Argument_Type_Error
from pygeo.base.pygeoconstants import *
from pygeo.base.pygeomath import *
from pygeo.base.pygeoprimitives import *

from pygeo.base.pygeoopts import *


CircleArrayClasses = ['CirclePencil']

CircleArrayDefs = ['CircleArray']

__all__= CircleArrayClasses+CircleArrayDefs


class CirclePencil(Real._CirclePencil):
   """
:constructors:

     - CiclePencil(sphere,planearray)

:returns:  the set of circles which the `plane sheaf`_ cuts from the sphere. See SphereCircle_

:site ref: http://mathworld.wolfram.com/SheafofPlanes.html
   """
   def __init__(self,sphere,pencil,**kws):
       self.sphere=sphere
       self.pencil=pencil
       Real._CirclePencil.__init__(self,*[sphere,pencil],**kws)
       self.density=self.pencil.density
       self.update()

   def _findSelf(self):
      for i,circle in enumerate(self.circles):
         plane = self.pencil.planes[i]
         circle._center.set(self.sphere._center)
         circle._u.set(plane._u)
         u=circle._u
         circle.set_s_from_u(u)
         s=circle._s
         circle._d= d = plane._d
         pt=homogenous(circle._center-u)
         equat=array([u.x,u.y,u.z,-d])
         mat= multiply.outer(equat,pt)
         k=matrixmultiply(pt,equat)
         for i in range(4):
             mat[i,i]-=k
         circle._center.to_3d(matrixmultiply(circle._center.homogenous(),mat))
         
         pdist = circle._center.distanceSquared(self.sphere._center)
         rsqr = self.sphere._radiusSquared-pdist
         if rsqr < 0:
             rsqr = 0
         circle._cpoint.set(circle._s*sqrt(rsqr)+circle._center)
         circle._radiusSquared=circle._center.distanceSquared(circle._cpoint)
         circle._radius=sqrt(circle._radiusSquared)
      return True


def  CircleArray(*args,**kws):
   """
:constructors:

     - CiclePencil(sphere,planearray)
     - CicleArray(sphere,planearray)

:returns:  the set of circles which the `plane sheaf`_ cuts from the sphere. See SphereCircle_

:site ref: http://mathworld.wolfram.com/SheafofPlanes.html
   """
   __sigs__=[[Real._Sphere,Real._PlaneArray]]
   t,i = method_get(__sigs__,args)
   if t is None:
      raise Argument_Type_Error(__sigs__,args)
   else:
      if i==0:
         return CirclePencil(t[0],t[1],**kws)
      else:
         raise Argument_Type_Error(__sigs__,args)