from pygeo import *
v=display(scale=50,axis=False,width=800,height=600,panel=False,view_drag=False)



#the double points of the co-basal projectivity and their line
X=FreePoint(-29,-18,label="X")
y=Point(30,-17)
xy=Line(X,y)
Y=Slider(xy,ratio=1.1,label="Y")

#two points on the line determining, with the double points, a crossratio for the
#projectivity
A=Slider(xy,ratio=.2,label="A")
Ap=Slider(xy,ratio=.225,label="A'")


# the array of points determined by applying the crossratio progressively
gm=GrowthMeasure(X,Y,A,Ap,density=60,color=BLUE,level=1)

#two random points and their line
a=FreePoint(-11,29,color=CYAN)
b=FreePoint(27,7,color=CYAN)
ab=Line(a,b,color=WHITE,linewidth=.05)

# the line through double point "Y" parrallel to the random line
Yp=Line(Y,ab,color=WHITE,linewidth=.05)



# a point on the line through double point "Y"
o=Slider(Yp)

# the array of lines connecting point "o" to the points
# of the co-basal projectivity "gm"

la=LineArray(o,gm,color=WHITE)

# an array of points on random line "ab" determined by the
# projection of the points of the growth measure through
# point "o", i.e. the points of intersection on the line with
# the array of lines through "o" and the points of the growth measure.

pa1=PointArray(la,ab,extend=True,color=RED)


# the line from double point "X", and projected through "o"
# to line "ab"
Xo=Line(X,o,color=BLACK)
xa=Intersect(Xo,ab,color=RED)


# for visual emphasis, we repeat the projection through "o" to
# an additional line on the plane parallel with line "ab".

c=FreePoint(-30,-4,color=CYAN)
cp=Line(c,ab,color=WHITE,linewidth=.05)
pa2=PointArray(la,cp,extend=True,color=RED)
xc=Intersect(Xo,cp,color=RED)

# the crossratio "multiplier" inplicit in the postion of the
# double points and points "A" and "A'"

multiplier =gm.multiplier()
#print "multiplier is %f" %multiplier


# we calculate the ratio of the distance from double point "X"
# of the successive points of the point array projected to line "ab"
# and should find them equal to the multiplier, since double point "Y",
# by construction, has been projected to the point at infinity on
# line "ab".

for i in range(len(pa1.points)-1):
    d1 =  xa.distance(pa1.points[i+1])
    d2 =  xa.distance(pa1.points[i])
    if multiplier < 0:
       d1=-d1


# the purely synthetic construction of the same growth measure
# determined by algorythm in the PyGeo code for the GrowthMeasure
# primitive

def Synthetic_Growth_Measure(line,X,Y,a,b,steps=20,level=1):
    O=Point(-24,24,label="O",level=level)
    OY=Line(O,Y,level=level,color=MAGENTA)
    Op=Slider(OY,ratio=.15,label="O'",level=level)
    Oa=Line(O,a,level=level,color=MAGENTA)
    Ob=Line(O,b,level=level,color=MAGENTA)
    Opb=Line(Op,b,level=level,color=MAGENTA)
    p1=Intersect(Oa,Opb,level=level)
    Xp1=Line(X,p1,level=level,color=MAGENTA)
    ab=Line(a,b,level=6).length()
    aY=Line(a,Y,level=6).length()
    bX=Line(b,X,level=6).length()
    YX=Line(Y,X,level=6).length()
    points=[]
    def step(seed,steps,level=level):

       if steps:
          l=Line(O,seed,level=level,color=BLACK,linewidth=.08)
          i=Intersect(l,Xp1,level=level)
          lp=Line(Op,i,level=level,color=BLACK,linewidth=.08)
          steps-=1
          p=Intersect(line,lp,level=level)
          points.append(p)
          step(p,steps)
    step(b,steps,level=level)
    return points

# the sythentic construction defintion is invoked, with the line,
# the double points, and the additional points, as arguments
# check "level 2" on the control panel to view.

Synthetic_Growth_Measure(xy,X,Y,A,Ap,steps=20,level=1)

v.pickloop()