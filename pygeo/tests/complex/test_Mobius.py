from pygeo import *

# testing of factory function for mobius transformations of the complex plane
v=display(scale=5)

z1 = zFreePoint(-2,-1,color=RED,pointsize=.1,level=-1)              # zFreePoint
z2 = zFreePoint(-1,1,color=MAGENTA,pointsize=.1,level=-1)           # zFreePoint  
z3 = zFreePoint(5,2,color=YELLOW,pointsize=.1,level=-1)             # zFreePoint
z4 = zFreePoint(2,1,color=RED,pointsize=.1,level=-1)                # zFreePoint
z5 = zFreePoint(1,-1,color=MAGENTA,pointsize=.1,level=-1)           # zFreePoint 
z6 = zFreePoint(-5,-2,color=YELLOW,pointsize=.1,level=-1)           # zFreePoint

z1a=zPoint(1,2,level=-1,color=GREEN)                                # zFreePoint
z2a = zFreePoint(1.4,0,level=-1,color=GREEN)                         # zFreePoint
z3a = zFreePoint(.1,1,level=-1,color=GREEN)                         # zFreePoint

u1=zCircle(z1,z2,level=-1)                                          #zCircleFromPoints  
u2=zCircle(z3,z4,level=-1)                                          #zCircleFromPoints 
u3=zCircle(z4,z5,z6,level=1)                                        #zCircumCircle 
u4=zCircle(z1a,z2a,z3a,level=1)

zc=zCirclePencil(u1,u2)                                             #zCircles  

mobTransform(u3,[zc],color=MAGENTA)                                 #mobUnitCircle
mobTransform(z1,[zc],color=GREEN)                                   #mobMultiply 
mobTransform(z1,[zc],alt=TRANSLATE,color=YELLOW)                    #mobTrannslate 

mobTransform([zc],level=2)                                          #mobReciprocate
m=mobTransform(z2a,[zc],level=1,alt=TRANSLATE)                              #mobMapCircles

mobTransform([z4,z5,z6],[z1a,z2a,z3a],[z1,z2,z3,zc],level=2)           #mobPointSets 
zPoint([z4,z5,z6,z1],[z1a,z2a,z3a])                                  #zCrossPoint  
zPoint([z4,z5,z6,z2],[z1a,z2a,z3a])                                  #zCrossPoint
zPoint([z4,z5,z6,z3],[z1a,z2a,z3a])                                  #zCrossPoint
mobTransform(z1,PI/4,[z1a,z2a,z3a],level=2,color=YELLOW)               #mobSphereRotation
zPoint(z1,z1a,angle=PI/4)                                              #zRotation  
zPoint(z1,z2a,angle=PI/4)                                              #zRotation
zPoint(z1,z3a,angle=PI/4)                                              #zRotation
zCircle()                                                          #z
v.pickloop()