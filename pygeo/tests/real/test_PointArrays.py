
from pygeo import *

v=display(scale=50)

# testing of factory function for array of circles in 3d space

                                                               # CLASS being called
#--------------------------------------------------

""" pickable points in space at initial x,y,z coords """

p1 = FreePoint(10.,-7,3,color=WHITE)                            #FreePoint     
p2 = FreePoint(-3,9,4,color=WHITE)                              #FreePoint  
p3 = FreePoint(3,19,-4,color=WHITE)                              #FreePoint  

#--------------------------------------------------

""" line through point arguments """

line1=Line(p1,p2)                                               #LineFromPoints

#--------------------------------------------------

""" array of points equally spaced on line """

pa1=PointArray(line1)                                            #PointPencil

#--------------------------------------------------

""" circle through given points """

circle=Circle(p1,p2,p3,CIRCUM)                                  #CircumCircle 


#--------------------------------------------------

""" array of points equally spaced on circle """

pa2=PointArray(circle)                                          #CirclePoints

#--------------------------------------------------

""" plane through given points """


plane=Plane(p1,p2,p3)                                   #PlaneFromPoints

#--------------------------------------------------

""" array of equally angular lines through
given point on given plane"""


la=LineArray(p3,plane,color=WHITE)                                          #LinePencil  


#--------------------------------------------------

""" array of points of intersection of given line
with given array of lines"""

pa3=PointArray(la,line1,color=MAGENTA)                          #CirclingPencil


#--------------------------------------------------
"""pickable point constrained to given plane"""

s1=Slider(plane,-3,-20,16,level=2)                             #PlaneSlideer
s2=Slider(plane,-10,7,9,level=2)                               #PlaneSlider


#--------------------------------------------------
"""array of points on the conic determined
by the 5 given points"""

pa4=PointArray(p1,p2,p3,s1,s2,color=RED,level=2)                   #Conic


#--------------------------------------------------
"""line through given points"""

line2=Line(s1,s2,level=2,color=WHITE)                         #LineFromPoints

#--------------------------------------------------
"""pickable point constraind to given line"""

s3=Slider(line2,ratio=1.2,level=2,color=ORANGE)                #LineSlider
s4=Slider(line2,ratio=1.25,level=2,color=ORANGE)               #LineSlider


#--------------------------------------------------
"""an array of points of the line of the given points 
   with any 2 successive points having a cross ratio 
   equal to that of 3rd and 4th point with respect
   to 1st and 2nd point"""

pa5=PointArray(s1,s2,s3,s4,level=2,color=RED)                   #GrowthMeasure


#--------------------------------------------------
"""array of points harmonic with the given array
with respect to the given points"""

PointArray(pa2,p1,p2,color=MAGENTA,level=1)                     #Harmonics  

PointArray(pa5,s2,s3,color=YELLOW,level=1)                       #Harmonics

#--------------------------------------------------
"""array of line through given point and points
of given point array"""


la2=LineArray(p1,pa5,level=1)                                   #Lines

#--------------------------------------------------
"""array of points of intersection of lines of given
line arrays"""

PointArray(la,la2,pointsize=1.4,color=BLUE,level=1)             #ArrayIntersect

#--------------------------------------------------
"""array of points determined as poles of the 
given conic with respect to the lines of the 
given line array"""


PointArray(pa4,la2,level=1)                                     #CorrelationPoints


#--------------------------------------------------

""" pickable points in space at initial x,y,z coords """


p4 = FreePoint(13,9,-44,color=BLUE,level=3)                              #FreePoint  
p5 = FreePoint(1,-9,11,color=BLUE,level=3)                              #FreePoint  
p6 = FreePoint(-19,-19,1,color=BLUE,level=3)                              #FreePoint  


#--------------------------------------------------

""" palne through given points """

plane2=Plane(p4,p5,p6,level=2)                                             #PlaneFromPoints

#--------------------------------------------------
"""array of points of intersection of plane with lines of given
line array"""

PointArray(plane2,la2,level=2,color=RED)                                 #PlanePoints
PointArray(plane2,la,level=2,color=GREEN)                                #PlanePoints

v.pickloop()