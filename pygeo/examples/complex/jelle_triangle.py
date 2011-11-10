
from pygeo import *
import pygeo.base.abstract_elements_complex as Complex 

v=display(scale=8)

#we are working on the complex plane - allowing us to play with the Mobius transformation

#the required (approx) angles, converted to radians
rads = PI/180
a1=115.*rads
a2=35.*rads
a3=30.*rads


#a class so that we set maintain the metrics while rotating the triangle freely
class zCircumRefPoint(Complex._zPoint):
   __opts__= Complex._zPoint.__opts__[:] +['angle']
   def __init__(self,zcircle,refpoint,**kws):
      self.zcircle=zcircle
      self.refpoint=refpoint
      self.angle=kws.get("angle",PI)*self.zcircle.a
      Complex._zPoint.__init__(self,*[zcircle,refpoint],**kws)
      self.update()

   def _findSelf(self):
      zcircle=self.zcircle
      refpoint=self.refpoint
      self.set((refpoint-zcircle._center)*(math_E**complex(0,self.angle))+zcircle._center)
      return True

# point at the origin
O=zFreePoint(color=MAGENTA)

# a point of the unit circle
c = zPolarPoint(angle=0,color=RED,level=5)

#draw the unit circle
zcircle=zCircle(O,c,fixed=True)

# a point on the unit circle that can be picked and freely moved around the circle
c1=zSlider(zcircle,angle=0)

# the 2 additional points on the unit circle that realize (together with the sliding
# point) the required angular matrics at the circle's center 

c2 = zCircumRefPoint(zcircle,c1,angle=a1+a2,color=GREEN)
c3 = zCircumRefPoint(zcircle,c1,angle=a1*2+a2+a3,color=BLUE)

# lines from the center point to the vertexes of the triangle
l1=zLine(O,c1,color=BLUE)
l2=zLine(O,c2,color=MAGENTA)
l3=zLine(O,c3,color=YELLOW)

# an arbitrary triangle and its circumcircle
z1 = zFixedPoint(5,0,level=-1)   
z2 = zFixedPoint(1,3,level=-1)
z3 = zFixedPoint(-4,-3,level=-1)              
zl1=zLine(z1,z2,color=RED,level=-1)
zl2=zLine(z2,z3,color=RED,level=-1)
zl3=zLine(z1,z3,color=RED,level=-1)
zcircle2=zCircle(z1,z2,z3,color=WHITE,level=-1)

# the Mobius tranformation mapping the vertexes of the 2 triangles
# and applied to the lines through the conforming triangle's center and vertices
# and to the center point.

# check level2 and clear level1 on UI to view

# the tangents to the intersecting circles at the transformed center point will have 
# the required angles, and each circle passes through a triangle vertex 

m=mobPointSets([c1,c2,c3],[z1,z2,z3],[O,l1,l2,l3,zl1,zl2,zl3,z1,z2,z3],level=2)
v.pickloop()

