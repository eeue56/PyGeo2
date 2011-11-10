from pygeo import *

v=display(title="Polarity per Yaglom",width=600,height=600,scale=60,
          axis=False,observe_on=False)

MAX=30



"""A construction of polars based
on plane intersections"""

p1 = FreePoint(4,-7,5,label='p1',level=1,color=RED,pointsize=.7)
p2 = FreePoint(-3,9,-7,label="p2",level=3)
p3 = FreePoint(-17,0,11,label="p3",level=3)
plane1=Plane(p1,p2,p3,level=6,scale=2)
pp=Line(plane1,p1,level=3)
s1 = Slider(pp,ratio=2.0,label="s2",level=3)
plane2=Plane(plane1,s1,color=BLUE,level=6,scale=10)
n=Divider(Line(p1,s1,level=3),label="m",level=3)
m=LineSlider(pp)
a=Slider(plane1,4,7,2,label="a",level=1,color=RED,pointsize=.7)
ap1=Line(a,p1,level=2)
f=Divider(ap1,p1,m,level=1,pointsize=1)
c1=Circle(p1,f,p2,color=BLUE)
b=Slider(plane1,-9,16,2,label="b",pointsize=.7,color=RED)

plane3=Plane(b,m,color=GREEN,level=6)
ab=Line(a,b,level=2)
circ=Circle(a,b,p1,color=YELLOW)
polar=[]
perp=[]
for i in range(MAX):
   x1=CircumPoint(circ,angle=2*PI*i/float(MAX))
   Line(x1,m,level=2,seg=True)
   plane3=Plane(x1,m,color=GREEN,level=6,scale=3)
   pline=Line(plane2,plane3,level=3,color=RED,drawlen=300)
   perp.append(Plane(plane1,pline.p1,pline.p2,color=WHITE,level=6,scale=3))
   polar.append(Line(perp[i],plane1,color=BLUE,drawlen=300))
for i in range (1,MAX):
   Intersect(polar[i-1],polar[i])

v.pickloop()
