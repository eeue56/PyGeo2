from pygeo import *

RECURSIONS=4

instructions = """
The points of the small tetra connected by blue lines
visible by clicking level 5 are the seed points of
a recursion reflection of an irregular tetra in its
sides.

The red point of the small level 5 tetra can be picked and
moved to change the height of the tetra, with the change
in the seed point position impacting the figures created
by recursive reflection and visible in levels 1 through 4 -
level 4 figure derived directly from level 5 figure,
3 derived from 4, etc.

Revise the script, playing  with the  starting positions of
the four "seed" points and recursion level.
"""

explanation = """Construction starts with an irregular tetrahedron,
and recursively reflects the opposite vertex and connecting lines
in each side, considered as a plane.

Displayed in level 1 is the fifth iteration. Add levels successively
to better see the genesis of the figure.
"""

# general display options
v=display(scale=125,width=800,height=800,axis=False,
          explanation=explanation,instruction=instructions)

# 3 fixed points in space and the plane determined by them
p1 = Point(0,-8,-8,color=BLUE,pointsize=2,level=5)
p2 = Point(0,-8,8,color=BLUE,pointsize=2,level=5)
p3 = Point(8,0,0,color=BLUE,pointsize=2,level=5)
plane=Plane(p1,p2,p3,level=7)

# the circumcenter of the triangle connecting the 3 points,
cp=CircumCenter(p1,p2,p3,level=5)

# a line through the circumcenter point, perpendicular to
# the 3 fixed points, and then a point free to be picked
# and moved, with the movement constrained to the
# perpendicular line.
pp=PlanePerp(plane,cp,level=5)
p4 = LineSlider(pp,ratio=1.5,color=RED,pointsize=2,level=5)



def lines(p,color,level=1):
   q=subsets(p,2)
   for s in q:
      Line(s[0],s[1],linewidth=1,color=color,level=level,seg=True)


# 4 planes determined by 4 points in a Python list argument
def planes(p):
   planes=[]
   q=subsets(p,3)
   for s in q:
      planes.append(Plane(s[0],s[1],s[2],level=7))
   return planes


# reflection of points in plane representing opposite side
# of a tetrahedron
def reflects(planes,p,color,level=1):
   points=[]
   points.append(Reflection(planes[3],p[0],pointsize=2,level=level,color=color))
   points.append(Reflection(planes[2],p[1],pointsize=2,level=level,color=color))
   points.append(Reflection(planes[1],p[2],pointsize=2,level=level,color=color))
   points.append(Reflection(planes[0],p[3],pointsize=2,level=level,color=color))
   return points



# we are creating 4 tetras from 2 lists each with 4 points
def tetra(s1,s2,level=1):
   for i in range(4):


      # m1= s1[:] is a short-cut way of making m1 into a copy of p1
      # m1=s1 would make m1 a reference to p1, so any changes
      # we subsequently made to m1 would effect p1, which is not
      # the behavior we want here
      m1=s1[:]

      # we substitute in turn 1 point of the 1st list
      # with 1 point of the second list and at each substitution
      # create a tetra of lines from the hybrid list
      m1[i]=s2[i]
      lines(m1,makecolor(),level=level)


# the starting 'seed' of our recursive iteration,
# as a list within a list

p=[[p1,p2,p3,p4]]
lines(p[0],color=BLUE,level=5)


# start from seed, and create new points as reflections
# in the plane of the opposite side of the tetra of which it is
# a member, and feedback the result for a new recursion

for i in range(RECURSIONS):
  p.append(reflects(planes(p[i]),p[i],makecolor(),level=RECURSIONS))
  tetra(p[i],p[i+1],level=RECURSIONS)
  RECURSIONS-=1



# we stay in a loop allowing us to pick and move the LineSlider and see
# and see the impact on the construction of the changed position
v.pickloop()



