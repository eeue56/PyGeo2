
# PyGeo modules
from pygeo.base.position3 import Position3
from pygeo.base.pygeoconstants import *
from pygeo.base.pygeomath import *
from pygeo.base.pygeoprimitives import *
from pygeo.base.pygeoopts import *
import pygeo.base.vdraw as Draw
from pygeo.base.element import Element,freepoints

AbstractRealClasses = ['_Point','_FreePosition', '_Line', '_Plane',
'_Circle', '_Sphere','_PointArray', '_LineArray', '_PlaneArray',
'_CirclePencil', '_Transformation']



__all__=AbstractRealClasses


#rads to degrees constant
RK=180/PI


# arguments to Element classes are tested against their constructor signature and
# returned ordered as per signature

def method_get(sigs,args):
   def order(sig,_args):
      w=[]
      args=_args[:]
      for S in sig:
         v=[issubclass(a.__class__,S) for a in args]

         if 1 in v:
            w.append(args[v.index(1)])
            args.pop(v.index(1))

      return w
   args=list(args)
   for i in range(len(args)):
      if type(args[i])== int:
         args[i]=float(args[i])
   ret=[]
   for S in sigs:
      if len(args) == len(S):
         final_args = order(S,args)
         if len(final_args) == len(S):
             ret.append([final_args,sigs.index(S)])
   if ret:
      return max(ret)
   else:
      return None,None


class _Point(Position3,Element,Draw.Point):
   """
:definition: an O dimensional object with a defined position in space. 
:inherits:  `class Element`_ , base.Position3, base.vdraw.Point
:site ref: http://mathworld.wolfram.com/Point.html
:attributes: 

   - x
   - y
   - z

:keywords: 

   inherited keywords: from `class Element`_ :

   ===========   ============================     =================  =====================
   Keyword       Definition                        Type               Default 
   ===========   ============================     =================  =====================
   color         drawn color of object            list of 3 numbers  [0,0,1] (BLUE) 
   level         visibility "level" - see GUI     integer            1
   trace         toggle for tracing function      boolean            False 
   texture       texture for Povray output        string             None
   ===========   ============================     =================  =====================

   class keywords:  

   ===========   ==========================   ==================     =====================
   pointsize     size of drawn point          numeric                .5 
   label         label rendered for point     string                 None 
   tracewidth    width of trace curve         numeric                pointsize/2  
   tracecolor    color of trace curve         list of 3 numbers      color
   fontsize      fontsize of label            constant               NORMALFONT
   fontcolor     color of label font          constant               BLACK
   fontXoffset   horizontal offset of label   numeric                pointsize/10.+ 3.0
   fontYoffset   vertical offset of label     numeric                pointsize/10.+ 3.0
   ===========   ==========================   ==================     =====================
   """                                    
   __opts__= Element.__opts__[:] + ["pointsize","tracewidth","tracecolor",
                                    "maxtrace","mintrace", "fontsize",
                                    "fontcolor","fontXofffset","fontYofffset"]
   def __init__(self,*args,**kws):
      #inherit geometric intelligence of the Position3 class
      
      Position3.__init__(self,*args)
      self.Not_null = True
      self._pos=None
      
      #inherit default attributes and functions common to all PyGeo elements. Overide
      #defaults where desired.
      
      Element.__init__(self,*args,**kws)
      # override defalut color of Element clasas
      
      self.color = kws.get("color",CYAN)
      
      #set defaults for keyword arguments specific to Points and derived classes.
      
      self.pointsize=kws.get("pointsize",.5)
      if self.label:
         self.fontsize=kws.get("fontsize",NORMALFONT)
         self.fontcolor=kws.get("fontcolor",BLACK)
         self.fontXoffset=kws.get("fontXoffset",self.pointsize/10.+3)
         self.fontYoffset=kws.get("fontYoffset",self.pointsize/10.+3)

      if self.trace:
         self.tmparray=Position3()
         self.tmparray.set(self)
         self.mintrace=kws.get("mintrace",.1)
         self.maxtrace=kws.get("maxtrace",200.)
         self.tracewidth=kws.get("tracewidth",self.pointsize/2.0)
         self.tracecolor=kws.get("tracecolor",self.color)
 
      
      self.deps=[]


   def setext(self):
         for line in self.lines:
             if line.seg:
                line.get_extension(self)
                line._redraw()

   def __eq__(self, other):
      if hasattr(other,'x'):
          return  ((abs(self.x - other.x)) < EPS and 
                (abs(self.y - other.y)) < EPS 
                 and (abs(self.z-other.z)) < EPS)
      else:
          return id(self)== id(other)
   
   def do_trace(self):
      #If, on update, traced point has moved within limits defined by
      #'mintrace' and 'maxtrace' append its new position to the trace
      #curve
      from pygeo.classes_real.points.basepoints import Point
      delta= self.distance(self.tmparray)

      if (self.mintrace < delta < self.maxtrace):
             self.rtrace.append(Point(self,pointsize=self.pointsize,color=self.tracecolor,
                     level=self.level))
             self.ntrace.append(pos=self.pos)
      self.tmparray.set(self)
      
   def reset_trace(self):
      #Re-intialize list of traced curves to None"""
      if self.trace:
         for r in self.rtrace:
            r.show=False
            r.setshow()
         self.rtrace=[]
         self.tmparray.set(self)

   def reset_trace_curves(self):
      #Re-intialize list of traced curves to None"""
      if self.trace:
         self.ntrace.pos=[]

   def polar(self):
     s = hypot(self.x,self.y)
     t=arctan2(self.y,self.x)
     p=arctan2(s,self.z)
     return p,t


class _FreePosition(_Point):
   """
:definition: an O dimensional object which can be picked and moved through the scene 
             display interface. 
:inherits:  `class _Pointt`_ 
:site ref: http://mathworld.wolfram.com/Point.html
:attributes: 

   - x: x coord
   - y: y coord
   - z: z coord

:keywords: 

   inherited keywords: from `class Element`_ :

   ===========   ============================     =================  =====================
   Keyword       Definition                        Type               Default 
   ===========   ============================     =================  =====================
   color         drawn color of object            list of 3 numbers  [0,0,1] (BLUE) 
   level         visibility "level" - see GUI     integer            1
   trace         toggle for tracing function      boolean            False 
   texture       texture for Povray output        string             None
   ===========   ============================     =================  =====================

   inherited keywords: from `class _Point`_ :

   ===========   ==========================   ==================     =====================
   pointsize     size of drawn point          numeric                .5 
   label         label rendered for point     string                 None 
   tracewidth    width of trace curve         numeric                pointsize/2  
   tracecolor    color of trace curve         list of 3 numbers      color
   fontsize      fontsize of label            constant               NORMALFONT
   fontcolor     color of label font          constant               BLACK
   fontXoffset   horizontal offset of label   numeric                pointsize/10.+ 3.0
   fontYoffset   vertical offset of label     numeric                pointsize/10.+ 3.0
   ===========   ==========================   ==================     =====================
   """
   def __init__(self,*args,**kws):
      _Point.__init__(self,*args,**kws)
      self.color = kws.get("color",BLUE)
      self.initcolor=self.color
      self.pointsize=kws.get("pointsize",.7)
      self.initpointsize=self.pointsize
      self.initvector=Position3()
      self.initvector.set(self)
      freepoints.append(self)
      self.dependants=[self]

   def _add_dependant(self,e):
      self.dependants.append(e)

   def reset(self):
      """Reset to position of start-up input"""
      self.pointsize=self.initpointsize
      self.color = self.initcolor
      self.set(self.initvector)
      _Point._redraw(self)


class _Line(Element,Draw.Line):
   """
:definition: an 1 dimensional object representing "breathless length"
:inherits: `class Element`_ ,base.vdraw.Line
:site ref: http://mathworld.wolfram.com/Line.html
:attributes:  

   - p1
   - p2

:keywords: 

   inherited keywords from `class Element`_ :
   
   ===========   ============================     =================  =====================
   Keyword       Definition                        Type               Default 
   ===========   ============================     =================  =====================
   color         drawn color of object            list of 3 numbers  [0,1,0] (GREEN) 
   level         visibility "level" - see GUI     integer            1
   trace         toggle for tracing function      boolean            False 
   texture       texture for Povray output        string             None
   ===========   ============================     =================  =====================

   class keywords:  

   ============  ==========================   ========       =====================
   linewidth     width of drawn line          numeric         .2 
   label         label rendered for point     string          None 
   fontsize      fontsize of label            constant        NORMALFONT
   fontcolor     color of label font          constant        BLACK
   fontXoffset   horizontal offset of label   numeric         pointsize/10.+ 3.0
   fontYoffset   vertical offset of label     numeric         pointsize/10.+ 3.0
   label_ratio   relative position of label   numeric         .5 (midpoint)   
   show_normal   draw line normal?            boolean         False
   ============  ==========================   ========       =====================
   """
   __opts__ = _Point.__opts__[:]+["linewidth","label_ratio","show_normal","seg"]
   __opts__.remove("pointsize")

   def __init__(self,*args,**kws):
      Element.__init__(self,*args, **kws)
      self.linewidth=kws.get("linewidth",.2)
      self.color = kws.get("color",GREEN)
      self.show_normal=kws.get("show_normal",False)
      self.normal_width=kws.get("normal_width",.4)
      self.seg=kws.get('seg',False)
      self.bounds1=None
      self.bounds2=None
      self.direction=Position3()
      self.normal=Position3()
      if self.label:
         self.fontsize=kws.get("fontsize",NORMALFONT)
         self.fontcolor=kws.get("fontcolor",BLACK)
         self.lratio=kws.get("label_ratio",.5)
         self.fontXoffset=kws.get("fontXoffset",self.linewidth/10+1)
	 self.fontYoffset=kws.get("fontYoffset",self.linewidth/10+1)

      self.p1=_Point(append=False)
      self.p2=_Point(append=False)
      if self.trace:
         self.tracewidth=kws.get("tracewidth",self.linewidth)
         self.tracecolor=kws.get("tracecolor",self.color)
      self.deps=[]
      
   def __repr__(self):
      return self.__class__.__name__ + "(" + str(self.p1) +"," + str(self.p2) + ")"

   def transform(self,mat,obj):
      self.p1.transform(mat,obj.p1)
      self.p2.transform(mat,obj.p2)
      if self.bounds1:
         obj.bounds1=_Point()
         self.bounds1.transform(mat,obj.bounds1)
      else:
         obj.bounds1=None
      if self.bounds2:
         obj.bounds2=_Point()
         self.bounds2.transform(mat,obj.bounds2)
      else:
         obj.bounds2=None


   def get_extension(self,point):
      if self.seg:
         if point.show and point.Not_null and self.show and self.Not_null:
            a=self.lengthSquared()
            b=self.p1.distanceSquared(point)
            c=self.p2.distanceSquared(point)
            if a > b and a > c:
                return False
            elif a < b:
                self.bounds2=point
                self.bounds1=None
                return True
            else:
                self.bounds1=point
                self.bounds2=None
                return True
         else:
             self.bounds1=None
             self.bounds2=None
             return False
      else:
         self.bounds1=None
         self.bounds2=None
         return False

   def homogenous_XY(self):
     tp1=toXY(self.p1)
     tp2=toXY(self.p2)
     return array(cross(tp1,tp2))

   def getNormal(self):
     N=self.getDirection()
     self.normal.set(self.p2 - self.p2.dot(N)*N)
     return self.normal
     
   def homogenous(self):
     cr=p1.cross(p2).norm()
     return array((cr[0],cr[1],cr[2],0.))

   def parameters(self):
      return self.getNormal(), self.getDirection()

   def getDirection(self):
      try:
         self.direction.set((self.p2-self.p1).norm())
      except ZeroDivisionError:
         self.direction.set(vector(0,0,0))
      return self.direction

   def lengthSquared(self):
      return self.p1.distanceSquared(self.p2)

   def length(self):
      return self.p1.distance(self.p2)

   def reset_trace(self):
      for r in self.rtrace:
          r.show=False
          r.setshow()
      self.rtrace=[]
 
   def do_trace(self):
     from pygeo.classes_real.lines.lines import Line

     """If, on update, traced point has moved within limits defined by
      'mintrace' and 'maxtrace' append its new position to the trace
     curve"""
     l=Line(Position3(self.p1),Position3(self.p2),
            linewidth=self.tracewidth,color=self.tracecolor,
            seg=self.seg,level=self.level)
     self.rtrace.append(l)


class _Plane(Element,Draw.Plane):
   """
:definition: a 2 dimensional surface spanned by two linearly independent vectors
:inherits:  `class Element`_  ,base.vdraw.Plane
:site ref: http://mathworld.wolfram.com/Plane.html
:attributes:  

   - _u : the unit normal
   - _d : the distance from origin
   - _s : unit vector perp to normal

:keywords: 

   inherited keywords from `class Element`_ :
   
   ===========   ============================     =================  =====================
   Keyword       Definition                        Type               Default 
   ===========   ============================     =================  =====================
   color         drawn color of object            list of 3 numbers  [1,0,0] (RED) 
   level         visibility "level" - see GUI     integer            1
   trace         toggle for tracing function      boolean            False 
   texture       texture for Povray output        string             None
   ===========   ============================     =================  =====================

   class keywords:  

   ============  ==========================   ========       =====================
   style         drawing style                constant        LINES
   linewidth     width of drawn lines         numeric        .02 
   scale         drawing scale                numeric         1 
   show_normal   draw normal                  boolean         False
   normal_width  width of drawn normal        numeric         .4
   ============  ==========================   ========       =====================
   """
   __opts__= Element.__opts__[:] + ["style","linewidth","scale",
                                   "show_normal","normal_width"]

   def __init__(self,*args,**kws):
      Element.__init__(self, *args,**kws)
      self.color = kws.get("color",WHITE)
      self.style = kws.get("style",LINES)
      self.linewidth=kws.get("linewidth",.02)
      self.scale=kws.get("scale",10)
      self.show_normal=kws.get("show_normal",False)
      self.normal_width=kws.get("normal_width",.4)
      self._u=Position3(0,0,0)
      self._s=Position3(0,0,0)
      self._d=0
      self.deps=[]

   def __repr__(self):
      return self.__class__.__name__ +  repr(self._u)#,self.p2,self.p3


   def __str__(self):
      return self.__class__.__name__  +  repr(self._u)#,self.p2,self.p3

   def set_uds_fromPoints(self):
        t= self.p1.coLinear(self.p2,self.p3)
        if t:
           print "plane's defining points are colinear"
           return False
        else:   
           self._u.set(cross3(self.p1,self.p2,self.p3).norm())
           self._d = self._u.dot(self.p1)
           self._s.set((self.p1-self.p2).norm())
           return True
        
   def set_s_from_u(self,u):
      lxy = hypot(u.x,u.y)
      if (lxy >= EPS):
         self._s.set(vector(-u.y/lxy,u.x/lxy,0.).norm())
      else:
         self._s.set(vector(1.,0.,0.))

   
   def rmatrix(self):
      s=self._s
      u=self._u
      v=s.cross(u).norm()
      normal=u*self._d
      return array(((u.x,u.y,u.z,0.),
                     (v.x,v.y,v.z,0.),
                     (s.x,s.y,s.z,0.),
                     (normal.x,normal.y,normal.z,1.)),'d')

   def parameters(self):
     normal=self._u*self._d
     t=cross(self._u,self._s)
     return normal,self._s,t

   def equat(self):
      u=self._u
      return array([u.x,u.y,u.z,-self._d])

   def setshow(self):
      Element.setshow(self)
      if self.show_normal:
         if self.show and self.Not_null:
            self.nrend.visible=True
         else:
            self.nrend.visible=False


class _Triangle(_Plane,Draw.Triangle):
    def _redraw(self):
       Draw.Triangle._redraw(self)

    def draw(self):
       Draw.Triangle.draw(self)

class _Circle(Element,Draw.Circle):
   """
:definition: the set of points in a plane_ that are equidistant from a given point_
:inherits:  `class Element`_ , base.vdraw.Circle
:site ref: http://mathworld.wolfram.com/Circle.html
:attributes:  

   - _u : the unit normal of the circle's plane
   - _d : the distance from origin of the circle's plane
   - _s : unit vector perp to normal of the circle's plane
   - _center: the circle's center
   - _cpoint: a point of the circle's circumference
   - _radius: the circle's radius
   - _radiusSquared: the square of circle's radius
:
:keywords: 

   inherited keywords from `class Element`_ :
   
   ===========   ============================     =================  =====================
   Keyword       Definition                        Type               Default 
   ===========   ============================     =================  =====================
   color         drawn color of object            list of 3 numbers  [0,0,1] (BLUE) 
   level         visibility "level" - see GUI     integer            1
   trace         toggle for tracing function      boolean            False 
   texture       texture for Povray output        string             None
   ===========   ============================     =================  =====================

   class keywords:  
   
   ============  ==========================   ========       =====================
   style         drawing style                constant        LINES
   linewidth     width of drawn lines         numeric        .2 
   precision     drawing precision            integer         40 
   show_normal   draw normal                  boolean         False
   normal_width  width of drawn normal        numeric         .4
   fixed         fix to initial radius        boolean         False   
   ============  ==========================   ========       =====================
   """

   __opts__= _Plane.__opts__[:] + ["precision","fixed","circle_type"]
   __opts__.remove("scale")

   def __init__(self,*args,**kws):
      Element.__init__(self,*args,**kws)
      self.precision = kws.get("precision",40)
      self.color = kws.get("color",BLUE)
      self.style = kws.get("style",LINES)
      self.show_normal=kws.get("show_normal",False)
      self.normal_width=kws.get("normal_width",.4)
      self.fixed = kws.get("fixed",False)
      self.linewidth = kws.get("linewidth",.2)
      if self.fixed is True:
          self.init=self._findSelf
      self._radius=0
      self._radiusSquared=0
      self._u=Position3(0,0,0)
      self._s=Position3(0,0,0)
      self._d=0
      self._center=_Point(append=False)
      self._cpoint=_Point(append=False)
      self.type = kws.get("type","Center")
#      self.draw()
      self.deps=[]


   def rmatrix(self):
      s=self._s
      u=self._u
      v=s.cross(u).norm() 
      return array(((u.x,u.y,u.z,0.),
                     (v.x,v.y,v.z,0.),
                     (s.x,s.y,s.z,0.),
                     (self._center.x,self._center.y,self._center.z,1.)),'d')


   def equat(self):
      return array([self._u.x,self._u.y,self._u.z,-self._d])

   def set_uds_fromPoints(self):
        self._u.set(cross3(self.p1,self.p2,self.p3).norm())
        self._d = self._u.dot(self.p1)
        self._s.set((self.p1-self.p2).norm())

   def set_s_from_u(self,u):
      lxy = hypot(u.x,u.y)
      if (lxy >= EPS):
         self._s.set(vector(-u.y/lxy,u.x/lxy,0.).norm())
      else:
         self._s.set(vector(1.,0.,0.))
     
   
   def transform(self,mat,obj):
       points=obj.points
       rad=PI/(self.precision/2.)
       for i,point in enumerate(points):
          point.set(self._cpoint)
          point.toCircumPoint(self,i*rad)
          point.transform(mat,point)
       return True

class _Sphere(Element,Draw.Sphere):
   """
:definition: the set of points in `Euclidian space`_ that are equidistant from a given point_
:inherits:  `class Element`_ , base.vdraw.Sphere
:site ref: http://mathworld.wolfram.com/Sphere.html
:attributes:  

   - _center  the sphere's center point
   - _cpoint  a point on the sphere's circumference
   - _radius: the sphere's radius
   - _radiusSquared: the square of the sphere's radius
   
:keywords: 

   inherited keywords from `class Element`_ :
   
   ===========   ============================     =================  =====================
   Keyword       Definition                        Type               Default 
   ===========   ============================     =================  =====================
   color         drawn color of object            list of 3 numbers  [0,1,0] (GREEN) 
   level         visibility "level" - see GUI     integer            1
   trace         toggle for tracing function      boolean            False 
   texture       texture for Povray output        string             None
   ===========   ============================     =================  =====================

   class keywords:  

   ============  ==========================   ========       =====================
   style         drawing style                constant        LINES
   linewidth     width of drawn lines         numeric        .1 
   precision     drawing precision            integer         10 
   fixed         fix to initial position      boolean         False   
   ============  ==========================   ========       =====================
   """
   __opts__= Element.__opts__[:] + ["precision","style","linewidth","fixed"]

   def __init__(self,*args,**kws):
      Element.__init__(self,*args,**kws)
      self.precision= kws.get('precision',10)
      self.color = (kws.get("color",GREEN))
      self.style=kws.get('style',LINES)
      self.linewidth = (kws.get("linewidth",.1))
      self.fixed = kws.get("fixed",False)
      self._radius=0
      self._radiusSquared=0
      self._cpoint=_Point(append=False)
      self._center=_Point(append=False)
      if self.fixed is True:
          self.init=self._findSelf
      self.deps=[]
      
   def rmatrix(self):
      center=self._center
      mat=Element.rmatrix(self)
      mat[3:]=array((center.x,center.y,center.z,1.0),'d')
      return mat


class _PointArray(Element,Draw.PointArray):
   """
:definition: an array_ of point_ s with a defined geoemtric relationship
:inherits:  `class Element`_ 
:site ref: http://mathworld.wolfram.com/Array.html
:attributes:  

   - points: the positioned points of the array

:keywords: 

   inherited keywords from `class Element`_ :
   
   ===========   ============================     =================  =====================
   color         drawn color of object            list of 3 numbers  [0,1,1] (CYAN) 
   level         visibility "level" - see GUI     integer            1
   trace         toggle for tracing function      boolean            False 
   texture       texture for Povray output        string             None
   ===========   ============================     =================  =====================

   class keywords:  
   
   ============  ==========================   ========       =====================
   pointsize     size of drawn points         numeric         .4
   density       points in array              integer         25 
   ============  ==========================   ========       =====================
   """

   __opts__= Element.__opts__[:] + ["pointsize","density","drawcurve","linewidth","drawpoints"]

   def __init__(self,*args,**kws):
      Element.__init__(self,*args,**kws)
      self.density=kws.get('density',50)
      self.pointsize=kws.get('pointsize',.4)
      self.color = kws.get("color",CYAN)
      self.drawcurve=kws.get("drawcurve",False)
      self.drawpoints=kws.get("drawpoints",True)
      if self.drawcurve:
         self.linewidth= kws.get("linewidth",.2)
      self.points=[]
      self.element_array=self.points
      self.deps=[]

   def __iter__(self):
      for point in self.points:
         yield point

   def __len__(self):
      return len(self.points)

   def povout(self,buf):
      print >> buf,"\n //BEGIN POINTARRAY//"

      for point in self.points:
         point.povout(buf)
      Draw.PointArray.povout(self,buf)

   def transform(self,mat,obj):
      for point, tpoint in zip(self.points,obj.points):
          point.transform(mat,tpoint)

   def _redraw(self):
      for point in self.points:
         point._redraw()
 
      Draw.PointArray._redraw(self)



   def draw(self):
      if self.drawpoints:
         p_append=self.points.append
         i=0
         while i < self.density:
           n=_Point(pointsize=self.pointsize,color=self.
                    color,level=self.level,append=False)
           n.args=[]
           n.draw()
           p_append(n)
           i+=1
      Draw.PointArray.draw(self)
      self.init_draw=True

class _LineArray(Element):
   """
:definition: an array_ of line_ s with a defined geoemtric relationship
:inherits:  `class Element`_ 
:site ref: http://mathworld.wolfram.com/Array.html
:attributes:  

   - lines: the postioned lines of the array

:keywords: 

   inherited keywords from `class Element`_ :
   
   ===========   ============================     =================  =====================
   Keyword       Definition                        Type               Default 
   ===========   ============================     =================  =====================
   color         drawn color of object            list of 3 numbers  [1, 0, 1] (MAGENTA) 
   level         visibility "level" - see GUI     integer            1
   trace         toggle for tracing function      boolean            False 
   texture       texture for Povray output        string             None
   ===========   ============================     =================  =====================

   class keywords:  
   
   ============  ==========================   ========       =====================
   linewidth     width of drawn lines         numeric         .1
   density       lines in the array           numeric         25 
   drawradius    lenght of drawn lines        numeric         .5
   ============  ==========================   ========       =====================
   """
   __opts__= Element.__opts__[:] + ["linewidth","density","drawradius"]

   def __init__(self,*args,**kws):
      Element.__init__(self,*args,**kws)
      self.color = kws.get("color",MAGENTA)
      self.density=kws.get('density',50)
      self.linewidth=kws.get('linewidth',.1)
      self.drawradius=kws.get('drawradius',5)
      self.lines=[]
      self.element_array=self.lines
      self.deps=[]

   def _redraw(self):

      for line in self.lines:
           line._redraw()
#          line.show=self.show
#          line.setshow()
      if self.extend:
         self.setext()


   def __iter__(self):
      for line in self.lines:
         yield line

   def __len__(self):
      return len(self.lines)

   def _findSelf(self):
      pass

   def povout(self,buf):
      print >> buf,"\n //BEGIN LINEARRAY//"
      for line in self.lines:
         line.povout(buf)

   def transform(self,mat,obj):
      for line, tline in zip(self.lines,obj.lines):
          line.transform(mat,tline)

   def draw(self):
      l_append=self.lines.append
      i=0
      while i < self.density:
         n=_Line(linewidth=self.linewidth,color=self.color,
                 level=self.level,append=False)
         n.draw()
         l_append(n)
         i+=1
      self.init_draw=True

class _PlaneArray(Element):
   """
:definition: an array_ of plane_ s with a defined geoemtric relationship
:inherits:  `class Element`_ 
:site ref: http://mathworld.wolfram.com/Array.html
:attributes:  

   - planes: the postioned planes of the array

:keywords: 

   inherited keywords from `class Element`_ :
   
   ===========   ============================     =================  =====================
   Keyword       Definition                        Type               Default 
   ===========   ============================     =================  =====================
   color         drawn color of object            list of 3 numbers  [1, 0, 0] (RED) 
   level         visibility "level" - see GUI     integer            1
   trace         toggle for tracing function      boolean            False 
   texture       texture for Povray output        string             None
   ===========   ============================     =================  =====================

   class keywords:  
   
   ============  ==========================   ========       =====================
   style         drawing style for planes     CONSTANT        FILL
   density       lines in the array           integer         25 
   scale         drawing scale of planes      numeric         1
   ============  ==========================   ========       =====================
   """
   __opts__= Element.__opts__[:] + ["linewidth","style","density","scale"]

   def __init__(self,*args,**kws):
      Element.__init__(self,*args,**kws)
      self.color = kws.get("color",RED)
      self.linewidth=kws.get('linewidth',.1)
      self.style=kws.get('style',"LINES")
      self.density=kws.get('density',25)
      self.scale=kws.get('scale',1)
      self.planes=[]
      self.element_array=self.planes
      self.deps=[]



   def __len__(self):
      return len(self.planes)

   def __iter__(self):
      for plane in self.planes:
         yield plane


   def _redraw(self):
      for plane in self.planes:
          plane.show=self.show
          plane.setshow()

   def _findSelf(self):
      pass

   def povout(self,buf):
      print >> buf,"\n //BEGIN PLANEARRAY//"
      for plane in self.planes:
         plane.povout(buf)

   def draw(self):
      p_append=self.planes.append
      i=0
      while i < self.density:
         n=_Plane(linewidth=self.linewidth,color=self.color,
                  level=self.level,scale=self.scale,
                  style=self.style,append=False)
         n.args=[]
         n.draw()
         p_append(n)
         i+=1
      self.init_draw=True

class _CirclePencil(Element):
   """
:definition: an array_ of circle_ s with a defined geoemtric relationship
:inherits:  `class Element`_ 
:site ref: http://mathworld.wolfram.com/Array.html
:attributes:  

   - circles: the positioned circles of the array

:keywords: 

   inherited keywords from `class Element`_ :
   
   ===========   ============================     =================  =====================
   Keyword       Definition                        Type               Default 
   ===========   ============================     =================  =====================
   color         drawn color of object            list of 3 numbers  [1, 0, 0] (RED) 
   level         visibility "level" - see GUI     integer            1
   trace         toggle for tracing function      boolean            False 
   texture       texture for Povray output        string             None
   ===========   ============================     =================  =====================

   class keywords:  
   
   ============  ==========================   ========       =====================
   style         drawing style for circles    CONSTANT        LINES
   linewidth     linewidth of drawn circles   numeric         .05
   precision     precision of drawn circles   integer         40
   density       lines in the array           integer         25 
   scale         drawing scale of planes      numeric         1
   ============  ==========================   ========       =====================
   """
   __opts__= Element.__opts__[:] + ["linewidth","style","density","precision"]

   def __init__(self,*args,**kws):
      Element.__init__(self,*args,**kws)
      self.precision=kws.get("precision",70)
      self.linewidth=kws.get("linewidth",.05)
      self.color=kws.get("color",RED)
      self.style=kws.get("style",LINES)
      self.density=kws.get("density",30)
      self.circles=[]
      self.deps=[]


   def __len__(self):
      return len(self.circles)

   def __iter__(self):
      for circle in self.circles:
         yield circle

   def _redraw(self):
      for circle in self.circles:
          circle.show=self.show
          circle.setshow()

   def povout(self,buf):
      print >> buf,"\n //BEGIN CIRCLEPENCEL//"
      for circle in self.circles:
         circle.povout(buf)



   def draw(self):
      c_append=self.circles.append
      i=0
      while i < self.density:
         n=_Circle(color=self.color,level=self.level,linewidth=self.linewidth,
                   precision=self.precision,style=self.style,append=True)
         n.update()
         c_append(n)
         i+=1
      self.init_draw=True


class _Transformation(Element):
   """
:definition: a mapping of geometric objects
:inherits:  `class Element`_ 
:site ref: http://mathworld.wolfram.com/Transformation.html
:attributes:  

   - transforms: the transformed positions of the given elements 

:keywords: 

   inherited keywords from `class Element`_ :
   
   ===========   ============================     =================  =======================
   Keyword       Definition                        Type               Default 
   ===========   ============================     =================  =======================
   color         drawn color of objects           list of 3 numbers  None (inherit object's) 
   level         visibility "level" - see GUI     integer            1
   trace         toggle for tracing function      boolean            False 
   texture       texture for Povray output        string             None
   ===========   ============================     =================  =======================
   """
   def __init__(self,*args,**kws):
      Element.__init__(self,*args,**kws)
      self.color = kws.get("color",None)
      self.level = kws.get("level",None)
      self.deps=[]

   def _findSelf(self):
      self._getMat()
      return True

   def _redraw(self):
      for e,t in zip(self.elements,self.transforms):
          e.transform(self.mat,t)
          t.show=self.show
          t.setshow()

   def povout(self,buf):
      print >> buf,"\n //BEGIN TRANSFORAMTION//"
      for t in self.transforms:
         t.povout(buf)

   def __len__(self):
      return len(self.transforms)

   def __iter__(self):
      for transform in self.transforms:
         yield transform


   def _getMat(self):
       pass

   def unravel(self,vec):
      if not isinstance(vec[0],(float,int)):
        vec=vec[0]
        self.unravel(vec)
      return list(vec)

   def draw(self):
       self.transforms=[]
       for e in self.elements:
         if self.color:
            color=self.color
         else:
            color=e.color
         if self.level:
            level=self.level
         else:
            level=e.level
         if isinstance(e,_Point):
            n=_Point(pointsize=e.pointsize,color=color,level=level)
            self.transforms.append(n)
         elif isinstance(e,_Line):
            n=_Line(linewidth=e.linewidth,color=color,level=level,seg=e.seg)
            self.transforms.append(n)
         elif isinstance(e,_Circle):
            n=_PointArray(linewidth=e.linewidth,color=color,level=level,
                          density=e.precision,drawcurve=False)
            self.transforms.append(n)
         elif isinstance(e,_PointArray):
            n=_PointArray(pointsize=e.pointsize,color=color,level=level,
                                     drawpoints=e.drawpoints,drawcurve=e.drawcurve)
            self.transforms.append(n)
       for t in self.transforms:
           t.update()
       self.init_draw=True


