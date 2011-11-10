from pygeo import *
v=display(scale=25,axis=False,trace_on=True,povout=False,panel=False)

C_RATE=72

"""A little animation of a Stinson line formed
from four points on a circle, as one
point traces the points of the circle"""

A=Point(7,-7,7,color=BLUE,label="A",level=2)
B=FreePoint(3,9,-4,color=RED,label="B",level=2)
C=FreePoint(-14,7,17,color=RED,label="C",level=2)
circle=CircumCircle(A,B,C)
P=CirclingPoint(circle,rate=C_RATE,pointsize=.9,level=2)
l1=Line(A,B,color=CYAN,level=2)
l2=Line(B,C,color=CYAN,level=2)
l3=Line(C,A,color=CYAN,level=2)
p1=Foot(l1,P,level=2)
p2=Foot(l2,P,level=2)
p3=Foot(l3,P,level=2)
s=Line(p1,p2,color=RED,level=2)
Line(P,p1,color=MAGENTA,level=2)
Line(P,p2,color=MAGENTA,level=2)
Line(P,p3,color=MAGENTA,level=2)

c=Chord(circle,s,trace=True,tracewidth=.1,tracecolor=BLUE)


v.animate(name="stinson",frames=C_RATE,delay=.2)
v.pickloop()