from pygeo import *


explanation = """Illustrates Desargue theorem - given
2 triangles whose vertexes meet in a point, the intersection
of corresponding sides of the triangles will meet on
a line.  Viewed in space and allowing the triangles
to be on separate planes, the line of intersection
of corresponding sides is necessarily the line of
intersection of the two planes..
"""

instruction  = """ Points can be picked and dragged to
change triangles.  Increase view levels to see planes
and plane intersections"""

v=display(scale=75,title="Desargue",axis=False,instruction=instruction,explanation =explanation)

# an arbitrary point in space to be our
   # perspective center

O=FreePoint(4,38,-7,level=0,label="O")

   # 3 additional arbitrary points in space
   # and the triangle connecting them

a=FreePoint(-17,-23,7,label='a',fontcolor=BLACK,level=1)
b=FreePoint(17,-23,-9,label='b',fontcolor=BLACK,level=1)
c=FreePoint(31,-33,9,label='c',fontcolor=BLACK,level=1)
#t1=Triangle(a,b,c,color=GREEN,style=FILL)

   # the lines connecting the triangle vertices
s1=Line(a,c,color=PURPLE)
s2=Line(a,b,color=GREEN)
s3=Line(b,c,color=BLUE)

   # the lines from the perspective center
   # through the three points

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

   # the lines connecting the triangle's
   # vertices

sp1=Line(ap,cp,color=PURPLE,level=0)
sp2=Line(ap,bp,color=GREEN,level=0)
sp3=Line(bp,cp,color=BLUE,level=0)

""" by construction triangles t1 and t2 will remain
perpective from point O, regardless of the movement
of the constructed points """

   # the intersection of the corresponding lines
   # of the perspective triangles

i1=Intersect(sp1,s1,label="P")
i2=Intersect(sp2,s2)
i3=Intersect(sp3,s3)


   # the lines through the points of intersection;
   # Desargue's Theorem predicts that these lines
   # will always be concurrent.

Line(i1,i2,color=RED,linewidth=.5,level=1)
Line(i2,i3,color=RED,linewidth=.5,level=1)
Line(i1,i3,color=RED,linewidth=.5,level=1)



    # another look at it - as the projection of
    # the sides of triangle t2 onto the plane
    # containing triangle t1


plane1=Plane(a,b,c,level=1,color=MAGENTA)
Transform(plane1,O,[t2],level=2,color=RED)

v.pickloop()