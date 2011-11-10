
from pygeo import *

v=display(title="Islamic Pattern 1",scale=25,width=800,height=800)

# a more "algorithmic" to creating patterns1.py"

p1 = Point(0,sqrt(300)-10,0,color=BLUE,pointsize=1,level=2)
p2 = Point(-10,-10,0,color=BLUE,pointsize=1,level=2)
p3 = Point(10,-10,0,color=BLUE,pointsize=1,level=2)
plane=Plane(p1,p2,p3,level=6)
P=Center(p1,p2,p3)


index=[0,1,2]
mindex = [2,0,1]

points=[[p1,p2,p3]]
lines=[]

def getMidPoints(plist):
   mlist=[]
   llist=[]
   color=makecolor(r=1)
   for i in range(3):
      indexcopy=index[:]
      indexcopy.remove(i)
      mlist.append(Divider(Line(plist[indexcopy[0]],plist[indexcopy[1]]),level=1))
   points.append(mlist)
   lines.append(llist)

for i in range(3):
   getMidPoints(points[i])
   color=makecolor(b=1)
   for j in range(3):
      Circle(points[i][j],points[i+1][mindex[j]],plane,color=color)


v.pickloop()

