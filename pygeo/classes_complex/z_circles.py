


import pygeo.base.abstract_elements_complex as Complex
import pygeo.base.abstract_elements_usphere as USphere
from pygeo.base.abstract_elements_real import method_get
from pygeo.base.pygeoexceptions import Argument_Len_Error,Argument_Type_Error
from pygeo.base.cposition import CPosition


from pygeo.base.pygeomath import *
from pygeo.base.pygeoconstants import *
from pygeo.base.pygeoopts import *

import cmath

zCircleClasses = ['zUnitCircle','zCircleFromPoints', 'zCircumCircle', 'zOrthoCircle',
 'zOrthoCircle_Circum', 'zInverseCircle', 'u_to_zCircle',
 'zFundamentalCircle']

zCircleDef = [ 'zCircle']

__all__ = zCircleClasses + zCircleDef


#circles on the copmplex plane


class zUnitCircle(Complex._zCircle):
   """
:constructors: 

     - zCircle()
     - zUnitCircle()
 
:returns:  the origin center `complex circle_` of radius 1
:site ref: http://mathworld.wolfram.com/UnitCircle.html
   """
   def __init__(self,**kws):
      Complex._zCircle.__init__(self,**kws)
      self._center = CPosition()
      self._radius=complex(1,0)
      self.set_hermitian_from_radius()
      self.update()

class zCircleFromPoints(Complex._zCircle):
   """
:constructors: 

     - zCircle(zpoint1,zpoint2)
     - zCircleFromPoints(zpoint1,zpoint2)

:returns:  the `complex circle`_ that with the first zpoint as center
           and the second zpoint on the circumference_ and determining 
           the radius_
           
:condition: points distinct
:else returns: None
:site ref: http://www.ies.co.jp/math/java/comp/cplcircle/cplcircle.html
   """
   def __init__(self,center,circum,**kws):
      Complex._zCircle.__init__(self,*[center,circum],**kws)
      self._center = center
      self._cpoint = circum
      self.fixed=kws.get('fixed',False)
      if self.fixed:
         self.set_radius_from_cpoint()
      self.update()

   def _findSelf(self):
      if not self.fixed:
         self.set_radius_from_cpoint()
      self.set_hermitian_from_radius()
      
      return True
   
 

class zCircumCircle(Complex._zCircle):
   """
:constructors: 

   - zCircle(zpoint1,zpoint2,zpoint3)
   - zCircumCircle(zpoint1,zpoint2,zpoint3)

:returns:  the `complex circle`_ through the 3 point_ arguments
:condition: points distinct
:else returns: None
:site ref: http://mathworld.wolfram.com/Circumcircle.html
   """
   def __init__(self,z1,z2,z3,**kws):
      Complex._zCircle.__init__(self,*[z1,z2,z3],**kws)
      self.c1=z1
      self.c2=z2
      self.c3=z3
      self._cpoint=self.c3
      self.deps=[self._center]
      self.update()

   def _findSelf(self):
      vxs = self.c3 - self.c1
      vxt = self.c2 - self.c1
      try:
         v=vxs/vxt
      except ZeroDivisionError:
         print self.__class__.__name__
         print "refence points not distinct,returning false"
         return False
      d=mod2(v)
      try:
         c=(v-d)/(v-v.conjugate())
      except ZeroDivisionError:
         print self.__class__.__name__
         print "refence points colinear,returning false"
         return False
      self._center.set(vxt*c+self.c1)
      self._radiusSquared=self._center.distanceSquared(self._cpoint)
      self._radius=sqrt(self._radiusSquared)
      self.set_hermitian_from_radius()
      return True

class zOrthoCircle(Complex._zCircle):
   """
:constructors: 

     - zCircle(zcircle,zpoint)
     - zOrthoCircle(zcircle,zpoint)

:returns:  the `complex circle`_ orthogonal_ to the given `complex circle`_ , with
           given zpoint as center_
           
:site ref: http://mathworld.wolfram.com/OrthogonalCircles.html
   """
   def __init__(self,circle,center,**kws):
      Complex._zCircle.__init__(self,*[circle,center],**kws)
      self.circle=circle
      self._center=center
      self.deps=[self._cpoint]
      self.update()

   def _findSelf(self):
      self._radiusSquared=mod2(self.circle._center-self._center)-self.circle._radiusSquared
      self._radius=cmath.sqrt(self._radiusSquared)
      self.set_hermitian_from_radius()
      return True

class zOrthoCircle_Circum(Complex._zCircle):
   """
:constructors: 

     - zCircle(zcircle,zpoint1,zpoint2)
     - zOrthoCircle_Circum(zcircle,zpoint1,zpoint2)

:returns:  the `complex circle`_ orthogonal_ to the given `complex circle`_ , 
           and through the given zpoint arguments.

:condition: points distinct
:else returns: None
:site ref: http://mathworld.wolfram.com/OrthogonalCircles.html
   """
   def __init__(self,circle,z1,z2,**kws):
      Complex._zCircle.__init__(self,*[circle,z1,z2],**kws)
      self.circle=circle
      self.c1=c1=z1
      self.c2=c2=z2
      self._cpoint=c2
      self.deps=[self._center]
      self.update()

   def _findSelf(self):
      h=self.circle._hermitian
      c=self.c1.conjugate()
      ipoint= (h.C*c+h.D)/(h.A*c+h.B)*-1
      vxs = self.c1 - ipoint
      vxt = self.c2 - ipoint
      d1  = vxs.real*vxt.real+vxs.imag*vxt.imag
      d2  = mod2(vxs)
      d3  = mod2(vxt)
      den = 2.0*(d2*d3-d1*d1)
      try:
        f1=(d2-d1)/den*d3
      except ZeroDivisionError:
         print self.__class__.__name__
         print "cirumference points at not unique, returning False"
         return False
      try:
         f2=(d3-d1)/den*d2
      except:
         return False
      vxs *= f1
      vxt *= f2
      self._center.set(vxs+vxt+ ipoint)
      self.set_radius_from_cpoint()
      self.set_hermitian_from_radius()
      return True


class zInverseCircle(Complex._zCircle):
   """
:constructors: 

     - zCircle(zcircle1,zcircle2)
     - zCircle(zcircle1,zcircle2,alt=INVERSE)
     - zInverseCircle(zcircle1,zcircle2)

:returns:  the `complex circle`_ inverse to the second zcircle argument with respect
           to the first zcircle argument, optional 'alt=Inverse' keyword to disambiguate
           the argument signature from `class zFundamentalCircle`_

:site ref: http://whistleralley.com/inversion/inversion.htm
   """
   def __init__(self,base_circle,i_circle,**kws):
      Complex._zCircle.__init__(self,*[base_circle,i_circle],**kws)
      self.circle1=base_circle
      self.circle2=i_circle
      self.deps=[self._center,self._cpoint]
      self.update()

   def _findSelf(self):
       h0=self.circle1._hermitian
       h1=self.circle2._hermitian
       d0=h0.A*h1.D+h1.A*h0.D - h0.B*h1.C-h1.B*h0.C
       d1=h0.B*h0.C-h0.A*h0.D
       self._hermitian=Hermitian(h0*d0+h1*d1)
       self.set_radius_from_hermitian()
       return True

class u_to_zCircle(Complex._zCircle):
   """
:constructors: 

     - zCircle(ucircle); 
     - u_to_zCircle(ucircle); 

:returns: the `stereographic projection`_ of the given `spheric section`_ of the `Riemann sphere`_
          to the `complex plane`_

:site ref: http://mathworld.wolfram.com/CrossSection.html
   """
   def __init__(self,ucircle,**kws):
     Complex._zCircle.__init__(self,*[ucircle],**kws)
     self.rcircle=ucircle
     self.deps=[self._center,self._cpoint]
     self.update()

   def _findSelf(self):
       a=self.rcircle._u.x
       b=self.rcircle._u.y
       c=-self.rcircle._u.z
       d=self.rcircle._d
       A=(d-c)*.5
       B=(a-b*complex(0,1))*.5
       C=B.conjugate()
       D=(d+c)*.5
       self._hermitian=Hermitian([[A,B],[C,D]])
       self.set_radius_from_hermitian()
       return True

class zFundamentalCircle(Complex._zCircle):
   __opts__= USphere._uFreePosition.__opts__[:] + ["alt"]

   """
:constructors: 

   - zCircle(zcircle1,zcircle2,alt=FUNDAMENTAL)
   - zFundamentalCircle(zcircle1,zcircle2)

:returns:  the `complex circle`_ in by which the first zcircle argument is tranformed to 
           second zcircle argument by inversion_ . required 'alt=FUNDAMENTAL' keyword 
           when initializing with zCircle facotry function to 
           disambiguate the argument signature from `class zInverseCircle`_

:site ref: http://whistleralley.com/inversion/inversion.htm
   """
   def __init__(self,circle1,circle2,**kws):
      Complex._zCircle.__init__(self,*[circle1,circle2],**kws)
      self.circle1=circle1
      self.circle2=circle2
      self.deps=[self._center,self._cpoint]
      self.update()

   def _findSelf(self):
       h1=self.circle1._hermitian
       h2=self.circle2._hermitian
       d1=determinant(h1)
       d2=determinant(h2)
       y=-cmath.sqrt(d1/d2)
       self._hermitian=h1+h2*y
       self.set_radius_from_hermitian()
       return True


def zCircle(*args,**kws):
   """
:constructors: 

   - zCircle();                                          calls: `class zUnitCircle`_
   - zCircle(zpoint1,zpoint2);                           calls: `class zCircleFromPoints`_
   - zCircle(zpoint1,zpoint2,zpoint3);                   calls: `class zCircumCircle`_
   - zCircle(zcircle,zpoint);                            calls: `class zOrthoCircle`_
   - zCircle(zcircle,zpoint1,zpoint2);                   calls: `class zOrthoCircle_Circum`_
   - zCircle(zcircle1,zcircle2,<alt=INVERSE>);           calls: `class zInverseCircle`_
   - zCircle(ucircle);                                   calls: `class u_to_zCircle`_
   - zCircle(zcircle1,zcircle2,alt=FUNDAMENTAL);         calls: `class zFundamentalCircle`_
 
:returns: an instance of an object derived from the `_zCircle`_ abstract class, determined
          uniquely by reference to its arguments  

**Keyword arguments**: see `_zCircle`_
   """
   __sigs__=[[Complex._zPoint,Complex._zPoint],
             [Complex._zPoint,Complex._zPoint,Complex._zPoint],
             [Complex._zCircle,Complex._zPoint],
             [Complex._zCircle,Complex._zPoint,Complex._zPoint],
             [Complex._zCircle,Complex._zCircle],
             [USphere._uCircle],[]]
   t,i = method_get(__sigs__,args)
   if t is None:
      raise Argument_Type_Error(__sigs__,args)
   else:
      if i==0:
         return zCircleFromPoints(t[0],t[1],**kws)
      elif i==1:
         return zCircumCircle(t[0],t[1],t[2],**kws)
      elif i==2:
         return zOrthoCircle(t[0],t[1],**kws)
      elif i==3:
         return zOrthoCircle_Circum(t[0],t[1],t[2],**kws)
      elif i==4:
         alt=kws.get("alt")
         if alt:
            if alt==FUNDAMENTAL:
               return zFundamentalCircle(t[0],t[1],**kws)
            elif alt==INVERSE:
               return zInverseCircle(t[0],t[1],**kws)
            else:
               raise Argument_Type_Error(__sigs__,args)
         else:
               return zInverseCircle(t[0],t[1],**kws)
      elif i==5:
            return u_to_zCircle(t[0],**kws)
      elif i==6:
            return zUnitCircle(**kws)
      else:
         raise Argument_Type_Error(__sigs__,args)
