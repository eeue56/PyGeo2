from pygeo import *
from pygeo.base.abstract_elements_usphere import _uPoint
from pygeo.base.abstract_elements_usphere import _uCircle

# testing of factory function for fixed points on complex plane
v=display(scale=5,camera_vector=[0,4,-1],trace_on=True)


""" point on complex plane at given x,y coords """

z1 = zFreePoint(1,-2,color=RED)                        # zFreePoint
#--------------------------------------------------

zo=zOrthoPoint(z1,color=RED)
z2= zFreePoint(2,2,color=RED)
zline= zLine(z1,zo)                # z_to_uFreePoint


s=[]
for i in range(-20,30):
   
   s.append(zSlider(zline,ratio=i/10.,color=makecolor(),pointsize=.07))                 #zRotation

t=[]
def step(seed,steps):
    if steps:
       p=mobRotate(zo,PI/50,seed)
       t.append(p)
       steps-=1
       step(p,steps)


seed=[s]

step(seed,100)

uTransform(t,level=1)
v.pickloop()