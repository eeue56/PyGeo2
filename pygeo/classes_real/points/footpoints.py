import pygeo.base.abstract_elements_real as Real
from pygeo.base.abstract_elements_real import method_get


from pygeo.base.pygeoexceptions import Argument_Type_Error
from pygeo.base.pygeoconstants import *
from pygeo.base.pygeomath import *
from pygeo.base.pygeoprimitives import *


from pygeo.base.pygeoopts import *

FootClasses = ['PlaneFoot', 'LineFoot']

FootDef = ['Foot']

#Insensitives=['Freepoint']

__all__= FootClasses + FootDef


class PlaneFoot(Real._Point):
   """
:constructors:

    - Foot(point, plane)
    - PlaneFoot(point,plane)

:returns: the point_ on the given plane_ at the intersection_ with
          the perpendicular_ to it through the given point_. returns the point
          untransformed if point is on the plane

:site ref: http://mathworld.wolfram.com/PerpendicularFoot.html
   """
   def __init__(self,plane,point,**kws):
       self.plane=plane
       self.point=point
       Real._Point.__init__(self,*[plane,point],**kws)
       self.update()

   def _findSelf(self):
      self.set(self.point)
      return self.toPlane(self.plane)

class LineFoot(Real._Point):
   """
:constructors:

    - Foot(point, line)
    - LineFoot(point,line)

:returns: the point_ on the given line_ at the intersection_ with the
          perpendicular_ to it through the given point; returns the point
          untransformed if point is on the line

:site ref:  http://mathworld.wolfram.com/PerpendicularFoot.html
   """
   def __init__(self,line,point,**kws):
       self.line=line
       self.point=point
       Real._Point.__init__(self,*[line,point],**kws)
       self.update()

   def _findSelf(self):
      self.set(self.point)
      return self.toLine(self.line.p1,self.line.p2)

def Foot(*args,**kws):
   """
:constructors:

   - Foot(line, point): calls: `class LineFoot`_
   - Foot(plane,point); calls: `class PlaneFoot`_

:returns: A point at the foot_ of a given point_
          with respect to a given geometric object

:site ref: http://mathworld.wolfram.com/PerpendicularFoot.html
   """
   __sigs__ = [[Real._Plane,vector],[Real._Line,vector]]
   t,i = method_get(__sigs__,args)
   if t is None:
      raise Argument_Type_Error(__sigs__,args)
   else:
     if i == 0:
        return PlaneFoot(t[0],t[1],**kws)
     elif i == 1:
        return LineFoot(t[0],t[1],**kws)
     else:
        raise Argument_Type_Error(__sigs__,args)

