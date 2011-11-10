from pygeo import *

v=display(scale=70)

# testing of factory function for points defined as
# points diving lines or circles

                                                           # CLASS being called
#--------------------------------------------------

""" pickable points in space at initial x,y,z coords """

p1 = FreePoint(10.,-7,-33,label="p1",color=WHITE)             #FreePoint
p2 = FreePoint(-3,9,4,label="p2",color=WHITE)                 #FreePoint 

p1a = FreePoint(40,-3,0,label="p1a",color=WHITE)              #FreePoint


#--------------------------------------------------

""" plane through given points """

plane=Plane(p1,p2,p1a,level=5)                                 #PlaneFromPoints

#--------------------------------------------------

""" pickable points in space constrined to given plane """

p2a = FreePoint(-50,-27,-32,label="p2a",color=WHITE)            #FreePoint


#--------------------------------------------------

""" line through given points"""

line1=Line(p1,p2)                                              #LineFromPoints 
line2=Line(p1a,p2a,level=1)                                    #LineFromPoints  

#--------------------------------------------------
"""point on line dividing the segment from the
line's p1 to p2 by the ratio keyword argument"""

d1=Divider(line1,ratio=.4,color=RED,pointsize=.7,label="d1")   #LineDivider

#--------------------------------------------------
"""point on line dividing the segment from p1 to
the distance between the point arguments"""                    

d2=Divider(line1,p1a,p2a,color=BLUE,pointsize=.7,label="d2")    #LineCut

#--------------------------------------------------
"""point on line harmonic to first point arguemtn
with respect to second and third point arguements"""                  

h1=Divider(d2,p1,p2,color=GREEN,pointsize=.7,label="h1")        #Harmonic


#--------------------------------------------------
"""pickable point constrained to line argument with
initial position determined by ratio keyowd argument"""                  

s1=Slider(line2,ratio=.7,level=1,label="s1")                   #LineSlider  


#--------------------------------------------------
"""point equalizing the cross ratio of the set of
three points to that of the set of four points"""                  

Divider([p1,p2,d1,d2],[p1a,p2a,s1],level=4,
         color=BLUE,pointsize=.7,label="c1")                    #CrossPoint  

#--------------------------------------------------
"""circle through 3 points"""                  

circle = Circle(p1,p2,p1a,CIRCUM,level=2)                      #CircumCircle

#--------------------------------------------------

"""point on cirumference of given circle, at angle
of given kewyord arguemtn from circles _cpoint)"""

Divider(circle,angle=PI/3,color=CYAN,pointsize=.7,level=2)     #CircumPoint
Divider(circle,angle=PI*2/3,color=CYAN,pointsize=.7,level=2)   #CircumPoint 


#draw harmonic synthetically

line3=Line(d2,p1a,color=WHITE,linewidth=.1,level=3)            #LineFromPoints  
s2=Slider(line3,color=WHITE,level=3,label="s2")                #LineSlider
line4=Line(p2,s2,color=WHITE,linewidth=.1,level=3)             #LineFromPoints 
line5=Line(p1,p1a,color=WHITE,linewidth=.1,level=3)            #LineFromPoints  
line6=Line(p2,p1a,color=WHITE,linewidth=.1,level=3)            #LineFromPoints 
line7=Line(p1,s2,color=WHITE,linewidth=.1,level=3)             #LineFromPoints 
v1=Intersect(line4,line5,color=WHITE,level=3)                  #LinesIntersect 
v2=Intersect(line6,line7,color=WHITE,level=3)                  #LinesIntersect  
Line(v1,v2,color=RED,linewidth=.1,level=3)                     #LineFromPoints

#draw crosspoint synthetically

l1=Line(s1,d1,color=WHITE,linewidth=.1,level=4)               #LineFromPoints  
O=Slider(l1,ratio=1.3,label='O',color=GREEN,level=4)          #LineSlider 
plane=Plane(p1,d1,s1,level=5)                                 #PlaneFromPoints
m=Slider(plane,level=4,color=WHITE,label="m")                 #PlaneSlider
m1=Line(s1,m,color=WHITE,linewidth=.1,level=4)                #LineFromPoints
l2=Line(p1,O,color=WHITE,linewidth=.1,level=4)                #LineFromPoints   
l3=Line(p2,O,color=WHITE,linewidth=.1,level=4)                #LineFromPoints 
l4=Line(d2,O,color=WHITE,linewidth=.1,level=4)                #LineFromPoints
r=Intersect(m1,l3,label='r',color=DARKGRAY,level=4)           #LinesIntersect 
s=Intersect(m1,l2,label='s',color=DARKGRAY,level=4)           #LinesIntersect
x=Intersect(m1,l4,label='x',color=DARKGRAY,level=4)           #LinesIntersect
as=Line(p1a,s,color=LIGHTGRAY,linewidth=.1,level=4)           #LineFromPoints
br=Line(p2a,r,color=LIGHTGRAY,linewidth=.1,level=4)           #LineFromPoints
o=Intersect(as,br,label='o',color=DARKGRAY,level=4)                   #LinesIntersect 
ox=Line(o,x,color=RED,linewidth=.1,level=4)                   #LineFromPoints


v.pickloop()

