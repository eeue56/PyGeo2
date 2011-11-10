import pygeo.base.abstract_elements_real as Real
from pygeo.base.abstract_elements_real import method_get


from pygeo.base.pygeoexceptions import Argument_Type_Error
from LinearAlgebra import LinAlgError
from pygeo.base.pygeoconstants import *
from pygeo.base.pygeomath import *
from pygeo.base.pygeoprimitives import *


from pygeo.base.pygeoopts import *


IntersectClasses = ['PlaneLineIntersect', 'LinesIntersect',
'PlanesIntersect']

IntersectDef = ['Intersect']

__all__= IntersectClasses + IntersectDef



class PlaneLineIntersect(Real._Point):
   """
:constructors:

     - Intersect(plane, line)
     - PlaneLineIntersect(plane, line)

:returns: the point_ of intersection_ of plane_ and line_ not on the plane_
:conditions: line not on the plane
:else returns: None

:site ref: http://mathworld.wolfram.com/Line-PlaneIntersection.html
   """
   def __init__(self,plane,line,**kws):
       self.plane=plane
       self.line=line
       Real._Point.__init__(self,*[plane,line],**kws)
       self.extend=kws.get("extend",True)
       self.lines=[self.line]
       self.update()

   def _findSelf(self):
      return self.toPlaneIntersection(self.plane,self.line.p1,self.line.p2)


class LinesIntersect(Real._Point):
   """
:constructors:

    - Intersect(line1, line2)
    - LinesIntersect(line1, line2)

:returns: the point_ of intersection_ of 2 coplanar_ line_ s.
          returns None if lines are skew_
:conditions: lines are coplanar_
:else returns: None

:site ref: http://mathworld.wolfram.com/Line-LineIntersection.html
   """
   def __init__(self,line1,line2,**kws):
       self.line1=line1
       self.line2=line2
       self.line=line1
       Real._Point.__init__(self,*[line1,line2],**kws)
       self.extend=kws.get("extend",True)
       self.lines=[self.line1,self.line2]
       self.update()

   def _findSelf(self):
      line1=self.line1
      line2=self.line2
      if self.toInterSection(line1.p1,line1.p2,line2.p1,line2.p2,
                                 test=DO_TESTS):
         return True
      else:
         print self.__class__.__name__
         print "lines are skew, no intersetion defined, returned False"
         return False


class PlanesIntersect(Real._Point):
   """
:constructors:

  - Intersect(plane1,plane2,plane3)
  - PlanesIntersect(plane1,plane2,plane3)

:returns: the point_ of intersection_ of 3 plane_.
:conditions: planes are distinct
:else returns: None

:site ref: http://astronomy.swin.edu.au/~pbourke/geometry/3planes/
   """
   def __init__(self,plane1,plane2,plane3,**kws):
       self.plane1=plane1
       self.plane2=plane2
       self.plane3=plane3
       Real._Point.__init__(self,*[plane1,plane2,plane3],**kws)
       self.update()

   def _findSelf(self):
 
     try:
         self.set(vector(solve(
            array([self.plane1._u,self.plane2._u,self.plane3._u]),
            array([self.plane1._d,self.plane2._d,self.plane3._d])
            )))
         return True
     except LinAlgError:
         print self.__class__
         print "planes are not distinct, no intersection found, returned False"
         return False

def Intersect(*args,**kws):
   """
:constructors:

  - Intersect(plane, line);  calls: `class PlaneLineIntersect`_
  - Intersect(line,line);  calls: `class LinesIntersect`_
  - Intersect(plane1,plane2,plane3); calls:`class PlanesIntersect`_

:returns: A point_ instance determined as an intersection_ of its arguments

:site ref: http://mathworld.wolfram.com/Intersection.html
   """
   __sigs__=[[Real._Plane,Real._Line],[Real._Circle,Real._Line],
             [Real._Line,Real._Line],
             [Real._Plane,Real._Plane,Real._Plane]]
   t,i = method_get(__sigs__,args)
   if t is None:
      raise Argument_Type_Error(__sigs__,args)
   else:
      if i==0 or i==1:
         return PlaneLineIntersect(t[0],t[1],**kws)
      elif i==2:
         return LinesIntersect(t[0],t[1],**kws)
      elif i==3:
         return PlanesIntersect(t[0],t[1],t[2],**kws)
      else:
         raise Argument_Type_Error(__sigs__,args)
