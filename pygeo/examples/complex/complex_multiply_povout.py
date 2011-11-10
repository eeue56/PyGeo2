from pygeo import *
from pygeo.utils.colors import * 

#Constants - better than picking through script when exploring effects of changes 

CYCLE=8
RECURSE=20
MULTIPLIER=.75
PROJECT=True
RECIPROCATE=True

if PROJECT:
   PLANELEVEL=2
else:
   PLANELEVEL=1 

EXPORT = False

#display window at given screen coords 

cDisplay=display(scale=1.6,panel=False,
          title="Mulipliers",background=WHITE,
          camera_vector=(0,1,-1))


#origin point of complex plane

O=zPoint(level=5)

#point of real line 

z1a = zPoint(1.0,level=5)

#line represeting real axis
radline=zLine(O,z1a,linewidth=.05,level=2)

#point movable along the real axis at initial position (.8,0) 
z2a = zSlider(radline,ratio=MULTIPLIER,pointsize=.1,level=2)

#origin center circles of radii determinec by the point
#movable along thereal line

u1=zCircle(O,z2a,color=GRAY85,level=PLANELEVEL)

#point moving along circle circumference at each update cycle

a1= zCirclingPoint(u1,color=TURQUOISE,level=PLANELEVEL,rate=CYCLE)                


#points of complex plane from which to build circles

z1 = zPoint(2,0,level=5)   
z2 = zPoint(1,1,level=5)
z3 = zPoint(-2,0,level=5)              
z4 = zPoint(-1,1,level=5)                
z5 = zPoint(0,2,level=5)
z6 = zPoint(1,1,level=5)                
z7 = zPoint(0,-2,level=5)
z8 = zPoint(1,-1,level=5)               

#circles on complex plane with given centers and circumference points

c1=zCircle(z1,z2,color=ORANGERED,export=False,level=PLANELEVEL)
c2=zCircle(z3,z4,color=ORANGERED,export=False,level=PLANELEVEL)
c3=zCircle(z5,z6,color=BRIGHTGOLD,export=False,level=PLANELEVEL)
c4=zCircle(z7,z8,color=BRIGHTGOLD,export=False,level=PLANELEVEL)



#function to recursively multiply a given list of elements by the complex 
#coordinates of a given point, with option to reciprocate at each iteration


t = [c1,c2,c3,c4]
def step(mpoint,seed,steps):
    if steps:
       a=mobMultiply(mpoint,seed,level=PLANELEVEL,export=False)
       t.append(a)
       if RECIPROCATE:
          p=mobReciprocate(a,export=False)
          t.append(p)
       steps-=1
       step(mpoint,a,steps)
    
#call the iterative function for the point circling the origan at a 
#distance of MULTIPLIER constant

step(a1,[c1,c2,c3,c4],RECURSE)


#project the circles of the iterative multiplication to the unit sphere

if PROJECT:
   uStereoProject(t,level=-1)



#enter animation loop

cDisplay.animate(frames=CYCLE,povout=EXPORT)