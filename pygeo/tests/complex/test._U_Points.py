from pygeo import *


v=display(scale=6,camera_vector=[0,4,-1],drag_view=False)

# testing of factory function for points on the unit sphere

                                                    # CLASS being called

""" unit sphere """

u=uSphere(color=WHITE)                                        # uSphere
#--------------------------------------------------

""" point on unit sphere at default theta and phi
angles (0 & PI, respectively) """

u1=uPoint()                             # uPolarPoint
#--------------------------------------------------

""" pickable point constrained to complex
plane at initial given x,y coords """

z=zFreePoint(-1,-1,pointsize=.1)                             # zFreePoint
#--------------------------------------------------


""" projection of given complex point to
the unit sphere """


u2=uPoint(z,color=MAGENTA)                         # z_to_uPoint
#--------------------------------------------------

"""point on unit sphere at given theta and phi angles
using postional arguments """

u3=uPoint(theta=PI/2,phi=PI/4*3,color=RED)                   # uPolarPoint
#--------------------------------------------------

""" point on unit sphere at given theta angle,
default phi angle, using positional arguments """

u4=uPoint(theta=PI/2*3,color=BLUE)                          # uPolarPoint
#--------------------------------------------------



""" pickable pointy on unit sphere at given theta
and phi angles """

u5=uSlider(theta=PI/4*5,phi=PI/2*3,color=RED)                # uSphereSlider
#--------------------------------------------------

""" circle through and determined by 3 points """

circle=uCircle(u1,u2,u5)                            # zCircumCircle
#--------------------------------------------------

""" point on unit sphere inverse to given point
with respect to given circle """

uPoint(circle,u5,color=RED)                        # uInversePoint
#--------------------------------------------------

"""point on unit sphere antipodal (opposite)
to given point """

uPoint(u2,color=MAGENTA)                            # uAntiPodal
#--------------------------------------------------
v.pickloop()