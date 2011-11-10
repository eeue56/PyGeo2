from pygeo import *

v=display(scale=70)

# testing of factory function for points defined as
# point from given poot to perpendiclar 
# foot of geiven geoemtric object
                                                           # CLASS being called
#--------------------------------------------------

""" pickable points in space at initial x,y,z coords """

p1 = FreePoint(10.,-7,-33,color=WHITE)             #FreePoint
p2 = FreePoint(-3,9,4,color=WHITE)                 #FreePoint
p3 = FreePoint(40,-3,0,color=WHITE)               #FreePoint

#--------------------------------------------------

""" plane through given points """

plane=Plane(p1,p2,p3)             #PlaneFromPoints

#--------------------------------------------------

""" pickable points in space constrined to given plane """

p1a = FreePoint(-50,-27,-32,color=WHITE)            #FreePoint


#--------------------------------------------------

"""point on plane interseting with the line perpendicular
to it from the point arguemnt"""

f1=Foot(plane,p1a,color=RED,pointsize=1,label="A")                        #PlaneFoot 

#--------------------------------------------------

"""line through point argument and perpendicular to
plane argument"""

Line(plane,f1)                                                  #PlanePerp

#--------------------------------------------------

"""line through point arguments"""

line=Line(p1,p2)                                                #LineFromPoints

#--------------------------------------------------


"""point on line interseting with the line perpendicular
to it from the point argument"""

f2=Foot(line,p3,color=ORANGE,pointsize=1,label="B")                       #LineFoot

#--------------------------------------------------

"""line through 2nd point argument, perpendicular
to line through 1st and 2nd point arguemtns, on
plane dtermined by 3 point arguments"""

Line(p1,f2,p3,color=RED)                                     #LinePerp

v.pickloop()

