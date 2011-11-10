
"""
   * 12/01/2001 - 17:18:39
   *
   * VPosition.py - PyGeo base analytics
   * Copyright (C) 2001 Arthur J. Siegel
   * ajs@ix.netcom.com
   * pygeo.sourceforge.net
   *
   * This program is free software; you can redistribute it and/or
   * modify it under the terms of the GNU General Public License
   * as published by the Free Software Foundation; either version 2
   * of the License, or any later version.
   *
   * This program is distributed in the hope that it will be useful,
   * but WITHOUT ANY WARRANTY; without even the implied warranty of
   * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   * GNU General Public License for more details.
   *
   * You should have received a copy of the GNU General Public License
   * along with this program; if not, write to the Free Software
   * Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
"""
import string

from pygeo.base.element import Element
from pygeo.base.pygeoexceptions import Assignment_Error
from pygeo.base.pygeoconstants import *
from pygeo.base.pygeomath import *
from pygeo.base.pygeoprimitives import *
from pygeo.base.pygeoopts import *
#import operator

#PRIMLIST = [type(1),type(1.0)]
VECT_TYPE=type(vector())

COORDSLIST = ['x','y','z']

ORIGIN_ARRAY=array([0.,0.,0.,1.])

class Position3(vector):
   def __init__(self,*args):
      v=[]
      for arg in args:
          if not isinstance(arg,Element):
             v.append(arg)
          else:
             if isinstance(arg,vector):
                v=vector(arg.x,arg.y,arg.z)
      vector.__init__(self,*v)

   def get_pos(self):
      if TEST_MAX:
         try:
            m=max(absolute(self))
         except OverflowError:
            return self             
         if m > MAX:
            return (self/m)*MAX
         else:
            return self
      else:
         return self


   pos= property(get_pos,None,None,"The 3 coordinate drawing position vector")

   def set(self,other):
      self.x=other.x
      self.y=other.y
      self.z=other.z
      
   def polar(self):
      xy=hypot(self.x,self.y)
      theta = arctan2(xy, self.z)
      phi = arctan2(self.y, self.x)
      return theta, phi

   def distance(self,other):
      return (self-other).mag

   def distanceSquared(self,other):
      return  (self-other).mag2

   def lengthSquared(self):
      return self.mag2

   def length(self):
       return self.mag

   # def returning array
   def homogenous(self):
      return  array((self.x,self.y,self.z,1.),'d')

   def transform(self,mat,point):
      tf=matrixmultiply(homogenous(self),mat)
      point.set(vector(tf[0:3]/tf[3]))

   def onPlane(self,plane):
      return absolute(matrixmultiply(plane.equat(),self.homogenous())) < EPS

   def coPlanar(self,p1,p2,p3):
      c= absolute(determinant(array([p1.homogenous(),
                                         p2.homogenous(),
                                         p3.homogenous(),
                                         self.homogenous()])))
      if c  < EPS:
        return True
      else:
         return False

   def coLinear(self,p1,p2):
      v1=p1-self
      v2=p2-p1
      return v1.cross(v2).mag2 < EPS

   def onLine(self,line):
      v1=line.p1 - self
      return v1.cross(line.getDirection).mag2 < EPS

   def toInterpolated(self,p1,p2,r):
       self.set(p1*(1.0-r)+p2*r)
       return True

   def to_3d(self,harray):
      try :
         self.set(vector(harray[0:3]/float(harray[3])))
      except (ZeroDivisionError,OverflowError):
         print self.__class__.__name__
         print "point at infinity in conversion from homogenous coordinates"
         print "vector set to 'MAX' times non-homogenous coordinates"
         self.set(vector(harray[0:3]*MAX))
      return True

   def toXY(self,point):
       __mat2=array([[-1.,0.,0.,0.],[0.,-1.,0.,0.],[0.,0.,0.,-1.],[0.,0.,0.,-1]])
       tf= matrixmultiply(point.homogenous(),__mat2)
      # [tf[0]/tf[3],tf[1]/tf[3],1]
       self.set(vector([tf[0]/tf[3],tf[1]/tf[3],1]))
       return True  

   def fromXY(self,equat,point):
       _zpt=array([0.,0.,-1.,1.])
       mat= multiply.outer(equat,_zpt)
       k=matrixmultiply(_zpt,equat)
       for i in range(4):
              mat[i,i]-=k
       tf=matrixmultiply(homogenous(point),mat)
       try :
          
          self.set(vector(tf[0:3]/tf[3]))
       except (ZeroDivisionError,OverflowError):
         print self.__class__.__name__
         print "point at infinity in conversion from homogenous coordinates"
         print "vector set to 'MAX' times non-homogenous coordinates"
         self.set(vector(tf[0:3][0:3])*MAX)
       return True


   def toLine(self,p1,p2):
      """move to foot of perpendicular from initial position of self
      to line connecting p1 & p2 arguments"""
      vxs = p2 - p1
      vxt = self -  p1
      try:
        factor= (
                 vxt.dot(vxs)
                 /
                 vxs.mag2
                 )
      except ZeroDivisionError:
         #print self.__class__.__name__
         #print " points defining line segments are coincident. toLine returned False"
         return False

 #     if absolute(factor) > MAX:
 #            print "scaling toLine to MAX"
 #            factor=MAX
      self.set(vxs*factor+p1)
      return True

   def toPlane(self,plane):
      """move to foot of perpendicular from initial position of self
      to plane argument. plane.s and plane.v are perpendicular
      normalized vectors orthogonal to plane normal"""
      pt=homogenous(self-plane._u)
      equat=plane.equat()
      mat= multiply.outer(equat,pt)
      k=matrixmultiply(pt,equat)
      for i in range(4):
         mat[i,i]-=k
      self.to_3d(matrixmultiply(self.homogenous(),mat))
      return True


   def toCircle(self,circle):
      self.toPlane(circle)
      vt=self-circle._center
      if vt.mag:
         factor =  circle._radius/vt.mag
         self.set(vt*factor+circle._center)
      else:
         lxy = hypot(circle._u.x,circle._u.y)
         if (lxy >= EPS):
            self.set(vector(-circle._u.y/lxy,circle._u.x/lxy,0).norm()
                       *circle._radius)
         else:
            self.vector=vector(1,0,0)
      return True




   def toSphere (self,sphere):
      """move to closest point on surface of sphere argument"""
      vt= self- sphere._center
      len=vt.mag
      if len:
          factor=sphere._radius/len
          self.set(vt*factor+sphere._center)
      else:
          self.set(vector(sphere._center.x+sphere._radius,
                                    sphere._center.y,
                                    sphere._center.z))
      return True


   def toCentroid(self,p1,p2,p3):
      self.set((p1+p2+p3)/3.0)
      return True

   def toOrthoCenter(self,p1,p2,p3):
      vxs=Position3()
      vxs.set(p3)
      vxs.toLine(p2,p1)
      vxt=Position3()
      vxt.set(p2)
      vxt.toLine(p3,p1)
      if self.toInterSection(p3,vxs,p2,vxt,test=False):
         return True
      else:
         self.__class__.__name__
         print "points are not distinct, no orthocenter defined, returned False"
         return False

   def toInCenter(self,p1,p2,p3):
      vxs=Position3()
      vxt=Position3()
      vxs.toBisector(p1,p2,p3)
      vxt.toBisector(p2,p1,p3)
      if self.toInterSection(p1,vxs,p2,vxt,test=False):
         return True
      else:
         self.__class__.__name__
         print "points are not distinct, no incenter defined, returned False"
         return False

   def toExCenter(self,p1,p2,p3):
      vxs=Position3()
      vxt=Position3()
      vxs.toExtBisector(p2,p1,p3)
      vxt.toExtBisector(p3,p1,p2)
      if self.toInterSection(p2,vxs,p3,vxt,test=0):
         return True
      else:
         self.__class__.__name__
         print "points are not distinct, no excenter defined, returned False"
         return False


   def toOpposite(self,object,point):
      try:
         v= (object._center-point).norm()
         self.set(v*object._radius+object._center)
         return True
      except ZeroDivisionError:
         print self.__class__.__name__
         print "point at object center, antipodal undefined, returned False"
         return False


   def toInterSection(self,p11,p12,p21,p22,test=True):
      if test:
         if not p11.coPlanar(p12,p21,p22):
            print self.__class__.__name__
            print "no intersection of skew lines; False returned"
            return False

      d1 = p12 - p11
      d2 = p22 - p21
      c =  d1.cross(d2)
      o = p21 - p11
      try:
         factor = determinant(array((o,d2,c)))/c.mag2
      except ZeroDivisionError:
         if (d1.mag <> 0 and d2.mag <> 0):
             print self.__class__.__name__
             print "intersection of parallel lines"
             print "returning MAX times vector"
             factor = MAX
         else:
             return False
      self.set(d1*factor+p11)
      return True

   def toPlaneIntersection(self,plane,p1,p2,test=True):
      if test:
         if p1.onPlane(plane) and p2.onPlane(plane):
            print self.__class__.__name__
            print "line on plane, degenerate intersection, False returned"
            return False
      pt1=p1.homogenous()
      pt2=p2.homogenous()
      equat=plane.equat()
      mat= multiply.outer(equat,pt2)
      k=matrixmultiply(pt2,equat)
      for i in range(4):
         mat[i,i]-=k
      self.to_3d(matrixmultiply(pt1,mat))
      return True


   def toPlaneReflection(self,u,d):
       x,y,z=u.x,u.y,u.z
       mat=transpose(array([[1-2*x**2,-2*x*y,-2*x*z,2*x*d],
                    [-2*x*y,1-2*y**2,-2*y*z,2*y*d],
                     [-2*x*z,-2*y*z,1-2*z**2,2*z*d],
                     [0.,0.,0.,1]]))
       self.to_3d(matrixmultiply(self.homogenous(),mat))
       return True


   def toSphereCenter(self,p1,p2,p3,p4):
      s1=p1.mag2
      s2=p2.mag2
      s3=p3.mag2
      s4=p4.mag2
      v21=p2-p1
      v31=p3-p1
      v41=p4-p1
      n1=determinant(array(((s2-s1,v21.y,v21.z),(s3-s1,v31.y,v31.z),(s4-s1,v41.y,v41.z))))
      n2=determinant(array(((v21.x,s2-s1,v21.z),(v31.x,s3-s1,v31.z),(v41.x,s4-s1,v41.z))))
      n3=determinant(array(((v21.x,v21.y,s2-s1),(v31.x,v31.y,s3-s1),(v41.x,v41.y,s4-s1))))
      d3=determinant(array((v21,v31,v41)))
      try:
         self.set(vector(float(n1)/(d3*2),float(n2)/(d3*2),float(n3)/(d3*2)))
         return True
      except ZeroDivisionError:
         print self.__class__.__name__
         print "points are not distinct, sphere center undefined, returned False"
         return False

   def toCircumCenter(self,p1,p2,p3):
      vxs = p2 - p1
      vxt = p3 - p1
      d1=vxs.dot(vxt)
      d2=vxs.mag2
      d3= vxt.mag2
      den=2.0*(d2*d3-d1*d1)
      try:
         f1=(d2-d1)/den*d3
         f2=(d3-d1)/den*d2
      except ZeroDivisionError:
        print self.__class__.__name__
        print "points are not distince, circumcenter not defined, returned False"
        return False
      self.set(vxs*f1+vxt*f2+p1)
      return True

   def toBisector(self,p1,p2,p3):
#      try:
      r=1.0/(p1.distance(p3)/p1.distance(p2)+ 1.0)
#      except:
#         r=1.0
      self.toInterpolated(p2,p3,r)
      return True

   def toExtBisector(self,p1,p2,p3):
#      try:
      r=1.0/(-p1.distance(p3)/p1.distance(p2)+1.0)
#      except:
#         r=1.0
      self.toInterpolated(p2,p3,r)
      return True

   def toInvertPoint(self,circle,p1):
      t=(p1 - circle._center)*circle._radiusSquared
      try:
         t /= float(p1.distanceSquared(circle._center))
         self.set(t + circle._center)
      except ZeroDivisionError:
         print self.__class__.__name__
         print "point at infinity returned by 'toInvertPoint', returning MAX"
         self.set(vector(MAX,MAX,MAX))
      return True

   def toCrossPoint(self,p1,p2,p3,p4,p1a,p2a,p3a):
      v1=vector(multiply((p3-p1),(p4-p2)))
      d1=v1.dot(p3a-p2a)
      v2=vector(multiply((p3-p2),(p4-p1)))
      d2=v2.dot(p3a-p1a)
      try:
         d=d1/d2
      except ZeroDivisionError:
         d=MAX
      try:
         t = 1.0/(1.0 - d)
      except ZeroDivisionError:
         t=0
         #print "toCrossPoint"
         #return False
      self.toInterpolated(p1a,p2a,t)
      return True


   def toCircumPoint(self,circle,rad):
       if not self==circle._center:
          self.set(rotate(self-circle._center,rad,
                       circle._u) + circle._center)
          return True

       else:
          return False


   def toHarmonic(self,p1,p2,p3):
         t3=(p2 + p3) * .5
         t2= p2 - t3
         t1 = p1 -t3
         m1 = t1.mag2
         m2 = t2.mag2
         v=t2*(2.0*t1.dot(t2)) - t1*m2
         try:
             self.set(v/m1+t3)
         except ZeroDivisionError:
             print self.__class__.__name__
             print "harmonic to mipoint, point at infinity, returned [MAX,MAX,MAX}"
             self.set(vector(MAX,MAX,MAX))
         return True

if __name__ == '__main__':
   a=Position3(1,7,4)
   b=Position3(3,3,4)
   c=array([1,7,5,3])
   print a.cross(b).norm()
   a+=b
   print a
   