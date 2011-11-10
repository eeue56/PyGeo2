import Numeric as N
#import numarray as N
import LinearAlgebra
import visual
from UserArray import UserArray
from pygeoopts import EPS



#math and array constants and functions
PI=N.pi
math_E=N.e
absolute=N.absolute
add=N.add
subtract=N.subtract
multiply=N.multiply
sqrt=N.sqrt
arctan=N.arctan
arctan2=N.arctan2
arccos=N.arccos
arcsin=N.arcsin
cos=N.cos
sin=N.sin
tan=N.tan


identity=N.identity
hypot=N.hypot
matrixmultiply=N.matrixmultiply
transpose=N.transpose
reshape=N.reshape
arrayrange=N.arrayrange
array=N.array
ones=N.ones
dot=N.dot
conjugate=N.conjugate
trace=N.trace
determinant=LinearAlgebra.determinant
solve=LinearAlgebra.solve_linear_equations
SVD= LinearAlgebra.singular_value_decomposition
inverse= LinearAlgebra.inverse
eigenvectors=LinearAlgebra.eigenvectors

norm=visual.norm
vector=visual.vector
cross=visual.cross
mag=visual.mag
mag2=visual.mag2
rotate=visual.rotate


vector=visual.vector
array=N.array

def toXY(point):
    __mat2=array([[-1.,0.,0.,0.],[0.,-1.,0.,0.],[0.,0.,0.,-1.],[0.,0.,0.,-1]])
    tf= matrixmultiply(homogenous(point),__mat2)
    return array([tf[0]/tf[3],tf[1]/tf[3],1])


def quadratic(a,b,c):
    try: 
       x1=sqrt(b**2-4*a*c)
       try:
          h1=(-b-x1)/(2*a)
          h2=(-b+x1)/(2*a)
       except ZeroDivisionError:
          h1=None
          h2=None
    except ValueError:
       h1=None
       h2=None
    return h1,h2

def cross3(v1,v2,v3):
    return cross(v2-v1,v3-v1)

def homogenous(narray):
  return array((narray[0],narray[1],narray[2],1.),'d')

def cross_ratio(a,b,c,d):
   ab=a.distance(b)
   bc=b.distance(c)
  # ac=a.distance(c)
   ad=a.distance(d)
  # bd=b.distance(d)
#   if bd > ad:
#      ab=-ab
   dc=-c.distance(d)
   return (ab/bc)/(ad/dc)
   
def mod2(c):
  return abs(c)**2

def mod(c):
  return abs(c)


class Hermitian(UserArray):
   def __init__(self,*args):
      UserArray.__init__(self,*args)
      #self.A=self.array[0][0]
      #self.B=self.array[0][1]
      #self.C=self.array[1][0]
      #self.D=self.array[1][1]
      #self.descriminant=determinant(self)
   
   def __setattr__(self,attr,value):
      # for .attributes for example, and any future attributes
      if attr == 'A':
         self.array[0][0] = value
      elif attr == 'B':
         self.array[0][1] = value
      elif attr == 'C':
         self.array[1][0] = value
      elif attr == 'D':
         self.array[1][1] = value
#      UserArray.__setattr__(self,attr,value)   
      self.__dict__[attr]=value
   
   def __getattr__(self,attr):
      # for .attributes for example, and any future attributes
      if attr == 'A':
         return self.array[0][0]
      elif attr == 'B':
         return self.array[0][1]
      elif attr == 'C':
         return self.array[1][0]
      elif attr == 'D':
         return self.array[1][1]
      elif attr== 'descriminant':
         return determinant(self)   
#      UserArray.__getattr__(self,attr)   
      return getattr(self.array, attr)
      
   def normalize(self):
      det=determinant(self.array)
      self.array/=det
      return self
   
   def invert(self):
      self.array=inverse(self.array)
      return self

class Mobius(UserArray):
   def __init__(self,*args):
      UserArray.__init__(self,*args)
   
   def __setattr__(self,attr,value):
      # for .attributes for example, and any future attributes
      if attr == 'a':
         self.array[0][0] = value
      elif attr == 'b':
         self.array[0][1] = value
      elif attr == 'c':
         self.array[1][0] = value
      elif attr == 'd':
         self.array[1][1] = value
#      UserArray.__setattr__(self,attr,value)   
      self.__dict__[attr]=value
   
   def __getattr__(self,attr):
      # for .attributes for example, and any future attributes
      if attr == 'a':
         return self.array[0][0]
      elif attr == 'b':
         return self.array[0][1]
      elif attr == 'c':
         return self.array[1][0]
      elif attr == 'd':
         return self.array[1][1]
#      UserArray.__getattr__(self,attr)   
      return getattr(self.array, attr)
      
   def normalize(self):
      det=determinant(self.array)
      self.array/=sqrt(det)
      return self
   
   
   def conjugate(self,mat):
      self.array= matrixmultiply(mat,matrixmultiply(self.array,inverse(mat)))
      return self
   
   def normal_form(self):
      f1,f2=self.getFixed()
      try:
         mat=array([[1.,-f2],[1.,-f1]])
         self.conjugate(mat)
      except TypeError:
         print "fixed point at infinity"
   
   def getFixed(self):
      if abs(determinant(self) -1) > EPS:
         self.normalize()
      evalues, evectors =  eigenvectors(self.array)
      return evectors

   def getMultiplier(self):
      if abs(determinant(self)-1)> EPS:
          self.normalize()
      evalues, evectors =  eigenvectors(self.array)
      return 1./(evalues[0]**2),1./(evalues[1]**2) 
   
   def getPole(self):
      return -self.d/self.c
      
   def getInversePole(self):
      return self.a/self.c
      
   def getTrace(self):
      return self.a + self.d
      
   def getDeterminant(self):
      return (self.a*self.d) - (self.b*self.c)
   
   def getConstant(self):
      determinant=self.getDeterminant()
      if abs(determinant-1)> EPS:
          self.normalize()
      trace=self.getTrace()
      invariant=(self.a-self.d)**2 +4 * self.b*self.c
      return (trace+sqrt(invariant*determinant))/(trace-sqrt(invariant*determinant))
      
   def getInvariant(self):
      if abs(determinant(self)-1)> EPS:
          self.normalize()
      return (self.a-self.d)**2 +4 * self.b*self.c

PyGeoMath=['PI','math_E','absolute','add','subtract','multiply','sqrt','arctan','arctan2',
'cos','sin','arccos','arcsin','tan','identity','hypot','matrixmultiply','transpose','arrayrange','array','dot',
'determinant','solve','norm','vector','cross','mag','mag2','rotate','SVD','reshape',
'ones','inverse','conjugate','trace','toXY','cross3','quadratic','homogenous','cross_ratio','eigenvectors',
'mod','mod2','Hermitian','Mobius']



__all__=PyGeoMath

if __name__ == '__main__':
   a=Hermitian(([1,5],[6,7]))
   print a
   a.A=7
   print a