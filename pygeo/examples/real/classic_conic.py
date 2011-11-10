from pygeo import *


explanation = """The classic view of a conic as the plane slice of
right circular cones.  Can also be viewed projectively
as the projection of any circle of the cone from the cone
vertex onto an arbitrary plane"""

instruction = """Pick and drag any of the red points outside
the cone to change the plane orietnation

Picking and dragging blue point at cone base will change
dimensions of cones"""

v=display(scale=60,panel=1,explanation=explanation,instruction=instruction,panel=False)

   # 3 arbitrary points in space and the unique
   # circle through them
a=FreePoint(-17,23,7)
b=FreePoint(17,23,-9)
c=FreePoint(0,14,9)
circle1=Circle(a,b,c,CIRCUM,linewidth=.5,precision=250,level=2)
plane1=Plane(a,b,c,level=6)

   # the circle's center point
d=Center(a,b,c)
#d=circle1._center
   # the line perpendicular to the circle,
   # through its center point
stick=Line(plane1,d,color=RED)

   # a pickable point constrained to the
   # line
ls=Slider(stick,ratio=2.7,color=BLUE,pointsize=1.5)

sline=Line(d,ls)

   # the point midpoint on the line segment
   # between the circles center and the
   # point sliding on the line; will be the
   # apex of the cones and the center of the
   # projection determining our conic

O=Divider(sline,label="O")
   # an array of <density> points equally spaced on the
   # cirlce's circumference

ca=PointArray(circle1,density=25,pointsize=1,level=2)

   # the array of lines through the midpoint
   # and the points on the circle; for visual
   # referencfe only
LineArray(ca,O,linewidth=.1,color=WHITE)

   # a plane parallel to the constructed plane, through
   # the point sliding on the line constructed perpendicular
   # to the circle.
pplane=Plane(circle1,ls,level=3)

   # the points intersecting the parallel plane and the
   # lines through the projection center and points on the
   # constructed circle
b1=Intersect(pplane,Line(O,b))
c1=Intersect(pplane,Line(O,c))

   # a circle on the parallel plane with the sliding point
   # as center
#circle2=Circle(ls,b1,c1,color=RED,linewidth=.5)

   # an array of points on the new circle and an array
   # of lines through the cone apex and those points
#ca1=PointArray(circle2,density=20,pointsize=1)
#LineArray(ca1,O,linewidth=.1)


   # 3 arbitrary points in space and the plane
   # determined by them
p1=FreePoint(19,4,16,color=RED,pointsize=1,level=1)
p2=FreePoint(-17,16,2,color=RED,pointsize=1,level=1)
p3=FreePoint(17,14,6,color=RED,pointsize=1,level=1)
plane=Plane(p1,p2,p3)

   # the conic formed by projecting the circles from the
   # apex of the cone to the arbitrary plane
Transform(plane,O,[circle1],color=RED)

v.pickloop()
