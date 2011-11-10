from pygeo import *

# a jackson pollacky type thingy

# a look at randonness
v=display(scale=30,width=600,height=600,view_drag=False,panel=False)

CURVES =20
p1= FreePoint(24,-18,0)
p2= FreePoint(-24,-21,0)
p3= FreePoint(19,25,-3)
plane = Plane(p1,p2,p3,level=6)
p4 = Slider(plane,-10,4,7,color=RED)
p5 = Slider(plane,-28,21,-2,color=RED)
p6 = Slider(plane,-21,-10,-2,color=RED)
conic=Conic(p1,p2,p3,p4,p5,level=2)

pp=[p1,p2,p3,p4,p5,p6]

DENSITY=20

x=0
while x < CURVES:
   c=[]
   for i in range(6):
       r=random()
       c.append(pp[randint(0,5)])
   Curve(c,color=makecolor(r=1,g=.8), linewidth=.1,density=DENSITY)
   x+=1

x=0
while x < CURVES:
   c=[]
   for i in range(5):
       c.append(pp[randint(0,4)])
   Curve(c,color=makecolor(b=1,r=.8), linewidth=.1,density=DENSITY,drawpoints=True)
   x+=1


x=0
while x < CURVES:
   c=[]
   for i in range(3):
       c.append(pp[randint(0,3)])
   Curve(c,color=makecolor(g=1,b=.8), linewidth=.1,density=DENSITY,drawpoints=True)
   x+=1

v.pickloop()


