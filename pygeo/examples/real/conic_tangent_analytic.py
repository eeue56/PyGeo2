from pygeo import *


v=display(title="Tangent to Conic",scale=50,panel=False)

# construct 5 co-planar points
p1=FreePoint(-18,-12.,3.,color=RED,label='p1',pointsize=1.25,level=1)
p2=FreePoint(3,-8.0,10.0,color=RED,label="p2",pointsize=1.25,level=1)
p3=FreePoint(-35.0,-2.0,-2.0,color=RED,label="p3",pointsize=1.25,level=1)
plane=Plane(p2,p1,p3,level=6)
p4=Slider(plane,(-9,18,16),color=RED,label='p4',pointsize=1.25,level=1)
p5=Slider(plane,(-35,17,6),color=RED,label='p5',pointsize=1.25,level=1)

#the (point) conic determined by the 5 points
conic=Conic(p1,p2,p3,p4,p5,density=200)

# a point pickalbe, consrained to the plane of the conic
P=Slider(plane,(18,16,25),color=RED,label="P",pointsize=1,fontcolor=BLACK,level=1)

# the chord polar to the given point with respect to the conic
polar=ConicPolar(conic,P,chord=True)

# the ends points of the chord
a=SegPoint(polar,seg=BEGIN)
b=SegPoint(polar,seg=END)

# the lines from the plane point to the chord endpoints are tangent to the conic
Line(a,P)
Line(b,P)

#enter pickloop
v.pickloop()