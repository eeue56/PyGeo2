import pygeo.base.abstract_elements_real as Real
from pygeo.base.abstract_elements_real import method_get


from pygeo.base.pygeoexceptions import Argument_Type_Error
from pygeo.base.pygeoconstants import *
from pygeo.base.pygeomath import *
from pygeo.base.pygeoprimitives import *

from pygeo.base.pygeoopts import *



TransformClasses = ['CentralProjection', 'ReflectTransform']

TransformDefs = ['Transform']


__all__= TransformClasses+TransformDefs
class CentralProjection(Real._Transformation):
   """
:constructors:

     - Transform(plane,point,[list of objects])
     - CentralProjection(plane,point,[list of objects])

:returns: the projection of the objects in the list from the given point to the
          given plane

:site ref: http://www.dai.ed.ac.uk/CVonline/LOCAL_COPIES/MOHR_TRIGGS/node9.html
   """
   def __init__(self,plane,point,elements,**kws):
      self.plane=plane
      self.point=point
      self.elements=[]
      for e in elements:
          for t in e:
              self.elements.append(t)
      args=[plane]+[point]+self.elements
      for element in elements:
          if not element in args:
              args.append(element)

      Real._Transformation.__init__(self,*args,**kws)
      self.update()

   def _getMat(self):
      pt=self.point.homogenous()
      equat=self.plane.equat()
      self.mat= multiply.outer(equat,pt)
      k=matrixmultiply(pt,equat)
      for i in range(4):
         self.mat[i,i]-=k
      return True


class ReflectTransform(Real._Transformation):
   """
:constructors:

     - Transform(plane,[list of objects])
     - ReflecttTransform(plane,[list of objects])

:returns:  the reflection_ of the objects in the given list in the given plane
:site ref: http://mathworld.wolfram.com/Reflection.html
   """
   def __init__(self,plane,elements,**kws):
      self.plane=plane
      self.elements=[]
      for e in elements:
          for t in e:
              self.elements.append(t)
      args=[plane]+self.elements
      for element in elements:
          if not element in args:
              args.append(element)

      Real._Transformation.__init__(self,*args,**kws)
      self.update()

   def _getMat(self):
      plane=self.plane
      x,y,z=plane._u.x,plane._u.y,plane._u.z

      self.mat=transpose(array([[1-2*x**2,-2*x*y,-2*x*z,2*x*self.plane._d],
                                [-2*x*y,1-2*y**2,-2*y*z,2*y*self.plane._d],
                                [-2*x*z,-2*y*z,1-2*z**2,2*z*self.plane._d],
                                [0.,0.,0.,1]]))
      return True




def  Transform(*args,**kws):
   """
:constructors:

   - Transform(plane,point,[list of objects]); calls: `class CentralProjection`_
   - Transform(plane,[list of objects]); calls: `class ReflectTransform`_

:returns: a defined transformation_ of a given list of objects
   """
   __sigs__=[[Real._Plane,vector,list],[Real._Plane,vector,tuple],
             [Real._Circle,vector,list],[Real._Circle,vector,tuple],
             [Real._Plane,list],[Real._Plane,tuple],
             [Real._Circle,list],[Real._Circle,tuple]]
   t,i = method_get(__sigs__,args)

   if t is None:
      raise Argument_Type_Error(__sigs__,args)
   else:
      if i==0 or i==1 or i==3:
         return CentralProjection(t[0],t[1],t[2],**kws)
      elif i==4 or i==5 or i==6 or i==7:
         return ReflectTransform(t[0],t[1],**kws)
      else:
         raise Argument_Type_Error(__sigs__,args)

