import pygeo.base.abstract_elements_real as Real

from pygeo.base.abstract_elements_real import method_get

from pygeo.base.position3 import Position3

from pygeo.base.pygeoexceptions import Argument_Type_Error
from pygeo.base.pygeoconstants import *
from pygeo.base.pygeomath import *
from pygeo.base.pygeoprimitives import *
from pygeo.classes_real.pointarrays import Conic

from pygeo.base.pygeoopts import *


InversionClasses = ['SpherePole', 'CirclePole', 'CircleInversion',
'SphereInversion','ConicPole']

InversionDef = ['Inversion']


__all__= InversionClasses +InversionDef



class SpherePole(Real._Point):
   """
:constructors:

    - Inversion(plane,sphere)
    - SpherePole(plane,sphere)

:returns: the pole_ of a given plane_ with respect to a given sphere_
:conditions: line not on sphere center
:else returns: point at [MAX,MAX,MAX]

:site ref: http://mathworld.wolfram.com/InversionPole.html
   """
   def __init__(self,plane,sphere,**kws):
       self.plane=plane
       self.sphere=sphere
       self.tmp=Real._Point()
       Real._Point.__init__(self,*[plane,sphere],**kws)
       self.update()

   def _findSelf(self):
      self.tmp.set(self.sphere._center)
      self.tmp.toPlane(self.plane)
      return self.toInvertPoint(self.sphere,self.tmp)

class CirclePole(Real._Point):
   """
:constructors:

    - Inversion(line,conic)
    - ConicPole(line,conic)

:returns: the pole_ of a given line with respect to a given coplanar_ conic_
:conditions: line and conic are coplanar_
:else returns: None

:site ref: http://mathworld.wolfram.com/InversionPole.html
   """
   def __init__(self,line,circle,**kws):
       self.line=line
       self.circle=circle
       self.tmp=Real._Point()
       Real._Point.__init__(self,*[line,circle],**kws)
       self.update()

   def _findSelf(self):
      self.tmp.set(self.circle._center)
      if DO_TESTS:
         t=(self.line.p1.onPlane(self.circle) and self.line.p2.onPlane(self.circle))
      else:
         t=True
      if t:
         self.tmp.toLine(self.line.p1,self.line.p2)
         return self.toInvertPoint(self.circle,self.tmp)
      else:
         print self.__class__
         print "circle and line not coplanar, no Pole defined, returned False"
         return False

class ConicPole(Real._Point):
   """
:constructors:

    - Inversion(line,conic)
    - ConicPole(line,conic)

:returns: the pole_ of a given line with respect to a given coplanar_ conic_
:conditions: line and conic are coplanar_
:else returns: None

:site ref: http://mathworld.wolfram.com/InversionPole.html
   """
   def __init__(self,line,conic,**kws):
      self.conic=conic
      self.line=line
      Real._Point.__init__(self,*[line,conic],**kws)
      self.update()

   def _findSelf(self):
      if DO_TESTS:
         t=(self.line.p1.coPlanar(self.conic.p1,self.conic.p2,self.conic.p3)
            and self.line.p2.coPlanar(self.conic.p1,self.conic.p2,self.conic.p3))
      else:
         t=True
      if t:
         C=self.conic.getC()
         h=self.line.homogenous_XY()
         equat=self.conic.getPlane()
         tp = matrixmultiply(inverse(C),h)
         tpz=array([tp[0]/tp[2],tp[1]/tp[2],0])
         return self.fromXY(equat,tpz)
      else:
         print self.__class__
         print "conic and line not coplanar, no Pole defined, returned False"
         return False


class CircleInversion(Real._Point):
   """
:constructors:

    - Inversion(point,circle)
    - CircleInversion(point, circle)

:returns: the `inverse point`_ of a given point_ with respect to a given coplanar_ circle_
:conditions: point and circle are coplanar_; point not circle center
:else returns: None ;  point at [MAX,MAX,MAX]

:site ref: http://mathworld.wolfram.com/InversePoints.html
   """
   def __init__(self,point,circle,**kws):
       self.point=point
       self.circle=circle
       Real._Point.__init__(self,*[point,circle],**kws)
       self.update()

   def _findSelf(self):
      if DO_TESTS:
         t=self.point.onPlane(self.circle)
      else:
         t=True
      if t:
         return self.toInvertPoint(self.circle,self.point)
      else:
         print self.__class__
         print "point not on plane of circle, inversion failed, False returned"
         return False

class SphereInversion(Real._Point):
   """
:constructors:

    - Inversion(point,sphere)
    - SphereInversion(point,sphere)

:returns: the point_ of inversion_ of a given point with respect
          to an `inversive sphere`_
:conditions: point not sphere center
:else returns: point at [MAX,MAX,MAX]

:site ref: http://mathworld.wolfram.com/InversionSphere.html
   """
   def __init__(self,point,sphere,**kws):
       self.point=point
       self.sphere=sphere
       Real._Point.__init__(self,*[point,sphere],**kws)
       self.update()

   def _findSelf(self):
       return self.toInvertPoint(self.sphere,self.point)

def Inversion(*args,**kws):
   """
:constructors:

  - Inversion(point,circle);  calls: `class CircleInversion`_
  - Inversion(point,sphere);  calls: `class SphereInversion`_
  - Inversion(line, circle);  calls: `class CirclePole`_
  - Inversion(plane, sphere); calls: `class SpherePole`_
  - Inversion(line, conic): calls: :calls: `class ConicPole`_

:returns: A point determined by a inversive_ transformation with respect to a
          given geometric object

:site ref: http://mathworld.wolfram.com/InversiveGeometry.html
   """
   __sigs__=[[Real._Plane,Real._Sphere],[Real._Circle,Real._Sphere],[Real._Line,Real._Circle],
            [Real._Line,Conic],[vector,Real._Circle],[vector,Real._Sphere]]
   t,i=method_get(__sigs__,args)
   if t is  None:
     raise Argument_Type_Error(__sigs__,args)
   else:
     if i==0 or i==1:
        return SpherePole(t[0],t[1],**kws)
     elif i==2:
        return CirclePole(t[0],t[1],**kws)
     elif i==2:
        return CirclePole(t[0],t[1],**kws)
     elif i==3:
        return ConicPole(t[0],t[1],**kws)
     elif i==4:
        return CircleInversion(t[0],t[1],**kws)
     elif i==5:
        return SphereInversion(t[0],t[1],**kws)
     else:
        raise Argument_Type_Error(__sigs__,args)
