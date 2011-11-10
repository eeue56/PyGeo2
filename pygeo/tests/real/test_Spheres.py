from pygeo import *

v=display(scale=50)

# testing of factory function for spheres in 3d space

                                                           # CLASS being called
#--------------------------------------------------

""" pickable points in space at initial x,y,z coords """

A=FreePoint(-2.0,-12.,3.,label='A',color=RED)                #FreePoint
C=FreePoint(11,-7.0,1.,label='C',color=RED)                  #FreePoint 
B=FreePoint(1,7.0,4.,label='B',color=RED)                    #FreePoint 

#--------------------------------------------------

""" spheres with initial point as center, second point
on  circumference """

sphere1=Sphere(A,C)                                          #CenterSphere

#--------------------------------------------------

""" spheres orthogonal to given sphere, with given
point as Center"""

Sphere(sphere1,B,color=BLACK)                                #OrthoSphere


#--------------------------------------------------

""" pickable points in space at initial x,y,z coords """
p1=FreePoint(11.0,7.0,0.0,label="p1",color=BLUE,level=2)     #FreePoint
p2=FreePoint(-6.5,-3.5,0.,label="p2",color=BLUE,level=2)     #FreePoint
p3=FreePoint(-9,17,11,label="p3",color=BLUE,level=2)         #FreePoint
p4=FreePoint(9,7,1,label="p3",color=BLUE,level=2)            #FreePoint


#--------------------------------------------------

""" spheres through 4 given points """

Sphere(p1,p2,p3,p4,color=WHITE,level=2)                       #CircumSphere

v.pickloop()



