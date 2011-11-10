
from pygeo import *

v=display(scale=50)

# testing of factory function for array of circles in 3d space

                                                               # CLASS being called
#--------------------------------------------------

""" pickable points in space at initial x,y,z coords """

p1 = FreePoint(10.,-7,3,label='p1',color=BLUE,fontsize=10)     #FreePoint     
p2 = FreePoint(-3,9,4,label="p2",color=WHITE)                  #FreePoint  

#--------------------------------------------------

""" line through point arguments """

line=Line(p1,p2)                                               #LineFromPoints

#--------------------------------------------------

""" sheaf of planes through given line """

planes=PlaneArray(line,level=3)                                #PlanePencil

#--------------------------------------------------

""" pickable points in space at initial x,y,z coords """

p1a = FreePoint(1.,-7,13,level=2)                              #FreePoint  
p2a = FreePoint(2,-2,-4,level=2)                               #FreePoint 

#--------------------------------------------------

""" sphere with first point at center, second point
on circumference"""

sphere=Sphere(p1a,p2a,level=2)                                 #CenterSphere  

#--------------------------------------------------

"""circles determined as the cross sections of the
sphere with the planes of the planes sheaf"""

ca=CircleArray(sphere,planes)                                     #CirclePencil


#--------------------------------------------------

""" pickable points in space at initial x,y,z coords """

p1b = FreePoint(27.,27,3,color=WHITE)                       #FreePoint
p2b = FreePoint(13,19,14,color=WHITE)                         #FreePoint
p3b = FreePoint(17,-24,31,color=WHITE)                        #FreePoint

#--------------------------------------------------

""" plane through points"""

plane2=Plane(p1b,p2b,p3b,color=BLUE)                             #Plane from Points                                         

#--------------------------------------------------

""" reflection of list elements in given plane """            #ReflectTransform


Transform(plane2,[ca])


v.pickloop()