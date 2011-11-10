
from pygeo import *

v=display(scale=50)

# testing of factory function for array of circles in 3d space

                                                               # CLASS being called
#--------------------------------------------------

""" pickable points in space at initial x,y,z coords """

p1 = FreePoint(10.,-7,3,color=WHITE)                            #FreePoint     
p2 = FreePoint(-3,9,-30,color=WHITE)                              #FreePoint  
p3 = FreePoint(-14,-12,-17,color=RED)                              #FreePoint  
p4 = FreePoint(31,9,7,color=WHITE)                              #FreePoint  
p5 = FreePoint(36,-4,7,color=WHITE)                              #FreePoint  
p6 = FreePoint(22,22,-20,color=WHITE)                              #FreePoint  


plane=Plane(p1,p2,p3,level=5)



#--------------------------------------------------

""" line2 through point arguments """

line1=Line(p1,p2)                                               #LineFromPoints
line2=Line(p3,p4)                                               #LineFromPoints
line3=Line(p5,p6)                                               #LineFromPoints


#--------------------------------------------------

"""array of lines through point on given plane"""

la=LineArray(plane,p3,color=WHITE,level=2)                     #LinePencil



#--------------------------------------------------

"""array of points of intersection of given line with
lines of given line array"""

pa1=PointArray(line1,la,color=YELLOW)                          #CirclingPencil



#--------------------------------------------------

"""array of lines through points of point array
and intersecting the given lines"""

LineArray(line2,line3,pa1,color=YELLOW)                         #Regulus


#--------------------------------------------------

"""array of points equally spaced on segment between
between p1 and p2 of given line"""

pa2=PointArray(line2,seg=True)                                  #PointPencil


#--------------------------------------------------

"""array of lines connecting points of given point arrays"""

LineArray(pa1,pa2,level=2,color=RED)                            #ArrayMap


#--------------------------------------------------

"""array2 of lines connecting given point with
points of given point array"""

LineArray(p6,pa1,level=4,color=ORANGE)                           #Lines
LineArray(p5,pa2,level=4,color=ORANGE)                           #Lines

#--------------------------------------------------

"""pencil of planes on given line"""


pp1=PlaneArray(line2,level=6)                                    #PlanePencil
pp2=PlaneArray(line3,level=6)                                    #PlanePencil


#--------------------------------------------------

"""array of lines of intersection of
planes of given array of planes"""

LineArray(pp1,pp2,level=3,color=CYAN)                           #PlanesPencilIntersect   


#--------------------------------------------------

"""pickable point constrained to given line"""

s1=Slider(line1,ratio=1.3)                                     #LineSlider
s2=Slider(line2,ratio=-.3)                                     


#--------------------------------------------------

"""array of lines connecting points of the projective 
correspondance defined by the first 3 given points and 
the second 3 given points"""

LineArray([p1,p2,s1],[p3,p4,s2])                               #PointMap


s4=Slider(plane,11,-17,-11,level=5,label="S4")
s5=Slider(plane,15,17,1,level=5,label="S5")

conic=PointArray(p1,p2,p3,s4,s5,level=5)

LineArray(conic,pa1,level=5,color=RED)
LineArray(conic,pa2,level=5,color=ORANGE)



v.pickloop()