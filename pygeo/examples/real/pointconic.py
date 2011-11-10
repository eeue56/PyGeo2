from pygeo import *
from pygeo.utils.colors import *

DENSITY=50

# the triple-quoted explanation, instruction, and reference
# text - if created -  can be provided as optional arguments
# when calling the PyGeo display (see display options,below),
# and will then appear as separate text boxes
# that can be accessed from the display panel's help menu


explanation = """The unique conic determined by 5 given co-planar
points, constructed as the points of intersection of two projective
(and non-perspective) pencils of lines.  Working backwards
from the construction helps to explain the projective
relationships of points on a conic"""

instruction =  """Add view levels to see construction
stages"""




def construct():

   #to create 5 points on the same plane we specify
   #three arbitrary points, the plane determined
   #by them and two additional point constrained
   #to that plane.


   p1=FreePoint(-5,-13.,3.,color=NAVYBLUE,label='p1',pointsize=1.25)
   p2=FreePoint(12,-12.0,10.0,color=NAVYBLUE,label="p2",pointsize=1.25)
   p3=FreePoint(-17.0,-8.0,-2.0,color=NAVYBLUE,label="p3",pointsize=1.25)
   plane=Plane(p1,p2,p3,level=6)

   #the intitial position of the PlaneSlider points is the point of the
   #plane closest to the given coordinate arguments.  The coordinate
   #arguments that are *on* the plane are not necessary
   
   p4=Slider(plane,(-12,18,2),color=NAVYBLUE,label='p4',pointsize=1.25)
   p5=Slider(plane,(14,8,3.5),color=NAVYBLUE,label='p5',pointsize=1.25)


   #four of the lines determined by the five points
   
   p14=Line(p1,p4,color=TURQUOISE,level=1)
   p23=Line(p2,p3,color=TURQUOISE,level=1)
   p45=Line(p4,p5,color=TURQUOISE,level=1)
   p35=Line(p3,p5,color=TURQUOISE,level=1)


   #the point of intersection of lines p14 and p23

   v1=Intersect(p14,p23,color=SKYBLUE,label='v1',level=1)

   # the LinePencil (the lines radiating from) point p2.
   # we use it for construction,

   lb=LineArray(plane,p2,density=DENSITY,level=6)


   # the array of points on line p45 that intersect
   # with the lines radiating from point p2.

   pm=PointArray(lb,p45,color=RICHBLUE,level=2)


   #the lines through point v1 and the points of pm


   la=Lines(pm,v1,color=VIOLETRED,level=1)

   #the lines through point p2 and the points of pm

   la2=LineArray(pm,p2,color=MEDIUMAQUAMARINE,level=1)


   """so now the lines through v1 (i.e. 'la') and those through
   p2 (i.e., 'la2') are in perspective  - through
   their common relationship with the array of points on
   line 45 (.i.e. 'pm')"""

   #the array of points on line p35 that intersect
   #with the lines of la.

   pa=PointArray(la,p35,color=RICHBLUE,level=2)

   #the lines through point p1 and the points of pa

   la3=LineArray(pa,p1,color=PLUM,level=1)

   LineArray(pa,v1,color=NEONPINK,level=1)

   """so now the lines through v1 (i.e. 'la') and those through
   p1 (i.e., 'la3') are in perspective  - through
   their common relationship with the array of points on
   line 35 (.i.e. 'pa')"""


   #the points of intersection of lines la2 and la3,
   #which are on the conic determined by the five
   #given points

   """'la2' and 'la3' are in projective relationship -
   each being in perspecitve relationship with 'la'
   All points in which they intersect are on the
   determined conic. So the definition holds - a point conic
   defined as the points of intersection of 2 projective
   and non-perspective pencils of line."""

   pa=PointArray(la2,la3,pointsize=1,level=1,color=SLATEBLUE)

   # after all that, display the PointConic primitive provided
   # by PyGeo - and check whtehter it conforms to the long-way-round
   # synthetic construction we've gone through.


if __name__ == "__main__":

   #create the display
   
   v=display(scale=35.,instruction = instruction, axis=False,
            explanation=explanation,title='Point Conic',width=800,height=600,view_drag=False)

   
   #call the construction
   
   construct()

   #stay in looping wating for points to be picked and moved

   v.pickloop()

