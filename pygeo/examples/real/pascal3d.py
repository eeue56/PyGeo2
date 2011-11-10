from pygeo import *


v=display(title="Pascal in 3d",scale=65,panel=False)

A=FreePoint(29,-25,4,color=ORANGE,label='A')
C=Point(-30,-24.,-13.,color=ORANGE,label='C')
E=Point(-15,-28,22.0,color=ORANGE,label='E')
circle=CircumCircle(A,C,E,style=LINES,color=BLUE,linewidth=.5,precision=100)


"""use CirclingPoint for animated sequence, otherwise CircleSlider"""

   #pickable point constrained to move on the circle's circumference

D=CircleSlider(circle,label='D',pointsize=1.5,angle=-PI/2,color=RED)

   #point which moves along circle at equal intervals at each update cycle

#D=CirclingPoint(circle,rate=C_RATE,label='D',pointsize=1.5,color=RED)

   #two additional points at fixed positions on circle's circumference

F=CircumPoint(circle,angle=PI/10,label='F',color=ORANGE)
B=CircumPoint(circle,angle=PI/4,label='B',color=ORANGE)


   #six lines representing "mystic hexagon" inscribed in the circle



   #six lines connecting non-adjacent points of the
   #"mystic hexagon" defined by the points on the
   #circles circumference

AE=Line(A,E,color=CYAN,linewidth=.3,seg=True)
BF=Line(B,F,color=CYAN,linewidth=.3,seg=True)
BD=Line(B,D,color=GREEN,linewidth=.3,seg=True)
CE=Line(C,E,color=GREEN,linewidth=.3,seg=True)
CF=Line(C,F,color=BLUE,linewidth=.3,seg=True)
AD=Line(A,D,color=BLUE,linewidth=.3,seg=True)


   #the points of intersection of the lines

i1=Intersect(AE,BF,color=CYAN,pointsize=1.5)
i2=Intersect(BD,CE,color=GREEN,pointsize=1.5)
i3=Intersect(CF,AD,color=BLUE,pointsize=1.5)


   #lines connecting connecting the points of
   #intersection.  If Pascal is correct, these
   #lines will always be concurrent.

pl1=Line(i1,i3,color=RED,linewidth=.3,seg=True)
pl2=Line(i2,i3,color=RED,linewidth=.3,seg=True)
pl3=Line(i1,i2,color=RED,linewidth=.3,seg=True)


   #3 more arbitrary points in space and the circle
   #which they define.

a=FreePoint(45.0,30.,-39.0,pointsize=1.5,color=PURPLE,level=1)
b=FreePoint(-49.,0.0,46.0,pointsize=1.5,color=PURPLE,level=1)
c=FreePoint(49.0,-50.0,40.0,pointsize=1.5,color=PURPLE,level=1)
planea=CircumCircle(a,b,c,color=(1,.9,.9),linewidth=.1,level=1)

   # an arbitrary point in space - the center of the projection to
   # be constructed

O=FreePoint(-2.0,38.0,0.0,label='O',pointsize=1.5)

   #the line connecting point O to the points on the
   #circles circumference. Not assigned to variable,
   #as "cosmetic" - lines are not referenced in construction

Line(O,A,color=YELLOW,linewidth=.35,seg=True)
Line(O,B,color=YELLOW,linewidth=.35,seg=True)
Line(O,C,color=YELLOW,linewidth=.35,seg=True)
Line(O,D,color=YELLOW,linewidth=.35,seg=True)
Line(O,E,color=YELLOW,linewidth=.35,seg=True)
Line(O,F,color=YELLOW,linewidth=.35,seg=True)

#now project the construction on the plane defined
#by the initial circle, to the plane defined by the
#new circle, from the arbitray 'center' point.
#This helps us visualize the generalization of
#Pascals theorem from the circle to the arbitray
#conic

Transform(planea,O,(B,A),color=(1.0,.7,.7))
Transform(planea,O,(AE,BF,i1),color=(.7,1.0,1.0))
Transform(planea,O,(BD,CE,i2),color=(1.0,.7,.7))
Transform(planea,O,(CF,AD,i3),color=(.7,.7,1.0))
Transform(planea,O,(pl1,pl2,pl3),color=RED)
Transform(planea,O,(circle,),color=BLUE)


v.pickloop()