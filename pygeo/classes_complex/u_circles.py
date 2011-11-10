import pygeo.base.abstract_elements_complex as Complex
import pygeo.base.abstract_elements_usphere as USphere
import pygeo.base.abstract_elements_real as Real
from pygeo.base.abstract_elements_real import method_get
from pygeo.base.pygeoexceptions import Argument_Type_Error

from pygeo.base.pygeomath import *
from pygeo.base.pygeoconstants import *
from pygeo.base.pygeoopts import *


UCircleClasses = ['uCircumCircle', 'z_to_uCircle',
                   'uCircleFromNormal','uPolarCircle']

UCircleDef = ['uCircle']


__all__ = UCircleClasses + UCircleDef



#circles on the unit sphere


class uCircumCircle(USphere._uCircle):
   """
:constructors: 

     - uCircle(uPoint,uPoint,uPoint) 
     - uCircumCircle(uPoint,uPoint,uPoint) 
 
:returns: `spheric section`_ through 3 given points on the `Riemann sphere`_ .

:site ref: http://mathworld.wolfram.com/Circumcircle.html
   """
   def __init__(self,p1,p2,p3,**kws):
       USphere._uCircle.__init__(self,*[p1,p2,p3],**kws)
       self.p1=p1
       self.p2=p2
       self.p3=p3
       self._cpoint=self.p2
       self.deps=[self._center]
       self.update()

   def _findSelf(self):
        if self._center.toCircumCenter(self.p1,self.p2,self.p3):
            self._radiusSquared=self._center.distanceSquared(self._cpoint)
            self._radius=sqrt(self._radiusSquared)
            self.set_uds_fromPoints()
            return True
        else:
            self._u.set(vector(0,0,1))
            self._s.set(vector(0,0,1))
            self._d=0
            return False

class z_to_uCircle(USphere._uCircle):
   """
:constructors: 

     - uCircle(zCircle) 
     - uCircle(zLine) 
     - z_to_uCircle(zCircle) 
     - z_to_uCircle(zLine) 
 
:returns: the `stereographic projection`_ circle of the given circle or line of the 
          `complex plane`_ onto the  `Riemann sphere`_. 
:site ref: http://mathworld.wolfram.com/StereographicProjection.html
   """   
   def __init__(self,zCircle,**kws):
     USphere._uCircle.__init__(self,*[zCircle],**kws)
     self.zcircle=zCircle
     self.deps=[self._cpoint,self._center]
     self.update()

   def _findSelf(self):
      h = self.zcircle._hermitian
      a = h.B+h.C
      b = (h.B-h.C)*1j
      c = h.D-h.A
      d = h.D+h.A
      v=vector(a.real,b.real,-c.real)
      self._u.set(v.norm())
      self._d = d.real/mag(v)
      self._center.set(self._u*self._d*-1)
      self._radiusSquared =1-self._center.lengthSquared()
      if self._radiusSquared < 0:
          self._radiusSquared = 0
          return False
      self._radius=sqrt(self._radiusSquared)
      self.set_s_from_u(self._u)
      self._cpoint.set(self._s*self._radius+self._center)
      return True

class uCircleFromNormal(USphere._uCircle):
   """
:constructors: 

     - uCircle(point,point) 
     - uCircleFromNormal(point,point) 
 
:returns: `spheric section`_ of the `Riemann sphere`_ cut by the plane_
          at the initial point argument that is normal_
          to the direction determined by the first and
          second point arguments 
:conditions: plane from normal_ cuts the `Riemann sphere`_
:else returns: None
:site ref: http://mathworld.wolfram.com/NormalVector.html
   """   
   def __init__(self,p1,p2,**kws):
      self.p1=p1
      self.p2=p2
      USphere._uCircle.__init__(self,*[p1,p2],**kws)
      self.deps=[self._center,self._cpoint]
      self.update()

   def _findSelf(self):
      self._u.set((self.p2-self.p1).norm())
      self._d = self._u.dot(self.p2)
      self._center.set(self._u*self._d)
      self._radiusSquared =1. - self._center.mag2
      if self._radiusSquared < 0:
          self._radiusSquared = 0
          print "plane does not cut the unit sphere, returned false"
          return False
      self._radius=sqrt(self._radiusSquared)
      self.set_s_from_u(self._u)
      self._cpoint.set(self._s*self._radius+self._center)
      return True

class uPolarCircle(USphere._uCircle):
   """
:constructors: 

     - uCircle(point) 
     - uPolarCircle(point) 
 
:returns: `spheric section`_ of `Riemann sphere`_ cut by the plane_
          polar_ to the point argument with respect
          to the `Riemann sphere`_ 
:conditions: point exterior to the unit sphere
:else returns: None
:site ref: http://mathworld.wolfram.com/Polar.html
   """   
   def __init__(self,pole,**kws):
      USphere._uCircle.__init__(self,*[pole],**kws)
      self.pole=pole
      self.deps=[self._center,self._cpoint]
      self.update()

   def _findSelf(self):
      self._u.set(self.pole.norm())
      self._d = self._u.dot(self._u)*(1./self.pole.length())
      self._center.set(self._u*self._d)
      self._radiusSquared =1.0 -self._center.lengthSquared()
      if self._radiusSquared < 0:
          self._radiusSquared = 0
          return False
      self._radius=sqrt(self._radiusSquared)
      self.set_s_from_u(self._u)
      self._cpoint.set(self._s*self._radius+self._center)
      return True


def uCircle(*args,**kws):
   """
:constructors: 

  - uCircle(uPoint,uPoint,uPoint);  calls: `class uCircumCircle`_
  - uCircle(point,point);  calls: `class uCircleFromNormal`_
  - uCircle(point);  calls: `class uPolarCircle`_
  - uCircle(zCircle);  calls: `class z_to_uCircle`_
  - uCircle(zLine);  calls: `class z_to_uCircle`_
  
  
:returns: A `spheric section`_ of the `Riemann sphere`_
          
:site ref: http://mathworld.wolfram.com/SphericSection.html
   """   
   __sigs__=[[USphere._uPoint,USphere._uPoint,USphere._uPoint],
               [Real._Point,Real._Point],
               [Real._Point],
               [Complex._zCircle],[Complex._zLine]]
   t,i = method_get(__sigs__,args)
   if t is None:
      raise Argument_Type_Error(__sigs__,args)
   else:
      if i==0:
         return uCircumCircle(t[0],t[1],t[2],**kws)
      elif i==1:
         return uCircleFromNormal(t[0],t[1],**kws)
      elif i==2:
         return uPolarCircle(t[0],**kws)
      elif i==3 or i==4:
         return z_to_uCircle(t[0],**kws)
      else:
         raise Argument_Type_Error(__sigs__,args)


