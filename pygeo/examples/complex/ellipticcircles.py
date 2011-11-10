from pygeo import *

# the elliptical pencil of circles determined by a sheaf of planes
# centered internally to the Riemann sphere

# set diaply options
v=display(title="Elliptic Circles",scale=5,width=600,height=600,
          panel=False,camera_vector=[0,4,-1])

# the density of the plane sheaf - as a constant if 
DENSITY=30

# the origin centered unit sphere
u=uSphere()

# pickable point constrained to the unit sphere, at
# given initial rotations from the north pole

n=uSlider(theta = PI/2,phi=PI/2,pointsize=.2)
s=uSlider(theta=-PI/2,phi=PI/2,pointsize=.2)

# a line through the pickable points

line=rLine(n,s,seg=True)

# the sheaf of planes on the line

planes=PlaneArray(line,level=3)

# the pencil of spheric sections cut by the sheaf of planes

u_pencil=uCirclePencil(planes,color=BLUE)

# the projection of the spheric sections to the complex plane

zCirclePencil(u_pencil,color=CYAN)

# enter loop for picking of movable points

v.pickloop()
