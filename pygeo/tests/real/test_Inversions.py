from pygeo import *

v=display(scale=50)

# testing of factory function for points defined as
# inverse to geometric objects

                                                           # CLASS being called
#--------------------------------------------------

""" pickable points in space at initial x,y,z coords """

p1 = FreePoint(10.,-7,3,color=BLUE)              #FreePoint
p2 = FreePoint(-3,9,4,color=WHITE)               #FreePoint 
p3 = FreePoint(38,10,3,color=WHITE)              #FreePoint
p6 = FreePoint(0,0,13,color=WHITE)       #FreePoint

#--------------------------------------------------

""" plane through given points """

plane1= Plane(p1,p2,p3,color=WHITE,scale=10,level=3)        #PlaneFromPoints

#--------------------------------------------------

""" pickable point constrained to given plane """

p4 = Slider(plane1,21,-5,3)                      #PlaneSlider
p5 = Slider(plane1,18,11,-1)                     #PlaneSlider


#--------------------------------------------------

""" circle through given points """
 
circle=Circle(p1,p2,p3,CIRCUM)                              #CircumCircle


p7=Slider(plane1,2,2,2,color=RED,pointsize=1.5)

#--------------------------------------------------

""" point inverse to given point with respect to given line"""

ipoint=Inversion(circle,p4,color=RED,pointsize=1.4,label = "A")          #CircleInversion

#--------------------------------------------------

""" line polar to given point with respect to given circle"""

tc=Line(circle,p4,seg=False,chord=False)                     #CirclePolar  

#--------------------------------------------------

""" point on given line intersecting with perpendiclular
from given point"""

Foot(p4,tc,level=2)                                          #LineFoot 

#--------------------------------------------------

""" pole of given line with respect to given circle"""

cpoint=Inversion(circle,tc,color=RED,pointsize=1.4,level=2,label="B")  #CirclePole

#--------------------------------------------------

""" array of points on conic through 5 given points"""

conic=Conic(p1,p2,p3,p4,p5,level=1)                          #Conic

#--------------------------------------------------

""" pole of given line with respect to given conic"""

cpoint2=Inversion(conic,tc,color=BLUE,pointsize=2,label="C")   #ConicPole


#--------------------------------------------------

""" polar of given point with respect to given conic"""

tc2=Line(conic,p7,color=BLUE,chord= False,level=2)     #ConicPolar


#--------------------------------------------------

""" spheres with initial point as center, second point
on  circumference """

sphere = Sphere(p6,p4,level=3)                              #CenterSphere

#--------------------------------------------------

""" pole of given plane with repsect to given sphere """    

Inversion(sphere,plane1,level=3,color=MAGENTA,pointsize=1.4,label="D") #SpherePole


""" inverse of given point with repsect to given sphere """    

Inversion(sphere,p2,level=3,color=BLUE,pointsize=1.4,label="E")        #SphereInversion


v.pickloop()

