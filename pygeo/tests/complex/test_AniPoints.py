from pygeo import *

v=display(scale=5,camera_vector=[0,.1,-.1],delay=.5,trace_on=1)

                                                     # CLASS being called

""" pickable points constrained to complex
plane at initial given x,y coords """
z1=zFreePoint(1,-3,color=BLACK)                       #Z_FreePostion
z2=zFreePoint(-1,-1,color=BLACK)                      #Z_FreePostion
z3=zFreePoint(1,-1,color=BLACK)                       #Z_FreePostion


""" circles on complex plane through and determined by
three point arguments """

zcircle=zCircle(z1,z2,z3,level=2)                     #zCircumCircle
#--------------------------------------------------

""" point of complex plane moving on the circumference
of the circle argument at each update cycle"""

zAniPoint(zcircle,rate=36,trace=True,color=RED)      #zCirclingPoint
#--------------------------------------------------

""" line on complex plane through point arguments"""

zline=zLine(z1,z2,level=1)                           #zLineFromPoints
#--------------------------------------------------

""" point of complex plane moving on the line
argument at each update cycle"""

zAniPoint(zline,rate=36,trace=True)                  #zSlidingPoint
#--------------------------------------------------

""" circle on unit sphere determined by
projection of circle on complex plane """

ucircle=uCircle(zcircle,level=1)                      #z_to_uCircle
#--------------------------------------------------

""" point of unit sphere moving on the cirfcumference
of the circle argument at each update cycle"""

uc=uAniPoint(ucircle,level=1)                          #uCirclingPoint
#--------------------------------------------------


""" projection of given point on unit sphere to point
to complex plane """

zPoint(uc,trace=True)                                  #u_to_zPoint
#--------------------------------------------------

""" point moving on surface of unit sphere """

us=uAniPoint(trace=True,color=BLUE)                    #uSpiral
#--------------------------------------------------

""" projection of given point on unit sphere to point
to complex plane """

zPoint(us,trace=True)                                  #u_to_zPoint
#--------------------------------------------------

""" renderingof the unit sphere """

uSphere()                                              #uSphere
#--------------------------------------------------

#v.pickloop()
v.animate()