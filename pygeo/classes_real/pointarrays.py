import pygeo.base.abstract_elements_real as Real
from pygeo.base.abstract_elements_real import method_get


from pygeo.base.position3 import Position3

from pygeo.base.pygeoexceptions import Argument_Type_Error
#from LinearAlgebra import LinAlgError
from pygeo.base.pygeoconstants import *
from pygeo.base.pygeomath import *
from pygeo.base.pygeoprimitives import *
from pygeo.base.pygeoopts import *



PointArrayClasses = [ 'PointPencil', 'CirclingPencil',
'CirclePoints','GrowthMeasure','Harmonics', 'Conic',
'ArrayIntersect','PlanePoints','CorrelationPoints', 'Bezier', 'PcCurve']

PointArrayDefs = ['PointArray', 'Curve']


__all__= PointArrayClasses+PointArrayDefs




class PointPencil(Real._PointArray):
   __opts__= Real._PointArray.__opts__[:] + ["seg"]

   """
:constructors:

     - PointArray(line)
     - SegmentPencil(line)

:returns: array of equidistnat points on the segment of a given line between
          the line's p1 and p2 attributes.

:site ref: http://mathworld.wolfram.com/LineSegmentRange.html
   """
   def __init__(self,line,**kws):
      self.line=line
      self.seg=kws.get('seg',False)
      Real._PointArray.__init__(self,*[line],**kws)
      self.update()

   def _findSelf(self):
      line =self.line
      p= line.getDirection()
      if (self.seg or self.line.seg):
         length=self.line.length()
         start=line.p1
      else:
         length=MAX*2
         start = (p*-MAX)+(line.p1+line.p2)/2
      steps=[length/float(self.density-1)*i for i in range(self.density)]
      for point,step in zip(self,steps):
         point.set(p*step+start)
      return True

class CirclingPencil(Real._PointArray):
   """
:constructors:

     - PointArray(line_array,line)
     - CirclingPencil(line_array,line)

:returns: array of points determined as the intersection of the given array of lines
          and the given line
:conditions: line and line array are coplanar
:else returns: None
:site ref: http://mathworld.wolfram.com/Pencil.html
   """
   def __init__(self,linearray,line,**kws):
      self.linearray=linearray
      self.line=line
      Real._PointArray.__init__(self,*[linearray,line],**kws)
      self.extend=kws.get("extend",True)
      self.density = self.linearray.density
      self.update()

   def _findSelf(self):
      if DO_TESTS:
         t = self.line.p1.coPlanar(self.line.p2,self.linearray.lines[0].p1,self.linearray.lines[0].p2)
      else:
        t =True
      if t :
         for point,line in zip(self,self.linearray):
            point.toInterSection(self.line.p1,self.line.p2,line.p1,line.p2)
         return True
      else:
         print self.__class__.__name__
         print "line and line array are not coplanar, points of intersection undefined,returned False"
         return False

   def setext(self):
   #   pass
      if self.Not_null:
         if self.show:
            for point,line in zip(self,self.linearray):
                 if line.show:
                      line.get_extension(point)
                      line._redraw()
                # if self.line.show:
                #      self.line.get_extension(point)
                #      line._redraw()
                #      self.line._redraw()



class CirclePoints(Real._PointArray):
   """
:constructors:

     - PointArray(circle)
     - CirclePoints(circle)

:returns: array of equidistant points on a given circle
:site ref: http://mathworld.wolfram.com/CirclePointPicking.html
   """
   def __init__(self,circle,**kws):
      self.circle=circle
      Real._PointArray.__init__(self,*[circle],**kws)
      t = arrayrange(0,2*PI,2*PI/self.density)
      self.c = transpose((0*t, sin(t), cos(t)))
      self.update()

   def _findSelf(self):
      for point,s in zip(self.points,self.c):
         t=s*self.circle._radius
         n=array([t[0],t[1],t[2],1])
         m=matrixmultiply(n,self.circle.rmatrix())
         point.to_3d(m)
      return True

class GrowthMeasure(Real._PointArray):
   """
:constructors:

     - PointArray(point1,point2,point3,point4)
     - GrowthMeasure(point1,point2,point3,point4)

:returns:  an array of points of the line of the given points with any 2 successive
           points having a cross ratio equal to that of point3 and point4 with respect
           to point1 and point2

:conditions: points are coplanar; points are distinct
:else returns: None; None
:site ref: http://mathworld.wolfram.com/Homographic.html
   """
   def __init__(self,M,N,a,b,**kws):
      self.a=a
      self.b=b
      self.M=M
      self.N=N
      Real._PointArray.__init__(self,*[M,N,a,b],**kws)
      self.update()

   def _findSelf(self):
      if DO_TESTS:
         t=self.M.coLinear(self.a,self.b) and self.N.coLinear(self.a,self.b)
      else:
         t= True
      if t :
         self.steps=self.density
         self.cd=self.M.distance(self.N)
         mt=self.multiplier()
         iter=self.__iter__()
         iter.next().set(self.a)
         iter.next().set(self.b)
         def step(seed):
            try:
               point=iter.next()
               ad=seed.distance(self.N)
               ac=seed.distance(self.M)
               if ad > self.cd:
                  ac=-ac
               try:
                   v= mt*ac/ad
                   point.set((self.M-self.N)/(1+v)+self.N)
               except ZeroDivisionError:
                   print self.__class__.__name__
                   print "coincident points causing zero division, returned False"
                   print "point set to double point 'M'"
                   v=0
                   point.set(self.M)
               step(point)
            except StopIteration:
               pass
         step(self.a)

         #self.points=self.tpoints
         return True
      else:
          print self.__class__.__name__
          print "points are not collinear, crossratio undefined, returning False"
          return False

   def multiplier(self):
      da=self.N.distance(self.a)
      ac=self.a.distance(self.M)
      bc=self.b.distance(self.M)
      db = self.N.distance(self.b)
      if da > self.cd:
         ac=-ac
      if db > self.cd:
         bc=-bc
      return (-da/ac)*(bc/-db)



class Harmonics(Real._PointArray):
   """
:constructors:

     -  PointArray(point_array,point1,point2)
     -  Harmonics(point_array,point1,point2)

:returns: array of points harmoinc to the given array, with respect to the given point arguments

:site ref: http://mathworld.wolfram.com/HarmonicConjugate.html
   """
   def __init__(self,pa,M,N,**kws):
      self.pa=pa
      self.M=M
      self.N=N
      Real._PointArray.__init__(self,*[pa,M,N],**kws)
      self.density=self.pa.density
      self.update()

   def _findSelf(self):
      for point,hpoint in zip(self,self.pa):
         point.toHarmonic(hpoint,self.M,self.N)
      return True


class Conic(Real._PointArray):
   """
:constructors:

     - PointArray(point1,point2,point3,point4,point5)
     - Conic(point1,point2,point3,point4,point5)

:returns: array of points on the conic determined by the 5 points
:conditions: points are coplanar; points are distinct, no 3 points are collinear
:else returns: None; None; undefined
:site ref: http://mathworld.wolfram.com/ConicSection.html
   """
   def __init__(self,p1,p2,p3,p4,p5,**kws):
      self.p1=p1
      self.p2=p2
      self.p3=p3
      self.p4=p4
      self.p5=p5
      self.m=Position3()
      self.a=Position3()
      self.t=Position3()
      self.c1=Position3()
      self.c2=Position3()
      self.c3=Position3()
      self.c4=Position3()
      self.c5=Position3()
      Real._PointArray.__init__(self,*[p1,p2,p3,p4,p5],**kws)
      self.i=[2*PI/self.density*i for i in range(self.density)]
      self.update()

   def _findSelf(self):
      p1=self.p1
      p2=self.p2
      p3=self.p3
      p4=self.p4
      p5=self.p5
      if DO_TESTS:
         t = (p1.coPlanar(p2,p3,p4) and p2.coPlanar(p3,p4,p5))
      else:
         t= True
      if t:
         if self.m.toInterSection(p1,p2,p3,p4):
            
            u=cross3(p1,p2,p3).norm()
            d=u.dot(p1)
            normal=u*d

            radius=p1.distance(p2)
            cpoint=(p2-p1).norm()*radius
            for point,rad in zip(self,self.i):
               p=p2 + cpoint.rotate(rad,u)
               self.a.toInterSection(p,p2,p3,p5,test=False)
               self.t.toInterSection(self.m,self.a,p1,p5,test=False)
               point.toInterSection(p,p2,self.t,p4,test=False)
            return True

         else:
            print self.__class__.__name__
            print "points are not distinct, conic undfined, returned False"
            return False
      else:
         print self.__class__.__name__
         print "points are not coPlanar, conic undefined, returned False"
         return False

   def getPlane(self):
      u= cross3(self.p1,self.p2,self.p3).norm()
      d=u.dot(self.p1)
      return array([u.x,u.y,u.z,-d])

   def getCenter(self):
      c=self.getC()
      fx= 2*c[0]
      fy= 2*c[1]

   def getC(self):
      
      self.c1.toXY(self.p1)
      self.c2.toXY(self.p2)
      self.c3.toXY(self.p3)
      self.c4.toXY(self.p4)
      self.c5.toXY(self.p5)
      c1=self.c1
      c2=self.c2
      c3=self.c3
      c4=self.c4
      c5=self.c5
      
      A=array([
      [c1.x**2,c1.x*c1.y,c1.y**2,c1.x,c1.y,1],
      [c2.x**2,c2.x*c2.y,c2.y**2,c2.x,c2.y,1],
      [c3.x**2,c3.x*c3.y,c3.y**2,c3.x,c3.y,1],
      [c4.x**2,c4.x*c4.y,c4.y**2,c4.x,c4.y,1],
      [c5.x**2,c5.x*c5.y,c5.y**2,c5.x,c5.y,1],
      [0,0,0,0,0,0]])
    #  svd=SVD(A)
    #  V = svd[2][5]
      evalues, evectors =  eigenvectors(A)
      V = evectors[5].real
      b2=V[1]/2.
      d2=V[3]/2.
      e2=V[4]/2
      C=array([[V[0],b2,d2],[b2,V[2],e2],[d2,e2,V[5]]])
      return C

class ArrayIntersect(Real._PointArray):
   """
:constructors:

     - PointArray(line_array1,line_array2)
     - ArrayIntersect(line_array1,line_array2)

:returns: array of points determined as the intersection of the given arrays of lines
:conditions: line arrays are coplanar
:else returns: None
:site ref: http://mathworld.wolfram.com/Pencil.html
   """
   def __init__(self,lp1,lp2,**kws):
      self.lp1=lp1
      self.lp2=lp2
      self.t=Position3()
      Real._PointArray.__init__(self,*[lp1,lp2],**kws)
      self.extend=kws.get("extend",False)
      self.density=min(lp1.density,lp2.density)
      self.update()

   def _findSelf(self):
      if DO_TESTS:
         t = self.lp1.lines[0].p1.coPlanar(self.lp1.lines[0].p2,
             self.lp2.lines[1].p2,self.lp2.lines[1].p2)
      else:
         t = True
      if t:
         for point,line1,line2 in zip(self,self.lp1,self.lp2):
            point.toInterSection(line1.p1,line1.p2,line2.p1,line2.p2)
         return True

      else:
         print self.__class__.__name__
         print "line arrays are not coplanar, points of intersections undefined, returned False"
         return False

   def setext(self):
       for point,line in zip(self,self.lp1):
          line.get_extension(point)
          line._redraw()
       for point,line in zip(self,self.lp2):
          line.get_extension(point)
          line._redraw()

class CorrelationPoints(Real._PointArray):
   """
:constructors:

     - PointArray(conic, line_array)
     - CorrelationPoints(conic, line_array)

:returns:  Array of poles of the lines of the line array with respect to the given conic
:conditions: line arrray and conic are coplanar
:else returns: undefined
:site ref: http://mathworld.wolfram.com/ProjectiveCorrelation.html
   """
   def __init__(self,conic,la,**kws):
      self.conic=conic
      self.line_array=la
      Real._PointArray.__init__(self,*[conic,la],**kws)
      self.h1=Position3()
      self.h2=Position3()
      self.tpz=Position3()
      self.density=self.line_array.density
      self.update()

   def _findSelf(self):
      if DO_TESTS:
         t = self.line_array.lines[0].p1.coPlanar(self.line_array.lines[0].p2,
             self.conic.p1,self.conic.p2)
      else:
         t = True
      if t:
         equat=self.conic.getPlane()
         Ci=inverse(self.conic.getC())
         for point,line in zip(self,self.line_array):
            self.h1.toXY(line.p1)
            self.h2.toXY(line.p2)
            h=self.h1.cross(self.h2)
            tp = matrixmultiply(Ci,h)
            self.tpz.set(vector(tp[0]/tp[2],tp[1]/tp[2],0))
            point.fromXY(equat,self.tpz)
         return True
      else:
         print self.__class__.__name__
         print "line array and conic are not coplanar, correlation points undefined,returned False"
         return False


class PlanePoints(Real._PointArray):
   """
:constructors:

     - PointArray(plane, line_array)
     - PlanePoints(plane, line_array)

:returns:  array of points of intersection of the lines of the line_array with the given plane
:conditions: line arrray not on plane
:else returns: undefined
:site ref: http://mathworld.wolfram.com/Line-PlaneIntersection.html
   """

   def __init__(self,plane,la,**kws):
      self.plane=plane
      self.line_array=la
      Real._PointArray.__init__(self,*[plane,la],**kws)
      self.density=self.line_array.density
      self.update()

   def _findSelf(self):
      if DO_TESTS:
         t = not (self.line_array.lines[0].p1.onPlane(self.plane) and self.line_array.lines[0].p2.onPlane(self.plane))
      else:
        t = True
      if t:
         for point,line in zip(self,self.line_array):
            point.toPlaneIntersection(self.plane,line.p1,line.p2)
         return True
      else:
         print self.__class__.__name__
         print "line array on plane, intersection points undefined,returned False"
         return False

def  PointArray(*args,**kws):
   """
:constructors:

   - PointArray(line); calls: `class SegmentPencil`_
   - PointArray(line_array,line); calls: `class CirclingPencil`_
   - PointArray(circle); calls: `class CirclePoints`_
   - PointArray(line_array1,line_array2); calls: `class ArrayIntersect`_
   - PointArray(point1,point2,point3); calls: `class Harmonics`_
   - PointArray(point1,point2,point3,point4); calls: `class GrowthMeasure`_
   - PointArray(point1,point2,point3,point4,point5); calls: `class Conic`_
   - PointArray(conic,linearray); calls: `class CorrelationPoints`_
   - PointArray(plane,linearray); calls: `class PlanePoints`_

:returns: An instance of an object derived from the `_Line`_ abstract class,
          representing an infinite line in space, or, in context, the line segment
          between the line 'p1' nnd 'p2' attributes.
   """
   __sigs__=[[Real._Line],[Real._LineArray,Real._Line],[Real._Circle],
             [vector,vector,vector,vector,vector],
             [Real._LineArray,Real._LineArray],[vector,vector,vector,vector],
             [Real._PointArray,vector,vector],[Conic,Real._LineArray],
             [Real._Plane,Real._LineArray]]
   t,i = method_get(__sigs__,args)
   if t is None:
      raise Argument_Type_Error(__sigs__,args)
   else:
      if i==0:
         return PointPencil(t[0],**kws)
      elif i==1:
         return CirclingPencil(t[0],t[1],**kws)
      elif i==2:
         return CirclePoints(t[0],**kws)
      elif i==3:
         return Conic(t[0],t[1],t[2],t[3],t[4],**kws)
      elif i==4:
         return ArrayIntersect(t[0],t[1],**kws)
      elif i==5:
         return GrowthMeasure(t[0],t[1],t[2],t[3],**kws)
      elif i==6:
         return Harmonics(t[0],t[1],t[2],**kws)
      elif i==7:
         return CorrelationPoints(t[0],t[1],**kws)
      elif i==8:
         return PlanePoints(t[0],t[1],**kws)
      else:
         raise Argument_Type_Error(__sigs__,args)



class Bezier(Real._PointArray):
   """
:constructors:

     - Curve([list of points])
     - BezierCurve([list of points])

:returns: the Bezier curve with the list of points as control points,
          point order significant
:site ref: http://www.moshplant.com/direct-or/bezier/
   """
   def __init__(self,inpoints,**kws):
      self.inpoints = inpoints
      Real._PointArray.__init__(self,*inpoints,**kws)
      coefs = self.getCoefs(len(self.inpoints)-1)
      bn = len(coefs)
      val=[]
      append=val.append
      for i in range (self.density+1):
         u=i/float(self.density)
         t =(1-u)
         for j in range(bn):
#           for k in range(3):
           cval = [coefs[j]*(t**(bn-j-1))*(u**j)]
           append(cval)
      self.U = reshape(array((val)),(self.density+1,bn))
      self.items =reshape(ones(3*len(self.inpoints),'d'),(len(self.inpoints),3))
      self.density=kws.get('density',25)
      self.color=kws.get('color',RED)
      self.linewidth=kws.get('linewidth',.3)
      self.drawpoints=kws.get("drawpoints",False)
      self.density+=1
      self.update()

   def getCoefs(self,fact):
      facts = []
      coefs = []
      nom=1
      f_append=facts.append
      c_append=coefs.append
      for i in range(fact):
         nom*=(i+1)
         f_append(nom)
      c_append(1.0)
      for  i in range(1,fact):
         c_append(float(facts[fact-1]/(facts[i-1]*facts[fact-1-i])))
      c_append(1.0)
      return coefs

   def _findSelf(self):
      for i,inpoint in enumerate(self.inpoints):
         self.items[i] = inpoint
      self.pos=[None]*self.density
      for i in range(self.density):
         r=matrixmultiply(
         transpose(self.items),
             self.U[i])
         if self.drawpoints:
            self.points[i].set(vector(r))
         if self.drawcurve:
            self.pos[i]=r
      return True

class PcCurve(Real._PointArray):
   """
:constructors:

     - Curve(point1,point2,point3,point4)
     - PcCurve(point1,point2,point3,point4)

:returns:  the cubic BSpline_ curve with point1 and point2 as end points and point3 and
           point4 as control points

:site ref: http://www.moshplant.com/direct-or/bezier/math.html
   """
   def __init__(self,p1,p2,p1u,p2u,**kws):
      self.p1=p1
      self.p2=p2
      self.p1u=p1u
      self.p2u=p2u
      self.M = array([[2.,-2.,1.,1.],[-3.,3.,-2.,-1.],[0.,0.,1.,0.],[1.,0.,0.,0.]],'d')
      Real._PointArray.__init__(self,*[p1,p2,p1u,p2u],**kws)
      self.update()

   def _findSelf(self):
      #self.points = []
      self.pos=[None]*self.density
      pu1=self.p1u-self.p1
      pu2=self.p2-self.p2u
      B=array((self.p1,self.p2,pu1,pu2),'d')
      for i in range(self.density):
         u=i/float(self.density)
         U = array((u**3,u**2,u,1),'d')
         m= matrixmultiply(U,self.M)
         r = matrixmultiply(m,B)
         #pt=Position3(r)
         if self.drawpoints:
             self.points[i].set(vector(r))
         self.pos[i]=r
      return True

def  Curve(*args,**kws):
   """
:constructors:

     - Curve(point1,point2,point3,point4)
     - PcCurve(point1,point2,point3,point4)

:returns:  the cubic BSpline_ curve with point1 and point2 as end points and point3 and
           point4 as control points

:site ref: http://www.moshplant.com/direct-or/bezier/math.html
   """
   __sigs__=[[list],[tuple],[vector,vector,vector,vector]]
   t,i = method_get(__sigs__,args)
   if t is None:
      raise Argument_Type_Error(__sigs__,args)
   else:
      if i==0 or i==1:
         return Bezier(t[0],drawcurve=True,**kws)
      elif i==2:
         return PcCurve(t[0],t[1],t[2],t[3],drawcurve=True,**kws)
      else:
         raise Argument_Type_Error(__sigs__,args)