from pygeo import *

# testing of factory function for fixed points on complex plane
v=display(scale=5,camera_vector=[0,4,-1])


z1 = zPoint(-1,1)

z2 = zFreePoint(1,-2)                        # zFixedPoint

z3=zFreePoint(-3,3)

z1a = zPoint(1,2)

z2a = zFreePoint(2,-3)                        # zFixedPoint

z3a=zFreePoint(4,-5)


zcircle1=zCircle(z1,z2,z3)

zcircle2=zCircle(z1a,z2a,z3a,color=RED)

zLine(zcircle1,zcircle2)

v.pickloop()