from pygeo import *


instruction ="""Pick and drag any of the five red points
determining the conic.  Increase view level to view
construction of tangent lines at points"""

explanation = """A pentagon exscribed around a
the conic dtermined by 5 points on a plane"""

v=display(title="Pentagon Exscribed Around a Conic",scale=50,axis=False,instruction = instruction,explanation=explanation,observe_on=1)

#to create 5 points on the same plane we specify
#three arbitrary points, the plane determined
#by them and two additional point constrained
#to that plane

p1=FreePoint(-5,-13.,color=RED,label='1',pointsize=1.5,level=0)
p2=FreePoint(12,-12.0,color=RED,label="2",pointsize=1.5,level=0)
p5=FreePoint(-22.0,-0.0,color=RED,label="5",pointsize=1.5,level=0)
plane=Plane(p1,p2,p5,level=5)
p3=Slider(plane,(14,8,0),color=RED,label='3',pointsize=1.5,level=0)
p4=Slider(plane,(-12,18,0),color=RED,label='4',pointsize=1.5,level=0)


#the conic defined by the 5 co-planar points
PointArray(p1,p2,p3,p4,p5,density=60,pointsize=1,level=0)


# lines connecting points  of the conic
p12=Line(p1,p2,color=BLUE,level=2)
p45=Line(p4,p5,color=BLUE,level=2)
p23=Line(p2,p3,color=BLUE,level=2)
p34=Line(p3,p4,color=BLUE,level=2)
p15=Line(p1,p5,color=BLUE,level=2)

#the points of intersection of connectin lines

M1=Intersect(p15,p23,color=RED,label="M1",level=2)
M2=Intersect(p12,p34,color=RED,label="M2",level=2)
M3=Intersect(p23,p45,color=RED,label="M3",level=2)
M4=Intersect(p34,p15,color=RED,label="M4",level=2)
M5=Intersect(p12,p45,color=RED,label="M5",level=2)


# synthetic construction of line tangent to the conic at
# each of the points by which the conic is defined...

M1M5=Line(M1,M5,level=3)
N1=Intersect(p34,M1M5,color=RED,level=3)
l1=Line(p1,N1,color=RED,level=1)

M1M2=Line(M1,M2,level=3)
N2=Intersect(p45,M1M2,color=RED,label="N2",level=3)
l2=Line(p2,N2,color=RED,level=0)

M2M3=Line(M2,M3,level=3)
N3=Intersect(p15,M2M3,color=RED,level=3)
l3=Line(p3,N3,color=RED,level=0)
M3M4=Line(M3,M4,level=3)
N4=Intersect(p12,M3M4,color=RED,level=3)
l4=Line(p4,N4,color=RED,level=0)

M4M5=Line(M4,M5,level=3)
N5=Intersect(p23,M4M5,color=RED,level=3)
l5=Line(p5,N5,color=RED,level=0)

v.pickloop()