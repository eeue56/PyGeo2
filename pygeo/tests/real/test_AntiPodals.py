from pygeo import *

v=display(scale=70)

# testing of factory function for points defined as
# opposite to a given point with respect to a given
#object
                                                           # CLASS being called
#--------------------------------------------------

""" pickable points in space at initial x,y,z coords """

p1 = FreePoint(10.,-7,-3,color=WHITE)             #FreePoint
p2 = FreePoint(-3,9,4,color=WHITE)                 #FreePoint
p3 = FreePoint(40,-3,0,color=WHITE)                #FreePoint


#--------------------------------------------------

""" circle through given points """

circle=CircumCircle(p1,p2,p3,level=1,color=WHITE)              #CircumCircle

#--------------------------------------------------

""" pickable point in constrined to given circle """

s1 = Slider(circle,angle=PI/3,label="s1",color=BLUE)            #CircleSlider


#--------------------------------------------------

"""point on circle opposite to given point"""

a1=AntiPodal(circle,s1,color=RED,pointsize=1,label="A1")         #CircleAntiPodal 

#--------------------------------------------------

"""plane through given points"""

plane = Plane(p1,p2,p3,level=4)                                   #PlaneFromPoints


#--------------------------------------------------

"""pickable point constrained to given plane"""

v1=Slider(plane,14,-44,-20,label="v1",color=GREEN,)               #PlaneSlider

#--------------------------------------------------

"""line through given points"""

line=Line(v1,s1,color=WHITE)                                       #LineFromPoints

#--------------------------------------------------

"""segment of given line contained in given circle"""
chord=Chord(line,circle)                                          #CircleChord


#--------------------------------------------------

"""end point of line segment opposite the
endpoint indicated by keyword argument"""

AntiPodal(chord,opposite=s1,label="A2",pointsize=1.4)              #SegPoint               

#--------------------------------------------------

""" spheres with initial point as center, second point
on  circumference """

sphere=Sphere(p1,p2,color=WHITE,level=2)                           #CenterSphere

#--------------------------------------------------

"""pickable point constrained to given sphere"""

s2=Slider(sphere,label="s2",color=BLUE,pointsize=1.4)              #SphereSlider


#--------------------------------------------------

"""point on sphere opposite to given point"""

AntiPodal(sphere,s2,color=RED,pointsize=1.4,level=2,label="A3")    #SphereAntiPodal


v.pickloop()

