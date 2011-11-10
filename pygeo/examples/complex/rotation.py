from pygeo import *
import random
from pygeo.utils.colors  import *

v=display(title="Complex Rotation",scale=9,axis=False,
scene_x=5,scene_y=5,background=WHITE,panel=False)

# an complex epicycle?

# ADJUSTABLE CONSTANTS

CYCLERATE=25
ITERATIONS=50

# 4 points on the complex plane

z1=zFreePoint(5,-5,color=BLUE,pointsize=.05,level=2)
z2=zFreePoint(-5,-5,color=BLUE,pointsize=.05,level=2)
z3=zFreePoint(5,5,color=BLUE,pointsize=.05,level=2)
z4=zFreePoint(-5,5,color=BLUE,pointsize=.05,level=2)


#a point spiraling along the circumference of the unit sphere, from north
#to south

u1=uSpiral(pointsize=.05,level=5,trace=False,rate=CYCLERATE)

# delta angle in radians for each rotation 
delta=PI/(ITERATIONS/2)


#complex rotation (projection of the sphere rotation) with the spiraling
#point as axis, applied to the 4 plane points

for i in range(ITERATIONS):

   center1=zPoint(u1,z1,angle=delta*i,color=BRIGHTGOLD,level=2)
   center2=zPoint(u1,z2,angle=delta*i,color=SPRINGGREEN,level=2)
   center3=zPoint(u1,z3,angle=delta*i,color=MEDIUMBLUE,level=2)
   center4=zPoint(u1,z4,angle=delta*i,color=ORANGERED,level=2)

   #complex rotation with the the projection of the points of the above
   #iteration as centers (axis of rotations), reapplied to the 4 points
   #of the complex plane
   
   for i in range(ITERATIONS):
       mobTransform(center1,delta*i,[z1],color=BRIGHTGOLD,level=1)

       mobTransform(center2,delta*i,[z2],color=SPRINGGREEN,level=1)
       mobTransform(center3,delta*i,[z3],color=MEDIUMBLUE,level=1)
       mobTransform(center4,delta*i,[z4],color=ORANGERED,level=1)


v.animate(povout=False,frames=CYCLERATE)