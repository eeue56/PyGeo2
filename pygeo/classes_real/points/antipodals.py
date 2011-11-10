import pygeo.base.abstract_elements_real as Real
from pygeo.base.abstract_elements_real import method_get


from pygeo.base.pygeoexceptions import Argument_Type_Error
from pygeo.base.pygeoconstants import *
from pygeo.base.pygeomath import *
from pygeo.base.pygeoprimitives import *


from pygeo.base.pygeoopts import *



AntiPodalClasses = ['CircleAntiPodal', 'SphereAntiPodal',
'SegPoint']

AntiPodalDef = ['AntiPodal']


__all__= AntiPodalClasses + AntiPodalDef

class CircleAntiPodal(Real._Point):
   """
:constructors:

    - AntiPodal(circle,point)
    - CircleAntiPodal(circle,point)

:returns: the point_ on hee diameter_ of the circle_ cut by the line of
          given point and the circle_ center, and opposite to the point
          of the diameter_ nearest the given point.
:conditions: point and circle are coplanar_; point not circle center
:else returns: None ;  None

:site ref: http://mathworld.wolfram.com/Diameter.html
   """
   def __init__(self,circle,point,**kws):
       self.circle=circle
       self.point=point
       Real._Point.__init__(self,*[circle,point],**kws)
       self.update()

   def _findSelf(self):
      if DO_TESTS:
         t=self.point.onPlane(self.circle)
      else:
         t=True
      if t:
         return self.toOpposite(self.circle,self.point)
      else:
         print self.__class__.__name__
         print "circle and point not coplanar, antipodal undefined, returned False"
         return False

class SphereAntiPodal(Real._Point):
   """
:constructors:

    - AntiPodal(sphere,point)
    - SphereAntiPodal(sphere,point)

:returns: the point_ on the diameter_ of the sphere_ cut by the line of
          given point and the sphere_ center, and opposite to the point
          of the diameter_ nearest the given point.
:conditions: point not sphere center
:else returns: None

:site ref: http://mathworld.wolfram.com/Diameter.html
   """
   def __init__(self,sphere,point,**kws):
       self.sphere=sphere
       self.point=point
       Real._Point.__init__(self,*[sphere,point],**kws)
       self.update()

   def _findSelf(self):
      return self.toOpposite(self.sphere,self.point)

class SegPoint(Real._Point):
   """
:constructors:

    - AntiPodal(line, point)
    - AntiPodal(line,seg=<BEGIN/END>)
    - SegPoint(line, point)
    - AntiPodal(line,seg=<BEGIN/END>

:returns: the endpoint_ of the `line segment`_ (the line_
          'p1' or 'p2' attributes) farthest from the given
          point.  returns line.p1, line.p2 respectively with
          use of keyword seg = BEGIN or seg = END.

:note:    a pygeo line can be treated as either infinite in length, or in
          this context, as the segment between its 'p1' and 'p2' attributes.

:site ref: http://mathworld.wolfram.com/LineSegment.html
   """
   __opts__= Real._Point.__opts__[:] + ["seg","opposite"]
   def __init__(self,line,**kws):
      self.line=line
      self.seg=kws.get('seg',BEGIN)
      self.opp=kws.get('opposite',None)
      Real._Point.__init__(self,*[line], **kws)
      self.update()

   def _findSelf(self):
      if self.opp:
         d1=self.line.p1.distance(self.opp)
         d2=self.line.p2.distance(self.opp)
         if d1 > d2:
            self.set(self.line.p1)
         else:
            self.set(self.line.p2)
      else:
         if self.seg == BEGIN:
            self.set(self.line.p1)
         else:
            self.set(self.line.p2)
      return True

def AntiPodal(*args,**kws):
   """
:constructors:

    - AntiPodal(circle,point); calls: `class CircleAntiPodal`_
    - AntiPodal(line,point); calls: `class Segpoint`_
    - AntiPodal(sphere,point); calls: `class SphereAntiPodal`_

:returns: A point_ instance determined as antipodal_ to a given point_ on a
          given geometric object

:site ref: http://mathworld.wolfram.com/AntipodalPoints.html
   """
   __sigs__=__sigs__=[[Real._Circle,vector],[Real._Sphere,vector],
                      [Real._Line,vector],[Real._Line]]
   t,i=method_get(__sigs__,args)
   if t is  None:
     raise Argument_Type_Error(__sigs__,args)
   else:
     if i==0:
        return CircleAntiPodal(t[0],t[1],**kws)
     elif i==1:
        return SphereAntiPodal(t[0],t[1],**kws)
     elif i==2:
        return SegPoint(t[0],t[1],**kws)
     elif i==3:
        return SegPoint(t[0],**kws)
     else:
        raise Argument_Type_Error(__sigs__,args)
