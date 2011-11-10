from pygeo.base.pygeoconstants import *
from pygeo.base.pygeomath import *
from pygeo.base.pygeoprimitives import *
from pygeo.base.position3 import Position3

#from pygeo.base.pygeoexceptions import Argument_Len_Error,Argument_Type_Error
from pygeo.base.pygeoopts import *


# Elements register their dependency on points that are interactively moveable



# arguments to Element classes are tested against their constructor signature and
# returned ordered as per signature

def constrain_draw(pos):
   if TEST_MAX:
      try:
         m=max(absolute(pos))
         if m > MAX:
            return (pos/m)*MAX
         else:
            return pos
      except OverflowError:
         return (MAX,MAX,MAX)
   else:
      return pos

class Point:


    def _redraw(self):
       if self.init_draw:
          self.rend[0].pos =self.pos
          if self.label:
              self.lab.pos= self.pos

    def draw(self):
       #For consistency in iterating Element's rendering objects, all elements
       #rendering information is in a list called self.rend. In the case of Points,
       #it is a single element list, containing a VPython sphere object

       self.rend.append(sphere(radius=self.pointsize))
       self.rend[0].color=self.rend[0].initcolor=self.color
       if self.label:
          self.lab=label(box=False, opacity=0.,
                         color=self.fontcolor,text=self.label,
                         xoffset=self.fontXoffset,yoffset= self.fontYoffset,
                         space=.5, height=self.fontsize, border=2)
       if self.trace:
          self.ntrace = curve(radius=self.tracewidth,
                             color=self.tracecolor)
       self.init_draw=True

    def povout(self,buf):
       print >>buf,"\n //POINT"
       if hasattr(self,'complex'):
         x=self.real
         y=self.imag
         z=0
       else:
         x=self.x
         y=self.y
         z=self.z
       print >>buf,"""
sphere {\n <%f, %f, %f> , %f
pigment {\n color rgb <%f, %f, %f> filter 0 transmit  0.0 }
}\n
"""       %(x,y,z,
            self.pointsize,self.color[0],
            self.color[1],self.color[2])
       if self.trace:
           print >>buf,"\n //POINT TRACE"
           for trace in self.rtrace:
               trace.povout(buf)
           i=0
           while i < len(self.ntrace.pos)-1:
              p1=self.ntrace.pos[i]
              p2=self.ntrace.pos[i+1]
              print >> buf, """
cylinder{\n<%f, %f, %f> , <%f, %f, %f>, %f
pigment {color rgb <%f, %f, %f> filter 0 transmit  0.0
\n} \n}"""     %(p1[0],p1[1],p1[2],
                 p2[0],p2[1],p2[2],
                 self.tracewidth,self.tracecolor[0],
                 self.tracecolor[1],self.tracecolor[2])
              print >>buf,"""
sphere {\n <%f, %f, %f> , %f
pigment {\n color rgb <%f, %f, %f> filter 0 transmit  0.0 }
}\n
"""       %(p1[0],p1[1],p1[2],
            self.tracewidth,self.tracecolor[0],
            self.tracecolor[1],self.tracecolor[2])
              i+=1



class Line:


   def _redraw(self):
      if self.seg:
          self.rend[0].pos=map(constrain_draw,[self.p1.pos,self.p2.pos])
          if self.bounds1:
              self.rend[0].append(pos=self.bounds1.pos)
          if self.bounds2:
              self.rend[0].append(pos=self.bounds2.pos)
          if self.label:
             self.setlabel()

      else:
         mid=(self.p1+self.p2)/2.
         dir=self.getDirection()
         self.f.axis=vector(dir.x,dir.y,dir.z)
         self.f.pos=vector(mid.x,mid.y,mid.z)
         self.rend[0].pos=self.m  #transpose((self.m, 0*self.m,0*self.m))

      if self.show_normal:
         norm=self.getNormal()
         self.nrend.axis = vector(norm.x,norm.y,norm.z)
      if self.extend:
         self.setext()
           

   def setlabel(self):
      labelpos=(self.p1+self.p2)/2
      self.lab.pos=labelpos

   def draw(self):
      self.f=frame()
      self.m = array([[MAX,0.,0.],[-MAX,0,0]])
      self.rend=[curve(frame=self.f,radius=self.linewidth)]
      self.rend[0].color=self.rend[0].inticolor=self.color
      if self.label:
         self.lab=label(frame=self.f,box=False, opacity=0.,
                               color=self.fontcolor,text=self.label,
                               xoffset=self.fontXoffset,yoffset= self.fontYoffset,
                               space=.5, height=self.fontsize, border=2)
      if self.show_normal:
         self.nrend=arrow(shaftwidth=self.normal_width,
                                 color=self.color)
      self.init_draw=True


   def povout(self,buf):
       print >> buf, "\n //LINE"
       if self.seg:
           i=0
           while i < len(self.rend[0].pos)-1:
              p1=self.rend[0].pos[i]
              p2=self.rend[0].pos[i+1]
              if max(absolute(p1-p2)) > EPS:
                  print >> buf, """
cylinder{\n<%f, %f, %f> , <%f, %f, %f>, %f
pigment {color rgb <%f, %f, %f> filter 0 transmit  0.0
\n} \n}"""     %(p1[0],p1[1],p1[2],
                 p2[0],p2[1],p2[2],
                 self.linewidth,self.color[0],
                 self.color[1],self.color[2])
                  print >>buf,"""
sphere {\n <%f, %f, %f> , %f
pigment {\n color rgb <%f, %f, %f> filter 0 transmit  0.0 }
}\n
"""       %(p1[0],p1[1],p1[2],
            self.linewidth,self.color[0],
            self.color[1],self.color[2])
              i+=1
       else:
           p1=self.rend[0].pos[0]
           p2=self.rend[0].pos[1]
           pos=self.f.pos
           theta,phi=Position3(self.f.axis).polar()
           d_convert=180./PI
           theta*=d_convert
           phi*=d_convert
           rotate = "rotate<%f,%f,%f>" %(0.,90.+theta,phi)
           translate="translate<%f,%f,%f>" %(pos.x,pos.y,pos.z)

           if max(absolute(p1-p2)) > EPS:
                print >> buf, """
cylinder{\n<%f, %f, %f> , <%f, %f, %f>, %f
%s
%s
pigment {color rgb <%f, %f, %f> filter 0 transmit  0.0
\n} \n}"""     %(p1[0],p1[1],p1[2],
                 p2[0],p2[1],p2[2],self.linewidth,
                 rotate,
                 translate,
                 self.color[0],self.color[1],self.color[2])
       if self.trace:
           for trace in self.rtrace:
               trace.povout(buf)


class Plane:

   def _redraw(self):
      self.f.axis = self._u
      if self._d:
         self.f.pos=self._u*self._d
      if self.show_normal:
         self.nrend.axis = self._u
         self.nrend.length= self._d


   def draw(self):
      self.f=frame()
      ext=self.scale*10

      if self.style == FILL:
         self.rend.append(box(frame=self.f,length=.01,height=ext,width=ext,
                           color=self.color,linewidth=self.linewidth))

      else:
        for i in range((self.scale*10+1)):
            self.rend.append(curve(frame=self.f,pos=[(0,2*i-ext,-ext),
                                         (0,2*i-ext,ext)],
                             color=self.color,linewidth=self.linewidth))
            self.rend.append(curve(frame=self.f,pos=[(0,-ext,2*i-ext),
                                         (0,ext,2*i-ext)],
                             color=self.color,linewidth=self.linewidth))
      if self.show_normal:
         self.nrend=arrow(shaftwidth=self.normal_width,
                                 color=self.color)
      self.init_draw=True

   def povout(self,buf):
       from pygeo.base.abstract_elements_real import _Triangle
       u=self._u
       d=self._d
       color=self.color
       if isinstance(self,_Triangle):
             print >> buf, "\n //Triangle"
             if self.style==FILL:
                p1=self.p1
		p2=self.p2
		p3=self.p3
                t1="<%f,%f,%f>\n" %(p1.x,p1.y,p1.z)
                t2="<%f,%f,%f>\n" %(p2.x,p2.y,p2.z)
                t3="<%f,%f,%f>\n" %(p3.x,p3.y,p3.z)
                print >> buf,"""
       
triangle{
          %s,
          %s
          %s
          pigment {color rgb <%f, %f, %f> filter 0 transmit  0.0
        }\n}"""     %(t1,t2,t3,color[0],color[1],color[2])
             

             else:
                 i=0
                 while i < len(self.rend[0].pos)-1:
                     p1=self.rend[0].pos[i]
                     p2=self.rend[0].pos[i+1]
                     if max(absolute(p1-p2)) > EPS:
                         print >> buf, """
cylinder{\n<%f, %f, %f> , <%f, %f, %f>, %f
pigment {color rgb <%f, %f, %f> filter 0 transmit  0.0
\n} \n}"""     %(p1[0],p1[1],p1[2],
                 p2[0],p2[1],p2[2],
                 self.linewidth,color[0],color[1],color[2])
                     i+=1                      

       else:
          print >> buf, "\n //PLANE"
          print >> buf, """

plane{ <%f,%f,%f>, %f  pigment {color rgb <%f, %f, %f> filter .95 transmit .95
}\n}""" %(u.x,u.y,u.z,d, color[0],color[1],color[2])   

class Circle:

   def _redraw(self):
      if hasattr(self._radius,'imag'):
         if abs(self._radius.imag) > EPS:
           radius = 0
         else:
           radius=self._radius.real
        
      else:
         if self._radius > MAX:
             radius= MAX
         else:
             radius=self._radius
      self.f.axis=self._u
      self.f.pos=constrain_draw(self._center.pos)
      self.rend[0].pos=constrain_draw((self.c*radius))
      if self.show_normal:
         self.nrend.axis=self._u
         self.nrend.length=-self._d

   def draw(self):
      self.f = frame()
      div=2*PI/self.precision
      t = arrayrange(div,2*PI+div*2,div)
      self.c = transpose( (0*t, sin(t), cos(t)) )

      if self.style==FILL:
         self.rend=[convex(frame=self.f,color=self.color)]
      else:
         self.rend=[curve(frame=self.f,color=self.color,
                                 radius=self.linewidth)]

      if self.show_normal:
         self.nrend=arrow(pos=(0,0,0),shaftwidth=self.normal_width,
                          color=self.color)
      self.init_draw=True

   def povout(self,buf):
      print >> buf, "\n //CIRCLE"
      center=self._center
      s=self._s
      radius=self._radius
      u=self._u
      v= s.cross(u).norm()
      matrix="matrix"
      matrix=matrix+"<%f,%f,%f,\n" %(u.x,u.y,u.z)
      matrix=matrix+" %f,%f,%f,\n" %(v.x,v.y,v.z)
      matrix=matrix+" %f,%f,%f,\n" %(s.x,s.y,s.z)
      matrix=matrix+" %f,%f,%f>\n" %(center.x,center.y,center.z)

      if self.style==LINES:
         print >> buf,"""
torus {
    %f, %f
    rotate <0,0,-90>
    %s
    pigment {color rgb <%f, %f, %f> filter 0 transmit  0.0
}\n}"""   %(radius,self.linewidth,matrix,
            self.color[0],self.color[1],self.color[2])

      else:
         poly=""

         for pos in self.rend[0].pos:
              poly = poly +   "<%f,%f,%f>\n" %(pos[0],pos[1],pos[2])
         print >> buf,"""
polygon{
   %i,
   %s
   %s
   pigment {color rgb <%f, %f, %f> filter 0 transmit  0.0
 }\n}"""     %(len(self.rend[0].pos),poly,matrix,
               self.color[0],self.color[1],self.color[2])

class Sphere:

   def _redraw(self):
      radius=self._radius
      center=constrain_draw(self._center.pos)
      if radius > MAX:
         radius= MAX
      if self.style == FILL:
         self.rend[0].pos=center
         self.rend[0].radius=radius
      else:
         self.f.pos=center
         j=0
         k=self.precision
         while j < self.precision:
           self.rend[j].pos= self.stacks[j] * radius
           self.rend[k].pos=self.slices[j] * radius
           j+=1
           k+=1

   def draw(self):
      self.f=frame()
      if self.style == FILL:
          self.rend.append(sphere(frame=self.f))
          self.rend[0].color=self.rend[0].initcolor=self.color
      else:
         ws=wiresphere(self.precision)
         self.stacks=ws.getstacks()
         self.slices=ws.getslices()
         self.f=frame()
         j=0
         while j < self.precision*2:
            self.rend.append(curve(frame=self.f,color=self.color,
                            radius=self.linewidth))
            j+=1
      self.init_draw=True

   def povout(self,buf):
       center=self._center
       if self.style==FILL:
          print >> buf,"\n //SPHERE"
          print >> buf,"""
sphere{\n <%f, %f, %f> , %f
 pigment {\n color rgb <%f, %f, %f> filter 0 transmit  0.0
 }\n}
"""     %(center.x,center.y,center.z,
          self._radius,self.color[0],
          self.color[1],self.color[2])
       elif self.style == LINES:
          for rend in self.rend:
             i=0
             while i < len(rend.pos)-1:
                p1=rend.pos[i]
                p2=rend.pos[i+1]
                print >> buf, """
cylinder{\n<%f, %f, %f> , <%f, %f, %f>, %f
translate <%f, %f, %f>
pigment {color rgb <%f, %f, %f> filter 0 transmit  0.0
\n} \n}"""     %(p1[0],p1[1],p1[2],
                 p2[0],p2[1],p2[2],
                 self.linewidth,
                 center.x,center.y,center.z,
                 self.color[0],
                 self.color[1],self.color[2])
                print >>buf,"""
sphere {\n <%f, %f, %f> , %f
translate <%f, %f, %f>
pigment {\n color rgb <%f, %f, %f> filter 0 transmit  0.0 }
}\n
"""       %(p1[0],p1[1],p1[2],
            self.linewidth,
            center.x,center.y,center.z,
            self.color[0],self.color[1],self.color[2])
                i+=1
class PointArray:

   def _redraw(self):
      if self.drawcurve:
         self.crend[0].pos=self.pos


   def draw(self):
      if self.drawcurve:
         self.crend=[curve(radius=self.linewidth)]
         self.crend[0].color=self.initcolor=self.color

   def povout(self,buf):
      if self.drawcurve:
         print >> buf,"\n //CURVE POINTS "
         rend=self.crend[0]
         i=0
         while i < len(rend.pos)-1:
            p1=rend.pos[i]
            p2=rend.pos[i+1]
            if max(absolute(p1-p2)) > EPS:

               print >> buf, """
cylinder{\n<%f, %f, %f> , <%f, %f, %f>, %f
pigment {color rgb <%f, %f, %f> filter 0 transmit  0.0
\n} \n}
"""         %(p1[0],p1[1],p1[2],
            p2[0],p2[1],p2[2],
            self.linewidth,
            self.color[0],
            self.color[1],self.color[2])

               print >>buf,"""
sphere {\n <%f, %f, %f> , %f
pigment {\n color rgb <%f, %f, %f> filter 0 transmit  0.0 }
}\n
"""        %(p1[0],p1[1],p1[2],
             self.linewidth,
             self.color[0],self.color[1],self.color[2])

            i+=1

class Triangle:

   def _redraw(self):
      if self.style == FILL:
          self.rend[0].pos=[self.p1.pos,self.p2.pos,self.p3.pos,self.p3.pos,self.p2.pos,self.p1.pos]
          norm1=self._u
          norm2=-self._u
          self.rend[0].normal=self._getNormal()
          self.rend[0].color=self.color
      else:
          self.rend[0].pos=[self.p1.pos,self.p2.pos,self.p3.pos,self.p1.pos]

   def draw(self):
     if self.style == FILL:
         self.rend=[faces()]
     else:
         self.rend=[curve(radius=self.linewidth)]
         self.rend[0].color=self.rend[0].initcolor=self.color
     self.init_draw=True
