from pygeo import *


v=display(scale=10,width=600,height=600,axis=False,trace_on=True)

C_RATE=60

c=Point(0,0,0,pointsize=.2)
color=makecolor()

x1=5*2
x2=10*2
y1=5*2
y2=0
color=makecolor()
circle=[]
circle.append(Circle(Point(-x1,y1,),Point(-x2,y2,),c,color=color))
circle.append(Circle(Point(x1,-y1,),Point(x2,y2,),c,color=color))
circle.append(Circle(Point(-x1,-y1,),Point(-x2,y2,),c,color=color))
circle.append(Circle(Point(x1,y1,),Point(x2,y2,),c,color=color))

cp=[]
for i in range(4):
   cp.append(CirclingPoint(circle[i],color=WHITE,rate=C_RATE))


t=[1,0,3,2]

p1=[]
color=makecolor()
for i in range(4):
  p1.append(Inversion(circle[i],cp[t[i]],pointsize=.2,trace=1,tracewidth=.2,tracecolor=color))

p2=[]
color=makecolor()
for i in range(4):
  p2.append(Inversion(circle[i],p1[t[i]],pointsize=.2,trace=1,tracewidth=.2,tracecolor=color))

p3=[]
color=makecolor()
for i in range(4):
  p3.append(Inversion(circle[i],p2[t[i]],pointsize=.2,trace=1,tracewidth=.2,tracecolor=color))

p4=[]
color=makecolor()
for i in range(4):
  p4.append(Inversion(circle[i],p3[t[i]],pointsize=.2,trace=1,tracewidth=.2,tracecolor=color))

p5=[]
color=makecolor()
for i in range(4):
  p5.append(Inversion(circle[i],p4[t[i]],pointsize=.2,trace=1,tracewidth=.2,tracecolor=color))

p6=[]
color=makecolor()
for i in range(4):
  p6.append(Inversion(circle[i],p5[t[i]],pointsize=.2,trace=1,tracewidth=.2,tracecolor=color))

p7=[]
color=makecolor()
for i in range(4):
  p7.append(Inversion(circle[i],p6[t[i]],pointsize=.2,trace=1,tracewidth=.2,tracecolor=color))

p8=[]
color=makecolor()
for i in range(4):
  p6.append(Inversion(circle[i],p7[t[i]],pointsize=.2,trace=1,tracewidth=.2,tracecolor=color))


v.animate(title="Inversions Design",frames=C_RATE)