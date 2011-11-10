from pygeo import *

reference = """Projective Geometry by Lawrence Edwards, Part 5, dual of construction of
Diagram 32, page 49"""


instruction =  """Pick and very slowly move the point " p " around the circle."""


explanation = """ 2 lines, " X " and " X' ", are given as generators of the conic.
Also given are two reference points, " o " and " o' ", and intermediate line " M ".
The point " a " is a point of the pencil of points of line " X ".
Point " a " with point "o" defines a line " A ". From the intermediate line " M ",
" A " is  projected to point " o' ", defining line " A' "
The point " a' " connecting " X' " and " A' " is a point of the pencil of point of
" X' " projective with point " a ", since " a " and " a' " are each perspective from
line " M ". By the projective definition of a conic, the line connecting " a " and " a' "
is a tangent to the conic determined by the given elements, as they are points of the
pencils of points " X " and " X' ", respectively, in projective one to one correspondance,
each in perspective with intermediate line "M". """


#start the display window, overriding defaults with keyword arguments"""

v=display(scale=50,axis=False,width=800,height=600,trace_on=True,reference=reference,
         explanation = explanation, instruction = instruction)

""" Define 2 co-planar lines, which will be tangent to the
conic to be produced, by construction """

x1=FreePoint(14,7.0,level=1,color=RED)
x2=FreePoint(-17.0,-8.0,level=1,color=RED)
X=Line(x1,x2,label="X",color=RED)
x1p=FreePoint(-17,-23.,level=1,color=RED)
plane=Plane(x1,x2,x1p,level=6)
x2p=Slider(plane,(16,0),level=1,color=RED)
Xp=Line(x1p,x2p,label="X'",color=RED)

"""Define 2 additional points on the plane"""
o=Slider(plane,(8,8),color=RED,label='o')
op=Slider(plane,(-22,8),color=RED,label="o'")

"""And an 'intermediate' line for the projection"""

m1=Slider(plane,(-12,18),color=BLUE,label='M')
m2=Slider(plane,(-9,-24),color=BLUE)
M=Line(m1,m2)

""" The given elements allow us to construct 3 additonal lines which will be found
to be tangent to the conic to be constructed. The line connecting given points
"o" and o'", the line connecting the point of intersection of given lines "M" and "X"
with given point "o'", and the line connecting the point of intersection of given
lines "M" and "X'" with given point "o"

These three lines, together with the given lines "X" and "X'" can be seen as the five
lines determining the conic"""

Line(Intersect(M,X),op,color=RED)
Line(Intersect(M,Xp),o,color=RED)
Line(op,o,color=RED)


"""An arbitrary circle on the plane, a point free to move around its circumference,
and the line from that point through the circle center. The as the point moves aroubd"""
c1=Slider(plane,(15,15),level=2)
c2=Slider(plane,(1,1),level=2)
circle=Circle(c1,c2,plane,color=WHITE,linewidth=.05)
x=Slider(circle,color=MAGENTA,label="p",angle=-PI/4)
ox=Line(c1,x,color=WHITE,linewidth=.05)


""" As the point 'x' moves around the circle, the intersection of line through 'x'
and the circle center with line 'X' represents a point in the pencil of points of X"""
a=Intersect(X,ox,label="a")

"""The point 'a' of line 'X' is projected to point 'o' """
A=Line(a,o,label="A")

""" The line projected from 'a' to 'o' intersectsw intermediate line 'M' at 'm' """
m=Intersect(M,A,label="m")

""" The intermediate point on "M" is projected to "o'" """
Ap=Line(m,op,label="A'")

""" The line of projected from "M" to "o'" intersects line "X'" at "a' """


ap=Intersect(Ap,Xp,label="a'")


"""The point "a" of X and "a'" of "X'" are now projectively related, as both
are perspective with point m of M. By the synthetic defintion
of a conic, the line connecting "a" and "a'" are therefore tangent to the conic
defined by the given lines X and X', the given points o and o', and the intermediate
line M. """

Line(a,ap,color=BLUE,trace=True)

v.pickloop()