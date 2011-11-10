from pygeo import *

explanation ="""Bezier curves are an interesting way to
visually explore issues related to permutations,
since unique curves are created by the same
control points provided in varying sequence to
the curve creation code"""

v=display(title="Bezier Permutations",scale=40,width=600,
          axis=False,height=600,explanation=explanation)

# 4 fixed points on the plane of the screen - only 2 coordinate
# arguments given so the z coordinate defaults to 0.
p1 = Point(30,30,level=2);
p2 = Point(-30,30,level=2)
p3 = Point(-30,-30,level=2)
p4 = Point(30,-30,0,level=2);

#  2 additional points, on the z axis.
p5 = Point(0,0,30,level=2);
p6 = Point(0,0,-30,level=2);


#a list of the points created above

L=[p1,p2,p3,p4,p5,p6]

# create a list of the integers (starting at zero)
# equal in numeber to the len of the list of points L

M = range(len(L))

# perform permutation on the list of points, and
# feed each permutation in turn to the BezierCurve
# code as its control points.

def drawcurve(p,size=None,color=(1,.1,.4),lw=.2,level=1):
   # P is our list of integer lists - a list with sublists.
   # It is set as 'global' because an outside function
   # "perms" needs to be able to effect its contents, and
   # therefore needs to be know of it.

   if not size:
      size = len(p)

   # We determine the number of control points we want to
   # feed BezierCurve.  For example if p is a list of
   # 6 points, and the size argment is 4, then the perms
   # function will return 4 element permutations of the
   # the 6 points. The perms function exlcudes permutuations
   # where permlist = permlist.reverse, as these would create
   # duplications of curves.

   P=permsets(p,size)

   # the actual points are in L, P is a list of sublists of
   # permutated integers.  P elements serve as
   # indexes which select from the points contained in L.

   for i in range(len(P)):
      #create a list of points selected acccording to the indexes
      #retrieved from the permsets function call

      cp=[L[j] for j in P[i]]
      # draw the curve based on the ordered set of points given as
      # an argument

      # toggle drawpoints and drawcurve boolean to see effects
      Curve(cp,linewidth=lw,density=25,level=level,color=color)



# select control points we want to start with as
# seeds.  We slice and concatenate elements wanted.

drawcurve(M[:1] + M[2:5],level=1)
drawcurve(M[:3] + M[5:6],level=1)
drawcurve(M[:3] + M[4:5],level=2)
drawcurve(M[:1] + M[2:4]+M[5:6],level=2)



# all perms of 3 control points

drawcurve(M,size=3,color=BLUE,level=3)


#display options

v.pickloop()