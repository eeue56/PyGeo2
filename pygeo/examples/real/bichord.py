from pygeo import *

instruction = """Slide point "L" along the chord connecting
the points of intersection of the shaded circle.

Can also pick and move other points to change the size and relative
positions of the shaded circles"""

explanation = """Given two circles and the chord of intersection,
(if any).  The tangents to the circles from a point anywhere on
the chord line (exterior to the circles) will be of the same
length. Euclid and friends had this one down"""

v=display(scale=55,explanation=explanation,instruction=instruction)


"""define pickable and movable points on the screen
plane:

initial x postion, initial y position
label parameter is drawn.
color parameter from GeoConstants."""

p1 = FreePoint(10.656,-7,label='p1',color=WHITE)
p2 = FreePoint(-3,9,label="p2",color=WHITE)
ps1 = FreePoint(-17,0,label="v1",color=YELLOW)
ps2 = FreePoint(-7,-4,label="v2",color=YELLOW)
ps3 = FreePoint(9,4,label="v3",color=YELLOW)



"""Circle in 2d space: point at center,
point on circumference
style parameter is to render colored-in (default is
to render outline)"""

circle1=Circle(p1,p2,ps1,color=CYAN)

"""The unique Circle with the three given points on its
circumference"""

circle2 = Circle(ps3,ps1,ps2,CIRCUM,color=CYAN)


"""Cosmetic circles, rendering the outline of circle1,
and of circle2.  Not referenced to variable since not
called again in script"""

Circle(p1,p2,ps1,color=MAGENTA)
Circle(ps3,ps1,ps2,CIRCUMCIRCLE,color=MAGENTA)


"""The chord connecting the points of intersection
of circle1 and circle2.  Null if circle1 and circle2
do not intersect"""


bc = Chord(circle1,circle2,color=CYAN)


"""Point that is pickable but constrained to move along
the direction of the BiCord.  No initial position is
given, so initial position is at point of BiChord closest
to the origin, other would be at point of BiChord closest
to given initial position"""

ls=Slider(bc,ratio=1.4,color=RED,label="L")

"""Chords connecting tangents to given circle from
given point.  Null if given point is interior to
circle"""

tc1 = Line(circle2,ls,chord=True,seg=True)
tc2 = Line(circle1,ls,chord=True,seg=True)
sp=SegPoint(tc2)

"""Lines connecting the slider and the points
of the tangent chords"""


Line(ls,tc1.p1,color=ORANGE,seg=True)
Line(ls,tc1.p2,color=ORANGE,seg=True)
Line(ls,tc2.p1,color=ORANGE,seg=True)
Line(ls,tc2.p2,color=ORANGE,seg=True)


"""Circle with the slider at center and a point of
the tangent chord on circumference.  Same circle is
created if p2 of the tangent to circle is given instead
of p1 - which is not too surprising."""

Circle(ls,tc1.p1,tc1.p2,linewidth=.2,color=WHITE)


"""But the same circle is created if p1 or p2 of the tangent
to circle2 is given as the circumference point -
which a bit more surprising."""

Circle(ls,tc2.p1,tc2.p2,linewidth=.4,color=RED,level=2)


v.pickloop()

