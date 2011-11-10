from pygeo import *

instruction = """Pick any of the points on the circle
to change the orietantion of the plane on which it
lies"""

explanation = """The Desargue configuration derived
as the intersection of an arbitrary plane and an
arbitrary complete space 5 point """


v=display(title="Desargue as Plane Slice",scale=30,height=600,width=600,axis=False,
          instruction=instruction,explanation =explanation)


#plane slice of lines connecting 5 points in space, forming plane Desargue construction


"""
5 arbitrary points in space
"""

P1 = FreePoint(10,17,17,label='P1',color=RED,pointsize=.4,level=2,fontsize=SMALLFONT)
P2 = FreePoint(-3,-19,14,label="P2",color=RED,pointsize=.4,level=2,fontsize=SMALLFONT)
P3 = FreePoint(-17,10,-19,label="P3",color=RED,pointsize=.4,level=2,fontsize=SMALLFONT)
P4 = FreePoint(0,-14,11,label="P4",color=RED,pointsize=.4,level=2,fontsize=SMALLFONT)
P5 = FreePoint(-9,4,2,label="P5",color=RED,pointsize=.4,level=2,fontsize=SMALLFONT)



"""
ten lines connecting points.  we now have a complete
space 5point

"""

m12=Line(P1,P2,color=BLUE,level=2,linewidth=.08)
m13=Line(P1,P3,color=BLUE,level=2,linewidth=.08)
m14=Line(P1,P4,color=BLUE,level=2,linewidth=.08)
m15=Line(P1,P5,color=BLUE,level=2,linewidth=.08)
m23=Line(P2,P3,color=BLUE,level=2,linewidth=.08)
m24=Line(P2,P4,color=BLUE,level=2,linewidth=.08)
m25=Line(P2,P5,color=BLUE,level=2,linewidth=.08)
m34=Line(P3,P4,color=BLUE,level=2,linewidth=.08)
m35=Line(P3,P5,color=BLUE,level=2,linewidth=.08)
m45=Line(P4,P5,color=BLUE,level=2,linewidth=.08)


"""
construct an arbitrary plane in space represented
as a circle

"""

X1 = FreePoint(-17,-16,12,color=WHITE,level=1)
X2 = FreePoint(11,13,-14,color=WHITE,level=1)
X3 = FreePoint(16,-11,27,color=WHITE,level=1)
vp=CircumCircle(X1,X2,X3,color=WHITE,level=1)



"""
the ten points of intersection of the complete
space 5 point and the arbitrary plane"""

P12=Intersect(vp,m12,label="P12",fontsize=SMALLFONT,fontcolor=BLACK,level=1)
P13=Intersect(vp,m13,label="P13",fontsize=SMALLFONT,fontcolor=BLACK,level=1)
P14=Intersect(vp,m14,label="P14",fontsize=SMALLFONT,fontcolor=BLACK,level=1,color=BLUE)
P15=Intersect(vp,m15,label="P15",fontsize=SMALLFONT,fontcolor=BLACK,level=1)
P23=Intersect(vp,m23,label="P23",fontsize=SMALLFONT,fontcolor=BLACK,level=1)
P24=Intersect(vp,m24,label="P24",fontsize=SMALLFONT,fontcolor=BLACK,level=1,color=RED)
P25=Intersect(vp,m25,label="P25",fontsize=SMALLFONT,fontcolor=BLACK,level=1)
P34=Intersect(vp,m34,label="P34",fontsize=SMALLFONT,fontcolor=BLACK,level=1,color=BLUE)
P35=Intersect(vp,m35,label="P35",fontsize=SMALLFONT,fontcolor=BLACK,level=1)
P45=Intersect(vp,m45,label="P45",fontsize=SMALLFONT,fontcolor=BLACK,level=1,color=BLUE)



"""
the ten lines connecting the intersection
points.
"""


m123=Line(P12,P13,color=RED)
m124=Line(P12,P14,color=MAGENTA)
m125=Line(P12,P15,color=RED)
m134=Line(P13,P14,color=CYAN)
m135=Line(P13,P15,color=BLUE)
m145=Line(P14,P15,color=CYAN)
m234=Line(P23,P24,color=MAGENTA)
m235=Line(P23,P35,color=RED)
m245=Line(P24,P25,color=MAGENTA)
m345=Line(P34,P35,color=CYAN)



"""
extend the lines in possible
combos, to achieve correct visual
orientation

"""

Line(P12,P23,color=RED)
Line(P13,P23,color=RED)

Line(P12,P24,color=MAGENTA)
Line(P14,P24,color=MAGENTA)

Line(P12,P25,color=RED)
Line(P15,P25,color=RED)

Line(P13,P34,color=CYAN)
Line(P14,P34,color=CYAN)

Line(P13,P35,color=BLUE)
Line(P15,P35,color=BLUE)

Line(P14,P45,color=CYAN)
Line(P15,P45,color=CYAN)

Line(P23,P34,color=MAGENTA)
Line(P24,P34,color=MAGENTA)

Line(P25,P35,color=RED)
Line(P23,P25,color=RED)

Line(P24,P45,color=MAGENTA)
Line(P25,P45,color=MAGENTA)

Line(P34,P45,color=CYAN)
Line(P35,P45,color=CYAN)

v.pickloop()




