
import pygeo.base.abstract_elements_real as Real
from pygeo.base.abstract_elements_real import method_get


from pygeo.base.pygeoexceptions import Argument_Type_Error
from pygeo.base.pygeoconstants import *
from pygeo.base.pygeomath import *
from pygeo.base.element import Element


from pygeo.base.pygeoopts import *

SliderClasses = [ 'LineSlider', 'PlaneSlider',
'CircleSlider', 'SphereSlider']

SliderDef = ['Slider']

__all__= SliderClasses + SliderDef



class LineSlider(Real._FreePosition):
   """
:constructors:

     - Slider(line, <ratio = numeric> )
     - LineSlider(line, <ratio = numeric> )

:returns: a point on the given line which can be picked, but with movement constrained to
          the line; initial position determined by the 'ratio' keyword. See LineDivider_

:site ref:  http://mathworld.wolfram.com/Line.html
   """
   __opts__= Real._FreePosition.__opts__[:] + ["ratio"]

   def __init__(self,line,**kws):
      self.line=line
      self.t=kws.get('ratio',.5)
      Real._FreePosition.__init__(self,*[line],**kws)
      self.extend=kws.get("extend",True)
      self.lines=[line]
      self.update()

   def init(self):
      self.toInterpolated(self.line.p1,self.line.p2,self.t)
      Element.init(self)

   def setext(self):
        self.line.get_extension(self)
        self.line._redraw()

   def _findSelf(self):
      self.toLine(self.line.p1,self.line.p2)
      self.line._redraw()
      return True

   def reset(self):
      self.init()
      Real._Point.update(self)


class PlaneSlider(Real._FreePosition):
   """
:constructors:

     - Slider(plane, <[numeric,numeric,numeric]>)
     - PlaneSlider(plane, <[numeric,numeric,numeric]>)

:returns: a pickable point, constrained to the plane argument, with initial position
          determined as the foot of the plane from the given x,y,z position. See PlaneFoot_

:site ref:  http://mathworld.wolfram.com/Plane.html
   """
   def __init__(self,plane,*args,**kws):
       self.plane=plane
       args=[plane]+list(args)
       Real._FreePosition.__init__(self,*args,**kws)
       self.update()

   def _findSelf(self):
      return self.toPlane(self.plane)



class CircleSlider(Real._FreePosition):
   """
:constructors:

    - Slider(circle, <angle = numeric>)
    - CircleSlider(circle, <angle = numeric>)

:returns: a point on the given circle which can be picked, with movement constrained to
          the circle, with initial potion determined by the 'angle' keyword. See CircumPoint_


:site ref:  http://mathworld.wolfram.com/Circumference.html
   """
   __opts__= Real._FreePosition.__opts__[:] + ["angle"]

   def __init__(self,circle,**kws):
       self.circle=circle
       self.angle=kws.get('angle',PI)
       Real._FreePosition.__init__(self,*[circle],**kws)
       self.update()

   def _findSelf(self):
      return self.toCircle(self.circle)

   def init(self):
      self.set(self.circle._cpoint)
      self.toCircumPoint(self.circle,self.angle)
      Element.init(self)

   def reset(self):
      self.init()
      Real._Point.update(self)

class SphereSlider(Real._FreePosition):
   """
:constructors:

    - Slider(sphere,<theta= numeric, phi = numeric>)
    - SphereSlider(sphere,<theta= numeric, phi = numeric>)

:returns: a point on the given sphere which can be picked, with movement constrained to
          the sphere, with initial potion determined by the 'phi and 'theta'' keywords.

:site ref: http://mathworld.wolfram.com/Sphere.html
   """
   __opts__= Real._FreePosition.__opts__[:] + ["theta","phi"]

   def __init__(self,sphere,**kws):
       self.sphere=sphere
       self.theta=kws.get('theta',PI)
       self.phi=kws.get('phi',PI)
       Real._FreePosition.__init__(self,*[sphere],**kws)
       self.update()

   def _findSelf(self):
      return self.toSphere(self.sphere)

   def reset(self):
      self.init()
      Real._Point.update(self)

   def init(self):
      x=sin(self.theta)*cos(self.phi)
      y=sin(self.theta)*sin(self.phi)
      z=cos(self.theta)
      self.set(vector(x,y,z)*self.sphere._radius+self.sphere._center)
      Element.init(self)

def  Slider(*args,**kws):
   """
:constructors:

   - Slider(line, <ratio = numeric> ); calls: `class LineSlider`_
   - Slider(plane, <[numeric,numeric,numeric]>); calls: `class PlaneSlider`_
   - Slider(circle, <angle = numeric>); calls: `class CircleSlider`_
   - Slider(sphere,<theta= numeric, phi = numeric>); calls: `class SphereSlider`_

:returns: A point_ that is pickable, with movement constrained with reference
          to a given geometric object
   """
   __sigs__ = [[Real._Line],[Real._Plane],
               [Real._Plane,float,float,float],[Real._Circle,float,float,float],
               [Real._Plane,list],[Real._Plane,tuple],
               [Real._Circle,list],[Real._Circle,tuple],
               [Real._Circle],[Real._Sphere]]
   t,i = method_get(__sigs__,args)
   if t is None:
      raise Argument_Type_Error(__sigs__,args)
   else:
     if i == 0:
        return LineSlider(t[0],**kws)
     elif i==1:
        return PlaneSlider(t[0],**kws)
     elif i==2 or i==3:
        return PlaneSlider(t[0],t[1],t[2],t[3],**kws)
     elif i==4 or i==5 or i==6 or i==7:
        return PlaneSlider(t[0],t[1][0],t[1][1],t[1][1],**kws)
     elif i==8:
        return CircleSlider(t[0],**kws)
     elif i==9:
        return SphereSlider(t[0],**kws)
     else:
         raise Argument_Type_Error(__sigs__,args)
