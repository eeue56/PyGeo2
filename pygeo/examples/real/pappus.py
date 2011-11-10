from pygeo import *

"""Projection of Pappus construtcion, with Paapus line at infinity,
intersecting lines become parallel"""

v=display(title="Pappus Projection",width=600,height=600,axis=False)

"""2 co-planar lines and there intersection
point"""

a = FreePoint(-13,13,-7,label='a')
b = FreePoint(-15,-11,5,label='b')
line1=Line(a,b,color=BLACK)
ap = FreePoint(6,14,2,label="a'")
plane=Plane(a,b,ap,scale=4,level=3)
bp = Slider(plane,(7,4,8),label="b'")
line2=Line(ap,bp,color=BLACK)
O=Intersect(line1,line2,level=1)


"""addition point on each line"""
c=LineSlider(line1,ratio=1.3,label="c")
cp=LineSlider(line2,ratio=1.7,label="c'")


"""the lines connecting the non-corresponding
points on each line, and there points of
intersection"""
abp=Line(a,bp,color=YELLOW)
acp=Line(a,cp,color=GREEN)
bap=Line(b,ap,color=YELLOW)
bcp=Line(b,cp,color=CYAN)
cap=Line(c,ap,color=GREEN)
cbp=Line(c,bp,color=CYAN)
li1=Intersect(abp,bap)
li2=Intersect(acp,cap)
li3=Intersect(bcp,cbp)


"""The lines connecting the intersection
points. The theorom says these three
lines are in fact the same line"""
Line(li1,li2,color=RED)
Line(li2,li3,color=RED)
Line(li1,li3,color=RED)


"""We go on to project the lines
from a plane on a plane through the
the lines of intersection, to an arbitrary
plane parrallel to it.  The Pappus line is now at infinity,
i.e. the lines are parallel"""

o1=FreePoint(10,-17,-17,label='o1',level=3)
planeo1=Plane(o1,li1,li3,scale=4,level=3,color=DARKGRAY)
o2=FreePoint(0,-9,-17,label='o2',level=3)
planeo2=Plane(planeo1,o2,level=3,color=DARKGRAY,scale=4)
Transform(planeo2,o1,[abp,bap],color=YELLOW,level=2)
Transform(planeo2,o1,[acp,cap],color=GREEN,level=2)
Transform(planeo2,o1,[bcp,cbp],color=CYAN,level=2)

v.pickloop()
