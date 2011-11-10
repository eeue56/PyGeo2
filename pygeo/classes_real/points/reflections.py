import pygeo.base.abstract_elements_real as Real
from pygeo.base.abstract_elements_real import method_get


from pygeo.base.pygeoexceptions import Argument_Type_Error
from pygeo.base.pygeoconstants import *
from pygeo.base.pygeomath import *
from pygeo.base.pygeoprimitives import *


from pygeo.base.pygeoopts import *



ReflectionnClasses = ['PlaneReflection', 'LineReflection']

ReflectionDef = ['Reflection']

__all__= ReflectionnClasses + ReflectionDef


class PlaneReflection(Real._Point):
   """
:constructors:

    - Reflection(point, line)
    - LineReflection(point,line)

:returns: the reflection_ of the given point_
          in the given plane_

:site ref: http://mathworld.wolfram.com/Reflection.html
   """
   def __init__(self,point,plane,**kws):
       self.plane=plane
       self.point=point
       Real._Point.__init__(self,*[point,plane],**kws)
       self.update()

   def _findSelf(self):
      self.set(self.point)
      return self.toPlaneReflection(self.plane._u,self.plane._d)

class LineReflection(Real._Point):
   """
:constructors:

    - Reflection(point, line)
    - LineReflection(point,line)

:returns: the reflection_ of the given point_
          in the given line_ and on the plane_ of the line_ and point_ .

:site ref: http://mathworld.wolfram.com/Reflection.html
   """
   def __init__(self,point,line,**kws):
       self.line=line
       self.point=point
       Real._Point.__init__(self,*[point,line],**kws)
       self.update()

   def _findSelf(self):
      line=self.line
      axis=line.p1-line.p2
      self.set(self.point-line.p1)
      self.set(self.rotate(PI,axis)+line.p1)
      return True



def Reflection(*args,**kws):
   """
:constructors:

   -  Reflection(point,line); calls:  `class LineReflection`_
   -  Reflection(point, plane); calls:  `class PlaneReflection`_

:returns:   A point_ instance determined as the `reflection`_ of a given
            point_ with respect to a given geometric object

:site ref: http://mathworld.wolfram.com/Reflection.html
   """
   __sigs__=[[vector, Real._Plane],[vector,Real._Line]]
   t,i=method_get(__sigs__,args)
   if t is  None:
     raise Argument_Type_Error(__sigs__,args)
   else:
     if i==0:
        return PlaneReflection(t[0],t[1],**kws)
     elif i==1:
        return LineReflection(t[0],t[1],**kws)
     else:
        raise Argument_Type_Error(__sigs__,args)
