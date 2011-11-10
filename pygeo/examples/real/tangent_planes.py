from pygeo import *

instructions="""The magenta colored points define the
connecting line, and the red points the center and
circumference point of a sphere.  The blue planes in
the construction's initial position are the unique planes
through the line and tangent to the sphere.

Consider the line as infinite in length, with what is drawn
(the segment between the points) only as an indication of
its postion and direction.

Pick and move a magenta point to reposition the line, and
the tangent planes as defined will followed.  If the line becomes
positioned so that it piecres the sphere,there is no real points
of tangency - the planes of tangency disappear and the chord of
the line through the sphere appears in yellow"""

explanation= """Given a sphere and an arbitrary line is space
not intersecting it, there are two planes that
include the line and are tangent to the sphere.
TangPlanes is the chord connecting the points of
tangency on the sphere.

SphereChord is the chord connecting the points
of intersection when the line does intersect
the sphere

In what sense can it be said that the TangPlanes points
are the real points of the imaginary intersection
of a sphere and a non-intersecting  line? """

# display options
v=display(title="Tangent Planes",scale=30,height=600,width=600,
         axis=False,instruction=instructions,explanation=explanation)


# 2 points free to move in space, with arbitrary starting
# positions

O=FreePoint(10,15.,0.,color=RED,label='O')
T=FreePoint(4,19.,3.,color=RED,label='T')

# the sphere with point O as center and point T on its surface

sphere=Sphere(O,T,style=LINES,precision=10,linewidth=.05,texture="Ruby_Glass")

# 2 more points free to move in space, with arbitrary starting
# positions, and the line connecting them

p1=FreePoint(-14,-5,15,label='p1',color=MAGENTA)
p2=FreePoint(18,0,4,label='p2',color=MAGENTA)
p1p2=Line(p1,p2,color=BLUE,linewidth=.2)

# the TangPlane is really a chord through the sphere connecting
# the points of tangency on its surface of planes (if such exist)
# which contain a given line.

ch=Chord(sphere,p1p2,color=RED,level=1)

# if we want the tangent points themselves we need to specify
# to get the two endpoints of the tangent chord.

tpoint1=SegPoint(ch,label='T')
tpoint2=SegPoint(ch,opposite=tpoint1,label='N')

# draw the planes determined by each endpoint of the chord,
# and the endpoints of the line.

Plane(p1,p2,tpoint1,color=BLUE,scale=2,style=LINES,texture='Ruby_Glass')
Plane(p1,p2,tpoint2,color=BLUE,scale=2,style=LINES,texture='Dark_Green_Glass')


# enter loop to allow free points to be picked and moved.
v.pickloop()
