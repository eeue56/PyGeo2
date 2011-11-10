import pygeo.base.abstract_elements_real as Real
from pygeo.base.abstract_elements_real import method_get



from pygeo.base.pygeoexceptions import Argument_Type_Error
from pygeo.base.pygeoconstants import *
from pygeo.base.pygeomath import *
from pygeo.base.pygeoprimitives import *
from pygeo.base.pygeoopts import *


PlaneClasses = ['PlaneFromPoints', 'ParaPointPlane',
'ParaLinesPlane', 
'PerpPlane', 'PlaneFromNormal', 'PolarPlane', 'Triangle']

PlaneDefs = ['Plane']


__all__= PlaneClasses+PlaneDefs




class PlaneFromPoints(Real._Plane):
   """
:constructors:

     - Plane(point1,point2,point3)
     - PlaneFromPoints(point1,point2,point3)

:returns:  the plane_ through the given points
:conditions: points are distinct and are not collinear
:else returns: None
:site ref: http://www.mathematics-online.org/inhalt/beispiel/beispiel519/
   """
   def __init__(self,p1,p2,p3,**kws):
       self.p1=p1
       self.p2=p2
       self.p3=p3
       Real._Plane.__init__(self,*[p1,p2,p3],**kws)
       self.update()

   def _findSelf(self):
        if self.set_uds_fromPoints():
           return True
        else:
           return False

class ParaPointPlane(Real._Plane):
   """
:constructors:

     - Plane(plane point)
     - ParaPointPlane(plane,point)

:returns: the plane_ through the given point and parallel_ to the given plane

:site ref: http://www.jtaylor1142001.net/calcjat/Solutions/VPlanes/VPPtParlPlane.htm
   """
   def __init__(self,plane,p1,**kws):
       self.plane=plane
       self.p1=p1
       Real._Plane.__init__(self,*[plane,p1],**kws)
       self.update()

   def _findSelf(self):
         self._u.set(self.plane._u)
         self._d=self._u.dot(self.p1)
         self._s.set(self.plane._s)
         return True

class ParaLinesPlane(Real._Plane):
   """
:constructors:

     - Plane(line1,line2,point)
     - ParaLinesPlane(line1,line2,point)

:returns: the plane_ through the given point and parallel to the given lines.
:conditions: lines are distinct
:else returns: None
:site ref: http://mathworld.wolfram.com/ParallelLineandPlane.html
   """
   def __init__(self,line1,line2,point,**kws):
       self.line1=line1
       self.line2=line2
       self.point=point
       Real._Plane.__init__(self,*[line1,line2,point],**kws)
       self.update()

   def _findSelf(self):
      try:
         self._s.set(self.line1.getDirection())
         self._u.set((self._s.cross(self.line2.getDirection())).norm())
         self._d=self._u.dot(self.point)
         return True

      except ZeroDivisionError:
         print self.__class__.__name__
         print "lines are not distinct, no parallel plane defined, returned False"
         return False

#left undocumented
#class ParaPointsLinePlane(Real._Plane):
#   def __init__(self,p1,p2,line,**kws):
#       self.p1=p1
#       self.p2=p2
#       self.line=line
#       Real._Plane.__init__(self,*[p1,p2,line],**kws)
#       self.update()

#   def _findSelf(self):
#      try:
#         self._s.set((self.p2-self.p1).norm())
#         self._u.set((self.line.getDirection().cross(self._s)).norm())
#         self._d=self._u.dot(self.p1)
#         return True
#      except ZeroDivisionError:
#         print self.__class__.__name__
#         print "points are on line or are not distinct, no parallel plane defined, returned False"
#         return False

class PerpPlane(Real._Plane):
   """
:constructors:

     - Plane(plane,point1,point2)
     - PerpPlane(plane,point1,point2)

:returns: the plane through the given points and perpendicular to the given plane
:conditions: points are distinct
:else returns: None
:site ref: http://mathworld.wolfram.com/NormalVector.html
   """
   def __init__(self,plane,p1,p2,**kws):
       self.plane=plane
       self.p1=p1
       self.p2=p2
       Real._Plane.__init__(self,*[plane,p1,p2],**kws)
       self.update()

   def _findSelf(self):
      try:
         self._s.set((self.p2-self.p1).norm())
         self._u.set((self._s.cross(self.plane._u)).norm())
         self._d=self._u.dot(self.p1)
         return True
      except ZeroDivisionError:
         print self.__class__.__name__
         print "points are not distinct, not perpendicular plane defined, returned False"
         return False


class PlaneFromNormal(Real._Plane):
   """
:constructors:

     - Plane(point1,point2)
     - PlaneFromNormal(point1,point2)

:returns: the plane on point2 and normal_ to the line connecting point1 and point2
:conditions: points are distinct
:else returns: None
:site ref: http://mathworld.wolfram.com/NormalVector.html
   """
   def __init__(self,p1,p2,**kws):
       self.p1=p1
       self.p2=p2
       Real._Plane.__init__(self,*[p1,p2],**kws)
       self.args=[self.p1,self.p2]
       self.update()

   def _findSelf(self):
      try:
         self._u.set((self.p2-self.p1).norm())
         self._d = self._u.dot(self.p2)
         self.set_s_from_u(self._u)
         return True
      except ZeroDivisionError:
         print self.__class__.__name__
         print "points are not distinct, plane from normal undefined, returned False"
         return False


class PolarPlane(Real._Plane):
   """
:constructors:

     - Plane(sphere,point)
     - PolarPlane(sphere,point)

:returns:  the plane polar to the point with respect to the sphere
:conditions: point not at sphere center
:else returns: None
:site ref: http://mathworld.wolfram.com/Polar.html
   """
   def __init__(self,sphere,pole,**kws):
       self.sphere=sphere
       self.pole=pole
       Real._Plane.__init__(self,*[sphere,pole],**kws)
       self.update()

   def _findSelf(self):
      pole=self.pole
      sphere=self.sphere
      try:
         self._u.set((pole-sphere._center).norm())
         factor = float(sphere._radiusSquared)/pole.distance(sphere._center)
         t=self._u*factor+self.sphere._center
         self._d =  self._u.dot(t)
         self.set_s_from_u(self._u)
         return True
      except ZeroDivisionError:
         print self.__class__.__name__
         print "point at sphere center, polar plane at infinity, returned False"
         return False

class Triangle(Real._Triangle):
   """
:constructors:

     - Plane(point1,point2,point3,TRIANGLE)
     - Triangle(point1,point2,point3)

:returns:  the triangle connecting, on the plane dtermined by, the given points
:conditions: points are distinct and are not collinear
:else returns: None
:site ref: http://mathworld.wolfram.com/Triangle.html
   """
   def __init__(self,p1,p2,p3,**kws):
       self.p1=p1
       self.p2=p2
       self.p3=p3
       Real._Triangle.__init__(self,*[p1,p2,p3],**kws)
       self.color = (kws.get("color",CYAN))
       self.style=kws.get('style',LINES)
       self.linewidth = (kws.get("linewidth",.3))
       self.update()

   def _findSelf(self):
       try:
         self._u.set(cross3(self.p1,self.p2,self.p3).norm())
         self._d=self._u.dot(self.p1)
         self._s.set((self.p1-self.p2).norm())
         return True
       except ZeroDivisionError:
          print self.__class__.__name__
          print "points are not distinct or collinear, triangle from points undefined, returned False"
          return False

   def _getNormal(self):
         norm1=self._u
         norm2=-self._u
         return[norm1,norm1,norm1,norm2,norm2,norm2]



def  Plane(*args,**kws):
   """
:constructors:

   - Plane(point1,point2,point3); calls: `class PlanefromPoints`_
   - Plane(point1,point2,point3,PLANE); calls: `class PlanefromPoints`_
   - Plane(point1,point2,point3,TRIANGLE); calls: `class Triangle`_
   - Plane(plane,point1); calls: `class ParaPointPlane`_
   - Plane(line1,line2,point); calls: `class ParaLinesPlane`_
   - Plane(point1,point2,line); calls: `class ParaPointsLinePlane`_
   - Plane(point1,point2); calls: `class PlaneFromNormal`_
   - Plane(plane,point1,point2); calls: `class PerpPlane`_
   - Plane(sphere,point); calls: `class PolarPlane`_

:returns: An instance of an object derived from the `_Plane`_ abstract class,
          representing an infinite plane_ in space.
   """

   __sigs__=[[vector,vector,vector],[Real._Plane,vector],
              [Real._Circle,vector],[Real._Line,Real._Line,vector],
              [vector,vector,Real._Line],
              [Real._Plane,vector,vector],
              [Real._Circle,vector,vector],[vector,vector],
              [Real._Sphere,vector],[vector,vector,vector,float]]
   t,i = method_get(__sigs__,args)
   if t is None:
      raise Argument_Type_Error(__sigs__,args)
   else:
      if i == 0:
         return PlaneFromPoints(t[0],t[1],t[2],**kws)
      elif i == 1 or i==2:
         return ParaPointPlane(t[0],t[1],**kws)
      elif i == 3:
         return ParaLinesPlane(t[0],t[1],t[2],**kws)
#      elif i == 4:
#         return ParaPointsLinePlane(t[0],t[1],t[2],**kws)
      elif i == 5 or i==6:
         return PerpPlane(t[0],t[1],t[2],**kws)
      elif i==7:
         return PlaneFromNormal(t[0],t[1],**kws)
      elif i==8:
         return PolarPlane(t[0],t[1],**kws)
      elif i==9:
         if t[3] == 0:
            return PlaneFromPoints(t[0],t[1],t[2],**kws)
         elif t[3] ==1:
            return Triangle(t[0],t[1],t[2],**kws)
         else:
            raise Argument_Type_Error(__sigs__,args)
      else:
         raise Argument_Type_Error(__sigs__,args)
