import pygeo.base.abstract_elements_complex as Complex
import pygeo.base.abstract_elements_usphere as USphere
from pygeo.base.abstract_elements_real import method_get
from pygeo.base.pygeoexceptions import Argument_Type_Error

from pygeo.base.pygeomath import *
from pygeo.base.pygeoconstants import *
from pygeo.base.pygeoopts import *

import cmath


zPencilClasses = ['zCircles','u_to_zCirclePencil']

zPencilDef = ['zCirclePencil']


__all__ = zPencilClasses + zPencilDef

class zCircles(Complex._zCirclePencil):
   def __init__(self,circle1,circle2,**kws):
      Complex._zCirclePencil.__init__(self,*[circle1,circle2],**kws)
      self.circle1=circle1
      self.circle2=circle2
      self.update()

   def _findSelf(self):
      for i,circle  in enumerate(self.zcircles):
         circle._hermitian=self.circle1._hermitian*i+self.circle2._hermitian*(self.density-i)
         circle.set_radius_from_hermitian()
      return True

class u_to_zCirclePencil(Complex._zCirclePencil):
   def __init__(self,r_pencil,**kw):
      Complex._zCirclePencil.__init__(self,*[r_pencil],**kw)
      self.density=r_pencil.density
      self.r_pencil=r_pencil
      self.update()

   def _findSelf(self):
      for i,circle in enumerate(self.zcircles):
         c_center=self.r_pencil.circles[i]._center
         d=mag(c_center)
         try:
            u=norm(c_center)
         except ZeroDivisionError:
            u=vector(0,0,0)
         a=u.x
         b=u.y
         c=u.z
         A=(d-c)*.5
         B=(a-b*complex(0,1))*.5
         C=B.conjugate()
         D=(d+c)*.5
         circle._hermitian=Hermitian([[A,B],[C,D]])
         circle.set_radius_from_hermitian()
      return True

def zCirclePencil(*args,**kws):
     __sigs__=[[Complex._zCircle,Complex._zCircle],
               [USphere._uCirclePencil]]
     t,i = method_get(__sigs__,args)
     if t is None:
        raise Argument_Type_Error(__sigs__,args)
     else:
        if i==0:
           return zCircles(t[0],t[1],**kws)
        elif i==1:
           return u_to_zCirclePencil(t[0],**kws)
        else:
           raise Argument_Type_Error(__sigs__,args)
