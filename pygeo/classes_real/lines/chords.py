
import pygeo.base.abstract_elements_real as Real
from pygeo.base.abstract_elements_real import method_get

from pygeo.base.position3 import Position3

from pygeo.base.pygeoexceptions import Argument_Type_Error
#from LinearAlgebra import LinAlgError
from pygeo.base.pygeoconstants import *
from pygeo.base.pygeomath import *
from pygeo.base.pygeoprimitives import *

from pygeo.classes_real.pointarrays import Conic
from pygeo.base.pygeoopts import *




ChordClasses = ['CircleChord', 'SphereChord',
'BiChord','ConicChord']

ChordDef = ['Chord']


__all__= ChordClasses+ChordDef

class CircleChord(Real._Line):
   """
:constructors:

     - Chord(circle,line)
     - CircleChord(circle,line)

:returns: the secant_ line joining the points of intersection of the
          circle_ and line_ with the p1 and p2 attributes at the points
          of intersection

:conditions: circle_ and line_ are coplanar; circle and line intersection is real
:else returns: None; None
:site ref: http://mathworld.wolfram.com/Circle-LineIntersection.html
   """
   def __init__(self,circle,line,**kws):
       self.tp=Position3()
       self.circle=circle
       self.line=line
       Real._Line.__init__(self,*[circle,line],**kws)
       self.seg=True
       self.deps=[self.p1,self.p2]
       self.update()

   def _findSelf(self):
      if DO_TESTS:
         t=self.line.p1.onPlane(self.circle) and self.line.p2.onPlane(self.circle)
      else:
         t=True
      if t:
         self.tp.set(self.circle._center)
         if self.tp.toLine(self.line.p1,self.line.p2):
            d=self.tp.distanceSquared(self.circle._center)
            if sqrt(d) > self.circle._radius:
                print self.__class__.__name__
                print "no real point of intersection for circle and line returned False"
                return False

            if not d < EPS:
               r=self.circle._radiusSquared
               factor=sqrt(r-d)/self.tp.distance(self.line.p1)
               self.p1.set((self.line.p1-self.tp)*factor+self.tp)
               self.p2.set(self.tp*2-self.p1)
            else:
               # line is through circle center
               self.p1.set(self.line.getDirection()*self.circle._radius+self.tp)
               self.p2.set(self.line.getDirection()*-self.circle._radius+self.tp)
            return True
         else:
             print self.__class__.__name__
             print "line segment points not distinct, toLine opreation returned Flase"
             return False
      else:
         print self.__class__.__name__
         print "circle and line are not coplanar, no intersection chord defined, returned False"
         return False

class SphereChord(Real._Line):
   """
:constructors:

     - Chord(sphere,line)
     - SphereCord(sphere,line)

:returns:  the secant_ line joining the points of intersection of the
           sphere_ and line_ with the p1 and p2 attributes at the points
           of intersection
:condition: sphere_ and line_ intersection is real
:else returns: None
:site ref: http://mathworld.wolfram.com/Chord.html
   """
   def __init__(self,sphere,line,**kws):
       self.sphere=sphere
       self.line=line
       self.t=Real._Point()
       Real._Line.__init__(self,*[sphere,line],**kws)
       self.seg=True
       self.deps=[self.p1,self.p2]
       self.update()

   def _findSelf(self):
       line=self.line
       sphere=self.sphere
       self.t.set(sphere._center)
       self.t.toLine(line.p1,line.p2)
       self.t-=sphere._center
       t2=self.t.mag2
       r2 = sphere._radiusSquared
       if t2 > r2:
          self.t*=.5
          r1sqr=self.t.mag2
          d = 0.50*(1.0+(r2-t2)/t2)
          self.t*=d
          crad = sqrt(r2 - d**2*t2)
          self.p1.set(cross3(line.p1,line.p2,sphere._center).norm())
          self.p1*=crad
          self.p2.set(self.p1*-1)
          self.t+=sphere._center
          self.p1+=self.t
          self.p2+=self.t
       else:
         self.p1.set((line.p2-line.p1).norm())
         crad=sqrt(r2-t2)
         self.p1*=crad
         self.p2.set(self.p1*-1)
         self.t += sphere._center
         self.p1 += self.t
         self.p2 += self.t

       return True

 
class BiChord(Real._Line):
   """
:constructors:

     -  Chord(circle1,circle2)
     -  BiChord(circle1,circle2)

:returns:  the secant_ line joining the points of intersection_ of the circles,
           with the p1 and p2 attributes at the points of intersection
:conditions: the cirles are coplanar; the circles intersection is real
:else returns: None; None
:site ref: http://mathworld.wolfram.com/Circle-CircleIntersection.html
   """
   def __init__(self,circle1,circle2,**kws):
       self.circle1=circle1
       self.circle2=circle2
       Real._Line.__init__(self,*[circle1,circle2],**kws)
       self.seg=True
       self.deps=[self.p1,self.p2]
       self.update()

   def _findSelf(self):
      circle1=self.circle1
      circle2=self.circle2
      if DO_TESTS:
         t=(circle1._center.onPlane(circle2) and circle1._cpoint.onPlane(circle2))
      else:
         t=True
      if t:
         dcenters=circle1._center.distance(circle2._center)
         if dcenters < EPS:
            print self.__class__.__name__
            print "circles are concentric, no intersection defined, return False"
            return False
         try:
            angle=arccos((circle1._center.distanceSquared(circle2._center)+
                             circle1._radiusSquared-circle2._radiusSquared)/
                             (2*dcenters*circle1._radius))
         except ValueError:
            print self.__class__.__name__
            print "circles do not intersect in real points, returning False"
            return False
         self.p1.set(circle2._center)
         self.p1.toCircle(circle1)
         self.p2.set(self.p1)
         self.p1.toCircumPoint(self.circle1,angle)
         self.p2.toCircumPoint(self.circle1,-angle)
         return True
      else:
         print self.__class__.__name__
         print "circles are not coplanar, no intersection defined, returning false"
         return False


class ConicChord(Real._Line):
   """
:constructors:

     - Chord(sphere,line)
     - TangPlanes(conic,line)

:returns: the secant_ line joining the points of intersection of the
          conic_ and line_
:conditions: conic_ and line_ are coplanar; conic and line intersection is real
:else returns: None; None
   """
   def __init__(self,conic,line,**kws):
       self.conic=conic
       self.line=line
       self.pt=array([0.,0.,-1.,1.])
       Real._Line.__init__(self,*[self.conic,self.line],**kws)
       self.deps=[self.p1,self.p2]
       self.update()

   def __repr__(self):
      return self.__class__.__name__ + "(" + str(self.p1) +"," + str(self.p2) + ")"

   def _findSelf(self):
     equat=self.conic.getPlane()
     tp1= toXY(self.line.p1)
     tp2= toXY(self.line.p2)
     C=self.conic.getC()
     cx = matrixmultiply(matrixmultiply(C,tp1),transpose(tp1))
     ax = matrixmultiply(matrixmultiply(C,tp2),transpose(tp2))
     bx =2*matrixmultiply(matrixmultiply(C,tp2),transpose(tp1))
     h= quadratic(ax,bx,cx)
     if h[0]:
        x1=tp1+tp2*h[0]
        x2=tp1+tp2*h[1]
        x1z=array([x1[0]/x1[2],x1[1]/x1[2],0])
        x2z=array([x2[0]/x2[2],x2[1]/x2[2],0])
        self.p1.fromXY(equat,x1z)
        self.p2.fromXY(equat,x2z)
        return True
     else:
        print self.__class__.__name__
        print "No real intersections between conic and line, returning False"
        return False




def  Chord(*args,**kws):
   """
:constructors:

   - Chord(circle,line); calls: `class CircleChord`_
   - Chord(sphere,line); calls: `class SphereChord`_
   - Chord(circle1,circle2); calls: `class BiChord`_

:returns: An instance of an object derived from the `_Line`_ abstract class,
          representing a  line in space with its 'p1' nnd 'p2' attributes on
          a given circle_ or sphere_
   """
   __sigs__=[[Real._Circle,Real._Line],[Real._Sphere,Real._Line],
             [Real._Circle,Real._Circle],[Conic,Real._Line]]
   t,i = method_get(__sigs__,args)
   if t is None:
      raise Argument_Type_Error(__sigs__,args)
   else:
      if i==0:
         return CircleChord(t[0],t[1],**kws)
      elif i==1:
         return SphereChord(t[0],t[1],**kws)
      elif i==2:
         return BiChord(t[0],t[1],**kws)
      elif i==3:
         return ConicChord(t[0],t[1],**kws)

      else:
         raise Argument_Type_Error(__sigs__,args)
