from pygeo import *

v=display(title="Line Conic",scale=35,panel=False,view_drag=False)

DENSITY=20

#two points on theline on the screen plane
A1 = FreePoint(-23,19,label="A1",color=RED,pointsize=1)
B1 = FreePoint(15,9,label="B1",color=RED,pointsize=1)

#the line connecting the two points
u1=Line(A1,B1,color=RED,linewidth=.3)

#a point constrained to move on the line
C1 = Slider(u1,ratio=1.4,label="C1",color=RED,pointsize=1)

#two points on theline on the screen plane
A2 = FreePoint(-20,-20,label="A2",color=RED,pointsize=1)
B2 = FreePoint(25,-19,label="B2",color=RED,pointsize=1)

#the line connecting the two points
u2=Line(A2,B2,color=RED,linewidth=.3)

#a point constrained to move on the line
C2 = Slider(u2,ratio=.4,label="C2",color=RED,pointsize=1)



#two lines from points of one reference line to points of other reference line
b1=Line(A2,B1)
b2=Line(A1,B2)

#the point of intersect of the lines crossing between reference lines
L=Intersect(b1,b2,label="L",color=BLACK)

#two additional lines from points of one reference line to points of other reference line
c1=Line(A2,C1)
c2=Line(A1,C2)

#the point of intersect of the additional crossing lines
M=Intersect(c1,c2,label="M",color=BLACK)


#the line connecting the points of intersection
w=Line(L,M,color=BLACK,seg=True)

#array of points along the line segment connecting the intersection points
pa=PointArray(w,level=2,density=DENSITY)

#arrays of lines from point of each reference line to array of
#points on intersection segment

paA1=LineArray(pa,A1,color=LIGHTGRAY)
paA2=LineArray(pa,A2,color=WHITE)

A2u1=PointArray(paA2,u1)

A1u2=PointArray(paA1,u2)

LineArray(A1u2,A2u1,color=BLUE)


paB1=LineArray(pa,B1,color=LIGHTGRAY)
B1u2=PointArray(paB1,u2)
paB2=LineArray(pa,B2,color=WHITE)
B2u1=PointArray(paB2,u1)
LineArray(B1u2,B2u1,color=RED)

paC1=LineArray(pa,C1,color=LIGHTGRAY)
C1u2=PointArray(paC1,u2)
paC2=LineArray(pa,C2,color=WHITE)
C2u1=PointArray(paC2,u1)
LineArray(C1u2,C2u1,color=GREEN)

a=Line(A1,A2,color=RED,linewidth=.3)
b=Line(B1,B2,color=RED,linewidth=.3)
c=Line(C1,C2,color=RED,linewidth=.3)
ac=Intersect(a,c)




v.pickloop()



