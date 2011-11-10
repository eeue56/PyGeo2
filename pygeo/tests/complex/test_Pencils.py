from pygeo import *
v=display(scale=5,camera_vector=[0,4,-1])

                                                       # CLASS being called
""" point on complex plane at given x,y coords """

z1=zPoint(2,2)                                        # zFixedPoint
#--------------------------------------------------

""" pickable points constrained to complex
plane at initial given x,y coords """

z2=zFreePoint(-1,-2)                               # zFreePosition
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

zc1a=zCircle(z1,z2,O="-")                             # zCircleFromPoints
#--------------------------------------------------

""" pencils of circles on complex plane determined by
given circles """

zp1=zCirclePencil(zc1,zc2)                                  # zCircles

zp2=zCirclePencil(zc1a,zc2,color=CYAN,level=2)                      # zCircles
#--------------------------------------------------

""" pencils of circles of unit sphere determined by
projection of pencil of the complex plane """
uStereoProject([zp1,zp2])
uCirclePencil(zp1)                                          # z_to_uCirclePencil
 #uCirclePencil(zp2,color=CYAN,style=FILL,level=2)                               # z_to_uCirclePencil
#--------------------------------------------------



""" unconstrained pickable 3d points """

r1=FreePoint(.5,.5,.5,color=GREEN,level=3,pointsize=.1)        # R_FreePosition
r2=FreePoint(.7,.6,-2.5,color=GREEN,level=3,pointsize=.1)      # R_FreePosition
#--------------------------------------------------

""" line in 3d space through given points """

rline=rLine(r1,r2,level=3)                            # rLine
#--------------------------------------------------

""" pencil of planes through given line """            # PlaneArray

pa=PlaneArray(rline,level=4)
#--------------------------------------------------

""" pencils of circles of unit sphere determined by
intersection of planes of plane pencil """

up=uCirclePencil(pa,level=3,color=YELLOW)                                # uSphereSlices
#--------------------------------------------------

""" pencils of circles on complex plane determined by
projection of pencil of circles of unit sphere """

zCirclePencil(up,level=3,color=YELLOW)                      # u_to_zCirclePencil
#--------------------------------------------------

v.pickloop()