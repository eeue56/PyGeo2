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
         if m > COMPLEX_MAX:
            return (pos/m)*COMPLEX_MAX
         else:
            return pos
      except OverflowError:
         return (COMPLEX_MAX,COMPLEX_MAX,COMPLEX_MAX)
   else:
      return pos

class zPoint:


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
          if self.tracecurve:
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



class zLine:

   def _redraw(self):
      h=self._hermitian
      b = h.C*1j
      c= -h.D/(2*h.B)
      self.f.axis=vector(b.real,b.imag,0)
      self.f.pos=vector(c.real,c.imag,0)
      self.rend[0].pos=self.m  #transpose((self.m, 0*self.m,0*self.m))

   def draw(self):
      self.f=frame()
      self.m = array([[COMPLEX_MAX,0.,0.],[-COMPLEX_MAX,0,0]])
      self.rend=[curve(frame=self.f,color=self.color,
                                 radius=self.linewidth)]
      self.init_draw=True


   def povout(self,buf):
      print >> buf, "\n //LINE"
      p1=self.rend[0].pos[0]
      p2=self.rend[0].pos[1]
      pos=self.f.pos
      theta,phi=Position3(self.f.axis).polar()
      d_convert=180/PI
      theta*=d_convert
      phi*=d_convert
      rotate = "rotate<%f,%f,%f>" %(0.,90.+theta,phi)
      translate="translate<%f,%f,%f>" %(pos.x,pos.y,0.)

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


class zCircle:
   def _redraw(self):
         try:
            h= self._hermitian
         except AttributeError:
            return
         if h.A  <> 0:
            if hasattr(self._radius,'imag'):
               if abs(self._radius.imag) > EPS:
                 radius = 0
               else:
                 radius=self._radius.real
            else:
               if self._radius > COMPLEX_MAX:
                   radius= COMPLEX_MAX
               else:
                  radius=self._radius
            self._radius

            self.f.pos=constrain_draw(self._center.pos)
            self.rend[0].pos=constrain_draw((self.c*radius))
         
         else:
            b = h.C*1j
            try:
               c= -h.D/(2*h.B)
            except ZeroDivisionError:
               c=COMPLEX_MAX
            self.f.axis=vector(b.real,b.imag,0)
            self.f.pos=vector(c.real,c.imag,0)
            self.rend[0].pos=self.m#transpose((self.m, 0*self.m,0*self.m))


   def povout(self,buf):
      print >> buf, "\n //CIRCLE"
      center=self._center
      if hasattr(self._radius,'real'): 
         radius=self._radius.real
      else:
         radius = self._radius
      color=self.color
      translate="translate<%f,%f,%f>" %(center.x,center.y,0.)
      if self._hermitian.A <> 0:
         if self.style==LINES:
             print >> buf,"""
torus {
    %f, %f
    rotate <90,0,00>
    %s
    pigment {color rgb <%f, %f, %f> filter 0 transmit  0.0
}\n}"""   %(radius,self.linewidth,translate,
            color[0],color[1],color[2])

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
 }\n}"""     %(len(self.rend[0].pos),poly,translate,
               self.color[0],self.color[1],self.color[2])
      else:
          print >> buf, "\n //LINE"
          p1=self.rend[0].pos[0]
          p2=self.rend[0].pos[1]
          pos=self.f.pos
          theta,phi=Position3(self.f.axis).polar()
          d_convert=180/PI
          theta*=d_convert
          phi*=d_convert
          rotate = "rotate<%f,%f,%f>" %(0.,90.+theta,phi)
          translate="translate<%f,%f,%f>" %(pos.x,pos.y,0.)

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
      

   def draw(self):
      self.f = frame()
      div=2*PI/self.precision
      t = arrayrange(div,2*PI+2*div,div)
      self.m = array([[COMPLEX_MAX,0.,0.],[-COMPLEX_MAX,0,0]])
      self.c = transpose( (sin(t), cos(t),0*t) )
      if self.style==FILL:
         self.rend=[convex(frame=self.f,color=self.color)]
      else:
         self.rend=[curve(frame=self.f,color=self.color,
                                 radius=self.linewidth)]

      if self.show_normal:
         self.nrend=arrow(pos=(0,0,0),shaftwidth=self.normal_width,
                          color=self.color)
      self.init_draw=True

