from pygeo import *

v=display(title="Regulus",scale=200,axis=False,view_drag=True)

# demonstrates that the plane intersection with an arbitrary rgulus in
# space is a conic


# a line through 2 arbitrary points in space and a point 
# constrained to move on that line

A1=FreePoint(-105,-13.,107,color=RED,label='A1',pointsize=5)
B1=FreePoint(112,-111.0,-19,color=RED,label="B1",pointsize=5)
l1=Line(A1,B1,label="u1",linewidth=1)
C1=Slider(l1,color=RED,label="C1",pointsize=5)

# an additional  line through 2 arbitrary points in space and a point 
# constrained to move on that line

A2=FreePoint(119,19.,2.0,color=RED,label='A2',pointsize=5)
B2=FreePoint(-14,7,-111.,color=RED,label="B2",pointsize=5)
l2=Line(A2,B2,label="u2")
C2=Slider(l2,color=RED,label="C2",pointsize=5,ratio=2)

# the line connecting of point of each previous created line, and a
# range of points of that line
a=Line(A1,A2)
av1=PointArray(a,level=4)

# lines connecting the 2 additional points of each original line
b=Line(B1,B2)
c=Line(C1,C2)

# an array of transversals line, through the points of the point range
# and intersecting each of the other line arguments.
la1=LineArray(b,c,av1,color=CYAN,linewidth=1)

# 3 arbitrary points in space and the plane defined by them

p1=FreePoint(-1,-11.,10,color=DARKGRAY,pointsize=5,level=1)
p2=FreePoint(17,24.0,17,color=DARKGRAY,pointsize=5,level=1)
p3=FreePoint(9,-19.,-20.0,color=DARKGRAY,pointsize=5,level=1)
plane=Plane(p1,p2,p3,level=1,scale=20,color=LIGHTGRAY)


# the array of points of intersection of the plane and the transversal
# lines -  which form a conic

PointArray(plane,la1,color=YELLOW,pointsize=3)

v.pickloop()

