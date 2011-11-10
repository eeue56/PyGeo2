from pygeo import *

v=display(scale=50)

# testing of factory function for circles in 3d space

                                                           # CLASS being called
#--------------------------------------------------

""" pickable points in space at initial x,y,z coords """

p1 = FreePoint(10.,-7,3,label="p1",color=BLUE,fontsize=10)  #FreePoint
p2 = FreePoint(-3,9,4,label="p2",color=WHITE)               #FreePoint
p3 = FreePoint(7,-14,3,label="p3",color=WHITE)              #FreePoint

#--------------------------------------------------

""" circle wtih center a p1,with p2 as point on circumference,
on the plane determined by points p1,p2,p3"""

ccircle=Circle(p1,p2,p3)                                     #CenterCircle                                         


#--------------------------------------------------

""" triangle with p1,p2,p3 as vertices"""
 
triangle=Triangle(p1,p2,p3)                                  #Triangle                           

#--------------------------------------------------

""" circle inscribed in the triangle with p1,p2,p3 as vertices"""

icircle=Circle(p1,p2,p3,INSCRIBED,color=RED)                 #InscribedCircle 


#--------------------------------------------------

""" circle exscribed in the triangle with p1,p2,p3 as vertices,
tangent to the side opposite to the first point argument"""


ecircle1=Circle(p1,p2,p3,EXSCRIBED,color=MAGENTA)             #ExscribedCircle 
ecircle2=Circle(p2,p1,p3,EXSCRIBED,color=MAGENTA)             #ExscribedCircle
ecircle3=Circle(p3,p1,p2,EXSCRIBED,color=MAGENTA)             #ExscribedCircle


#--------------------------------------------------

""" pickable point constrained to circle argment"""

p4 = Slider(ccircle,angle=PI/4,label="p4",color=RED)          #CircleSlider


#--------------------------------------------------

""" circle through 3 point arguments"""

ccircle=Circle(p1,p2,p4,CIRCUM,color=ORANGE)                   #CircumCircle

#--------------------------------------------------

""" circle orthoganal to given circle,
with given point as center"""

ocircle=Circle(icircle,p4,color=CYAN,style=FILL)               #OrthoCircle  

#--------------------------------------------------

""" pickable points in space at initial x,y,z coords """

p1a = FreePoint(1.,-7,13,level=2)                              #FreePoint
p2a = FreePoint(2,-2,-4,level=2)                               #FreePoint 

#--------------------------------------------------

""" spheres with initial point as center, second point
on  circumference """

sphere1=Sphere(p1a,p2a,level=2)                                #CenterSphere
sphere2=Sphere(p4,p2a,level=2)                                 #CenterSphere 

#--------------------------------------------------

"""circle determined as the intersection of the 
2 sphere arguments"""

scircle=Circle(sphere1,sphere2,level=2)                        #SpheresIntersect

#--------------------------------------------------

"""plane through 3 point arguments"""

plane=Plane(p1,p1a,p2a,level=2,scale=10)                       #PlaneFromPoint

#--------------------------------------------------

"""circle with center at first point, radius =
to the distance between first and secoond point, 
on given plane"""

pcircle=Circle(p1,p2a,plane, level=2, color=CYAN)               #SpheresIntersect

"""circles determined as the cross section of the
sphere with the plane"""

Circle(sphere1,plane, color=RED, level=2)                        #SphereCircle
Circle(sphere2,plane, color=RED, level=2)                        #SphereCircle


v.pickloop()