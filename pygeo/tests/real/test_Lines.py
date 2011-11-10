from pygeo import *

v=display(scale=50)

# testing of factory function for lines in 3d space

                                                           # CLASS being called
#--------------------------------------------------

""" pickable points in space at initial x,y,z coords """

p1 = FreePoint(10.,-7,3,color=WHITE)  #FreePoint
p2 = FreePoint(-3,9,4,color=WHITE)                             #FreePoint

#--------------------------------------------------

""" line through given points"""

line1=Line(p1,p2,label="A")                               #LineFromPoints

p3 = FreePoint(7,-14,3,color=WHITE)                             #FreePoint

#--------------------------------------------------

""" plane through given points"""

plane1=Plane(p1,p2,p3)                                          #PlaneFromPoints                                         

#--------------------------------------------------

"""pickable point constrained to given plane """

s1=Slider(plane1,17,11,2)                                       #PlaneSlider

#--------------------------------------------------

"""line through given point perpendiclar to given plane """


line2=Line(plane1,s1,label="B",color=BLUE)                #PlanePerp

#--------------------------------------------------

""" pickable points in space at initial x,y,z coords """

p1a = FreePoint(1.,17,-11,color=CYAN,level=2)                   #FreePoint
p2a = FreePoint(3,19,-7,color=RED,level=2)                     #FreePoint
p3a = FreePoint(3,-7,-4,color=WHITE,level=2)                     #FreePoint

#--------------------------------------------------

""" plane through given points"""

plane2=Plane(p1a,p2a,p3a,level=2)                                #PlaneFromPoints                                         

#--------------------------------------------------

""" line determined as intersection of given planes"""

line3=Line(plane1,plane2,level=2,color=RED,label="C")      #PlanesLine                                         
 
p4a = FreePoint(13,7,4,color=BLUE,level=2)                       #FreePoint

#--------------------------------------------------

""" line through given point parallel to given line,
on plane of line and point"""

line4=Line(line3,p4a,color=ORANGE,label="D",level=2)             #ParaLine                                         

#--------------------------------------------------

""" pickable points in space at initial x,y,z coords """

p5a = FreePoint(1,1,17,color=BLUE,level=3)                       #FreePoint

#--------------------------------------------------

""" line through given points"""

line5=Line(p4a,p5a,level=3)                                #LineFromPoints

#--------------------------------------------------

""" line connecting nearest point on two skew lines"""


line6 = Line(line5,line1,level=3,label="E"
             ,color=CYAN,seg=True)                        #NearLine

#--------------------------------------------------

""" pickable points in space at initial x,y,z coords """

p6a = FreePoint(10,-14,1,color=YELLOW,level=3)                     #FreePoint


#--------------------------------------------------

""" line through given point and intersecting with given lines"""

line7=Line(p6a,line1,line5,level=3
          ,color=YELLOW,label="F")                         #Transversal

#--------------------------------------------------

"""line through given point perpendiclar to given plane """

line8=Line(p6a,plane1,level=3
          ,color=BLUE,label="G")                         #PlanePerp



#CirclePolar - see test_Inversions
#ConicPolar - see test_Inversions
#PerpLine  - see test_FootPoints

v.pickloop()