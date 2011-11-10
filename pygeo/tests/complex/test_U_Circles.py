from pygeo import *

v=display(scale=5,camera_vector=[0,4,-1])

# testing of factory function for circles of the unit sphere

                                                 # CLASS being called
#--------------------------------------------------

""" the unit sphere """

u=uSphere()                                     # uSphere()
#--------------------------------------------------

""" point that slides on the surface of
unit sphere """

u1=uSlider(phi=PI,theta=PI/2,color=GREEN)       # uSphereSlider
#--------------------------------------------------

""" points fixed on surface of unit sphere at
given theta and phi angles, using keyword arguments """

u2=uPoint(phi=PI/4,theta=PI/3*2,color=GREEN)    # uPolarPoint
u3=uPoint(phi=PI/3*2,theta=PI/3*2,color=GREEN)  # uPolarPoint
#--------------------------------------------------

""" circle of unit sphere through and
determined by 3 points """

uCircle(u1,u2,u3)                               # uCircumCircle
#--------------------------------------------------

""" fixed point in 3d space at given
x,y,z coords """

p1=rPoint(.5,.5,.5)                             # rPoint
#--------------------------------------------------

""" unconstrained pickable point in  3d space at given
x,y,z coords """

p2=rFreePoint(.7,.7,1,color=RED)             # R_FreePosition
#--------------------------------------------------

""" circle of the unit sphere cut by the plane
at the initial point argument that is normal
to the direction determined by the first and
second point arguments """

uCircle(p2,p1,color=CYAN)                       # uCircleFromNormal
#--------------------------------------------------

""" circle of unit sphere cut by the plane
polar to the point argument with respect
to the unit sphere """

uCircle(p2,color=RED)                           # uPolarCircle
#--------------------------------------------------

""" point at given x,y coords """

z1=zPoint(2,2)                                   # zPoint
#--------------------------------------------------

""" pickable point constrained to complex
plane at initial given x,y coords """

z2=zFreePoint(-1,-2)                          # zFreePoint
#--------------------------------------------------

""" circle on complex plane from
center,circumference points """

zc=zCircle(z1,z2,color=MAGENTA)                  # zCircleFromPoints
#--------------------------------------------------

""" circle on unit sphere determined by
projection of circle on complex plane """

uCircle(zc,color=MAGENTA)                        # z_to_uCircle
#--------------------------------------------------

""" line on complex plane through points
arguments """

zl=zLine(z1,z2,color=RED)                        # zLineFromPoints
#--------------------------------------------------

""" circle on unit sphere determined by
projection of line on complex plane """

uCircle(zl,color=RED)                            # z_to_uCircle
#--------------------------------------------------

v.pickloop()