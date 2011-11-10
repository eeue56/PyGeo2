from pygeo import *

v=display(scale=50)

# testing of factory function for circles in 3d space

                                                           # CLASS being called
#--------------------------------------------------

""" pickable points in space at initial x,y,z coords """

p1 = FreePoint(10.,-7,-13,color=WHITE)                       #FreePoint
p2 = FreePoint(-3,9,4,color=WHITE)                         #FreePoint
p3 = FreePoint(7,-14,23,color=WHITE)                        #FreePoint

#--------------------------------------------------

""" plane through points"""

plane1=Plane(p1,p2,p3,color=BLUE)                             #Plane from Points                                         

#--------------------------------------------------

"""plane through given points drawn as triangle"""

Triangle(p1,p2,p3)


#--------------------------------------------------

""" pickable points in space at initial x,y,z coords """

p1a = FreePoint(1.,-17,13,color=CYAN)                       #FreePoint
p2a = FreePoint(-13,-9,-4,color=WHITE,level=2)                         #FreePoint
p3a = FreePoint(17,-1,-3,color=WHITE,level=2)                        #FreePoint

#--------------------------------------------------

""" plane through point parallel to given plane"""

plane2=Plane(p1a,plane1,color=CYAN)                             #ParaPointPlane                                      

#--------------------------------------------------

""" linet through points"""

line1=Line(p1,p3,level=2)                                  #LineFromPoints
line2=Line(p1a,p3a,level=2)                                #LineFromPoints 

#--------------------------------------------------

""" plane through point parallel to given lines"""

plane3= Plane(line1,line2,p2a,level=2,color=ORANGE)                  #ParaLinesPlane

#--------------------------------------------------

""" plane through first point perpendicular to
lines through points"""

plane4= Plane(p3a,p2a,level=2,color=YELLOW)                  #PlaneFromNormal

#--------------------------------------------------

""" sphere through given points"""

sphere=Sphere(p2a,p3a,p1,p2,level=3)                               #CircumSphere

#--------------------------------------------------

""" pickable point in space at initial x,y,z coords """

p1b = FreePoint(1,-11,11,color=RED,level=3)                        #FreePoint


#--------------------------------------------------

""" plane polar to given point with respect to given 
sphere"""

plane5=Plane(sphere,p1b,level=3,color=RED)                        #PolarPlane


#--------------------------------------------------

""" center of sphere through given points """

center=Center(p2a,p3a,p1,p2,level=3)                             #TetraCenter   


#--------------------------------------------------

""" line through given points"""

line3=Line(center,plane5,level=3)                                #LineFromPoints

#--------------------------------------------------

"""point on plane interseting with the line perpendicular
to it from the point arguemnt"""


Foot(center,plane5,color=BLACK,level=3)                          #PlaneFoot

v.pickloop()