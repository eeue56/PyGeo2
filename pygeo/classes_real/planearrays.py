
import pygeo.base.abstract_elements_real as Real

from pygeo.base.abstract_elements_real import method_get

from pygeo.base.pygeoexceptions import Argument_Type_Error
from pygeo.base.pygeoconstants import *
from pygeo.base.pygeomath import *
from pygeo.base.pygeoprimitives import *
from pygeo.base.pygeoopts import *

PlaneArrayClasses = ['PlanePencil']

PlaneArrayDefs = ['PlaneArray']

__all__= PlaneArrayClasses+PlaneArrayDefs

class PlanePencil(Real._PlaneArray):
   """
:constructors:

     - PlaneArray(line)

:returns:  the set of planes through the given line

:site ref: http://mathworld.wolfram.com/SheafofPlanes.html
   """
   def __init__(self,line,**kws):
      self.line=line
      Real._PlaneArray.__init__(self,*[line],**kws)
      self.v=PI/self.density
      self.update()

   def _findSelf(self):
      line=self.line
      dir=line.getDirection()
      st=(line.p2+line.p1)*.5
      lxy = hypot(st.x,st.y)
      if (lxy >= EPS):
          try:
             s=vector(-dir.y/lxy,dir.x/lxy,0.).norm()
          except ZeroDivisionError:
             print self.__class__.__name__
             print "line segment's points coincident, no array of planes defined, returned False"
             return False
      else:
            s=vector(1.,0.,0.)
      for i,plane  in enumerate(self.planes):

         rad=i*self.v
         r=s.rotate(rad,dir)+st
         u=cross3(line.p1,line.p2,r).norm()
         d=line.p1.dot(u)
         plane._u=u
         plane._d=d
         plane._s=s
         plane._v=s.cross(u).norm()

      return True


def  PlaneArray(*args,**kws):
   """
:constructors:

     - PlanePencil(list)
     - PlaneArray(list)

:returns:  the set of planes through the given line

:site ref: http://mathworld.wolfram.com/SheafofPlanes.html
   """
   __sigs__=[[Real._Line]]
   t,i = method_get(__sigs__,args)
   if t is None:
      raise Argument_Type_Error(__sigs__,args)
   else:
      if i==0:
         return PlanePencil(t[0],**kws)
      else:
         raise Argument_Type_Error(__sigs__,args)