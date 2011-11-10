from pygeo import *
v=display(scale=75,view_drag=False)
p1=FreePoint(-18,-12.,15,color=RED,label='p1',pointsize=1.25,level=1)
p2=Point(3,-8.0,0,color=RED,label="p2",pointsize=1.25,level=1)
p3=Point(-35.0,-2.0,25,color=RED,label="p3",pointsize=1.25,level=1)
plane=Plane(p2,p1,p3,level=6)
p4=Slider(plane,(-9,18),color=RED,label='p4',pointsize=1.25,level=1)
p5=Slider(plane,(-35,17),color=RED,label='p5',pointsize=1.25,level=1)
#z=FreePoint(35.0,12.0,2,color=GREEN,label="p3",pointsize=1.25,level=1)

conic=Conic(p1,p2,p3,p4,p5,density=200)
for p in conic.points:
   ConicPolar(conic,p)


x=Slider(plane,1,26.,16,color=RED,label='x')
y=Slider(plane,-38,25.0,10,color=RED,label="y")
p1a=FreePoint(1,-1.,-15,color=RED,label='p1',pointsize=1.25,level=1)
p2a=FreePoint(13,8.4,0,color=RED,label="p2",pointsize=1.25,level=1)
p3a=FreePoint(-3.0,12.0,-5,color=RED,label="p3",pointsize=1.25,level=1)
p4a=FreePoint(2,17,11)
x1=Slider(plane,12,17.,-6,color=RED,label='x')
y1=Slider(plane,-3,2.0,-1,color=RED,label="y")

line1=Line(p1a,p2a)
line2=Line(p3a,p4a)

LineArray(conic,line1,line2)
line=Line(x,y,color=RED,level=2)
cc=Chord(conic,line,seg=True)
cp1=ConicPolar(conic,x,color=BLUE,chord=False)
cp2=ConicPolar(conic,y,color=BLUE,chord=True)

ConicPole(line,conic,pointsize=1,color=BLUE)

p1a=Slider(plane,(9,1),color=BLUE,label='p1a',pointsize=1.25,level=1)
p2a=Slider(plane,(-3,7),color=BLUE,label='p2a',pointsize=1.25,level=1)
p3a=Slider(plane,(11,2),color=BLUE,label='p3a',pointsize=1.25,level=1)
p4a=Slider(plane,(-24,7),color=BLUE,label='p4a',pointsize=1.25,level=1)
p5a=Slider(plane,(-5,17),color=BLUE,label='p5a',pointsize=1.25,level=1)
conic2=Conic(p1a,p2a,p3a,p4a,p5a,density=200,color=RED)
pl1=LineArray(conic,conic2,color=BLUE,linewidth=.3,level=2)
v.pickloop()