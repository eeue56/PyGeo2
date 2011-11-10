from pygeo import *

v=display(scale=50)

# testing of factory function for lines in 3d space

                                                           # CLASS being called
#--------------------------------------------------

""" pickable points in space at initial x,y,z coords """

p1 = FreePoint(10.,-7,3,color=WHITE)  #FreePoint
p2 = FreePoint(-3,9,4,color=WHITE)                             #FreePoint
p3 = FreePoint(7,-14,3,color=WHITE)                             #FreePoint

#--------------------------------------------------

""" circle through given points"""

circle1=Circle(p1,p2,p3,CIRCUM)                               #CircumCircle

#--------------------------------------------------

"""pickable points constrained to plane of circle"""

s1=Slider(circle1,11,9,3)                                   #PlaneSlider
s2=Slider(circle1,1,-14,9)                                    #PlaneSlider
s3=Slider(circle1,-3,19,-4,color=RED)                                    #PlaneSlider

#--------------------------------------------------

"""line through given points"""

line1=Line(s1,s2,level=3)                                     #LineFromPoints
line2=Line(s1,s3,level=3)                                     #LineFromPoints

#--------------------------------------------------

"""segment of given line interior to given circle"""

c1=Chord(circle1,line1,color=RED)                                       #CircleChord                                    


#--------------------------------------------------

"""sphere with 1st point on center, 2bd point on surface"""

sphere1=Sphere(p1,p2,color=WHITE)                                #CenterSphere

#--------------------------------------------------

"""segment of given line interior to given sphere"""

c2=Chord(sphere1,line2,color=YELLOW)                            #CircleChord  


#--------------------------------------------------

"""with chord and seg keytwords, segment of polar
of circle with respect to given point that is 
interior to the circle"""

Line(circle1,s3,color=BLUE,chord=True,seg=True)                  #CirclePolar


#--------------------------------------------------

""" circle through given points"""


circle2=Circle(s1,s2,s3,CIRCUM)                                  #CircumCircle


#--------------------------------------------------

""" line segment connecting points of intsection
of circle arguments"""

c3=Chord(circle1,circle2,color=ORANGE)                            #BiChord


v.pickloop()