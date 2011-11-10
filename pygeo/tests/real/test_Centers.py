from pygeo import *

v=display(scale=50)

# testing of factory function for points defined as
# "centers" of geometric objects

                                                           # CLASS being called
#--------------------------------------------------

""" pickable points in space at initial x,y,z coords """

p1 = FreePoint(10.,-7,3,color=BLUE)              #FreePoint
p2 = FreePoint(-3,9,4,color=WHITE)               #FreePoint
p3 = FreePoint(38,10,3,color=WHITE)              #FreePoint
p4 = FreePoint(8,1,-13,color=WHITE,level=4)      #FreePoint

#--------------------------------------------------

""" circle through given points"""

ccircle=Circle(p1,p2,p3,CIRCUM)                              #CircumCircle                                         


#--------------------------------------------------

""" triangle with p1,p2,p3 as vertices"""
 
t1=Line(p1,p2,color=BLACK,linewidth=.12)                      #LineFromPoints
t2=Line(p1,p3,color=BLACK,linewidth=.12)                      #LineFromPoints  
t3=Line(p2,p3,color=BLACK,linewidth=.12)                      #LineFromPoints   


#--------------------------------------------------

""" circumcenter of the triangle defined by
the 3 points as vertices"""

A=Center(p1,p2,p3,color=RED,label="A")                                 #CircumCenter

#--------------------------------------------------

""" centroid of the triangle defined by
the 3 points as vertices"""

B=Center(p1,p2,p3,CENTROID,color=GREEN,label="B")                      #Centroid

#--------------------------------------------------

""" midpoints of the given lines"""

d1=Divider(t1,ratio=.5,level=2)                               #LineDivider 
d2=Divider(t2,ratio=.5,level=2)                               #LineDivider   
d3=Divider(t3,ratio=.5,level=2)                               #LineDivider


#--------------------------------------------------

""" lines connecting the point arguments"""

Line(p3,d1,level=2,color=WHITE,linewidth=.1)                  #LineFromPoints
Line(p2,d2,level=2,color=WHITE,linewidth=.1)                  #LineFromPoints  
Line(p1,d3,level=2,color=WHITE,linewidth=.1)                  #LineFromPoints 


#--------------------------------------------------

""" orthocenter of the triangle defined by
the 3 points as vertices"""

C=Center(p1,p2,p3,ORTHO,color=MAGENTA,label="C")                       #OrthoCenter

#--------------------------------------------------

""" point on given line intersecting with 
the perpendicular to it from the given point"""

f1=Foot(p1,t3,level=3,color=WHITE)                            #LineFoot
f2=Foot(p2,t2,level=3,color=WHITE)                            #LineFoot 
f3=Foot(p3,t1,level=3,color=WHITE)                            #LineFoot

#--------------------------------------------------

""" lines connecting the point arguments"""

Line(f1,p1,level=3,color=WHITE,linewidth=.1)                   #LineFromPoints
Line(f2,p2,level=3,color=WHITE,linewidth=.1)                   #LineFromPoints  
Line(f3,p3,level=3,color=WHITE,linewidth=.1)                   #LineFromPoints 


#--------------------------------------------------

""" center of the circle inscribale in the triangle 
defined by the 3 points as vertices"""

D=Center(p1,p2,p3,INCENTER,color=MAGENTA,label="D")                     #InCenter

#--------------------------------------------------

""" circle inscribed in the triangle 
defined by the 3 points as vertices"""

Circle(p1,p2,p3,INSCRIBED,color=WHITE)                          #InscribedCircle

#--------------------------------------------------

""" center of the circle exscribale in the triangle 
defined by the 3 points as vertices, tangent to the
triangle line opposite the first point arguement"""

E1=Center(p1,p2,p3,EXCENTER,color=CYAN,label="E1")                         #ExCenter
E2=Center(p2,p1,p3,EXCENTER,color=CYAN,label="E2")                         #ExCenter
E3=Center(p3,p1,p2,EXCENTER,color=CYAN,label="E3")                         #ExCenter

#--------------------------------------------------

""" circle exscribed in the triangle with p1,p2,p3 as vertices,
tangent to the side opposite to the first point argument"""

Circle(p1,p2,p3,EXSCRIBED,color=WHITE)                           #ExscribedCircle
Circle(p2,p1,p3,EXSCRIBED,color=WHITE)                           #ExscribedCircle
Circle(p3,p1,p2,EXSCRIBED,color=WHITE)                           #ExscribedCircle


#--------------------------------------------------

""" center of the sphere through the 4 given points"""

F=Center(p1,p2,p3,p4,level=4,color=BLUE,pointsize=2,label="F")   #SphereCenter                                       #TetraCenter 


#--------------------------------------------------

""" sphere through the 4 given points"""

Sphere(p1,p2,p3,p4,level=4)                                      #CircumSphere 

v.pickloop()