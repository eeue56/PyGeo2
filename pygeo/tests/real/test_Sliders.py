from pygeo import *

v=display(scale=50)

# testing of factory function for pickable and animated points in 3d space

                                                              # CLASS being called
#--------------------------------------------------

""" pickable points in space at initial x,y,z coords """

p1 = FreePoint(10.,-7,3,color=WHITE)                           #FreePoint 
p2 = FreePoint(-3,9,4,color=WHITE)                             #FreePoint
p3 = FreePoint(7,-14,13,color=WHITE)                           #FreePoint   

#--------------------------------------------------

""" pickable points in space at initial x,y,z coords """

circle=CircumCircle(p1,p2,p3)                                  #CircumCircle 


#--------------------------------------------------

""" pickable point constrained to the circumference
of given circle at initial point determined by angle keyword
argument relative to circle _cpoint, defaults to PI"""

Slider(circle,color=BLUE)                                      #CircleSlider

#--------------------------------------------------

""" sphere with initial point as center, second point
on  circumference """


sphere= Sphere(p1,p2)                                          #CenterSphere

#--------------------------------------------------

""" pickable point constrained to the surface 
of given sphere at initial point determined by theta and
phi keyword arguments"""

Slider(sphere,color=RED,theta=-PI/3,level=1,label="S2")         #SphereSlider

#--------------------------------------------------

"""plane through 3 given point arguments """

plane=Plane(p1,p2,p3,color=WHITE,scale=10)                      #PlaneFromPoints 

#--------------------------------------------------

"""pickable point constrained to the given plane
argument with initial position on plane closest
to to xyz coordinate argumens"""

Slider(plane,(-31,3,7),color=CYAN)                              #PlaneSlider  

#--------------------------------------------------

"""line through 2 given point arguments """

line=Line(p1,p2)                                                #LineFromPoints

"""pickable point constrained to the given line
argument with initial position determined as the
ratio on the line segment length from the lines p1
and p2 attributes"""

Slider(line,color=MAGENTA,ratio=1.7)                            #LineSlider 



v.pickloop()