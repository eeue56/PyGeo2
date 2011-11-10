from pygeo import *
v=display(scale=5,camera_vector=[0,4,-1])

                                                       # CLASS being called
""" point on complex plane at given x,y coords """

z1=zPoint(2,2)                                        # zFixedPoint
#--------------------------------------------------

""" pickable points constrained to complex
plane at initial given x,y coords """

z2=zFreePoint(-1,-2)                               # zFreePoint
z3=zFreePoint(1.5,-1)
#--------------------------------------------------

""" circle on complex plane from center &
circumference points """

zc1=zCircle(z1,z2)                                    # zCircleFromPoints
#--------------------------------------------------

""" circles on complex plane through and determined by
three point arguments """

zc2=zCircle(z1,z2,z3,color=RED)                       # zCircumCircle
#--------------------------------------------------

""" circle on complex plane from center &
circumference points with counter orientation """

#zc1a=zCircle(z1,z2,O="-")                             # zCircleFromPoints
#--------------------------------------------------

""" pencils of circles on complex plane determined by
given circles """

zp1=zCirclePencil(zc1,zc2)                                  # zCircles


line1=zLine(z1,z2)
line2=zLine(z1,z3)
line3=zLine(z2,z3)

uTransform([zp1,z1,z2,z3,zc1,zc2,line1,line2,line3])

v.pickloop()