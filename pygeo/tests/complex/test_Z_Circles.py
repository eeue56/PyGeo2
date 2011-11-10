from pygeo import *

v=display(scale=8,camera_vector=[0,4,-1])

# testing of factory function for circles on the complex plane


                                                   # CLASS being called
""" point on complex plane at given x,y coords """

z1=zPoint(2,2,level=2)                                    # zFixedPoint
#--------------------------------------------------

""" pickable point constrained to complex
plane at initial given x,y coords """

z2=zFreePoint(-1,-2)                           # zFreePoint
#--------------------------------------------------

""" circle on complex plane from center &
circumference points """

zc1=zCircle(z1,z2,color=BLACK)                                # zCircleFromPoints
#--------------------------------------------------

""" pickable points constrained to complex
plane at initial given x,y coords """

z3=zFreePoint(1.5,-1)                          # zFreePoint
z4=zFreePoint(-5,.5)                           # zFreePoint
#--------------------------------------------------

""" circles on complex plane through and determined by
three point arguments """

zc2=zCircle(z2,z3,z4,color=RED)                   # zCircumCircle
#--------------------------------------------------

""" circle inverse to first circle argument with respect
to second circle argument """

zc3=zCircle(zc1,zc2,color=CYAN)                   # zInverseCircle
#--------------------------------------------------

""" circle in which the first circle argument is inverted to
generate the second circle argument """

zc4=zCircle(zc2,zc3,alt=FUNDAMENTAL,level=2,color=BLACK)          # zFundamentalCircle
#--------------------------------------------------

""" circle orthogonal to circle argument, centered at
point argument """

zc5=zCircle(zc1,z4,color=MAGENTA)                 # zOrthoCircle
#--------------------------------------------------

""" circle orthogonal to circle argument, through two
point arguments """

zc6=zCircle(zc1,z3,z4,color=GREEN)                # zOrthoCircle_Circum
#--------------------------------------------------

""" circles on unit sphere determined by projection of
circle on complex plane """

u1=uCircle(zc1,level=2)                           # z_to_uCircle
u2=uCircle(zc2,level=2)                          # z_to_uCircle
u3=uCircle(zc3,level=2,color=CYAN)                           # z_to_uCircle
u4=uCircle(zc4,level=2)                           # z_to_uCircle
u5=uCircle(zc5,level=2)                           # z_to_uCircle
u6=uCircle(zc6,level=2)                           # z_to_uCircle
#--------------------------------------------------

"""circles on complex plane determined by projection of
circle on unit sphere """

zCircle(u1,level=3)                               # u_to_zCircle
zCircle(u2,level=3,color=RED)                               # u_to_zCircle
zCircle(u3,level=3,color=CYAN)                               # u_to_zCircle
zCircle(u4,level=3)                               # u_to_zCircle
zCircle(u5,level=3)                               # u_to_zCircle
zCircle(u6,level=3)                               # u_to_zCircle
#--------------------------------------------------

uSphere()

v.pickloop()