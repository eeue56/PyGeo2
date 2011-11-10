from pygeo import *

v=display(scale=50)

# testing of factory function for points defined as
# reflections in geometric objects

                                                           # CLASS being called
#--------------------------------------------------

""" pickable points in space at initial x,y,z coords """

p1 = FreePoint(10.,-7,-33,label="p1",color=BLUE)              #FreePoint
p2 = FreePoint(-3,9,4,label="p2",color=WHITE)                 #FreePoint
p3 = FreePoint(38,10,3,label="p3",color=WHITE)                #FreePoint
p4 = FreePoint(0,0,13,label="p4",color=WHITE)                 #FreePoint

#--------------------------------------------------

""" plane through given points """

plane1= Plane(p1,p2,p3,color=WHITE,scale=10)                  #PlaneFromPoints

#--------------------------------------------------


""" reflection of the given point in the given plane """

Reflection(plane1,p4,color=RED,pointsize=2)                   #PlaneReflection

#--------------------------------------------------

""" line through given points"""

line=Line(p1,p2)                                              #LineFromPoints 

""" reflection of the given point in the given line on
the plane of the line and point"""

Reflection(line,p4,color=BLUE,pointsize=2)                    #LineReflection


v.pickloop()

