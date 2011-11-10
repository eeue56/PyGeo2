import pygeo.base.abstract_elements_complex as Complex

from pygeo.base.abstract_elements_real import method_get


from pygeo.base.pygeoexceptions import Argument_Type_Error
from pygeo.base.pygeoconstants import *
from pygeo.base.pygeomath import *
from pygeo.base.pygeoprimitives import *

from pygeo.base.pygeoopts import *



TransformClasses = ['mobPointSets','mobMultiply','mobTranslate'
,'mobReciprocate','mobUnitCircle','mobFromFixed','mobMapCircles','mobRotate',
 'mobInverse']

TransformDefs = ['mobTransform']


__all__= TransformClasses+TransformDefs

class mobPointSets(Complex._zTransformation):
   """
:constructors: 

     - mobTransform([z1,z2,z3],[z1a,z2a,z3a],[list of objects])
     - mobPointSets([z1,z2,z3],[z1a,z2a,z3a],[list of objects])

:returns: the `Mobius transformation`_ which maps the 3 (ordered) points of the first point set
          to the 3 (ordered) points of the second point set, applied to the 
          given list of objects of the complex plane.
          
:site ref: http://en.wikipedia.org/wiki/Mobius_group#Specifying_a_transformation_by_three_points
   """
   def __init__(self,v,w,elements,**kws):
      self.v=v
      self.w=w
      self.elements=[]
      for e in elements:
         for t in e:
            self.elements.append(t)
      args=self.v+self.w+self.elements
      for element in elements:
         if not element in args:
            args.append(element)
      Complex._zTransformation.__init__(self,*args,**kws)
      self.normal_form = kws.get('normal_form',False)
      self.update()

   def _getMobius(self):
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
      try:
         self._mobius= Mobius([[a,b],[c,d]]).normalize()
         if self.normal_form:
             self._mobius.normal_form()
      except ValueError:
         self._mobius = Mobius([[0,0],[0,0]])
         print "degenerate Mobius matrix"
         return False
      return True

class mobUnitCircle(Complex._zTransformation):
   """
:constructors: 

     - mobTransform(zcircle,[list of objects])
     - mobUnitCircle(zcircle,[list of objects])

:returns: a `Mobius transformation`_ which maps the given circle to the unit circle, applied to the 
          given list of objects of the complex plane.
          
:site ref: http://mathworld.wolfram.com/UnitCircle.html
   """
   def __init__(self,zcircle,elements,**kws):
      self.zcircle=zcircle
      self.elements=[]
      for e in elements:
         for t in e:
            self.elements.append(t)
      args=[zcircle]+[elements]+self.elements
      for element in elements:
         if not element in args:
            args.append(element)

      Complex._zTransformation.__init__(self,*args,**kws)
      self.update()


   def _getMobius(self):
      t_mat=Hermitian([[1,-self.zcircle._center],[0,1]])
      d_mat=Hermitian([[1.0/self.zcircle._radius,0],[0,1]])
      self._mobius= Mobius(matrixmultiply(d_mat,t_mat)).normalize()
      return True

class mobMultiply(Complex._zTransformation):
   """
:constructors: 

     - mobTransform(zpoint,[list of objects])
     - mobMultiply(zpoint,[list of objects])

:returns: a `normal form`_ elliptical `Mobius transformation`_ with the given complex point as multiplier, applied to the 
          given list of objects of the complex plane.
          
:site ref:http://en.wikipedia.org/wiki/Mobius_group#Elliptic_transformations
   """
   __opts__= Complex._zTransformation.__opts__[:] +['alt']

   def __init__(self,z,elements,**kws):
      self.z=z
      self.elements=[]
      for e in elements:
         for t in e:
            self.elements.append(t)
      args=[z]+[elements]+self.elements
      for element in elements:
         if not element in args:
            args.append(element)

      Complex._zTransformation.__init__(self,*args,**kws)
      self.update()

   def _getMobius(self):
      k=sqrt(self.z.toComplex())
      try:
          self._mobius= Mobius([[k,0.],[0,1/k]]).normalize()
      except ZeroDivisionError:
          return False
      return True


   def _normalize(self):
      self.mat=self.mat*1/sqrt(determinant(self.mat))


class mobTranslate(Complex._zTransformation):
   """
:constructors: 

     - mobTransform(zpoint,[list of objects],alt=TRANSLATE)
     - mobTranslate(zpoint,[list of objects])

:returns: a `normal form`_ parabolic `Mobius transformation`_ translating the given
          given list of objects in the direction of the given point of the complex plane/
          
:site ref:http://en.wikipedia.org/wiki/Mobius_group#Hyperbolic_transformations
   """

   __opts__= Complex._zTransformation.__opts__[:] +['alt']

   def __init__(self,z,elements,**kws):
      self.z=z
      self.elements=[]
      for e in elements:
         for t in e:
            self.elements.append(t)
      
      args=[z]+[elements]+self.elements
      for element in elements:
         if not element in args:
            args.append(element)
      Complex._zTransformation.__init__(self,*args,**kws)
      self.update()

   def _getMobius(self):
      self._mobius= Mobius([[1,self.z.toComplex()],[0,1]]).normalize()
      return True

class mobReciprocate(Complex._zTransformation):
   """
:constructors: 

     - mobTransform([list of objects])
     - mobReciprocate([list of objects])

:returns: a `normal form`_ `Mobius transformation`_ reciprocating the given
          given list of objects of the complex plane/
          
:site ref:http://mathworld.wolfram.com/Reciprocal.html
   """
   def __init__(self,elements,**kws):
      self.elements=[]
      for e in elements:
         for t in e:
            self.elements.append(t)
      args=self.elements+[elements] 
      for element in elements:
         if not element in args:
            args.append(element)
      Complex._zTransformation.__init__(self,*args,**kws)
      self.update()

   def _getMobius(self):
      self._mobius= Mobius([[0.,1j],[1j,0.]])
      return True

class mobFromFixed(Complex._zTransformation):
   def __init__(self,f1,f2,k,elements,**kws):
      self.f1=f1
      self.f2=f2
      self.k=k
      self.elements=[]
      for e in elements:
         for t in e:
            self.elements.append(t)
      
      args=[f1]+ [f2]+[k]+[elements]+self.elements
      for element in elements:
         if not element in args:
            args.append(element)
      Complex._zTransformation.__init__(self,*args,**kws)
      self.update()

   def _getMobius(self):
      f1=self.f1
      f2=self.f2
      k=self.k
      A=f1-k*f2
      B=f1*f2*(k-1)
      C=1-k
      D=k*f1-f2
      self._mobius= Mobius([[A,B],[C,D]]).normalize()
      return True

class mobMapCircles(Complex._zTransformation):
   """
:constructors: 

     - mobTransform(zcircle1,zcircle2,[list of objects])
     - mobMapCircles(zcircle1,zcircle2,[list of objects])

:returns: a `Mobius transformation`_ mapping the interior of the first given circle 
          to the exterior of the second given circle, applied to the given list
          of geometric objects

:site ref:http://www.americanscientist.org/template/BookReviewTypeDetail/assetid/17185;jsessionid=aaa6s5lwY8zkwS
   """
   def __init__(self,circle1,circle2,elements,**kws):
      self.circle1=circle1
      self.circle2=circle2
      self.elements=[]
      for e in elements:
         for t in e:
            self.elements.append(t)
      args=[circle1]+[circle2]+self.elements
      for element in elements:
         if not element in args:
            args.append(element)
      Complex._zTransformation.__init__(self,*args,**kws)
      self.normal_form = kws.get('normal_form',False)
      self.update()

   def _getMobius(self):
      c1=self.circle1._center.toComplex()
      c2=self.circle2._center.toComplex()
      r1=self.circle1._radius
      r2=self.circle2._radius
      mat1=Mobius([[1,-c1],[0,1.]])
      mat2=Mobius([[0.,r1*r2],[1j,0]]).normalize()
      mat3=Mobius([[1,c2],[0,1.]])
      m=matrixmultiply(mat3,matrixmultiply(mat2,mat1))
      try:
          self._mobius=Mobius(m).normalize()
          if self.normal_form:
              self._mobius.normal_form()
      except ValueError:
          self._mobius = Mobius([[0,0],[0,0]])
          print "degenerate Mobius matrix"
          return False
      return True


class mobRotate(Complex._zTransformation):
   """
:constructors: 

     - mobTransform(zpoint,numeric,[list of objects])
     - mobRotate(zpoint,numeric,[list of objects])

:returns: the `Mobius transformation`_ induced by the rotation of the `Riemann sphere`_,
          with the `stereographic projection`_ of the given complex point as axis, by
          an the given numeric angle (in radians), and applied to the given list of geometric
          objects.

:site ref:http://en.wikipedia.org/wiki/Mobius_group#Hyperbolic_transformations
   """
   def __init__(self,zcenter,angle,elements,**kws):
      self.zcenter=zcenter
      self.angle=angle
      self.elements=[]
      for e in elements:
         for t in e:
            self.elements.append(t)
      args=[zcenter]+self.elements
      for element in elements:
         if not element in args:
            args.append(element)
      Complex._zTransformation.__init__(self,*args,**kws)
      self.normal_form = kws.get('normal_form',False)
      self.update()

   def _getMobius(self):
       center=self.zcenter
       h_angle=self.angle/2.
       a=math_E**complex(0,h_angle)*center.mod2()+math_E**-(complex(0,h_angle))
       b=(0+2j)*sin(h_angle)*center
       c=-b.conjugate()
       d=a.conjugate()
       try:
           self._mobius=Mobius([[a,b],[c,d]]).normalize()
           if self.normal_form:
               self._mobius.normal_form()
       except ValueError:
           self._mobius = Mobius([[0,0],[0,0]])
           print "degenerate Mobius matrix"
           return False
       return True


class mobInverse(Complex._zTransformation):
   """
:constructors: 

     - mobTransform(mobTransform,[list of objects])
     - mobInverse(mobTransform,[list of objects])

:returns: a `Mobius transformation`_ defined by the `matrix inverse`_ of matrix
          represetning the given Mobius transformation.
   """

   def __init__(self,transform,elements,**kws):
      self.mobius=transform
      self.elements=[]
      for e in elements:
         for t in e:
            self.elements.append(t)
      args=[transform]+self.elements
      for element in elements:
         if not element in args:
            args.append(element)
      Complex._zTransformation.__init__(self,*args,**kws)
      self.normal_form = kws.get('normal_form',False)
      self.update()

   def _getMobius(self):
      self._mobius=Mobius(inverse(self.mobius._mobius))
      return True

def mobTransform(*args,**kws):
    __sigs__=  [[list,list,list],
               [Complex._zCircle,list], [Complex._zPoint,list],
               [Complex._zCircle,Complex._zCircle,list],[list],
               [Complex._zPoint,float,list]]

    t,i = method_get(__sigs__,args)
    if t is None:
       raise Argument_Type_Error(__sigs__,args)
    else:
       if i==0:
          if (len(t[0])==3 and len(t[1])==3): 
             return mobPointSets(t[0],t[1],t[2],**kws)     
       elif i==1:
          return mobUnitCircle(t[0],t[1],**kws)
       elif i==2:
          alt=kws.get("alt")
          if alt:
             if alt==TRANSLATE:
                return mobTranslate(t[0],t[1],**kws)
             elif alt==MULTIPLY:
                return mobMultiply(t[0],t[1],**kws)
             else:
                raise Argument_Type_Error(__sigs__,args)
          else:
             return mobMultiply(t[0],t[1],**kws)
       elif i==3:
          return mobMapCircles(t[0],t[1],t[2],**kws)
       elif i==4:
          return mobReciprocate(t[0],**kws)
       elif i==5:
          return mobRotate(t[0],t[1],t[2],**kws)
       else:
          raise Argument_Type_Error(__sigs__,args)
