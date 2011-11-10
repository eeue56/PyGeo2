from pygeo import *

#the characteristic parallelogram of a Mobius transformation

v=display(scale=10,panel=False)

# 6 pickable points of the complex plane
z1 = zFreePoint(-2,-1,pointsize=.1,level=-1)        
z2 = zFreePoint(-1,1,pointsize=.1,level=-1)           
z3 = zFreePoint(-6,4,pointsize=.1,level=-1)             
z4 = zFreePoint(2,1,pointsize=.1,level=-1)              
z1a=zFreePoint(4,4,pointsize=.1,level=-1)
z2a=zFreePoint(-3,-1,pointsize=.1,level=-1)

# 2 circles determined by (circumscribing) 3 of the points
zCircle(z1,z2,z1a)
zCircle(z3,z4,z2a)

#the Mobius transofrmation mapping 3 points to 3 points
m=mobTransform([z1,z2,z1a],[z3,z4,z2a],[],color=MAGENTA)

# the fixed points of the Mobius transofrmation
f1=mobFixed(m,fixed=0,color=RED)
f2=mobFixed(m,fixed=1,color=RED)

# the pole and inverse pole of the Mobius transormation 
p1=mobPole(m,color=MAGENTA)
p2=mobInversePole(m,color=MAGENTA)

# line connecting fixed points and poles
zLine(f1,p1,color=RED)
zLine(f2,p2,color=RED)
zLine(f1,p2,color=RED)
zLine(f2,p1,color=RED)

#enter pickloop
v.pickloop()