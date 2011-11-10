from pygeo import *

v=display(scale=50,trace_on=True)

# testing of factory function for pickable and animated points in 3d space

                                                              # CLASS being called
#--------------------------------------------------

""" pickable points in space at initial x,y,z coords """

p1 = FreePoint(10.,-7,3,color=WHITE)                           #FreePoint 
p2 = FreePoint(-3,9,4,color=WHITE)                             #FreePoint
p3 = FreePoint(7,-14,-13,color=WHITE)                           #FreePoint   

#--------------------------------------------------

""" pickable points in space at initial x,y,z coords """

circle=CircumCircle(p1,p2,p3,level=2)                           #CircumCircle 


#--------------------------------------------------

""" animated point which moves along the circumference
of given circle at initial point determined by angle keyword
argument relative to circle _cpoint, defaults to PI,
circumnavigating the circle in the number of update
cylces given by the rate keyword argument"""

AniPoint(circle,angle=PI/3,color=BLUE,rate=36,trace=True)       #CirclingPoint


#--------------------------------------------------

""" line segment connecting given points """


line=Line(p1,p2,level=2,seg=True)                                #LineFromPoints

#--------------------------------------------------

"""animated point which moves along the given line
segment argument between the lines p1 and p2 attributes
with initial position determined as the
ratio on the line segment length """

AniPoint(line,color=MAGENTA,rate=36,trace=True)                  #LineSlider 


#--------------------------------------------------

""" line through given points """


line=Line(p1,p3,level=2,color=WHITE)                             #LineFromPoints


#--------------------------------------------------

"""animated point which moves along the given line
argument """

AniPoint(line,color=RED,rate=36,trace=True)                       #LineSlider 


v.animate(frames=37)