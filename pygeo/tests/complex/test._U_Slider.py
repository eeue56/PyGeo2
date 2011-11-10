from pygeo import *

# testing of factory function for constrained pickable points
# on unit sphere

v=display(scale=3,camera_vector=[0,4,-1])
                                                     # CLASS being called
""" the unit sphere """

u=uSphere()                                         # uSphere
#--------------------------------------------------

""" pickable 3d point constrained to surface of
unit sphere at initial default theta and phi angles
(0 & PI, respectively) """

u1=uSlider()                                        # uSphereSlider
#--------------------------------------------------

""" pickable 3d point constrained to surface of
unit sphere at initial given theta and phi angles -
using positional arguments """

u2=uSlider(theta=PI/2,phi=PI/4)                              # uSphereSlider
#--------------------------------------------------

""" pickable 3d point constrained to  surface of
unit sphere at initial given theta and default
phi angle (PI) - using positional argument """

u3=uSlider(phi=PI)                                    # uSphereSlider
#--------------------------------------------------

""" pickable 3d point constrained to  surface of
unit sphere at initial given theta and default
phi angle (PI) - using keyword argument """

uSlider(theta=PI/2,color=RED,level=2)               # uSphereSlider
#--------------------------------------------------

""" pickable 3d point constrained to surface of
unit sphere at initial given theta and phi angles -
using keyword arguments """

uSlider(theta=PI/2,phi=PI/4,color=CYAN,level=2)     # uSphereSlider
#--------------------------------------------------

""" circle of unit sphere through and
determined by 3 points """

c1=uCircle(u1,u2,u3)                                # uCircumCircle
#--------------------------------------------------


""" pickable 3d point constrained to circumferfence
of given circle argument at initial circumpoint -
using positional argument """

uSlider(c1,angle=PI/6,color=GREEN)                  # U_CirleSlider
#--------------------------------------------------

""" pickable 3d point constrained to circumerfence
of given circle argument at initial circumpoint -
using keyword arguments """

uSlider(c1,angle=PI/3,color=MAGENTA)                      # U_CirleSlider
#--------------------------------------------------

v.pickloop()