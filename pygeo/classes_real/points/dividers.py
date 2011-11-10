import pygeo.base.abstract_elements_real as Real
from pygeo.base.abstract_elements_real import method_get


from pygeo.base.pygeoexceptions import Argument_Type_Error
from pygeo.base.pygeoconstants import *
from pygeo.base.pygeomath import *
from pygeo.base.pygeoprimitives import *


from pygeo.base.pygeoopts import *

DividerClasses = ['LineDivider', 'LineCut', 'CrossPoint', 'Harmonic',
'CircumPoint']

DividerDef = ['Divider']


__all__= DividerClasses + DividerDef



class LineDivider(Real._Point):
   """
:constructors:

    - Divider(line, ratio=<numeric>)
    - LineDivider(line, ratio=<numeric>)

:returns: point_ of the given line_ dividing it so that the length of the segment
          from the lines 'p1' attribute is in the given ratio with
          respect to the total length of the `line segment`_ .

:site ref:  http://mathworld.wolfram.com/LineSegment.html
   """
   __opts__= Real._Point.__opts__[:] + ["ratio"]

   def __init__(self,line,**kws):
       self.line=line
       self.ratio=kws.get('ratio',.5)
       Real._Point.__init__(self,*[line],**kws)
       self.extend=kws.get("extend",True)
       self.lines=[self.line]
       self.update()

   def _findSelf(self):
      self.toInterpolated(self.line.p1,self.line.p2,self.ratio)
      return True


class LineCut(Real._Point):
   """
:constructors:

    - Divider(line, point1, point2)
    - Divider(line1,line2)
    - LineCut(line, point1, point2)
    - Divider(Line1,line2)

:returns: a point_ of the given line_ dividing it so that the length of the segment
          from the lines 'p1' attribute is equal to the distance between the 2 point
          arguments 

:site ref:  http://mathworld.wolfram.com/LineSegment.html
   """

   def __init__(self,line,p1,p2,**kws):
       self.line=line
       self.p1=p1
       self.p2=p2
       Real._Point.__init__(self,*[line,p1,p2],**kws)
       self.extend=kws.get("extend",True)
       self.lines=[self.line]
       self.update()

   def _findSelf(self):
      v=(self.line.p2-self.line.p1).norm()
      d=self.p1.distance(self.p2)
      self.set(v*d + self.line.p1)
      return True

class CrossPoint(Real._Point):
   """
:constructors:

    - Divider([p1_a,p1_b,p1_c,p1_d],[p1a,p2_a,p2_b,p2_c])
    - CrossPoint([p1_a,p1_b,p1_c,p1_d],[p1a,p2_a,p2_b,p2_c])

:returns: the 4th point_ on the line of the 3 collinear_ point_ arguments which determines
          a `cross ratio`_ equal ( equicross_ ) to that of the 4 collinear_ point arguments.
:conditions: 4 points collinear_ and 3 points collinear_
:else returns: None
:site ref:  http://mathworld.wolfram.com/Cross-Ratio.html
   """
   def __init__(self,list1,list2,**kws):
      self.p1=list1[0]
      self.p2=list1[1]
      self.p3=list1[2]
      self.p4=list1[3]
      self.p1a=list2[0]
      self.p2a=list2[1]
      self.p3a=list2[2]
      args=list1+list2
      Real._Point.__init__(self, *args,**kws)
      self.update()

   def _findSelf(self):
      if DO_TESTS:
         t= (self.p1.coLinear(self.p2,self.p3)
             and self.p1.coLinear(self.p3,self.p4)
             and self.p1a.coLinear(self.p2a,self.p3a))
      else:
         t=True
      if t:
         return self.toCrossPoint(self.p1,self.p2,self.p3,self.p4,self.p1a,self.p2a,self.p3a)
      else:
         print self.__class__.__name__
         print "reference or target points are not collinear, crosspoint undefined, returned False"
         return False

class Harmonic(Real._Point):
   """
:constructors:

    - Divider(point1, point2, point3)
    - Harmonic(point1, point2, point3)

:returns: the `harmonic conjugate`_ of point1 with respect to point2 and point3.
:condition: points collinear_
:else returns: None
:site ref:  http://mathworld.wolfram.com/HarmonicConjugate.html
   """
   def __init__(self,p1,p2,p3,**kws):
      self.p1=p1
      self.p2=p2
      self.p3=p3
      Real._Point.__init__(self,*[p1,p2,p3],**kws)
      self.update()

   def _findSelf(self):
      if DO_TESTS:
          t = self.p1.coLinear(self.p2,self.p3)
      else:
          t =True
      if t:
          self.toHarmonic(self.p1,self.p2,self.p3)
          return True
      else:

          print self.__class__.__name__
          print "points are not collinear, harmonic not defined, retured False"
          return False



class CircumPoint(Real._Point):
   """
:constructors:

    - Divider(circle, angle = PI/2)
    - CircumPoint(circle, angle = PI/2)

:returns: the point on the circle_ circumference_ rotated by 'angle' (in radian_ s) from
          the circle_ 'cpoint' attribute.

:site ref:  http://mathworld.wolfram.com/Circumference.html
   """
   __opts__= Real._Point.__opts__[:] + ["angle"]

   def __init__(self,circle,**kws):
      self.circle=circle
      self.angle=kws.get('angle',PI)
      Real._Point.__init__(self,*[circle],**kws)
      self.update()

   def _findSelf(self):
      self.set(self.circle._cpoint)
      return self.toCircumPoint(self.circle,self.angle)


def Divider(*args,**kws):
   """
:constructors:

    - Divider(line, ratio_ =.4); calls:  `class LineDivider`
    - Divider(line,point1, point2); calls: `class LineCut`_
    - Divider(line1,line2); calls: `class LineCut`_
    - Divider(p1_a,p1_b,p1_c,p1_d,p1a,p2_a,p2_b,p2_c); calls: class CrossPoint`_
    - Divider(point1, point2, point3);calls: `class Harmonic`_

:returns:   a point_ which divides a geometric object
   """
   __sigs__ = [[Real._Line],[Real._Line,float],[Real._Line,vector,vector],
               [Real._Line,Real._Line],
               [vector, vector,vector],
               [list,list],   
               [Real._Circle]]
   t,i = method_get(__sigs__,args)
   if t is None:
      raise Argument_Type_Error(__sigs__,args)
   else:
     if i == 0:
         return LineDivider(t[0],**kws)
     elif i == 1:
         return LineDivider(t[0],t[1],**kws)
     elif i == 2:
         return LineCut(t[0],t[1],t[2],**kws)
     elif i == 3:
         return LineCut(t[0],t[1].p1,t[1].p2,**kws)
     elif i == 4:
         return Harmonic(t[0],t[1],t[2],**kws)
     elif i == 5:
          if (len(t[0])==4 and len(t[1])==3):
              return CrossPoint(t[0],t[1],**kws)
     elif i == 6:
         return CircumPoint(t[0],**kws)
     else:
         raise Argument_Type_Error(__sigs__,args)
