from pygeo import *

v=display(title="Sphere Inverse",scale=5,width=600,height=600,background=(0,.7,1),
camera_vector=(0,-.2,-1))

# point at the origin
O=Point(pointsize=.05)

#point on the y-axis distance 1 from the origin
N=Point(0,1,0,pointsize=.07,color=BLUE)

# the plane normal to the y-axis at the orignal - i.e the xz plane
C_plane=Plane(N,O,scale=5,level=1)

# the unit orignal centered sphere
R_sphere=Sphere(O,N,color=WHITE,style=FILL)

# 3 arbitrary points on the spehere that can pcik and moved, constrained
# to the sphere
a=Slider(R_sphere,theta=PI,phi=PI/4,pointsize=.09,color=RED)
b=Slider(R_sphere,theta=PI/3,phi=PI/3,pointsize=.09,color=RED)
c=Slider(R_sphere,theta=PI/2,phi=PI*.15,pointsize=.09,color=RED)

#  the circle through the 3 points
circle=CircumCircle(a,b,c,linewidth=.05,color=BLUE)

# the plane normal to the 3 points as vectors from the origin
p1=Plane(O,a,level=5,color=WHITE)
p2=Plane(O,b,level=5,color=WHITE)
p3=Plane(O,c,level=5,color=WHITE)


# the point of intersection of the 3 normal planes,
# which is the pole of the plane of the circle with respect to
# sphere

pole=Intersect(p1,p2,p3,pointsize=.15,color=WHITE)

# an array of points on the circle
pp=PointArray(circle,pointsize=.04,level=1)

# an an array of lines through the pole and the cirle points,
# which are then tangent to the sphere

LineArray(pp,pole,level=1,linewidth=.02,color=BLACK)

v.pickloop()
