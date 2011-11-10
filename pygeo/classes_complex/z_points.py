
import pygeo.base.abstract_elements_complex as Complex
import pygeo.base.abstract_elements_usphere as USphere
from pygeo.base.abstract_elements_real import method_get
from pygeo.base.element import Element
from pygeo.base.pygeoexceptions import Argument_Len_Error,Argument_Type_Error

from pygeo.base.pygeomath import *
from pygeo.base.pygeoconstants import *
from pygeo.base.pygeoopts import *


import cmath


zPointClasses = [ 'zFixedPoint', 'zFreePoint', 'zPolarPoint', 'zOrthoPoint', 'zConjugate',
  'u_to_zPoint','zInversePoint', 'zPowerPoint', 'zRotation','z_uRotation', 'zCircumPoint',
 'zHarmonic', 'zCrossPoint','zCircleSlider', 'zSlidingPoint', 'zCirclingPoint','zRotatingPoint',
 'zLineSlider','mobPole','mobInversePole','mobFixed']

zPointDefs = ['zPoint', 'zSlider','zAniPoint']


__all__ = zPointClasses + zPointDefs


class zFixedPoint(Complex._zPoint):
   """
:constructors: 

     - zPoint(<float>,<float>)  
     - zPoint(complex)  
     - zFixedPoint(<float>,<float>)  
     - zFixedPoint(complex)  
 
:returns: a point on the complex plane. With 2 float arguments, the 1st is the real, 
          the second the imaginary element. Also accepts a complex number argument.  

:site ref: http://mathworld.wolfram.com/ComplexPlane.html
   """

   def __init__(self,*args,**kws):
      Complex._zPoint.__init__(self,*args,**kws)
      self.update()


class zPolarPoint(Complex._zPoint):
   """
:constructors: 

     - zPoint(angle=<float>,dist=<float>)  
     - zPolarPoint(angle=<float>,dist=<float>)  
 
:returns: a point on the complex plane expressed in `polar coordinates`_ , with 
          the angle keyword argument defaulting to PI and the dist keyword argument
          defaulting to 1.

:site ref: http://mathworld.wolfram.com/PolarRepresentation.html
   """

   def __init__(self,angle=PI,dist=1.0,**kw):
      Complex._zPoint.__init__(self,**kw)
      self.angle=angle
      self.dist=dist
      self.update()

   def _findSelf(self):
      self.set(math_E**complex(0,self.angle)*self.dist)
      return True



class zOrthoPoint(Complex._zPoint):
   """
:constructors: 

     - zPoint(zPoint,alt=ORTHO)  
     - zOrthoPoint(zPoint)  
 
:returns: the point of the complex plane orthogonal_ to the given complex point, 
          i.e. the point antipodal_ to it's `stereographic projection`_ onto the 
          'unit sphere`_.
          
:site ref: http://www.bbc.co.uk/dna/h2g2/A974397
   """

   __opts__= Complex._zPoint.__opts__[:] +['alt']
   def __init__(self,cpoint,**kws):
      Complex._zPoint.__init__(self,*[cpoint],**kws)
      self._cpoint=cpoint
      self.update()

   def _findSelf(self):
      self.set(-1./self._cpoint.conjugate())
      return True



class zConjugate(Complex._zPoint):
   """
:constructors: 

     - zPoint(zPoint)  
     - zPoint(zPoint,alt=CONJUGATE)  
     - zConjugate(zPoint)  
 
:returns: the complex conjugate of the given complex point. 

:site ref: http://mathworld.wolfram.com/ComplexConjugate.html
   """

   def __init__(self,cpoint,**kws):
      Complex._zPoint.__init__(self,*[cpoint],**kws)
      self._cpoint=cpoint
      self.update()

   def _findSelf(self):
      cpoint=self._cpoint
      self.real=cpoint.real
      self.imag=-cpoint.imag
      return True


class u_to_zPoint(Complex._zPoint):
   def __init__(self,upoint,**kws):
      Complex._zPoint.__init__(self,*[upoint],**kws)
      self.upoint=upoint
      self.update()

   def _findSelf(self):
       t,p=self.upoint.polar()
       try:
          self.set(1.0/tan(t/2.0)*(math_E**complex(0,p)))
       except ZeroDivisionError:
          print self.__class__.__name__
          print """zpoint at infinity, returned False"""
          return False
       return True

class zInversePoint(Complex._zPoint):
   """
:constructors: 

     - zPoint(zpoint,zcircle)  
     - zInversePoint(plane, line)  

:returns: the point of complex 'inverse point'_ to the given complex point with
          respect to the given circle
          
:site ref: http://mathworld.wolfram.com/InversePoints.html
   """

   def __init__(self,cpoint,circle,**kws):
      Complex._zPoint.__init__(self,*[cpoint,circle],**kws)
      self._cpoint=cpoint
      self.circle=circle
      self.update()

   def _findSelf(self):
       h=self.circle._hermitian
       c=self._cpoint.conjugate()
       self.set((h.C*c+h.D)/(h.A*c+h.B)*-1)
       return True

class zPowerPoint(Complex._zPoint):
   """
:constructors: 

     - zPoint(zcircle1,zcircle2)  
     - zPowerPoint(zcircle1,zcircle2)  

:returns: the point of intersection of the `radical axis`_ of the given 
          circles and the line of the circles' centers
:site ref: http://mathworld.wolfram.com/Circle-CircleIntersection.html
   """

   def __init__(self,circle1,circle2,**kws):
      Complex._zPoint.__init__(self,*[circle1,circle2],**kws)
      self.zCircle1=circle1
      self.zCircle2=circle2       
      self.update()

   def _findSelf(self):
      z0=self.zCircle1._center
      z1 =self.zCircle2._center
      v=z1-z0
      d2=mod2(v)
      d=sqrt(d2)
      r02=self.zCircle1._radiusSquared
      r12=self.zCircle2._radiusSquared
      a = (r02 - r12 + d2 ) / (2*d)
      self.set(z0 + a * v / d)
      return True

class zRotation(Complex._zPoint):
   """
:constructors: 

     - zPoint(zpoint,zpoint,<angle=PI>)  
     - zRotation(zpoint,zpoint,<angle=PI>)  

:returns: the point determined by `stereographic projection`_ of the rotation of 
          the second point argument, with the projection of the first point argument 
          as the rotation axis, by the given single.

:site ref: http://www.math.union.edu/~dpvc/math/4D/stereo-projection/welcome.html
   """

   __opts__= Complex._zPoint.__opts__[:] +['angle']
   def __init__(self,zcenter,cpoint,**kws):
      Complex._zPoint.__init__(self,*[cpoint,zcenter], **kws)
      self.angle=kws.get("angle",PI)
      self.c_point=cpoint
      self.z_center=zcenter
      self.update()

   def _findSelf(self):
      self.set(self.c_point)
      center=self.z_center.uVector()
      self.uRotate(center,self.angle)
      return True

class z_uRotation(Complex._zPoint):
   """
:constructors: 

     - zPoint(upoint,zpoint,<angle=PI>)  
     - z_uRotation(Upoint,zpoint,<angle=PI>)  

:returns: the point determined by `stereographic projection`_ of the rotation of 
          the second point argument, with the first point argument as the rotation
          axis, by the given single.

:site ref: http://www.math.union.edu/~dpvc/math/4D/stereo-projection/welcome.html
   """

   __opts__= Complex._zPoint.__opts__[:] +['angle']
   def __init__(self,ucenter,cpoint,**kws):
      Complex._zPoint.__init__(self,*[ucenter,cpoint], **kws)
      self.angle=kws.get("angle",PI)
      self.c_point=cpoint
      self.u_center=ucenter
      self.update()

   def _findSelf(self):
      self.set(self.c_point)
      self.uRotate(self.u_center,self.angle)
      return True

class zCircumPoint(Complex._zPoint):
   """
:constructors: 

     - zPoint(zcircle,<angle=PI>)  
     - zCircumPoint(zcircle,<angle=PI>)  

:returns: the point on the given circle rotated by the given angle (in radians)

:site ref: http://mathworld.wolfram.com/Circumference.html
   """

   __opts__= Complex._zPoint.__opts__[:] +['angle']
   def __init__(self,zcircle,**kws):
      self.zcircle=zcircle
      self.angle=kws.get("angle",0)
      Complex._zPoint.__init__(self,*[zcircle],**kws)
      self.update()

   def _findSelf(self):
      circle=self.zcircle
      self.set(circle._radius*(math_E**complex(0,self.angle))+circle._center)
      return True

      
      
class zHarmonic(Complex._zPoint):
   """
:constructors: 

     - zPoint(zpoint1,zpoint2,zpoint3)  
     - zHarmonic(zpoint1,zpoint2,zpoint3)  

:returns: the `harmonic conjugate`_ of the 3rd argument with the respect to the
          first 2 arguments
          
:site ref: http://mathworld.wolfram.com/HarmonicConjugate.html
   """

   def __init__(self,z1,z2,z3,**kws):
      Complex._zPoint.__init__(self,*[z1,z2,z3], **kws)
      self.c1= z1
      self.c2= z2
      self.c3= z3
      self.update()

   def _findSelf(self):
      t3 =(self.c2 + self.c3) * .5
      t2 = self.c2 -  t3
      t1 = self.c1 - t3
      d  = t1.real*t2.real+t1.imag*t2.imag
      m1 = mod2(t1)
      m2 = mod2(t2)
     
      v=t2*(2.0*d) - t1*m2
      try:
         self.set(v/m1+t3)
      except ZeroDivisionError:
          print self.__class__.__name__
          print "reference points noe distinct, harmonic undefined, returning False"
          return False
      return True

class zCrossPoint(Complex._zPoint):
   """
:constructors: 

     - zPoint([zpoint1,zpoint2,zpoint3,zpoint4],[zpoint1a,zpoint2a,zpoint3a])  
     - zCrossPoint([zpoint1,zpoint2,zpoint3,zpoint4],[zpoint1a,zpoint2a,zpoint3a],zpoint4)  

:returns: the Mobius transformation of the 4th point of the first point set, defined by the ordered 
          correspondance of the first 3 points in the first point set to the 3 points in the
          second point set

:site ref: http://s13a.math.aca.mmu.ac.uk/Geometry/M23Geom/XRatio/xratio.html
   """

   def __init__(self,c1,c2,**kws):
       args=c1+c2
       Complex._zPoint.__init__(self,*args,**kws)
       self.v=c1
       self.w=c2
       self.update()

   def moebius(self):
       p=self.v[0]
       q=self.v[1]
       r=self.v[2]
       p1=self.w[0]
       q1=self.w[1]
       r1=self.w[2]
       s=(p-r)/(q-r)
       s1=(p1-r1)/(q1-r1)
       a=s*p1-s1*q1
       b=p*q1*s1-p1*q*s
       c=s-s1
       d=p*s1-q*s
       return array([[a,b],[c,d]])

   def _findSelf(self):
       p = self.v[3]
       mat = matrixmultiply(self.moebius(),p.homogenous())
       self.toC(mat)
       return True
 
   def double_points(self):
       mat=self.moebius()
       a=mat[0][0]
       b=mat[0][1]
       c=mat[1][0]
       d=mat[1][1]
       return self.quadratic(a,b,c,d)

   def quadratic(a,b,c,d):
       try:
          h1=(a-d+N.sqrt(d-a**2-4*b*c))/(2*c)
       except ValueError:
          h1=None
       try:
          h2=(a-d-N.sqrt(d-a**2-4*b*c))/(2*c)
       except ValueError:
          h2=None
       return h1,h2

class mobPole(Complex._zPoint):

   def __init__(self,transform,**kws):
       Complex._zPoint.__init__(self,*[transform],**kws)
       self.mobius=transform
       self.update()

   def _findSelf(self):
       self.set(self.mobius._mobius.getPole())
       return True

class mobInversePole(Complex._zPoint):

   def __init__(self,transform,**kws):
       Complex._zPoint.__init__(self,*[transform],**kws)
       self.mobius=transform
       self.update()

   def _findSelf(self):
       self.set(self.mobius._mobius.getInversePole())
       return True


class mobFixed(Complex._zPoint):
   __opts__= Complex._zPoint.__opts__[:] + ["fixed"]
   def __init__(self,transform,**kws):
       Complex._zPoint.__init__(self,*[transform],**kws)
       self.mobius=transform
       self.fixed=kws.get('fixed',0)
       self.update()

   def _findSelf(self):
       evectors=self.mobius._mobius.getFixed()
       if self.fixed:
           try:
              self.set(evectors[1][0]/evectors[1][1])
           except ZeroDivisionError:
              print self.__class__.__name__
              print "fixed point at infinity, returning False"
              return False
       else:
           try:
              self.set(evectors[0][0]/evectors[0][1])
           except ZeroDivisionError:
              print self.__class__.__name__
              print "fixed point at infinity, returning False"
              return False
       return True

def zPoint(*args,**kws):
    """
:constructors: 

  - zPoint(<float>, <float>);  calls: `class zFixedPoint`_
  - zPoint(<complex>);  calls: `class zFixedPoint`_
  - zPoint(angle=<float>, dist=<float>);  calls: `class zPolarPoint`_
  - zPoint(zpoint,<alt= CONJUGATE>);  calls: `class zConjugate`_
  - zPoint(zpoint,alt=ORTHO);  calls: `class zOrthoPoint`_
  - zPoint(zpoint,zcircle);  calls: `class zInversePoint`_
  - zPoint(zcircle,zcircle); calls:`class zPowerPoint`_
  - zPoint(zpoint,zpoint,<float>); calls:`class zRotation`_
  - zPoint(zcircle,zcircle); calls:`class zPowerPoint`_
  
:returns: A point of the origin centered 'unit sphere'_, as determined by its arguments

:site ref: http://mathworld.wolfram.com/UnitSphere.html
    """   
    __sigs__=[[],[float,float],[complex],[float],
               [Complex._zPoint],
               [USphere._uPoint],[Complex._zPoint,Complex._zCircle],
               [Complex._zCircle,Complex._zCircle],
               [Complex._zPoint,Complex._zPoint],
               [USphere._uPoint,Complex._zPoint],
               [Complex._zCircle],
               [Complex._zPoint,Complex._zPoint,Complex._zPoint],
               [list,list]]

    t,i = method_get(__sigs__,args)
    if t is None:
       raise Argument_Type_Error(__sigs__,args)
    else:
       if i==0:
          if kws.get("angle"):
             return zPolarPoint(**kws)
          else:   
             return zFixedPoint(**kws)
       elif i==1:
          return zFixedPoint(t[0],t[1],**kws)
       elif i==2:
          return zFixedPoint(t[0],**kws)
       elif i==3:
          return zFixedPoint(t[0],0,**kws)
       elif i==4:
          alt=kws.get("alt")
          if alt:
             if alt==ORTHO:
                return zOrthoPoint(t[0],**kws)
             elif alt==CONJUGATE:
                return zConjugate(t[0],**kws)
             else:
                raise Argument_Type_Error(__sigs__,args)
          else:
             return zConjugate(t[0],**kws)
       elif i==5:
          return u_to_zPoint(t[0],**kws)
       elif i==6:
          return zInversePoint(t[0],t[1],**kws)
       elif i==7:
          return zPowerPoint(t[0],t[1],**kws)
       elif i==8:
          return zRotation(t[0],t[1],**kws)
       elif i==9:
          return z_uRotation(t[0],t[1],**kws)
       elif i==10:
          return zCircumPoint(t[0],**kws)
       elif i==11:
          return zHarmonic(t[0],t[1],t[2],**kws)
       elif i==12:
          return zCrossPoint(t[0],t[1],**kws)
       else:
          raise Argument_Type_Error(__sigs__,args)



class zFreePoint(Complex._zFreePosition):
   """
:constructors: 

  - zFreePoint(): 
  - zFreePoint(<numeric>, <numeric> ): 
  
:returns: a point_ defined by (real,imaginary) coordinates that can be picked and 
          moved freely on the `complex plane`_ 

:site ref: http://mathworld.wolfram.com/ComplexNumber.html
   """
   def __init__(self,*args,**kws):
      Complex._zFreePosition.__init__(self,*args,**kws)
      self.update()


class zCircleSlider(Complex._zFreePosition):
   """
:constructors: 

    - zSlider(zcircle, <angle = numeric>)  
    - zCircleSlider(zcircle, <angle = numeric>)  

:returns: a point_ on the given circle_ which can be picked, with movement constrained to
          the given circle_,of the `complex plane`_ with initial position determined 
          by the 'angle' keyword. 
  

:site ref:  http://mathworld.wolfram.com/Circumference.html
   """
   __opts__= Complex._zPoint.__opts__[:] + ["angle"]
   def __init__(self,zcircle,**kw):
      self.zcircle=zcircle
      self.angle=kw.get("angle",PI)*self.zcircle.a
      Complex._zFreePosition.__init__(self,*[zcircle],**kw)
      self.update()

   def _findSelf(self):
      circle=self.zcircle
      vt=self-circle._center
      len=mod(vt)
      if len:
         factor =  circle._radius/len
         c = vt*factor+circle._center
      else:
         c=complex(1,0)*circle._radius+circle._center
      self.real=c.real
      self.imag=c.imag
      return True

   def reset(self):
      self.init()
      Complex._zPoint.update(self)

   def init(self):
      circle=self.zcircle
      self.set(circle._radius*(math_E**complex(0,self.angle))+circle._center)
      Element.init(self)



class zLineSlider(Complex._zFreePosition):
   """
:constructors: 

     - Slider(zline, <ratio = numeric> )  
     - LineSlider(zline, <ratio = numeric> )  

:returns: a point_ on the given line_ of the `complex plane`_ which can be picked, 
          but with movement constrained to the line; initial position determined
          by the 'ratio' keyword. 

:site ref:  http://mathworld.wolfram.com/Line.html
   """
   __opts__= Complex._zPoint.__opts__[:] + ["ratio"]
   def __init__(self,zline,**kw):
      self.zline=zline
      self.ratio=kw.get("ratio",.5)
      Complex._zFreePosition.__init__(self,*[zline],**kw)
      self.update()

   def _findSelf(self):
       p1=self.zline.p1
       p2=self.zline.p2
       vxs = p2 - p1
       vxt = self -  p1
       try:
           factor= (
                  (vxt.real*vxs.real+vxt.imag*vxs.imag)
                  /
                  mod2(vxs)
                  )
       except ZeroDivisionError:
           print self.__class__.__name__
           print " points defining line segments are coincident. toLine returned False"
           return False
    
       self.set(vxs*factor+p1)
       return True

   def reset(self):
      self.init()
      Complex._zPoint.update(self)

   def init(self):
      self.set(self.zline.p1*(1.0-self.ratio)+self.zline.p2*self.ratio)
      Element.init(self)


def zSlider(*args,**kws):
   """
:constructors: 

   - zSlider(line, <ratio = numeric> ); calls: `class zLineSlider`_
   - zSlider(circle, <angle = numeric>); calls: `class zCircleSlider`_
  
:returns: A point_ that is pickable, with movement constrained with reference 
          to a given geometric object of the `complex plnae`_
   """

   __sigs__ = [[Complex._zCircle],[Complex._zLine]]
   t,i = method_get(__sigs__,args)
   if t is None:
      raise Argument_Type_Error(__sigs__,args)
   else:
      if i == 0:
         return zCircleSlider(t[0],**kws)
      elif i == 1:
         return zLineSlider(t[0],**kws)
      else:
         raise Argument_Type_Error(__sigs__,args)


# points of the complex plane that move on update cyles

class zSlidingPoint(Complex._zPoint):
   """
:constructors: 

    - zAniPoint(line, <rate=integer>,<ratio=numeric>)
    - zSlidingPoint(line, <rate=integer>,<ratio=numeric>)
    
 :returns: a point which moves along the given line_ , at a rate
           determined by the 'rate' keyword, and initial position as determined by
           the 'ratio' keyword. 

:site ref:  http://mathworld.wolfram.com/Line.html

   """

   __opts__= Complex._zPoint.__opts__[:] + ["rate"]

   def __init__(self,zline,**kws):
      self.zLine=zline
      Complex._zPoint.__init__(self,*[zline], **kws)
      self.rate=kws.get("rate",36)
      self.xdelta=1./self.rate
      self.delta=0
      self.update()

   def _findSelf(self):
      self.delta+=self.xdelta
      self.set(self.zLine.p1*(1.0-self.delta)+self.zLine.p2*self.delta)
      return True

   def init(self):
      self.set(self.zLine.p1)
      Element.init(self)

class zCirclingPoint(Complex._zPoint):
   """
:constructors: 

    - zAniPoint(circle,<rate=integer>,<angle=numeric>) 
    - zCirclingPoint(circle,<rate=integer>,<angle=numeric>)
    
 :returns: a point which moves around the circumference of the given circle, at a rate
           determined by the 'rate' keyword, and initial position as determined by
           the 'angle' keyword. 

   """
   __opts__= Complex._zPoint.__opts__[:] + ["rate","angle"]

   def __init__(self,zcircle,**kws):
      self.zcircle=zcircle
      Complex._zPoint.__init__(self,*[zcircle], **kws)
      self.rate=kws.get("rate",36)
      self.rad=2.*PI/self.rate
      self.angle=kws.get("angle",0)
      self.delta=0
      self.update()

   def _findSelf(self):
      circle=self.zcircle
      self.set(circle._radius*(math_E**complex(0,self.delta))+circle._center)
      self.delta+=self.rad
      return True

   def init(self):
      self.set(self.zcircle._s*self.zcircle._radius+self.zcircle._center)
      Element.init(self)

class zRotatingPoint(Complex._zPoint):
   """
:constructors: 

    - zAniPoint(zpoint1,zpoint2, <rate=integer>)
    - zRotatingPoint(zpoint1,zpoint2, <rate=integer>)
    
 :returns: the rotation of the second point_ argument induced by the rotation of the `unit sphere`_ ,
           with the `stereographic projection`_ of the first point argmuent as `axis of rotation`_ .

   """
   __opts__= Complex._zPoint.__opts__[:] + ["rate","angle"]

   def __init__(self,zcenter,cpoint,**kws):
      self.angle=kws.get("angle",0)
      self.c_point=cpoint
      self.z_center=zcenter
      Complex._zPoint.__init__(self,*[zcenter,cpoint], **kws)
      self.rate=kws.get("rate",36)
      self.rad=2.*PI/self.rate
      self.delta=0
      self.update()

   def _findSelf(self):
      self.set(self.c_point)
      center=self.z_center.uVector()
      self.uRotate(center,self.delta)
      self.delta+=self.rad
      return True

def zAniPoint(*args,**kws):
   """
:constructors: 


  - zAniPoint(zcircle,<rate=integer>,<angle=numeric>); calls `class zCirclingPoint`_
  - zAniPoint(zline, <rate=integer>,<ratio=numeric>); calls `class zSlidingPoint`_ 
  - zAniPoint(zpoint,zpoint,<rate=integer>); calls `class zRotatingPoint`_ 

:returns: a point which moves constrained to a given geometric object of the `complex plane`_
          at each display update cycle, with the initial position and rate of movement
          determinable by keyword argument.

   """

   __sigs__ = [[Complex._zCircle],[Complex._zLine],
                [Complex._zPoint,Complex._zPoint]]
   t,i = method_get(__sigs__,args)
   if t is None:
      raise Argument_Type_Error(__sigs__,args)
   else:
      if i == 0:
         return zCirclingPoint(t[0],**kws)
      elif i == 1:
         return zSlidingPoint(t[0],**kws)
      elif i == 2:
         return zRotatingPoint(t[0],t[1],**kws)
      else:
         raise Argument_Type_Error(__sigs__,args)

