
import pygeo.base.abstract_elements_real as Real
from pygeo.base.abstract_elements_real import method_get

from pygeo.base.position3 import Position3

from pygeo.base.pygeoexceptions import Argument_Type_Error
from LinearAlgebra import LinAlgError
from pygeo.base.pygeoconstants import *
from pygeo.base.pygeomath import *
from pygeo.base.pygeoprimitives import *

from pygeo.classes_real.pointarrays import Conic

from pygeo.base.pygeoopts import *

LineArrayClasses = ['LinePencil', 'Regulus', 'PointMap', 'ArrayMap',
'PlanesPencilIntersect', 'Lines', 'CorrelationLines']

LineArrayDef = ['LineArray']

__all__= LineArrayClasses+LineArrayDef

class LinePencil(Real._LineArray):
   """
:constructors:

     - LineArray(point,plane)
     - CirclingLines(point,plane)

:returns:  array of equidistint lines on the given plane and through the given point
:conditions: point on the plane
:else returns: None
:site ref: http://mathworld.wolfram.com/Pencil.html
   """
   __opts__ = Real._LineArray.__opts__ + ["start"]
   def __init__(self,point,plane,**kws):
      self.point=point
      self.plane=plane
      Real._LineArray.__init__(self,*[point,plane],**kws)
      self.v=2*PI/self.density
      self.start=kws.get("start",0)
      self.update()

   def _findSelf(self):
      if DO_TESTS:
         t = self.point.onPlane(self.plane)
      else:
         t = True
      if t:
         cpoint = self.plane._s*self.drawradius
         for i,line in enumerate(self.lines):
            rad=i*self.v/2
            line.p1.set(cpoint.rotate(rad+self.start,self.plane._u) + self.point)
            line.p2.set(self.point)
         return True
      else:
         print self.__class__.__name__
         print "point not on plane, line array undefined, returned false"
         return False

class Regulus(Real._LineArray):
   """
:constructors:

     - LineArray(pointarray,line1,line2)
     - Regulus(pointarray,line1,line2)

:returns:  array of lines tranversal to the given lines and through the array of points
:conditions: lines distinct
:else returns: None
:site ref: http://mathworld.wolfram.com/QuadraticSurface.html
   """
   def __init__(self,pointpencil,line1,line2,**kws):
      self.pointpencil=pointpencil
      self.line1=line1
      self.line2=line2
      Real._LineArray.__init__(self,*[pointpencil,line1,line2],**kws)
      self.density=self.pointpencil.density
      self.extend=kws.get("extend",False)
      self.update()


   def _findSelf(self):
      for i,line in enumerate(self.lines):
         l1=self.line1
         l2=self.line2
         u1=cross3(l1.p1,l1.p2,self.pointpencil.points[i])
         d1=u1.dot(l1.p1)
         u2=cross3(l2.p1,l2.p2,self.pointpencil.points[i])
         d2=u2.dot(l2.p1)
         dir=u1.cross(u2)
         try:
            ip1 = vector(solve(
                    array([u1,u2,dir]),
                    array([d1,d2,0.])))
                 
         except LinAlgError:
            print self.__class__.__name__
            print "lines are not distinct, quadric undefined, returned False"
            return False
         ip2= dir + ip1
         line.p1.toInterSection(ip1,ip2,self.line1.p1,self.line1.p2,test=False)
         line.p2.toInterSection(ip1,ip2,self.line2.p1,self.line2.p2,test=False)
      return True

 #  def setext(self):
 #     if self.Not_null:
 #        if self.show:
 #           for point,line,rend in zip(self.pointpencil,self,self.crend):
 #              v = self.get_extension(line,point)
 #              if v:
 #                  rend.pos=[v.pos,point.vector]
 #              else:
 #                  rend.pos=[]
 #        else:
 #           for rend in self.crend:
 #                  rend.pos=[]
 #     else:
 #        for rend in self.crend:
 #                  rend.pos=[]

 #  def get_extension(self,line,point):
 #     a=line[0].distance(line[1])
 #     b=line[0].distanceSquared(point)
 #     c=line[1].distanceSquared(point)
 #     if a > b and a > c:
 #        return False
 #     elif a < b:
 #        return line[0]
 #     else:
 #        return line[1]

 #  def draw(self):
 #     append=self.crend.append
 #     if self.extend:
 #        for i in range(self.density):
 #           append(curve(radius=self.linewidth,color=self.color))

 #     _LineArray.draw(self)
 #     self.init()
 #     self.update()


class PointMap(Real._LineArray):
   """
:constructors:

     - LineArray([point1,point2,point3],[point1a,point2a,point3a])
     - PointMap([point1,point2,point3],[point1a,point2a,point3a])

:returns: array of lines connecting points of the projective correspondance
          defined by the first 3 given points and the second 3 given points
:site ref: http://mathworld.wolfram.com/FundamentalTheoremofProjectiveGeometry.html
   """

   def __init__(self,points1,points2,**kws):
      self.p1a=points1[0]
      self.p1b=points1[1]
      self.s1=points1[2]
      self.p2a=points2[0]
      self.p2b=points2[1]
      self.s2=points2[2]
      args=points1 + points2   
      Real._LineArray.__init__(self,*args,**kws)
      self.update()

   def _findSelf(self):
      for i, line in enumerate(self.lines):
         step=(1/float(len(self.lines)))*i
         line.p1.toInterpolated(self.p1a,self.p1b,step)
         line.p2.toCrossPoint(self.p1a,self.s1,self.p1b,
                             line.p1,
                             self.p2a,self.s2,self.p2b)

      return True




class ArrayMap(Real._LineArray):
   """
:constructors:

     - LineArray(pointarray1,pointarray2)
     - ArrayMap((pointarray1,pointarray2)

:returns: array of lines connecting the points of the point arrays
   """
   def __init__(self,pointarray1,pointarray2,**kws):
      self.pa1=pointarray1
      self.pa2=pointarray2
      Real._LineArray.__init__(self,*[pointarray1,pointarray2],**kws)
      self.density=min(self.pa1.density,self.pa2.density)
      self.update()

   def _findSelf(self):
      for line,p1,p2 in zip(self.lines,self.pa1,self.pa2):
         line.p1.set(p1)
         line.p2.set(p2)
      return True

class PlanesPencilIntersect(Real._LineArray):
   """
:constructors:

     - LineArray(planepencil1,planepencil2)
     - PlanesPencilIntersect(planearray1,planearray2)

:returns:  array of lines of intersection of the 2 pencils of planes arguments
:conditions: plane pencils distintct
:else returns: None
:site ref: http://mathworld.wolfram.com/Plane-PlaneIntersection.html
   """
   def __init__(self,planes1,planes2,**kws):
      self.planes1=planes1
      self.planes2=planes2
      self.density=min(self.planes1.density,self.planes2.density)
      Real._LineArray.__init__(self,*[planes1,planes2],**kws)
      self.drawlen=kws.get("drawlen",40)
      self.update()

   def _findSelf(self):
      planes1 =self.planes1
      planes2 = self.planes2
      for p1,p2,line in zip(planes1,planes2,self.lines):
            try:
               dir=cross(p1._u,p2._u)
            except IndexError:
               print self.__class__.__name__
               print "plane pencil empty, intersection array undefined, returned False"
               return False
            try:
               line.p1.set(vector(solve(
                              array([p1._u,p2._u,dir]),
                              array([p1._d,p2._d,0.]))
                                    ))
            except LinAlgError:
               print self.__class__.__name__
               print "plane pencils not distinct, intersection array undefined, returned False"
               return False
            line.p2.set(dir*self.drawlen+line.p1)
      return True


class Lines(Real._LineArray):
   """
:constructors:

     - LineArray(pointarray,point)
     - Lines(pointarray,point)

:returns: array of lines through the points of the point array and the given point

:site ref: http://mathworld.wolfram.com/Pencil.html
   """
   def __init__(self,pointarray,point,**kws):
      self.pa=pointarray
      self.point=point
      self.density=self.pa.density
      Real._LineArray.__init__(self,*[pointarray,point],**kws)
      self.update()

   def _findSelf(self):
      for point,line in zip(self.pa,self.lines):
        line.p1.set(point)
        line.p2.set(self.point)
      return True

class CorrelationLines(Real._LineArray):
   """
:constructors:

     - LineArray(conic,pointarray)
     - Correlation(conic,pointarray)

:returns: array of lines polar to the points of the point array with respect to the conic
:site ref: http://mathworld.wolfram.com/GeometricCorrelation.html
   """
   def __init__(self,conic,pointarray,**kws):
      self.conic=conic
      self.pa=pointarray
      self.density=self.pa.density
      self.x1z=Position3()
      self.x2z=Position3()
      Real._LineArray.__init__(self,*[conic,pointarray],**kws)
      self.update()

   def _findSelf(self):
      equat=self.conic.getPlane()
      C=self.conic.getC()
      for point,line in zip(self.pa,self.lines):
         L= matrixmultiply(C*2,point)
         tp1=array([0.,-L[2]/L[1],1.])
         tp2=array([-L[2]/L[0],0.,1.])
         cx = matrixmultiply(matrixmultiply(C,tp1),transpose(tp1))
         ax = matrixmultiply(matrixmultiply(C,tp2),transpose(tp2))
         bx =2*matrixmultiply(matrixmultiply(C,tp2),transpose(tp1))
         h=quadratic(ax,bx,cx)
         if h[0]:
            x1=tp1+tp2*h[0]
            x2=tp1+tp2*h[1]
         else:
            x1=tp1
            x2=tp2
         self.x1z.set(vector([x1[0]/x1[2],x1[1]/x1[2],0]))
         self.x2z.set(vector([x2[0]/x2[2],x2[1]/x2[2],0]))
         line.p1.fromXY(equat,self.x1z)
         line.p2.fromXY(equat,self.x2z)
      return True

def  LineArray(*args,**kws):
   """
:constructors:

   - LineArray(point,plane); calls: `class CirclingLines`_
   - LineArray(pointarray,line1,line2); calls: `class Regulus`_
   - LineArray(pointarray1,pointarray2); calls: `class ArrayMap`_
   - LineArray(planepencil1,planepencil2); calls: `class PlanesPencilIntersect`_
   - LineArray(pointarray,point); calls: `class Lines`_
   - LineArray(conic,pointarray); calls: `class CorrelationLines`_

:returns: An instance of an object derived from the `_Line`_ abstract class,
          representing an infinite line in space, or, in context, the line segment
          between the line 'p1' nnd 'p2' attributes.

   """
   __sigs__=[[Real._PointArray,vector],[vector,Real._Plane],
              [vector,Real._Circle],[Real._PointArray,Real._Line,Real._Line],
              [list,list],
              [Real._PointArray,Real._PointArray],[Real._PlaneArray,Real._PlaneArray],
              [Conic,Real._PointArray]]

   t,i = method_get(__sigs__,args)
   if t is None:
      raise Argument_Type_Error(__sigs__,args)
   else:
      if i ==0:
         return Lines(t[0],t[1],**kws)
      elif i==1 or i==2:
         return LinePencil(t[0],t[1],**kws)
      elif i==3:
         return Regulus(t[0],t[1],t[2],**kws)
      elif i==4:
         return PointMap(t[0],t[1],**kws)
      elif i==5:
         return ArrayMap(t[0],t[1],**kws)
      elif i==6:
         return PlanesPencilIntersect(t[0],t[1],**kws)
      elif i==7:
         return CorrelationLines(t[0],t[1],**kws)
      else:
         raise Argument_Type_Error(__sigs__,args)
