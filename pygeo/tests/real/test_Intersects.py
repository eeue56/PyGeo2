from pygeo import *

v=display(scale=50)

# testing of factory function for points defined as
# the intersection of geometric objects

                                                           # CLASS being called
#--------------------------------------------------

""" pickable points in space at initial x,y,z coords """

p1 = FreePoint(10.,-7,3,color=BLUE)              #FreePoint
p2 = FreePoint(-3,9,4,color=WHITE)               #FreePoint
p3 = FreePoint(38,10,3,color=WHITE)              #FreePoint
#--------------------------------------------------

""" plane through given points """

plane1= Plane(p1,p2,p3,color=WHITE,scale=10,level=3)        #PlaneFromPoints

p4 = Slider(plane1,8,1,-13)                      #PlaneSlider


#--------------------------------------------------

""" lines through given points """
 
line1=Line(p1,p2,color=BLACK,linewidth=.12)                  #LineFromPoints
line2=Line(p3,p4,color=BLACK,linewidth=.12)                  #LineFromPoints  


#--------------------------------------------------

""" point of intersection of the given lines"""

Intersect(line1,line2,color=RED,pointsize=1,label="A")                #LinesIntersect

#--------------------------------------------------
 
 
""" pickable points in space at initial x,y,z coords """

p1a = FreePoint(1.,7,-3,color=BLUE,level=2)       #FreePoint
p2a = FreePoint(13,-4,11,color=WHITE,level=2)     #FreePoint
p3a = FreePoint(8,-17,-19,color=WHITE,level=2)    #FreePoint
 
#--------------------------------------------------

""" plane through given points """

plane2= Plane(p1a,p2a,p3a,level=2,color=WHITE,scale=10)        #PlaneFromPoints
 

#--------------------------------------------------

""" point of intersection of the given line with
given plane"""

Intersect(line1,plane2,color=MAGENTA,pointsize=1.4,level=2,label="B1")    #PlaneLineIntersect
Intersect(line2,plane2,color=MAGENTA,pointsize=1.4,level=2,label="B2")    #PlaneLineIntersect


#--------------------------------------------------
 
 
""" pickable points in space at initial x,y,z coords """

p1b = FreePoint(-34.,17,12,color=BLUE,level=3)     #FreePoint
p2b = FreePoint(1,-14,1,color=WHITE,level=3)       #FreePoint
p3b = FreePoint(-8,7,29,color=WHITE,level=3)       #FreePoint
 
#--------------------------------------------------

""" plane through given points """

plane3= Plane(p1b,p2b,p3b,level=3,color=WHITE,scale=10)        #PlaneFromPoints


""" point of intersection of the given planes"""

Intersect(plane1,plane2,plane3,color=CYAN,
          pointsize=1.4,level=3,label="C")#PlanesIntersect



v.pickloop()