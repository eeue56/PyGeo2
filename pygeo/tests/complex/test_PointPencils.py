from pygeo import *
v=display(scale=5,camera_vector=[0,4,-1])

                                                       # CLASS being called

""" pickable points constrained to complex
plane at initial given x,y coords """

z2=zFreePoint(-1,-2)                               # zFreePoint
z3=zFreePoint(1.5,-1)
#--------------------------------------------------

""" circle on complex plane from center &
circumference points """

zc1=zCircle(z2,z3)                                    # zCircleFromPoints
#--------------------------------------------------

zp=zPointArray(zc1)

zl=zLineArray(z2)

uStereoProject([zl,zp])
v.pickloop()