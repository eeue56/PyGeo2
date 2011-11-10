
from pygeo import *


v=display(scale=25,width=800,height=800,panel=False)

C_RATE=360

ccolor=makecolor(b=1)

p1 = Point(1,.5,color=ccolor,pointsize=1,level=1)
p2 = Point(-10,-10,0,color=BLUE,pointsize=1,level=6)
p3 = Point(1,10,0,color=BLUE,pointsize=1,level=6)
plane=Plane(p1,p2,p3,level=6)
line=Line(p1,p3,level=2,seg=True)
sl=AniPoint(line,color=RED,rate=C_RATE,ratio=.001,level=1)
circle=Circle(p1,sl,plane,color=ccolor)
cp=AniPoint(circle,color=RED,rate=C_RATE,level=2)



c=Circle(p1,cp,plane,color=ccolor,level=3)
p2=CirclingPoint(c,level=2)
C=Circle(p1,p2,plane,color=ccolor,level=1)

p=[]
ccolor=makecolor(b=1)

hex=PI*2/6
for i in range(6):
  p.append(CircumPoint(C,angle=i*hex,level=1))

ccolor=makecolor(b=1)

lines=[]
for i in range(6):
   lines.append(Line(p1,p[i],color=ccolor,seg=True))

centers=[]
for l in lines:
   centers.append(Divider(l,ratio=1.7,color=ccolor))

ccolor=makecolor(r=1)

for c in centers:
   Circle(c,p1,plane,color=ccolor)
ccolor=makecolor(b=1)

circles=[]
for i in range(6):
   circles.append(Circle(p[i],p1,plane,color=ccolor,level=1))

ccolor=makecolor(r=1)
cpoints=[]
for i in range(len(circles)):
   cpoints.append(AniPoint(circles[i],level=2,rate=C_RATE))

ccolor=makecolor(r=.5,g=0)

for i in range(6):
   Circle(cpoints[i],p1,plane,color=ccolor,level=2)

ccolor=makecolor(r=.5,g=0)

bchords=[]
for i in range(6):
   if i+ 1 > 5:
      j = 0
   else:
      j=i+1
   bchords.append(Chord(circles[i],circles[j],color=ccolor))
bchords.append(Chord(circles[5],circles[0],color=ccolor))
v.animate(title="Islamic Pattern 5",frames=800,delay=0)
