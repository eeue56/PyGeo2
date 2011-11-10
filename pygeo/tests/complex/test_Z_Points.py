from pygeo import *

# testing of factory function for fixed points on complex plane
v=display(scale=5,camera_vector=[0,4,-1])


                                       # CLASS being called

""" point at origin """

O = zPoint(color=GREEN)
#--------------------------------------------------

""" point on complex plane at given x,y coords """

z1 = zPoint(1,-2)                        # zFixedPoint
#--------------------------------------------------

""" pickable point constrained to complex
plane at initial given x,y coords """

z2 = zFreePoint(-2,-2)                # zFreePoint
#--------------------------------------------------
zRotation(z1,z2,angle=PI/3)
""" point on complex plane at given polar corrdinates """

z3 = zPoint(angle=PI/6,dist=4,color=BLACK)     # zPolarPoint
#--------------------------------------------------

""" conjugate of argument point """

z4 = zPoint(z2,color=RED)                # zConjugate
#--------------------------------------------------

""" point orthogonal to argument point """

z5 = zPoint(z4,alt=ORTHO,color=RED)          # zOrthoPoint
#--------------------------------------------------

""" circle on complex plane from center, circumference point """

zc1 = zCircle(z1,z2)                     # zCircleFromPoints
#--------------------------------------------------

""" inverse of argument point with respect
to argument circle """


z6 = zPoint(z3,zc1,color=BLACK)           # zInversePoint
#--------------------------------------------------

""" circle through and determined by argument points """

zc2 = zCircle(z3,z4,z5,color=CYAN)       # zCircumCircle
#--------------------------------------------------


""" point as power of given circle arguments """

z7 = zPoint(zc1,zc2,color=BLUE,level=3)          # zPowerPoint
#--------------------------------------------------

""" point on circumference of circle at given angle -
 using keyword argument """

z8 = zPoint(zc2,color=BLUE,angle=PI/3)    # zCircumPoint
#--------------------------------------------------

""" 3d point on surface of unit sphere at intial theta and
 phi angles -  using positional arguments """

u = uSlider(theta=PI/5*3,phi=PI/9*7,level=2,color=MAGENTA)       # uSphereSlider
#--------------------------------------------------

""" projection of given point on unit sphere to point
to complex plane """

z10 = zPoint(u,color=MAGENTA,level=2)    # R_tozPoint
#--------------------------------------------------

""" the unit sphere """

s=uSphere(level=2)                     # uSphere
#--------------------------------------------------

""" line in 3d space from north pole of unit sphere to
projection point. """

#rLine(s.N,z10,level=2)                   # rLine
#--------------------------------------------------

""" point harmonic to first argument with respect to
second and third argument """

zPoint(z3,z4,z5,color=MAGENTA,level=2)            # zHarmonic
#--------------------------------------------------

""" point transormed by the Moebius transformation determined 
    by the 2 set of 3 points"""

zPoint([z1,z2,z3,z7],[z4,z5,z6],color=MAGENTA,level=2)            # zCrossPoint
#--------------------------------------------------


v.pickloop()