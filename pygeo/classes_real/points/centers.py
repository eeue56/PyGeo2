import pygeo.base.abstract_elements_real as Real
from pygeo.base.abstract_elements_real import method_get


from pygeo.base.pygeoexceptions import Argument_Type_Error
from pygeo.base.pygeoconstants import *
from pygeo.base.pygeomath import *
from pygeo.base.pygeoprimitives import *


from pygeo.base.pygeoopts import *



CenterClasses = ['Centroid','OrthoCenter', 'InCenter',
'ExCenter', 'CircumCenter', 'TetraCenter']

CenterDef = ['Center']

__all__= CenterClasses +CenterDef





class Centroid(Real._Point):
   """
:constructors:

    - Center(point1, point2, point3, CENTROID):
    - Center(triangle. CENTROID):
    - Centroid(point1, point2, point3):
    - Centroid(triangle):

:conditions: points distinct
:else returns: the LineDivider_ with ratio=1/3
:returns: the `triangle centroid`_ (`center of mass`_)  of a triangle_
:site ref: http://mathworld.wolfram.com/TriangleCentroid.html
   """

   def __init__(self,p1,p2,p3,**kws):
       self.p1=p1
       self.p2=p2
       self.p3=p3
       Real._Point.__init__(self,*[p1,p2,p3],**kws)
       self.update()

   def _findSelf(self):
      return self.toCentroid(self.p1,self.p2,self.p3)

class OrthoCenter(Real._Point):
   """
:constructors:

    - Center(point1, point2, point3, ORTHO)
    - Center(triangle, ORTHO)
    - OrthoCenter(point1, point2, point3)
    - OrthoCenter(triangle)

:returns: the orthocenter_ (intersection of the three altitude_ s), of a triangle_
:conditions: points distinct
:else returns: undefined
:site ref: http://mathworld.wolfram.com/Orthocenter.html
   """
   def __init__(self,p1,p2,p3,**kws):
       self.p1=p1
       self.p2=p2
       self.p3=p3
       Real._Point.__init__(self,*[p1,p2,p3],**kws)
       self.update()

   def _findSelf(self):
      return self.toOrthoCenter(self.p1,self.p2,self.p3)

class InCenter(Real._Point):
   """
:constructors:

    - Center(point1, point2, point3,INCENTER)
    - Center(triangle, INCENTER)
    - InCenter(point1, point2, point3)
    - InCenter(triangle)

:returns: the incenter_, (center of the incircle_ ) of a triangle_
:conditions: points distinct
:else returns: undefined
:site ref: http://mathworld.wolfram.com/Incenter.html
   """
   def __init__(self,p1,p2,p3,**kws):
       self.p1=p1
       self.p2=p2
       self.p3=p3
       Real._Point.__init__(self,*[p1,p2,p3],**kws)
       self.update()

   def _findSelf(self):
      return self.toInCenter(self.p1,self.p2,self.p3)

class ExCenter(Real._Point):
   """
:constructors:

    - Center(point1, point2, point3, EXCENTER) #order siginificant
    - Center(triangle, ExCENTER)  #triangle vertex order significant
    - ExCenter(point1, point2, point3) #order siginificant
    - ExCenter(triangle) #triangle vertex order significant

:returns: an excenter_, (center_ of one of the 3 excircle_ s) of a triangle_
:conditions: points distinct
:else returns: undefined
:site ref: http://mathworld.wolfram.com/Excenter.html
   """
   def __init__(self,p1,p2,p3,**kws):
       self.p1=p1
       self.p2=p2
       self.p3=p3
       Real._Point.__init__(self,*[p1,p2,p3],**kws)
       self.update()

   def _findSelf(self):
      return self.toExCenter(self.p1,self.p2,self.p3)

class CircumCenter(Real._Point):
   """
:constructors:

    - Center(point1, point2, point3 )
    - Center(point1, point2, point3, CIRCUM)
    - Center(triangle)
    - Center(triangle, CIRCUM)
    - CircumCente(point1, point2, point3 )
    - CircumCenter(triangle)

:returns: the circumcenter_ (center_ of the circumcircle_) of a triangle_.
:conditions: points distinct
:else returns: undefined
:site ref: http://mathworld.wolfram.com/Circumcenter.html
   """
   def __init__(self,p1,p2,p3,**kws):
       self.p1=p1
       self.p2=p2
       self.p3=p3
       Real._Point.__init__(self,*[p1,p2,p3],**kws)
       self.update()

   def _findSelf(self):
      return self.toCircumCenter(self.p1,self.p2,self.p3)

class TetraCenter(Real._Point):
   """
:constructors:

     - Center(point1, point2, point3,point4)
     - TetraCenter(point1, point2, point3,point4)

:returns: the center_ of circumsphere_ of the (possibly irregular) tetrahedron_
          defined by four points
:conditions: points distinct
:else returns: undefined
:site ref: http://astronomy.swin.edu.au/~pbourke/geometry/spherefrom4/
   """

   def __init__(self,p1,p2,p3,p4,**kws):
       self.p1=p1
       self.p2=p2
       self.p3=p3
       self.p4=p4
       Real._Point.__init__(self,*[p1,p2,p3,p4],**kws)
       self.update()

   def _findSelf(self):
      return self.toSphereCenter(self.p1,self.p2,self.p3,self.p4)

def Center(*args,**kws):
   """
:constructors:

   - Center(point1, point2, point3); calls: `class CircumCenter`_
   - Center(triangle); calls: `class CircumCenter`_
   - Center(point1, point2, point3, CIRCUM); calls: `class CircumCenter`_
   - Center(triangle, CIRCUM); calls: `class CircumCenter`_
   - Center(point1, point2, point3, ORTHO); calls: `class OrthoCenter`_
   - Center(triangle, ORTHO); calls: `class OrthoCenter`_
   - Center(point1, point2, point3, CENTROID); calls:  `class Centroid`_
   - Center(triangle. CENTROID); calls:  `class Centroid`_
   - Center(point1, point2, point3, INCENTER); calls:  `class InCenter`_
   - Center(triangle, INCENTER); calls:  `class InCenter`_
   - Center(point1, point2, point3, EXCENTER); calls:  `class ExCenter`_
   - Center(triangle, ExCENTER) ; calls:  `class ExCenter`_
   - Center(point1, point2, point3,point4) calls: `class TetraCenter`_

:returns: a point_  instance determined as a geometric center_ in reference to
          its arguments

:site ref:  http://www.geocities.com/kiranisingh/center.html
   """
   __sigs__ = [[vector, vector, vector],[Real._Triangle],
                 [vector, vector, vector,float],[Real._Triangle,float],
                 [vector, vector, vector, vector]]


   t,i = method_get(__sigs__,args)
   if t is None:
      raise Argument_Type_Error(__sigs__,args)
   else:
      if i==0:
         return CircumCenter(t[0],t[1],t[2],**kws)
      elif i ==1:
         return CircumCenter(t[0].p1,t[0].p2,t[0].p3,**kws)
      elif i==2:
         if t[3] ==1:
           return OrthoCenter(t[0],t[1],t[2],**kws)
         elif t[3]==2:
           return InCenter(t[0],t[1],t[2],**kws)
         elif t[3] ==3:
           return ExCenter(t[0],t[1],t[2],**kws)
         elif t[3] ==4:
           return CircumCenter(t[0],t[1],t[2],**kws)
         elif t[3] ==5:
           return Centroid(t[0],t[1],t[2],**kws)
         else:
            raise Argument_Type_Error(__sigs__,args)
      elif i==3:
         if t[1] ==1:
           return OrthoCenter(t[0].p1,t[0].p2,t[0].p3,**kws)
         elif t[1]==2:
           return InCenter(t[0].p1,t[0].p2,t[0].p3,**kws)
         elif t[1] ==3:
           return ExCenter(t[0].p1,t[0].p2,t[0].p3,**kws)
         elif t[1] ==4:
           return CircumCenter(t[0].p1,t[0].p2,t[0].p3,**kws)
         elif t[1] ==5:
            return Centroid(t[0].p1,t[0].p2,t[0].p3,**kws)
         else:
            raise Argument_Type_Error(__sigs__,args)
      elif i==4:
         return TetraCenter(t[0],t[1],t[2],t[3],**kws)
      else:
         raise Argument_Type_Error(__sigs__,args)
