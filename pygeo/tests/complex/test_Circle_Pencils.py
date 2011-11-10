from pygeo import *
v=display(scale=5,camera_vector=[0,4,-1])

                                                       # CLASS being called
""" point on complex plane at given x,y coords """

z1=zFreePoint(2,2)                                        # zFixedPoint
#--------------------------------------------------

""" pickable points constrained to complex
plane at initial given x,y coords """

z2=zFreePoint(-1,-2)                               # zFreePosition
z3=zFreePoint(3,-3)
z4=zFreePoint(4,-4)

#--------------------------------------------------

""" circle on complex plane from center &
circumference points """

zc1=zCircle(z1,z2)                                    # zCircleFromPoints
#--------------------------------------------------

""" circles on complex plane through and determined by
three point arguments """

zc2=zCircle(z3,z4,color=RED)                       # zCircumCircle
#--------------------------------------------------

""" circle on complex plane from center &
circumference points with counter orientation """

zc1a=zCircle(z1,z2,O="-")                             # zCircleFromPoints
#--------------------------------------------------

""" pencils of circles on complex plane determined by
given circles """

zp1=zCirclePencil(zc1,zc2)                                  # zCircles

zp2=zCirclePencil(zc1a,zc2,color=CYAN,level=2)                      # zCircles
#--------------------------------------------------
uStereoProject([zp1,zp2])
v.pickloop()