
import pygeo.base.abstract_elements_real as Real
from pygeo.base.abstract_elements_real import method_get

from pygeo.base.position3 import Position3

from pygeo.base.pygeoexceptions import Argument_Type_Error
from LinearAlgebra import LinAlgError
from pygeo.base.pygeoconstants import *
from pygeo.base.pygeomath import *
from pygeo.base.pygeoprimitives import *
from pygeo.base.element import Element
from pygeo.classes_real.pointarrays import Conic


from pygeo.base.pygeoopts import *



LineClasses = ['LineFromPoints', 'PlanePerp',
'PlanesLine', 'ParaLine', 'Transversal','NearLine','ConicPolar','LinePerp', 'CirclePolar']

LineDef = ['Line']


__all__= LineClasses+ LineDef





class LineFromPoints(Real._Line):
   """
:constructors:

     - Line(point1,point2)
     - LinefromPoints(point1,point2)

:returns:  the line_ connecting the point_ arguments

:site ref: http://mathworld.wolfram.com/Line.html
   """
   def __init__(self,p1,p2,**kws):
       Real._Line.__init__(self,*[p1,p2],**kws)
       self.p1=p1
       self.p2=p2
       self.update()

   def __repr__(self):
      return self.__class__.__name__ + "(" + str(self.p1) +"," + str(self.p2) + ")"

   def _findSelf(self):
      if DO_TESTS:
         if self.p1 == self.p2:
            print self.__class__.__name__
            print "points are not distinct, no line defined, returned False"
            return False
      return True


class PlanePerp(Real._Line):
   """
:constructors:

     - Line(plane,point)
     - PlanePerp(plane,point)

:returns:  The line_ perpendicular_ to the given plane_  and through the given
           point_.  See PlaneFoot_
:conditions: point not on plane
:else returns: None
:site ref: http://mathworld.wolfram.com/PerpendicularFoot.html
   """
   def __init__(self,plane,p1,**kws):
       self.plane=plane
       self.drawlen=kws.get("drawlen",20)
       Real._Line.__init__(self,*[plane,p1],**kws)
       self.p1=p1
       self.deps=[self.p2]
       self.update()


   def _findSelf(self):
       t=self.p1.onPlane(self.plane)
       if t:
         self.p2.set(self.plane._u*self.drawlen+self.p1)
       else:
         self.p2.set(self.p1)
         self.p2.toPlane(self.plane)
       return True



class LinePerp(Real._Line):
   """
:constructors:

     - Line(point1,point2,point3)
     - LinePerp(point1,point2,point3)

:returns: The line through point 2 perpendicular_ to the line through
          point1 and point 2, on the plane dtermined by the 3 given points

:condition: point and circle are coplanar
:else returns: None
:site ref: http://mathworld.wolfram.com/Perpendicular.html
   """

   def __init__(self,p1,p2,p3,**kws):
       self.n1 = p1
       self.drawlen=kws.get("drawlen",20)
       self.n3 = p3
       self.n2=p2
       self.u1=Position3()
       self.u2=Position3()
       self.n=Position3()
       Real._Line.__init__(self,*[p1,p2,p3],**kws)
       self.deps=[self.p1,self.p2]
       self.update()


   def _findSelf(self):
       n1=self.n1
       n2=self.n2
       n3=self.n3
       u1=self.u1
       u2=self.u2
       drawlen=self.drawlen/2.
       u1.set((n2-n1).norm())
       d1 = u1.dot(n2)
       u2.set(cross3(n1,n2,n3).norm())
       d2=u2.dot(n2)

       
       direction = u2.cross(u1).norm()
       self.n.set(vector(solve(
                        array([u2,u1,direction]),
                           array([d2,d1,0.]))))
       self.p1.set(direction*drawlen+self.n)
       self.p2.set(direction*-drawlen+self.n)
       return True

class PlanesLine(Real._Line):
   """
:constructors:

     - Line(plane1,plane2)
     - PlanesLine(plane1,plane2)

:returns:   the line_ determined by the intersection_ of the given plane_ arguments.
:conditions: planes not parallel
:else returns: None
:site ref: http://mathworld.wolfram.com/Plane-PlaneIntersection.html
   """
   __opts__ = Real._Line.__opts__[:]+["drawlen"]

   def __init__(self,plane1,plane2,**kws):
       self.plane1=plane1
       self.plane2=plane2
       self.drawlen=kws.get("drawlen",20)
       Real._Line.__init__(self,*[plane1,plane2],**kws)
       self.deps=[self.p1,self.p2]
       self.update()

   def getDirection(self):
      return self.plane1._u.cross(self.plane2._u).norm()

   def getNormal(self):
      plane1=self.plane1
      plane2=self.plane2
      return vector(solve(
                        array([plane1._u,plane2._u,self.getDirection()]),
                           array([plane1._d,plane2._d,0.])))


   def parameters(self):
      plane1=self.plane1
      plane2=self.plane2
      direction = self.getDirection()
      try:
         normal =  vector(solve(
                        array([plane1._u,plane2._u,direction]),
                           array([plane1._d,plane2._d,0.])))
      except LinAlgError:
         print self.__class__.__name__
         print "planes parallel, not intersection found"
         return None,None
      return normal,direction

   def _findSelf(self):
      
      normal,direction=self.parameters()
      if normal:
          drawlen=self.drawlen/2.
          self.p1.set(direction*drawlen+normal)
          self.p2.set(direction*-drawlen+normal)
          return True
      else:
         print self.__class__.__name__
         print " planes parallel, returned False"
         return False
      
class ParaLine(Real._Line):
   """
:constructors:

     - Line(point,line)
     - ParaLine(point,line)

:returns:  The line_ parallel_ to the given line_, through the given point_, on the plane_
           of the point_ and the line_.

:site ref: http://mathworld.wolfram.com/Parallel.html
   """
   def __init__(self,line,point,**kws):
       self.line=line
       self.point=point
       Real._Line.__init__(self,*[line,point],**kws)
       self.drawlen=kws.get("drawlen",20)
       self.deps=[self.p1,self.p2]
       self.update()

   def parameters(self):
      direction=self.line.getDirection()
      normal =  self.point - self.point.dot(direction)*direction
      return normal, direction

   def _findSelf(self):
      normal,direction=self.parameters()
      drawlen=self.drawlen/2.
      self.p1.set(direction*drawlen+normal)
      self.p2.set(direction*-drawlen+normal)
      return True

class NearLine(Real._Line):
   """
:constructors:

     - Line(line1,line2)
     - NearLine(line1,line2)

:returns: The line_ connecting the nearest points of the given skew_ lines
:conditions: lines are not coincident, lines do not intersect
:else returns: None
:site ref: http://sun.uni-regensburg.de/idl-5.5/html/idl4/jhuapl.doc/vectors/v_skew.html
   """
   def __init__(self,line1,line2,**kws):
       self.line1=line1
       self.line2=line2
       Real._Line.__init__(self,*[line1,line2],**kws)
       self.lines=[self.line1,self.line2]
       self.drawlen=kws.get("drawlen",20)
       self.deps=[self.p1,self.p2]
       self.extend=kws.get("extend",True)
       self.update()


   def _findSelf(self):
      n1,d1=self.line1.parameters()
      n2,d2=self.line2.parameters()
      c=d1.cross(d2)
      o=n2-n1
      try:
         f1=determinant(array((o,d2,c)))/c.mag2
         f2=determinant(array((o,d1,c)))/c.mag2
         self.p1.set(d1*f1+n1)
         self.p2.set(d2*f2+n2)
         if self.p1 == self.p2:
             print self.__class__.__name__
             print "Lines intersect, Near line of zero length"
             return False
      except ZeroDivisionError:
         print self.__class__.__name__
         print "lines are parallel, near line undefined, returned False"
         return False 
      return True


   def setext(self):
      if self.Not_null:
         if self.show:
            for line in self.lines:
                if (self.line1.get_extension(self.p1) or 
                        self.line1.get_extension(self.p2)):
                    self.line1._redraw()
                if (self.line2.get_extension(self.p1) or 
                        self.line2.get_extension(self.p2)):
                    self.line2._redraw()

class Transversal(Real._Line):
   """
:constructors:

     - Line(line1,line2,point)
     - Transversal((line1,line2,point)

:returns:  the line_ through the given point_ and intersecting the given lines

:site ref: http://mathworld.wolfram.com/TransversalLine.html
   """
   def __init__(self,line1,line2,point,**kws):
       self.line1=line1
       self.line2=line2
       self.point=point
       Real._Line.__init__(self,*[line1,line2,point],**kws)
       self.deps=[self.p1,self.p2]
       self.pointsize=kws.get('pointsize',5)
       self.extend=kws.get("extend",True)
       self.lines=[self.line1,self.line2]
       self.ip1=Position3()
       self.ip2=Position3()
       self.update()

   def _findSelf(self):
      ip1=self.ip1
      ip2=self.ip2
      line1=self.line1
      line2=self.line2
      point=self.point
      
      u1= cross3(line1.p1,line1.p2,point)
      d1=u1.dot(line1.p1)
      u2= cross3(line2.p1,line2.p2,point)
      d2=u2.dot(line2.p1)
      dir=u1.cross(u2)
      try:
         ip1.set(vector(solve(
              array([u1,u2,dir]),
              array([d1,d2,0.])
               )))
      except LinAlgError:
         print self.__class__.__name__
         if u1 == u2:
             print "lines conincident, transversal undefined, returned False"
         else:
            print "point is on a given line, transversal undefined, returned False"
         return False
      
      ip2.set(dir + ip1)
      self.p1.toInterSection(ip1,ip2,line1.p1,line1.p2)
      self.p2.toInterSection(ip1,ip2,line2.p1,line2.p2)
      return True

   def setext(self):
       self.get_extension(self.point)
       for line in self.lines:
         if self.Not_null:
           if self.show:
              if line.show:
                 line.get_extension(self.p1)


class CirclePolar(Real._Line):
   """
:constructors:

     - Line(circle,point)
     - Line(circle,point,chord=True)
     - CirclePolar(circle,point)
     - CirclePolar(circle,point,chord=True)

:returns: the polar of the given point with the respect to the given circle.
          if keyword chord=True, the line p1 and p2 are the points on circle
          of line of tangency from point argument to circle

:condition: point and circle are coplanar
:else returns: None
:site ref: http://mathworld.wolfram.com/InversionPole.html
   """
   __opts__= Real._Line.__opts__[:] + ["chord"]

   def __init__(self,epoint,circle,**kws):
       self.circle=circle
       self.epoint=epoint
       Real._Line.__init__(self,*[circle,epoint],**kws)
       self.chord=kws.get('chord',True)
       self.drawlen=kws.get("drawlen",20)
       self.deps=[self.p1,self.p2]
       self.u=Position3()
       self.n=Position3()
       self.tp=Position3()
       self.update()

   def _findSelf(self):
      circle=self.circle
      point=self.epoint
      if DO_TESTS:
         t=point.onPlane(circle)
      else:
         t=True
      if t:
          drawlen=self.drawlen/2.
          self.p2.toInvertPoint(circle,self.epoint)
          self.u.set((self.p2-self.epoint).norm())
          d = self.u.dot(self.p2)
          direction = circle._u.cross(self.u).norm()
          try:
             self.n.set(vector(solve(
                           array([circle._u,self.u,direction]),
                              array([circle._d,d,0.]))))
          except LinAlgError:
             print self.__class__.__name__
             print "epoint at center, polar at infinity, returned False"
             return False
          self.p1.set(direction*drawlen+self.n)
          self.p2.set(direction*-drawlen+self.n)
          if self.chord:
             self.tp.set(self.circle._center)
             self.tp.toLine(self.p1,self.p2)
             dist=self.tp.distanceSquared(circle._center)
             if sqrt(dist) > circle._radius:
                 print self.__class__.__name__
                 print "no real point of intersection for circle and line returned False"
                 return False

             if not dist < EPS:
                 rad2=circle._radiusSquared
                 factor=sqrt(rad2-dist)/self.tp.distance(self.p1)
                 self.p1.set((self.p1-self.tp)*factor+self.tp)
                 self.p2.set(self.tp*2-self.p1)
             else:
                # line is through circle center
                 self.p1.set(direction*circle._radius+self.tp)
                 self.p2.set(direction*-circle._radius+self.tp)
          return True

      else:
         print self.__class__.__name__
         print "circle and point are not coplanar, no polar defined, returned False"
         return False

class ConicPolar(Real._Line):
   """
:constructors:

     - Line(conic,point)
     - Line(conic,point,chord=True)
     - ConicPolar(conic,point)
     - ConicPolar(conic,point,chord=True)

:returns:  the polar_ of the point_ with respect to the conic_, if chord=true then
           the line.p1 and line.p2 are the points of intersection of the polar_
           and the conic_

:conditions: if chord = True, then point exterior to conic_
:else returns: None
:site ref: http://mathworld.wolfram.com/Polar.html
   """
   __opts__= Element.__opts__[:] + ["chord"]

   def __init__(self,conic,point,**kws):
       self.conic=conic
       self.point=point
       Real._Line.__init__(self,*[conic,point],**kws)
       self.deps=[self.p1,self.p2]
       self.chord=kws.get('chord',True)
       if self.chord:
          self.seg=True
       self.tp=Position3()
       self.update()

   def _findSelf(self):
     if DO_TESTS:
        t = self.point.coPlanar(self.conic.p1,self.conic.p2,self.conic.p3)
     else:
        t = True
     if t:
        tp=self.tp
        equat=self.conic.getPlane()
        tp.toXY(self.point)
        C=self.conic.getC()
        L=matrixmultiply(self.tp,C)
        if absolute(
           matrixmultiply(L,transpose(tp))) < EPS: #pointis on conic
           try:
              L1=array([0,-L[2]/L[1],0])
           except ZeroDivisionError:
              print self.__class__.__name__
              print "ZDE"
              L1=array([-L[2]/L[0],0,0])
              return False
           self.p1.set(self.point)
           self.p2.fromXY(equat,L1)
        else:
           L= matrixmultiply(C*2,tp)
           tp1=array([0.,-L[2]/L[1],1.])
           tp2=array([-L[2]/L[0],0.,1.])
           cx = matrixmultiply(matrixmultiply(C,tp1),transpose(tp1))
           ax = matrixmultiply(matrixmultiply(C,tp2),transpose(tp2))
           bx =2*matrixmultiply(matrixmultiply(C,tp2),transpose(tp1))
           h= quadratic(ax,bx,cx)
           if h[0]:
              x1=tp1+tp2*h[0]
              x2=tp1+tp2*h[1]

           else:
              if self.chord:
                 x1=tp1+tp2
                 x2=tp1+tp2
                 print self.__class__.__name__
                 print "point interior to conic, no chord defined, returning False" 
                 return False
              else:
                 x1=tp1
                 x2=tp2
           x1z=array([x1[0]/x1[2],x1[1]/x1[2],0])
           x2z=array([x2[0]/x2[2],x2[1]/x2[2],0])
           self.p1.fromXY(equat,x1z)
           self.p2.fromXY(equat,x2z)
        return True
     else:
         print self.__class__.__name__
         print "point and conic not coplanar, polar undefined, returned False"
         return False


def  Line(*args,**kws):
   """
:constructors:

   - Line(point1,point2); calls: `class LinefromPoints`_
   - Line(plane,point); calls: `class PlanePerp`_
   - Line(plane1,plane2); calls: `class PlanesLine`_
   - Line(line,point); calls: `class ParaLine`_
   - Line(line1,line2); calls: `class NearLine`_
   - Line(line1,line2,point); calls: `class Transversal`_
   - Line(conic,point); calls: `class ConicPolar`_
   """
   __sigs__=[[vector,vector],[Real._Plane,vector],
             [Real._Plane,Real._Plane],[Real._Line,vector],[Real._Line,Real._Line],
             [Real._Line,Real._Line,vector],[Conic,vector],
             [vector,vector,vector],[vector,Real._Circle,]]
   t,i = method_get(__sigs__,args)
   if t is None:
      raise Argument_Type_Error(__sigs__,args)
   else:
      if i==0:
          return LineFromPoints(t[0],t[1],**kws)
      elif i==1:
          return PlanePerp(t[0],t[1],**kws)
      elif i==2:
          return PlanesLine(t[0],t[1],**kws)
      elif i==3:
          return ParaLine(t[0],t[1],**kws)
      elif i==4:
          return NearLine(t[0],t[1],**kws)
      elif i==5:
          return Transversal(t[0],t[1],t[2],**kws)
      elif i==6:
          return ConicPolar(t[0],t[1],**kws)
      elif i==7:
          return LinePerp(t[0],t[1],t[2],**kws)
      elif i==8:
          return CirclePolar(t[0],t[1],**kws)
      
      else:
          raise Argument_Type_Error(__sigs__,args)
