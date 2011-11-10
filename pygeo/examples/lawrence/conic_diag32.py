from pygeo import *

# the triple-quoted explanation, instruction, and reference
# text - if created -  can be provided as optional arguments
# when calling the PyGeo display (see display options,below),
# and will then appear as separate text boxes
# that can be accessed from the display panel's help menu


reference = """Projective Geometry by Lawrence Edwards, Part 5, Diagram 32, page 49"""


instruction =  """Pick and very slowly move the point "p" around the circle about "X"."""

explanation = """ 2 points, "X" and "X'", are given as generators of the conic.
Also given are two reference lines, "o" and "o'", and intermediate point "M".
The line "a" connecting any point "p" with X is a line of the pencil of lines
about X. The intersection of line "a" with line "o" defines a point "A".
From the intermediate point "M", "A" is  projected to line "o'", defining point "A'"
The line "a'" connecting "X'" and "A'" is a line of the pencil of lines about
"X'" projective with line "a", since "a" and "a' are each perspective from point
M". By the projective definition of a conic, the intersection of the lines "a" and "a'"
is a point of the conic determined by the given elements, as they are lines of the
pencils of lines around "X" and "X'", respectively, in projective one to one correspondance,
each perspective with intermediate point "M". """


#start the display window, overriding defaults with keyword arguments"""

v=display(scale=35,axis=False,width=800,height=600,trace_on=True,reference=reference,
         explanation = explanation, instruction = instruction)



"""Create two points defining line "o" and one other point,
giving us 3 points defining the plane on which all of the construction will
occur."""

o_p1=FreePoint(3,-20.0,level=1,color=CYAN)
o_p2=FreePoint(-17.0,-8.0,level=1,color=CYAN)
o=Line(o_p1,o_p2,label="o",color=BLUE)

o1_p1=FreePoint(-17,-23.,level=1,color=CYAN)
plane=Plane(o1_p1,o_p1,o_p2,level=6)


"""Create an additional point on the plane which, together with the 3rd point created
above, defines line o'. """

o1_p2=Slider(plane,(16,0),level=3,color=CYAN)
o1=Line(o1_p1,o1_p2,label="o'",color=BLUE)
#Intersect(o,o1,color=RED)


"""Create point "X" as a generating center of one pencil. Create "c" as a reference point
with which we define a circle with "X" as center. Create point "ac" constrained to
move on this circle. The line connecting "X" and "ac" is a line of the pencil through X. """


X=Slider(plane,(8,8),color=RED,label='X')
c=Slider(plane,(11,14),color=RED,label='a',level=5)
xc=Circle(plane,X,c,color=WHITE,linewidth=.05)
ac=Slider(xc,angle=PI,label="p",color=MAGENTA)
a=Line(ac,X,label='a',color=CYAN,linewidth=.1)


"""Create point " X' " as the second generating pencil center and point " M " as an
intermediate point of the projection to be constructed. """

X1=Slider(plane,(-22,8),color=RED,label="X'")
M=Slider(plane,(-12,18),color=BLUE,label='M')


""" Create point " A " as the intersection of line " a " and line " o' " """

A=Intersect(o,a,label="A")


""" The line " m " from intermediate point " M " and point " A " is projected to
line " o' ", and the projection point " A1"  indentified as the intersection of
the lines " m " and " o' "   """

m=Line(M,A,color=CYAN,linewidth=.1)
A1=Intersect(o1,m,label="A'")


""" The line " a1 " connecting the points " A1 " and the " X' " (as the second
generating point) is created. Lines " a " and " a1 " are now projectively corresponding
lines through points " X " and X', respectively.  The curve is defined as the locus of
points " P " - the intersection of lines " a " and " a1 " -  as line " a " rotates
about point " X " ."""

a1=Line(X1,A1,label="a'",color=CYAN,linewidth=.1)
P=Intersect(a,a1,label="P",color=RED,trace=True)


""" As visual reference points we create the lines containing the intermediate point
" M " and the generating points " X " and " X1 ". The points of intersection of the
line connecting " M " and " X " with line " o' ", and the line connecting " M "
and " X' " with line " o " will be on the curve, as will be the intersection of lines
" o " and " o' ".  These 3 points together with the given generating points " X " and
" X' " can be seen as the five points determining the conic.
"""

m1=Line(M,X,color=WHITE,linewidth=.1)
m2=Line(M,X1,color=WHITE,linewidth=.1)
Intersect(o,o1,color=RED,label="p3")
Intersect(m1,o1,color=RED,label="p4")
Intersect(m2,o,color=RED,label="p5")

v.pickloop()