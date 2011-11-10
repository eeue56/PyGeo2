
from pygeo.base.position3 import Position3
import pygeo.base.abstract_elements_complex as Complex
import pygeo.base.abstract_elements_usphere as USphere
from pygeo.base.abstract_elements_real import method_get
from pygeo.base.pygeoexceptions import Argument_Type_Error
from pygeo.base.pygeomath import *
from pygeo.base.pygeoconstants import *
from pygeo.base.element import Element
from pygeo.base.pygeoopts import *

uPointClasses = ['uPolarPoint', 'z_to_uPoint', 'uAntiPodal', 'uInversePoint',
 'uCirclingPoint', 'uSpiral', 'uSphereSlider', 'uCircleSlider']


uPointsDefs = ['uPoint','uSlider', 'uAniPoint']


__all__ = uPointClasses + uPointsDefs




class uPolarPoint(USphere._uPoint):
   """
:constructors: 

     - uPoint(<float>,<float>)  
     - uPoint(theta=float,phi=float)  
     - uPolarPoint(float,float)  
     - uPolarPoint(theta=float,phi=float)  
 
:returns: the point of the origin centered unit sphere at the given spherical 
          coordinates, in radians; with defaults PI/2; accepts named arguments "theta"
          and "phi"

:site ref: http://mathworld.wolfram.com/SphericalCoordinates.html
   """
   __opts__= USphere._uPoint.__opts__[:] + ["theta","phi"]

   def __init__(self,theta=PI/2,phi=PI/2,**kws):
      self.theta=theta
      self.phi=phi
      USphere._uPoint.__init__(self,**kws)
      self.update()

   def init(self):
     x=sin(self.theta)*cos(self.phi)
     y=sin(self.theta)*sin(self.phi)
     z=cos(self.theta)
     self.set(vector(x,y,z))
     self.initvector=Position3()
     self.initvector.set(self)
     Element.init(self)

   def _findSelf(self):
      return True


class z_to_uPoint(USphere._uPoint):
   """
:constructors: 

     - uPoint(zPoint) 
     - z_to_uPoint(zPoint) 
     
:returns: the stereographic image of the given point of the complex plane onto
          origin centered unit sphere.

:site ref: http://mathworld.wolfram.com/StereographicProjection.html
   """
   def __init__(self,zpoint,**kws):
      self.color = kws.get("color",RED)
      USphere._uPoint.__init__(self,*[zpoint],**kws)
      self.zpoint=zpoint
      self.update()

   def _findSelf(self):
      return self.zpoint.to_uSphere(self)

class uAntiPodal(USphere._uPoint):
   """
:constructors: 

     - uPoint(uPoint)  
     - uAntipodal(uPoint)  

:returns: the point of the origin centered unit sphere antipodal to the given uPoint.

:site ref: http://mathworld.wolfram.com/AntipodalPoints.html
   """
   def __init__(self,upoint,**kws):
      USphere._uPoint.__init__(self,*[upoint],**kws)
      self.upoint=upoint
      self.update()

   def _findSelf(self):
      self.set(self.upoint * -1)
      return True


class uInversePoint(USphere._uPoint):
   """
:constructors: 

     - Intersect(plane, line)  
     - PlaneLineIntersect(plane, line)  

:returns: the point of the origin centered unit sphere inverse to the given point with
          respect to the given circle on the sphere
          
:site ref: http://mathworld.wolfram.com/InversionCircle.html
   """
   def __init__(self,ucircle,upoint,**kws):
      USphere._uPoint.__init__(self,*[ucircle,upoint],**kws)
      self.ucircle=ucircle
      self.upoint=upoint
      self.update()

   def _findSelf(self):
      equat=self.ucircle.equat()
      m = self.upoint.dot(self.ucircle._u)
      d=self.ucircle._d*-1.
      factor=2*d*(m+d)/(dot(equat,equat)+2*d*m)
      try:
         c=vector(self.ucircle._u/self.ucircle._d)
         self.set((1-factor)*self.upoint+factor*c)
      except:
         self.set(vector(COMPLEX_MAX,COMPLEX_MAX,COMPLEX_MAX))
      return True

def uPoint(*args,**kws):
   """
:constructors: 

  - uPoint(<float>, <float>);  calls: `class uPolarPoint`_
  - uPoint(uPoint);  calls: `class uAntipodal`_
  - uPoint(zPoint); calls:`class z_to_uPoint`_
  - uPoint(uCircle,uPoint); calls:`class uInversePoint`_
  
:returns: A point of the origin centered 'unit sphere'_, as determined by its arguments

:site ref: http://mathworld.wolfram.com/UnitSphere.html
   """
   __sigs__=[[],[float],[float,float],
             [USphere._uPoint],
             [Complex._zPoint],
             [USphere._uCircle,USphere._uPoint]]
   t,i = method_get(__sigs__,args)
   if t is None:
      raise Argument_Type_Error(__sigs__,args)
   else:
      if i==0:
         return uPolarPoint(**kws)
      elif i==1:
         return uPolarPoint(t[0],**kws)
      elif i==2:
         return uPolarPoint(t[0],t[1],**kws)
      elif i==3:
         return uAntiPodal(t[0],**kws)
      elif i==4:
         return z_to_uPoint(t[0],**kws)
      elif i==5:
         return uInversePoint(t[0],t[1],**kws)
      else:
         raise Argument_Type_Error(__sigs__,args)


class uCirclingPoint(USphere._uPoint):
   """
:constructors: 

     - AniPoint(ucircle)  
     - uCirclingPoint(ucircle)

:returns: a point constrained to the move along the circumference_ of a `spheric section`_
          of the `Riemann sphere`_, at each update cycle, with the initial position
          determinable by the 'angle' and the spped inverse to the 'rate' keyword
          argument.

:site ref:  http://mathworld.wolfram.com/SphericalSpiral.html
   """
   __opts__= USphere._uFreePosition.__opts__[:] + ["rate","angle"]

   def __init__(self,ucircle,rate=36,angle=0,**kws):
     self.ucircle=ucircle
     self.rate=rate
     self.rad=2.*PI/self.rate
     self.delta=0
     USphere._rPoint.__init__(self,*[ucircle],**kws)
     self.update()

   def _findSelf(self):
      self.set(self.ucircle._cpoint)
      self.toCircumPoint(self.ucircle,self.delta)
      self.delta+=self.rad
      return True

   def init(self):
      self.set(self.ucircle._cpoint)
      Element.init(self)




class uSpiral(USphere._uPoint):
   """
:constructors: 

     - AniPoint(<theta=numeric>, <phi=numeric>, <rate=integer>)  
     - uSpiral(<theta=numeric>, <phi=numeric>, <rate=integer>)

:returns: a point constrained to the `Riemann sphere`_, which moves along the 
          course of a `spherical spiral`_ from the  north pole toward the 
          south pole at each update cycle, with initial position determinable 
          by the 'theta' and 'phi' keyword arguments, and the speed inverse 
          to the 'rate' keyword argument.

:site ref:  http://mathworld.wolfram.com/SphericalSpiral.html
   """
   __opts__= USphere._uFreePosition.__opts__[:] + ["theta","phi", "t_factor","p_factor","rate"]
   def __init__(self,**kws):
     self.rate=kws.get('rate',36)
     self.rad=PI/self.rate
     self.t_factor=kws.get('t_factor',1)
     self.p_factor=kws.get('p_factor',1)
     self.theta=kws.get('theta',0)
     self.phi=kws.get('phi',0)
     USphere._uPoint.__init__(self,**kws)
     self.update()

   def _findSelf(self):
      phi =self.phi*self.p_factor
      theta = self.theta*self.t_factor
      x=sin(theta)*cos(phi)
      y=sin(theta)*sin(phi)
      z=cos(theta)
      self.set(vector(x,y,z))
      self.theta+=self.rad
      self.phi+=self.rad
      return True

def uAniPoint(*args,**kws):
   """
:constructors: 

  - uAniPoint(<theta=numeric>, <phi=numeric>, <rate=integer>);  calls: `class uSpiral`_
  - uAniPoint(ucircle,<angle=nmeric>,<rate=integer> );  calls: `class uCirclingPoint`_
  
:returns: A point of the `Riemann sphere`_ that moves at each 
          update cycle, constrained as determined by its arguments.
   """
   __sigs__=[[],
             [USphere._uCircle]]
   t,i = method_get(__sigs__,args)
   if t is None:
      raise Argument_Type_Error(__sigs__,args)
   else:
      if i==0:
         return uSpiral(**kws)
      elif i==1:
         return uCirclingPoint(t[0],**kws)
      else:
         raise Argument_Type_Error(__sigs__,args)

#3d point which can be picked and moved  - with restraints
class uSphereSlider(USphere._uFreePosition):
   """
:constructors: 

     - uSlider(<float>,<float>)  
     - uSphereSlider(<float>,<float>)  
 
:returns: a point of the `Riemann sphere`_ that can be picked and moved
          constrained to the sphere and with initial position at the given 
          `spherical coordinates`_, in radians_ ; with defaults PI/2; accepts named 
          keyword arguments "theta" and "phi"

:site ref: http://mathworld.wolfram.com/SphericalCoordinates.html
   """
   __opts__= USphere._uFreePosition.__opts__[:] + ["theta","phi"]
   def __init__(self,**kws):
      self.theta=kws.get('theta',PI/2)
      self.phi=kws.get('phi',PI/2)
      USphere._uFreePosition.__init__(self,**kws)
      self.update()

   def _findSelf(self):
      try:
          factor=1.0/self.mag
          self.set(self*factor)
      except ZeroDivisionError:
          self.set(vector(0,0,1))
      return True

   def init(self):
     x=sin(self.theta)*cos(self.phi)
     y=sin(self.theta)*sin(self.phi)
     z=cos(self.theta)
     self.set(vector(x,y,z))
     Element.init(self)

class uCircleSlider(USphere._uFreePosition):
   """
:constructors: 

     - uSlider(ucircle,<float>)  
     - uCircleSlider(ucircle,<float>)

:returns: a point of the given `spheric section_` of the `Riemann sphere`_ that can
          be picked and moved constrained to the `spheric section_` , with its initial position
          on the circle dtermined by optinal float argument, in radians_ , 
          defaulted to PI..

:site ref: http://mathworld.wolfram.com/SphericSection.html
   """
   __opts__= USphere._uFreePosition.__opts__[:] + ["angle"]
   def __init__(self,ucircle,angle=PI,**kws):
     self.ucircle=ucircle
     self.angle=angle
     USphere._uFreePosition.__init__(self,*[ucircle],**kws)
     self.update()

   def init(self):
      self.set(self.ucircle._cpoint)
      self.toCircumPoint(self.ucircle,self.angle)
      Element.init(self)

   def _findSelf(self):
     self.toCircle(self.ucircle)
     return True

def uSlider(*args,**kws):
    """
:constructors: 

  - uSlider(<float>, <float);  calls: `class uSphereSlider`_
  - uSlider(uCircle,<float>);  calls: `class uCircleSlider`_
  
:returns: A point of the origin centered `Riemann sphere`_ that can be picked and moved,
          with initial position and constraints as determined by its arguments.
          
:site ref: http://mathworld.wolfram.com/UnitSphere.html
    """
    __sigs__=[[],[float],[float,float],
              [USphere._uCircle],[USphere._uCircle,float]]
    t,i = method_get(__sigs__,args)
    if t is None:
       raise Argument_Type_Error(__sigs__,args)
    else:
       if i==0:
          return uSphereSlider(**kws)
       elif i==1:
          return uSphereSlider(t[0],**kws)
       elif i==2:
          return uSphereSlider(t[0],t[1],**kws)
       elif i==3:
          return uCircleSlider(t[0],**kws)
       elif i==4:
          return uCircleSlider(t[0],t[1],**kws)

       else:
          raise Argument_Type_Error(__sigs__,args)


