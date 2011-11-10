from pygeo import *
from pygeo.utils.colors import * 
import pygeo.base.abstract_elements_complex as Complex


#shottky group of tangent circles as per Indra's Pearls


#Adjustable constant
levmax=6

# initialize display
zDisplay=display(scale=4,panel=False,scene_x=5,scene_y=75,
          title="Complex Plane")



#points of complex plane from which to build circles
z1 = zPoint(2,0,level=5)   
z2 = zPoint(1,1,level=5)
z3 = zPoint(-2,0,level=5)              
z4 = zPoint(-1,1,level=5)                
z5 = zPoint(0,2,level=5)
z6 = zPoint(1,1,level=5)                
z7 = zPoint(0,-2,level=5)
z8 = zPoint(1,-1,level=5)               

#circles on complex plane with given centers and circumference points

c1=zCircle(z1,z2,color=RED,export=False)
c2=zCircle(z3,z4,color=GREEN,export=False)
c3=zCircle(z5,z6,color=BLUE,export=False)
c4=zCircle(z7,z8,color=YELLOW,export=False)

#a list of the circles, to seed the dance

seed=[c1,c2,c3,c4]


# return the Mobius transofrmation matrix mapping the
# interior of a given circle to the exterior of another
#given circle

def getMobius(circle1,circle2):
   c1=circle1._center.toComplex()
   c2=circle2._center.toComplex()
   r1=circle1._radius
   r2=circle2._radius
   mat1=array([[1,-c1],[0,1.]])
   mat2=array([[0.,r1*r2],[1j,0]])
   mat3=array([[1,c2],[0,1.]])
   m=matrixmultiply(mat3,matrixmultiply(mat2,mat1))
   return Mobius(m).normalize()



#the Mobius transformations matrixes mapping the circles
#interior to exterior

a=getMobius(c1,c2)
b=getMobius(c3,c4)

#the inverses of the mapping matrixes
A=inverse(a)
B=inverse(b)


#constants for breadth first search algorithm
lev=0
gens=[a,b,A,B]
inv=[2,3,0,1]
gensletter=["a","b","A","B"]
cumletter=[]
group=[]
tag=[]
num=[0]



# a class transforming a given circle by  a given Mobius transformtaion matrix.
class mobMatrix(Complex._zCircle):
   def __init__(self,matrix,zcircle,**kws):
      self.zcircle=zcircle
      self._mobius = matrix
      Complex._zCircle.__init__(self,*[zcircle],**kws)
      self.color=zcircle.color
      self.linewidth=.01
      self.update()

   def _findSelf(self):
      mat=self._mobius
      t1=inverse(mat)
      self._hermitian=Hermitian(matrixmultiply(transpose(t1),
                                     matrixmultiply(self.zcircle._hermitian,conjugate(t1))))
      self.set_radius_from_hermitian()
      return True
 

if __name__=="__main__":
   
   #the breadth first search eliminating adjacent inverse transformations
   for i in range(4):
      group.append(gens[i])
      cumletter.append(gensletter[i])
      tag.append(i)
   num.append(i+1)

   for lev in range(1,levmax):
      inew=num[lev]
      for iold in range(num[lev-1], num[lev]):
          for j in range(4):
             if j == inv[tag[iold]]:
                pass
             else:
                group.append(matrixmultiply(group[iold],gens[j]))
                cumletter.append(cumletter[iold]+gensletter[j])
                tag.append(j)
                inew=inew+1
      num.append(inew)       

 
   #the circles of the dance
   p=[]
   for i in range(num[levmax-1]):
      for j in range(4):
         print j,inv[tag[i]] 
         if j == inv[tag[i]]:
            print cumletter[i]
         else:
            p.append(mobMatrix(group[i],seed[j]))
   
   