from pygeo import *


explanation = """Desargue construction as the lines of intesection
of 5 planes in space
"""

v=display(scale=75,title="Desargue From Planes",axis=False,explanation =explanation)

# an arbitrary point in space to be our
   # perspective center

O=FreePoint(4,38,-7,level=0,label="O")

   # 3 additional arbitrary points in space
   # and the triangle connecting them

a=FreePoint(-17,-23,7,label='a',fontcolor=BLACK,level=1)
b=FreePoint(17,-23,-9,label='b',fontcolor=BLACK,level=1)
c=FreePoint(0,-14,9,label='c',fontcolor=BLACK,level=1)
t1=Triangle(a,b,c,color=GREEN,style=FILL)


l1=Line(O,a,linewidth=.2,color=YELLOW,level=0)
l2=Line(O,b,linewidth=.2,color=YELLOW,level=0)
l3=Line(O,c,linewidth=.2,color=YELLOW,level=0)

   # a point constrained to each of the
   # three lines and the triangle connecting
   # them

ap=Slider(l1,ratio=.7,label="a'",fontcolor=BLACK,level=1)
bp=Slider(l2,ratio=.8,label="b'",fontcolor=BLACK,level=1)
cp=Slider(l3,ratio=.4,label="c'",fontcolor=BLACK,level=1)
t2=Triangle(ap,bp,cp,color=CYAN,level=0,style=FILL)

plane1=Plane(a,b,c,level=2,color=MAGENTA)
plane2=Plane(ap,bp,cp,level=3,color=CYAN)

r1=Plane(O,b,c,level=3,color=WHITE)
r2=Plane(O,a,c,level=4,color=WHITE)
r3=Plane(O,a,b,level=5,color=WHITE)


# Desaurge contruction
planes=[r1,r2,r3,plane1,plane2]

for p in subsets(planes,2):
   Line(p[0],p[1])

for p in subsets(planes,3):
   Intersect(p[0],p[1],p[2],pointsize=2,color=BLUE,level=2)

v.pickloop()