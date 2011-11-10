from pygeo import *



C_RATE=144
DENSITY=20


#the instructions,explanation, and reference are options that
#when utilized as herein, makes there way to the help menu
#of the constructions control panel

instructions = """This one's an animation. Sit back and let
it run.

Click mouse at any point to end animation and
return contol over diagram."""


explanation = """ Were the BLUE line at infinity, what we would
be looking at is the tracing (in WHITE ) of
concentric circles.

What we have instead is concentric circles in
perspectic view.


The script illustrates PyGeo animation capabilities.
"""


reference = """Lawrence Edwards - "Projective Geometry" -
  Cover Illustration; construction as per diagram 117"""

v=display(scale=65,axis=0,panel=1,trace_on =True,instruction=instructions,
   explanation=explanation, reference = reference)


# Three arbitrary points in space and the plane
# defined by the points

a=Point(-28,10,0,level=2)
b=Point(28,10,0,level=2)
c=Point(0,-28,0,level=2)
plane=Plane(a,b,c,scale=1,level=2)

# The line containing points a and b

ab=Line(a,b,color=BLUE)


# Two points at arbitrary positions on the
# previously defined plane, and the line
# containing them

A=Slider(plane,(-2,-6,0),label="A",fontsize=TINYFONT)
B=Slider(plane,(4,-11.5,0),label="B",fontsize=TINYFONT)
AB=Line(A,B)


# the intersection of the two co-planar lines

X=Intersect(AB,ab,label="X",fontsize=TINYFONT,extend=True)

# the point harmonic to X, with respect to A & B

Xp=Harmonic(X,A,B,label="X'",fontsize=TINYFONT)


# we create an arbirtray circle on the plane and...

O=Slider(plane,(-1,18,0))
t=Slider(plane,(-1,4,0),level=2)
track=Circle(O,t,a,color=BLACK)

# a point to revolve on the circles circumference,
# and is the key 'control point' for the animation.


cs=AniPoint(track,rate=C_RATE,color=MAGENTA,pointsize=.8)


pp=Plane(plane,O,cs,color=BLUE,scale=1,level=2)
p1=Intersect(pp,ab,label="p1")
pn=Plane(cs,O,scale=1,level=2)
p2=Intersect(pn,ab,label="p2")

Line(O,p1,color=RED)
Line(O,p2,color=RED)


As = []
Bs = []
pas = []
pbs = []

for i in range(DENSITY):
   Bs.append(Divider(AB,ratio=(i+1)*1.5,color=RED,extend=True))
   As.append(Harmonic(Bs[i],X,Xp,color=LIGHTGRAY))
   pbs.append(Line(Bs[i],p2,linewidth=.2,color=WHITE))
   pas.append(Line(As[i],p1,linewidth=.2,color=WHITE))
   Intersect(pas[i],pbs[i],pointsize=.7,trace=1,tracewidth=.3,mintrace=0.001,maxtrace=1000,color=BLUE,level=1)



v.animate(name="concentrics",povout=0,frames=C_RATE/2+1,delay=.5)
