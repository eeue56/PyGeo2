from pygeo import *
v=display(scale=5,camera_vector=[0,4,-1])


z1=zFreePoint(1-2j)
#--------------------------------------------------

""" pickable point constrained to complex
plane at initial given x,y coords """

z2 = zFreePoint(-2,-2,color=GREEN)                # zFreePoint
#--------------------------------------------------

""" point on complex plane at given polar corrdinates """

z3 = zPoint(angle=PI/6,dist=4,color=BLACK)     # zPolarPoint
#--------------------------------------------------

""" conjugate of argument point """

z4 = zPoint(z3,color=RED)                # zConjugate
#--------------------------------------------------


zc1=zCircle(z2,z3,z4)


z1p=zInversePoint(z1,zc1,color=RED)
uCircle(zc1)
uSphere(color=WHITE)
uPoint(z1,color=BLUE)

uPoint(z1p,color=RED)
v.pickloop()