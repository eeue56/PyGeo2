from pygeo import *

# testing of factory function for fixed points on complex plane
v=display(scale=5,camera_vector=[0,4,-1])


                                       # CLASS being called

""" point at origin """

#O = zPoint()
#--------------------------------------------------

""" point on complex plane at given x,y coords """

#z1 = zPoint(1,-2)                        # zFixedPoint
z1=zPoint(1-2j)
#--------------------------------------------------

""" pickable point constrained to complex
plane at initial given x,y coords """

z2 = zFreePoint(-2,-2,color=GREEN)                # zFreePoint
#--------------------------------------------------
#zRotation(z1,z2,angel=PI/3)
""" point on complex plane at given polar corrdinates """

zc1 = zCircle(z1,z2)                     # zCircleFromPoints
#--------------------------------------------------

""" pickable point constrained to move on given circle"""

z6 = zSlider(zc1,color=BLUE,angle=-PI/3)           # zCircleSlider
#--------------------------------------------------

""" line trhough given points"""

zl1= zLine(z1,z2)                                  #zLineFromPoints

#--------------------------------------------------

""" pickable point constrained to move on given line"""

zSlider(zl1,ratio=.3,color=RED)                    #ZLineSlider

v.pickloop()