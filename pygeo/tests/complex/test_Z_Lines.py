from pygeo import *

v=display(scale=8,camera_vector=[0,4,-1])

# testing of factory function for circles on the complex plane


                                                   # CLASS being called
""" point on complex plane at given x,y coords """

z1=zPoint(2,-2)                                    # zFixedPoint
#--------------------------------------------------

""" pickable point constrained to complex
plane at initial given x,y coords """

z2=zFreePoint(-1,-2)                           # zFreePoint
#--------------------------------------------------

""" 'Line' connecting the 2 points """

zl1=zLine(z1,z2)                                 # zLineFromPoints
#--------------------------------------------------


""" circle on complex plane from center &
circumference points """

zc1=zCircle(z1,z2)                                # zCircleFromPoints
#--------------------------------------------------

""" pickable point constrained to complex
plane at initial given x,y coords """

z3=zFreePoint(1.5,-1)                          # zFreePoint
#--------------------------------------------------

""" circles on complex plane through and determined by
three point arguments """

zc2=zCircle(z1,z2,z3,color=RED)                   # zCircumCircle
#--------------------------------------------------

""" line on complex plane through points of intersection of the
two circles"""

zl2=zLine(zc1,zc2)
#--------------------------------------------------

""" circles on unit sphere determined by projection of
line on complex plane """

u1=uCircle(zl1,level=2,linewidth=.05)                           # z_to_uCircle
u2=uCircle(zl2,level=2,linewidth=.05)                           # z_to_uCircle

"""lines on complex plane determined by projection of
circle on unit sphere """

zCircle(u1,level=3)                               # u_to_zCircle
zCircle(u2,level=3)                               # u_to_zCircle


uSphere(color=WHITE,level=2)

v.pickloop()