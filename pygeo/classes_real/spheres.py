
import pygeo.base.abstract_elements_real as Real
from pygeo.base.abstract_elements_real import method_get


from pygeo.base.pygeoexceptions import Argument_Type_Error
from pygeo.base.pygeoconstants import *
from pygeo.base.pygeomath import *
from pygeo.base.pygeoprimitives import *
from pygeo.base.pygeoopts import *

SphereClasses = ['CenterSphere', 'OrthoSphere', 'CircumSphere']

SphereDefs = ['Sphere']

__all__= SphereClasses + SphereDefs



class CenterSphere(Real._Sphere):
   """
:constructors:

     - Sphere(point1,point2)
     - CenterSphere(point1,point2)

:returns:  sphere with center at point1 and through point2

:site ref: http://mathworld.wolfram.com/Sphere.html
   """
   def __init__(self,center,cpoint,**kws):
       self.linewidth=kws.get('linewidth',.2)
       Real._Sphere.__init__(self,*[center,cpoint],**kws)
       self._cpoint=cpoint
       self._center=center
       self.update()

   def _findSelf(self):
       self._radiusSquared = self._center.distanceSquared(self._cpoint)
       self._radius=sqrt(self._radiusSquared)
       return True


class OrthoSphere(Real._Sphere):
   """
:constructors:

     - Sphere(sphere,point)
     - OrthoSphere(sphere,point)

:returns:  sphere with center at given point and orthogonal to given sphere
:conditions: point exterior to sphere
:else returns: None
:site ref: http://mathworld.wolfram.com/OrthogonalCircles.html
   """
   def __init__(self,sphere,center,**kws):
       Real._Sphere.__init__(self,*[sphere,center],**kws)
       self.sphere=sphere
       self._center=center
       self.deps=[self._cpoint]
       self.update()

   def _findSelf(self):
       s_radius=self.sphere._radius
       pdist = self.sphere._center.distance(self._center)-s_radius
       rsqr =pdist*(2*s_radius+pdist)
       if rsqr <= 0:
         print self.__class__.__name__
         print "point is interior to sphere, othogonal sphere undefined, returned False"
         return False
       self._cpoint.set(self._center.norm()*sqrt(rsqr)+self._center)
       self._radiusSquared = self._center.distanceSquared(self._cpoint)
       self._radius=sqrt(self._radiusSquared)
       return True

class CircumSphere(Real._Sphere):
   """
:constructors:

     - Sphere((point1,point2,point3,point4)
     - CircumSphere((point1,point2,point3,point4)

:returns:  the sphere through the 4 given points
:conditions: points are unique
:else returns: None
:site ref: http://mathworld.wolfram.com/Circumsphere.html
   """
   def __init__(self,p1,p2,p3,p4,**kws):
       self.p1=p1
       self.p2=p2
       self.p3=p3
       self.p4=p4
       Real._Sphere.__init__(self,*[p1,p2,p3,p4],**kws)
       self._cpoint=self.p1
       self.deps=[self._center]
       self.update()

   def _findSelf(self):
      if self._center.toSphereCenter(self.p1,self.p2,self.p3,self.p4):
          self._radiusSquared = self._center.distanceSquared(self._cpoint)
          self._radius=sqrt(self._radiusSquared)
          return True
      else:
         return False

def  Sphere(*args,**kws):
   """
:constructors:

   - Sphere(point1,point2); calls: `class CenterSphere`_
   - Sphere((sphere,point);  calls: `class OrthoSphere`_
   - Sphere((point1,point2,point3,point4); calls: `class CircumSphere`_

:returns: An instance of an object derived from the `_Sphere`_ abstract class,
          representing all points in space equidistant from a given point
   """
   __sigs__=[[vector,vector],[Real._Sphere,vector],
             [vector,vector,vector,vector]]
   t,i = method_get(__sigs__,args)
   if t is None:
      raise Argument_Type_Error(__sigs__,args)
   else:
      if i == 0:
         return CenterSphere(t[0],t[1],**kws)
      elif i == 1:
         return OrthoSphere(t[0],t[1],**kws)
      elif i==2:
         return CircumSphere(t[0],t[1],t[2],t[3],**kws)
      else:
         raise Argument_Type_Error(__sigs__,args)
