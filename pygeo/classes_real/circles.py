import pygeo.base.abstract_elements_real as Real
from pygeo.base.abstract_elements_real import method_get


from pygeo.base.pygeoexceptions import Argument_Type_Error
from pygeo.base.pygeoconstants import *
from pygeo.base.pygeomath import *
from pygeo.base.pygeoprimitives import *
from pygeo.base.pygeoopts import *
from pygeo.base.position3 import Position3

CircleClasses = ['CircleOnPlane',
'CircumCircle', 'CenterCircle','InscribedCircle',
'ExscribedCircle', 'OrthoCircle','SphereCircle', 'SpheresIntersect',
]

CircleDefs = ['Circle']

__all__= CircleClasses+CircleDefs

class CircleOnPlane(Real._Circle):
   """
:constructors:

     - Circle(point1,point2,plane)
     - CircleOnPlane(point1,point2,plane)

:returns:  the circle_ on the given plane_ with 'point1' at center_ and radius equal
           to the distance between point1 and point2
:conditions: points on plane
:else returns: None
:site ref: http://mathworld.wolfram.com/Circle.html
   """
   def __init__(self,p1,p2,plane,**kws):
       self.plane=plane
       self.p1=p1
       self.p2=p2
       Real._Circle.__init__(self,*[p1,p2,plane],**kws)
       self._cpoint=self.p2
       self._center=self.p1
       self.update()

   def _findSelf(self):
      if DO_TESTS:
          t = (self.p1.onPlane(self.plane) and self.p2.onPlane(self.plane))
      else:
          t = True
      if t:
         self._radiusSquared=self._center.distanceSquared(self._cpoint)
         self._radius=sqrt(self._radiusSquared)
         self._u.set(self.plane._u)
         self._d = self.plane._d
         self._s.set(self.plane._s)
         return True
      else:
         print self.__class__.__name__
         print "points not on plane, circle undefined, returned False"
         return False

class CircumCircle(Real._Circle):
   """
:constructors:

     - Circle(point1,point2,point3, CIRCUM)
     - CircumCircle(point1,point2,point3)

:returns:  the circle_ that pass through the 3 point arguments
:condition: points distinct
:else returns: None
:site ref: http://mathworld.wolfram.com/Circumcircle.html
   """
   def __init__(self,p1,p2,p3,**kws):
       self.p1=p1
       self.p2=p2
       self.p3=p3
       Real._Circle.__init__(self,*[p1,p2,p3],**kws)
       self.deps=[self._center]
       self._cpoint=self.p2
       self.update()

   def _findSelf(self):
        if self._center.toCircumCenter(self.p1,self.p2,self.p3):
            self._radiusSquared=self._center.distanceSquared(self._cpoint)
            self._radius=sqrt(self._radiusSquared)
            self.set_uds_fromPoints()
            return True
        else:
            self._u=Position3(0,0,1)
            self._s=Position3(0,0,1)
            self._d=0
            return False

class CenterCircle(Real._Circle):
   def __init__(self,p1,p2,p3,**kws):
       self.p1=p1
       self.p2=p2
       self.p3=p3
       Real._Circle.__init__(self,*[p1,p2,p3],**kws)
       self._cpoint=self.p2
       self._center=self.p1
       self.update()

   def _findSelf(self):
      self._radiusSquared=self._center.distanceSquared(self._cpoint)
      self._radius=sqrt(self._radiusSquared)
      try:
         self._u=cross3(self.p1,self.p2,self.p3).norm()
         self._d=self._u.dot(self.p1)
         self._s=(self.p1-self.p2).norm()
         return True
      except ZeroDivisionError:
          print self.__class__.__name__
          print "points are not distinct, circle undefined, returned False"
          return False

class InscribedCircle(Real._Circle):
   """
:constructors:

     - Circle(point1,point2,point3, INSCRIBED)
     - InscribedCircle(point1,point2,point3)

:returns:  the circle_ inscribed_ in the triangle_ connecting the 3 point_ arguements
:condition: points distinct
:else returns: None
:site ref: http://mathworld.wolfram.com/Incircle.html
   """
   def __init__(self,p1,p2,p3,**kws):
       self.p1=p1
       self.p2=p2
       self.p3=p3
       Real._Circle.__init__(self,*[p1,p2,p3],**kws)
       self.deps=[self._center,self._cpoint]
       self.update()

   def _findSelf(self):
       try:
          self._center.toInCenter(self.p1,self.p2,self.p3)
          self._cpoint.set(self._center)
          self._cpoint.toLine(self.p1,self.p2)
          self._radiusSquared=self._center.distanceSquared(self._cpoint)
          self._radius=sqrt(self._radiusSquared)
          self.set_uds_fromPoints()
          return True

       except ZeroDivisionError:
          print self.__class__.__name__
          print "points are not distinct, circle undefined, returned False"
          return False

class ExscribedCircle(Real._Circle):
   """
:constructors:

     - Circle(point1,point2,point3, INSCRIBED)
     - InscribedCircle(point1,point2,point3)

:returns:  the circle_ inscribed_ in the triangle_ connecting the 3 point_ arguements
:condition: points distinct
:else returns: None
:site ref: http://mathworld.wolfram.com/Incircle.html
   """
   def __init__(self,p1,p2,p3,**kws):
       self.p1=p1
       self.p2=p2
       self.p3=p3
       Real._Circle.__init__(self,*[p1,p2,p3],**kws)
       self.deps=[self._center,self._cpoint]
       self.update()

   def _findSelf(self):
       try:
          self._center.toExCenter(self.p1,self.p2,self.p3)
          self._cpoint.set(self._center)
          self._cpoint.toLine(self.p1,self.p2)
          self._radiusSquared=self._center.distanceSquared(self._cpoint)
          self._radius=sqrt(self._radiusSquared)
          self.set_uds_fromPoints()
          return True
       except ZeroDivisionError:
          print self.__class__.__name__
          print "points are not distinct, circle undefined, returned False"
          return False


class OrthoCircle(Real._Circle):
   """
:constructors:

     - Circle(circle,point)
     - OrthoCircle(circle,point)

:returns:  the circle_ with center_ at the point_ argument and orthogonal_ to the circle_ argument
:conditions: point and circle are coplanar; point exterior to circle
:else returns: None; None
:site ref: http://mathworld.wolfram.com/OrthogonalCircles.html
   """
   def __init__(self,circle,point,**kws):
       self.circle=circle
       self.point=point
       Real._Circle.__init__(self,*[circle,point],**kws)
       self.deps=[self._cpoint]
       self._center=self.point
       self.update()

   def _findSelf(self):
      if DO_TESTS:
         t=self.point.onPlane(self.circle)
      else:
         t =True
      if t:
         self._d = self.circle._d
         self._u.set(self.circle._u)
         self._s.set(self.circle._s)
         pdist= self.circle._center.distance(self._center)-self.circle._radius
         rsqr = pdist*(2*self.circle._radius+pdist)
         if rsqr < 0:
            print self.__class__.__name__
            print "point is interior to circle, orthocircle through point as \
                   center is undefined, returned False"
            return False
         
         self._cpoint.set(self._s*sqrt(rsqr)+self._center)
         self._radiusSquared=self._center.distanceSquared(self._cpoint)
         self._radius=sqrt(self._radiusSquared)
         return True
      else:
         print self.__class__.__name__
         print "circle and point are not coplanar, orthocircle undefined, returned False"
         return False


class SphereCircle(Real._Circle):
   """
:constructors:

     - Circle(sphere,plane);
     - SphereCircle(sphere,plane);

:returns: the circle_ at the circumference_ of the disk determined by the `cross section`_
          the given sphere and the given plane
:conditions: sphere and plane intersection is real
:else returns: None
:site ref: http://mathworld.wolfram.com/CrossSection.html
   """
   def __init__(self,sphere,plane,**kws):
       self.sphere=sphere
       self.plane=plane
       Real._Circle.__init__(self,*[sphere,plane],**kws)
       self.deps=[self._center,self._cpoint]
       self.update()

   def _findSelf(self):
         self._d = self.plane._d
         self._u.set(self.plane._u)
         self._s.set(self.plane._s)
         self._center.set(self.sphere._center)
         self._center.toPlane(self.plane)
         pdist = self._center.distanceSquared(self.sphere._center)
         rsqr = self.sphere._radiusSquared-pdist
         if rsqr < 0:
             print self.__class__.__name__
             print "no real plane, sphere intersection, returned false"
             return False
         self._cpoint.set(self._s*sqrt(rsqr)+self._center)
         self._radiusSquared=self._center.distanceSquared(self._cpoint)
         self._radius=sqrt(self._radiusSquared)
         return True

class SpheresIntersect(Real._Circle):
   """
:constructors:

     - Circle(sphere1,sphere2)
     - SpheresIntersect(circle,point)

:returns:  the circle_ determined by the intersection_ of the 2 sphere_ arguments
:conditions: spheres' intersection is real, spheres are not concentric
:else returns: None; None
:site ref: http://mathworld.wolfram.com/Sphere-SphereIntersection.html
   """
   def __init__(self,sphere1,sphere2,**kws):
       self.sphere1=sphere1
       self.sphere2=sphere2
       Real._Circle.__init__(self,*[sphere1,sphere2],**kws)
       self.deps=[self._center,self._cpoint]
       self.update()

   def _findSelf(self):
         sphere1=self.sphere1
         sphere2=self.sphere2
         
         tnormal= sphere1._center - sphere2._center
         rsum = sphere1._radius+ sphere2._radius
         tlen=  tnormal.mag2
         if tlen > rsum**2:
            print self.__class__.__name__
            print "spheres do not intersect, not real intersection, returned false"
            return False
         try:
             t = 0.5*(1.0+(sphere1._radiusSquared-sphere2._radiusSquared)/tlen)
         except ZeroDivisionError:
             print self.__class__.__name__
             print "spheres are concentric, no intersection defined, returned false"
             return False
         normal=tnormal*t
         self._d=normal.mag
         self._u.set(normal.norm())
         self.set_s_from_u(self._u)
         self._center.set(sphere1._center-normal)
         rsqr = sphere1._radiusSquared - (t**2)*tlen
         if rsqr < 0:
            print self.__class__.__name__
            print "a sphere is interior to the other, not real intersection, returned false"
            return False
         self._cpoint.set(self._s*sqrt(rsqr)+self._center)
         self._radiusSquared=self._center.distanceSquared(self._cpoint)
         self._radius=sqrt(self._radiusSquared)
         return True


def  Circle(*args,**kws):
   """
:constructors:

   - Circle(point1,point2,point3); calls: `class CenterCircle`_
   - Circle(point1,point2,point3,CENTER); calls: `class CenterCircle`_
   - Circle(point1,point2,point3,CIRCUM); calls: `class CircumCircle`_
   - Circle(point1,point2,point3,INSCRIBED); calls: `class InscribedCircle`_
   - Circle(point1,point2,point3,EXSCRIBED); calls: `class ExscribedCircle`_
   - Circle(point1,point2,plane); calls: `class CircleOnPlane`_
   - Circle(circle,point);                   calls: `class OrthoCircle`_
   - Circle(sphere,plane);                   calls: `class SphereCircle`_
   - Circle(sphere1,sphere2);                calls: `class SpheresIntersect`_

:returns: an instance of an object derived from the `_Circle`_ abstract class, determined
          uniquely by reference to its arguments

   """
   __sigs__=[[vector,vector,Real._Plane],[vector,vector,Real._Circle],
             [vector,vector,vector],[Real._Triangle],
             [vector,vector,vector,float],
             [Real._Triangle,float],[Real._Circle,vector],[Real._Sphere,Real._Plane],
             [Real._Sphere,Real._Sphere]]
   t,i = method_get(__sigs__,args)
   if t is None:
      raise Argument_Type_Error(__sigs__,args)
   else:
      if i ==0 or i==1:
         return CircleOnPlane(t[0],t[1],t[2],**kws)
      elif i == 2:
         type = kws.get("circle_type","Center")
         if type=="Center":
            return CenterCircle(t[0],t[1],t[2],**kws)
         elif type == "Circum":
            return CircumCircle(t[0],t[1],t[2],**kws)
         elif type == "Inscribed":
            return InscribedCircle(t[0],t[1],t[2],**kws)
         elif type == "Exscribed":
            return ExscribedCircle(t[0],t[1],t[2],**kws)
         else:
            raise Argument_Type_Error(__sigs__,args)
      elif i == 3:
         if type==0:
            return CenterCircle(t[0].p1,t[0].p2,t[0].p3,**kws)
         elif type == 1:
            return CircumCircle(t[0].p1,t[0].p2,t[0].p3,**kws)
         elif type == 2:
            return InscribedCircle(t[0].p1,t[0].p2,t[0].p3,**kws)
         elif type == 3:
            return ExscribedCircle(t[0].p1,t[0].p2,t[0].p3,**kws)
         else:
            raise Argument_Type_Error(__sigs__,args)
      elif i==4:
         if t[3]== 1:
            return CircumCircle(t[0],t[1],t[2],**kws)
         if t[3] == 2:
            return InscribedCircle(t[0],t[1],t[2],**kws)
         elif t[3] == 3:
            return ExscribedCircle(t[0],t[1],t[2],**kws)
         else:
            raise Argument_Type_Error(__sigs__,args)
      elif i==5:
         if t[1]== 1:
            return CircumCircle(t[0].p1,t[0].p2,t[0].p3,**kws)
         if t[1] == 2:
            return InscribedCircle(t[0].p1,t[0].p2,t[0].p3,**kws)
         elif t[1] == 3:
            return ExscribedCircle(t[0].p1,t[0].p2,t[0].p3,**kws)
         else:
            raise Argument_Type_Error(__sigs__,args)
      elif i==6:
         return OrthoCircle(t[0],t[1],**kws)
      elif i==7:
         return SphereCircle(t[0],t[1],**kws)
      elif i==8:
         return SpheresIntersect(t[0],t[1],**kws)
      else:
         raise Argument_Type_Error(__sigs__,args)
