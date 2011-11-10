#Python modules
import cmath

#PyGeo modules
from pygeo.base.cposition import CPosition

from pygeo.base.pygeoconstants import *
from pygeo.base.pygeomath import *
from pygeo.base.element import Element,freepoints
import pygeo.base.zdraw as Z_Draw

from pygeo.base.pygeoopts import *
from LinearAlgebra import LinAlgError



AbstractClassesComplex = ['_zPoint', '_zFreePosition',
'_zLine','_zCircle','_zCirclePencil','_zTransformation']


__all__=AbstractClassesComplex


class _zPoint(CPosition,Element,Z_Draw.zPoint):
   """
:definition: an O dimensional object with a defined postion on the complex plane . 
:inherits:  `class. Element`,base.CPosition, base.zdraw.zPoint 
:site ref: http://en.wikipedia.org/wiki/Complex_number
:attributes: 

   - real: the real coordinate
   - imag  the imaginary coordinate
   
:keywords: 

   inherited keywords: from `class Element`_ :

   ===========   ============================     =================  =====================
   Keyword       Definition                        Type               Default 
   ===========   ============================     =================  =====================
   color         drawn color of object            list of 3 numbers  [0,1,1] (CYAN) 
   level         visibility "level" - see GUI     integer            1
   trace         toggle for tracing function      boolean            False 
   texture       texture for Povray output        string             None
   ===========   ============================     =================  =====================

   class keywords:  

   ===========   ==========================   ===================  =====================
   pointsize     size of drawn point          numeric               .1 
   label         label rendered for point     string                 None 
   tracewidth    width of trace curve         numeric                pointsize/2  
   tracecolor    color of trace curve         list of 3 numbers      color
   fontsize      fontsize of label            constant               TINYFONT
   fontcolor     color of label font          constant               BLACK
   fontXoffset   horizontal offset of label   numeric                pointsize/10.+ 3.0
   fontYoffset   vertical offset of label     numeric                pointsize/10.+ 3.0
   ===========   ==========================   ===================  =====================
   """
   __slots__= ("_pos","args","Not_null")
   __opts__= Element.__opts__[:] + ["pointsize","tracewidth","tracecolor",
                                    "maxtrace","mintrace", "fontsize",
                                    "fontcolor","fontXofffset","fontYofffset","tracecurve"]
   def __init__(self,*args,**kws):
       self.Not_null = True
       self._pos=None

      #inherit default attributes and functions common to all PyGeo elements. Overide
      #defaults where desired.
       Element.__init__(self,*args,**kws)
       
       self.color = kws.get("color",CYAN)
      #set defaults for keyword arguments specific to Points and derived classes.
       self.pointsize=kws.get("pointsize",.1)
       if self.label:
           self.fontsize=kws.get("fontsize",TINYFONT)
           self.fontcolor=kws.get("fontcolor",BLACK)
           self.fontXoffset=kws.get("fontXoffset",self.pointsize/10.+3)
           self.fontYoffset=kws.get("fontYoffset",self.pointsize/10.+3)
       if self.trace:
           self.tmparray=CPosition()
           self.tmparray.set(self)
           self.tracecurve=kws.get("tracecurve",True)
           self.mintrace=kws.get("mintrace",.0001)
           self.maxtrace=kws.get("maxtrace",50.)
           self.tracewidth=kws.get("tracewidth",self.pointsize/2.0)
           self.tracecolor=kws.get("tracecolor",self.color)
       self.deps=[]


   def __description(self, precision):
       if self.real != 0.:
           return self.__class__.__name__ + "(%.*g%+.*gj)"%(precision, 
                                             self.real, precision, self.imag)
       else:
           return self.__class__.__name__ + "%.*gj"%(precision, self.imag)


   def __repr__(self):
       return self.__description(self.PREC_REPR)


   def __str__(self):
       return self.__description(self.PREC_STR)
  
   def do_trace(self):
      #If, on update, traced point has moved within limits defined by
      #'mintrace' and 'maxtrace' append its new position to the trace
      #curve

      delta= self.distance(self.tmparray)
      if (self.mintrace < delta < self.maxtrace):
          from pygeo.classes_complex.z_points import zFixedPoint
          self.rtrace.append(zFixedPoint(self.real,self.imag,pointsize=self.pointsize,color=self.tracecolor,
                  level=self.level))
          if self.tracecurve:
             self.ntrace.append(pos=self.pos)
      self.tmparray.set(self)

   def reset_trace(self):
      #Re-intialize list of traced curves to None"""
      if self.trace:
         for r in self.rtrace:
            r.show=False
            r.setshow()
         self.rtrace=[]
         self.tmparrayset(self)

   def reset_trace_curves(self):
      #Re-intialize list of traced curves to None"""
      if self.trace:
         self.ntrace.pos=[]
   
   def _findSelf(self):
       return True


   def _redraw(self):
      #If point is to be rendered, filter its postion to within drawing
      #range and set the position of the VPython sphere object,
      #representing the point, to the filtered position. Same as to any associated
      #label to be rendered.

       self.rend[0].pos =self.pos
       if self.label:
           self.lab.pos= self.pos

   def transform(self,mat,w_point):
       try:
          t1=inverse(mat)
       except LinAlgError:
          return False
       t2= conjugate(t1)
       t3= transpose(t1)
       h=Hermitian(matrixmultiply(t3,matrixmultiply(self.setHermitian(),t2)))
       w_point.from_hermitian(h)
       return True

   def uRotate(self,ucenter,angle):
       h_angle=angle/2.
       cs=cos(h_angle)
       sn=sin(h_angle)
       a=complex(cs,ucenter.z*sn)
       b=complex(-ucenter.y,ucenter.x)*sn
       c=-b.conjugate()
       d=a.conjugate()
       mat1=([[a,b],[c,d]])
       mat2=self.homogenous()
       self.toC(matrixmultiply(mat1,mat2))
       return True

   def toC(self,h_array):
       self.set(h_array[0]/h_array[1])
       return True
    
   def uVector(self):
       modplus=self.mod2()+1
       modminus=self.mod2()-1
       xy=2*self/modplus
       z=modminus/modplus
       return vector(xy.real,xy.imag,z)   

   def to_uSphere(self,upoint): 
       upoint.set(self.uVector())
       return True
  
       
 
   def from_hermitian(self,h):
       self.set(-h.C/h.A)
 

   def setHermitian(self):
       A=1
       C=-self
       B=C.conjugate()
       D = B*C
       self._hermitian = Hermitian(conjugate(transpose(array([[A,B],[C,D]]))))
       return self._hermitian

#   def setext(self):
#       if self.Not_null:
#           if self.show:
#               for line in self.lines:
#                   if line.show:
#                       line.get_extension(self)
#                       line._redraw()

class _zFreePosition(_zPoint):
   """
:definition: an O dimensional object of the complex plane that can picked and moved, either
             freely on the plnae or constrained to a given geoemtric object of the plane. 
:inherits:  `class. _Point`_ 
:site ref: http://en.wikipedia.org/wiki/Complex_number
:attributes: 

   - real: the real coordinate
   - imag  the imaginary coordinate
   
:keywords: 

   inherited keywords: from `class Element`_ :

   ===========   ============================     =================  =====================
   Keyword       Definition                        Type               Default 
   ===========   ============================     =================  =====================
   color         drawn color of object            list of 3 numbers  [0,1,1] (CYAN) 
   level         visibility "level" - see GUI     integer            1
   trace         toggle for tracing function      boolean            False 
   texture       texture for Povray output        string             None
   ===========   ============================     =================  =====================

   inherited keywords: from `class Point`_ :

   ===========   ==========================   ===================  =====================
   pointsize     size of drawn point          numeric               .1 
   label         label rendered for point     string                 None 
   tracewidth    width of trace curve         numeric                pointsize/2  
   tracecolor    color of trace curve         list of 3 numbers      color
   fontsize      fontsize of label            constant               TINYFONT
   fontcolor     color of label font          constant               BLACK
   fontXoffset   horizontal offset of label   numeric                pointsize/10.+ 3.0
   fontYoffset   vertical offset of label     numeric                pointsize/10.+ 3.0
   ===========   ==========================   ===================  =====================
   """
   def __init__(self,*args,**kws):
      _zPoint.__init__(self,*args,**kws)
      self.color = kws.get("color",BLUE)
      self.initcolor=self.color
      self.pointsize=kws.get("pointsize",.12)
      self.initpointsize=self.pointsize
      self.initvector=vector(self.real,self.imag)
      freepoints.append(self)
      self.dependants=[]

   def _add_dependant(self,e):
      self.dependants.append(e)

   def reset(self):
      """Reset to position of start-up input"""
      self.pointsize=self.initpointsize
      self.drawcolor = self.initcolor
      self.vector=self.initvector
      _zPoint.update(self)

class _zLine(Element,Z_Draw.zLine):
   """
:definition: a straight line of the 'complex plane'_ , representing a 'complex circle'_ of 
             infinite radius
             
:inherits: `class Element`_ , base.zdraw.zLine  
:site ref: http://mathworld.wolfram.com/Line.html
:attributes:  

   - p1: a complex point on the line 
   - p2  a second complex point on the line 
   - _hermitian: the hermitian matrix associated with the line

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
   linewidth     width of drawn line          numeric         .02 
   label         label rendered for point     string          None 
   fontsize      fontsize of label            constant        NORMALFONT
   fontcolor     color of label font          constant        BLACK
   fontXoffset   horizontal offset of label   numeric         pointsize/10.+ 3.0
   fontYoffset   vertical offset of label     numeric         pointsize/10.+ 3.0
   label_ratio   relative position of label   numeric         .5 (midpoint)   
   show_normal   draw line normal?            boolean         False
   ============  ==========================   ========       =====================
   """
   __opts__ = _zPoint.__opts__[:]+["linewidth","label_ratio","show_normal"]
   __opts__.remove("pointsize")

   def __init__(self,*args,**kws):
      Element.__init__(self,*args,**kws)
      self.precision = kws.get("precision",40)
      self.linewidth=kws.get("linewidth",.02)
      self.color = kws.get("color",GREEN)
      self.show_normal=kws.get("show_normal",False)
      self.normal_width=kws.get("normal_width",.02)
      self.bounds1 = None
      self.bounds2 = None
      if self.label:
         self.fontsize=kws.get("fontsize",TINYFONT)
         self.fontcolor=kws.get("fontcolor",BLACK)
         self.fontXoffset=kws.get("fontXoffset",self.pointsize/10.+3)
         self.fontYoffset=kws.get("fontYoffset",self.pointsize/10.+3)
         self.lratio=kws.get("label_ratio",.5)
      self.p1=_zPoint(append=False)
      self.p2=_zPoint(append=False)

   def _findSelf(self):
      self.set_hermitian_from_points()
      return True

   def __description(self):
      return self.__class__.__name__ + "(%s,%s)" %(self.p1,self.p2) 

   def __repr__(self):
       return self.__description()


   def __str__(self):
       return self.__description()



   def setlabel(self):
      labelpos=add(multiply(1-self.lratio,
                             self.p1),
                      multiply(self.lratio,
                             self.p2))
      self.lab.pos=labelpos
  
   def transform(self,mat,h_circle):
      t1=inverse(mat)
      h_circle._hermitian =Hermitian(matrixmultiply(transpose(t1),
                           matrixmultiply(self._hermitian,conjugate(t1))))
      h_circle.set_radius_from_hermitian()
      return True

   def to_uSphere(self,uCircle):
        h=self._hermitian
        a=h.B+h.C
        b=(h.B-h.C)*1j
        c=h.D-h.A
        d=h.D+h.A
        v=vector(a.real,b.real,-c.real)
        try:
           uCircle._u.set(v.norm())
           uCircle._d = d =  d.real/mag(v)*-1.
        except ZeroDivisionError:
           uCircle._u.set(vector(0,0,1))
           uCircle._d=0
        u=uCircle._u   
        uCircle.set_s_from_u(u)
        uCircle._center.set(u*d)
        pdist = uCircle._center.mag2
        uCircle._radiusSquared=1-pdist
        try:
            uCircle._radius=sqrt(uCircle._radiusSquared)
        except ValueError:
            uCircle._radius=0
        return True
      


#   def get_extension(self,point):
#      a=self.lengthSquared()
#      b=self.p1.distanceSquared(point)
#      c=self.p2.distanceSquared(point)
#      if a > b and a > c:
#         return False
#      elif a < b:
#         self.bounds2=point
#         self.bounds1=None
#         return True
#      else:
#         self.bounds1=point
#         self.bounds2=None
#         return True


   def direction(self):
      v = self.p1-self.p2
      v /= mod(v)
      return v

   def angle(self):
      dir=self.direction()
      try:
         return arctan(float(dir.imag)/dir.real)
      except ZeroDivisionError:
         return PI/2.0

   def normal(self):
      c = complex(self.p2.imag-self.p1.imag,self.p1.real-self.p2.real)
      c /= mod(c)
      return c

   def distance(self):
      n=self.normal()
      d = n.real*self.p1.real + n.imag*self.p1.imag
      return d

   def set_hermitian_from_points(self):
      p1=self.p1
      p2=self.p2
      c=complex(p2.imag-p1.imag,p1.real-p2.real)
      c /= abs(c)
      a = arctan2(-c.imag,c.real)
      n=complex( cos(a),sin(a))
      self._hermitian = Hermitian([[0,n],[n.conjugate(),-self.distance()*2]])


class _zCircle(Element,Z_Draw.zCircle):
   """
:definition: the set of points the `complex plane`_ that are equidistant from a given point 
             of the plane
:inherits:  `class Element`_ , base.zdraw.zCircle                
:site ref: http://www.ies.co.jp/math/java/comp/cplcircle/cplcircle.html
:attributes:  

   - _center: the complex point on circle's center
   - _cpoint: a complex point on circle circumference
   - _hermitian: the hermitian matrix associated with the circle
   - _radius: the circle's radius 
   - _radiusSquared: the square of the circle's radius 
   
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
   linewidth     width of drawn lines         numeric        .02 
   precision     drawing precision            integer         40 
   show_normal   draw normal                  boolean         False
   normal_width  width of drawn normal        numeric         .4
   fixed         fix to initial radius        boolean         False   
   ============  ==========================   ========       =====================
   """
   __opts__= Element.__opts__[:] + ["style","linewidth","precision","fixed","circle_type","O"]
   def __init__(self,*args,**kws):
      self.precision = kws.get("precision",40)
      self.style = kws.get("style",LINES)
      self.linewidth = kws.get("linewidth",.02)
      self.show_normal=False
      self._u=vector(0,0,1)
      self._s=CPosition(1,0)
      self._radiusSquared=0
      self._radius=0
      self._d=0
      self._center=_zPoint(append=False)
      self._cpoint=_zPoint(append=False)
      Element.__init__(self,*args,**kws)
      self.color = kws.get("color",BLUE)
      O = kws.get("O","+")
      if O=="+":
         self.a=1
      else:
         self.a=-1

   def _findSelf(self):
      self.set_hermitian_from_radius()
      return True

   def __description(self):
      return self.__class__.__name__ + "(%s,%.5f)" %(self._center,self._radius) 
   def __repr__(self):
       return self.__description()


   def __str__(self):
       return self.__description()
   
   def transform(self,mat,h_circle):
      t1=inverse(mat)
      h_circle._hermitian=Hermitian(matrixmultiply(transpose(t1),
                                    matrixmultiply(self._hermitian,conjugate(t1))))
      h_circle.set_radius_from_hermitian()
      return True

  
   def to_uSphere(self,uCircle):
        h=self._hermitian
        a=h.B+h.C
        b=(h.B-h.C)*1j
        c=h.D-h.A
        d=h.D+h.A
        v=vector(a.real,b.real,-c.real)
        try:
           uCircle._u.set(v.norm())
           uCircle._d = d =  d.real/mag(v)*-1.
        except ZeroDivisionError:
           uCircle._u.set(vector(0,0,1))
           uCircle._d=0
        u=uCircle._u   
        uCircle.set_s_from_u(u)
        uCircle._center.set(u*d)
        pdist = uCircle._center.mag2
        uCircle._radiusSquared=1-pdist
        try:
            uCircle._radius=sqrt(uCircle._radiusSquared)
        except ValueError:
            uCircle._radius=0
        return True
      

   
   def set_radius_from_hermitian(self):
     h=self._hermitian
     
     try:
        self._center.set(-h.C/h.A)
        fact=h.D/h.A
        self._radiusSquared = self._center.mod2() - fact
        self._radius = cmath.sqrt(self._radiusSquared)
     except ZeroDivisionError:
        pass
     
   def set_radius_from_cpoint(self):
      self._radiusSquared=self._center.distanceSquared(self._cpoint)
      self._radius=cmath.sqrt(self._radiusSquared)

   def set_hermitian_from_radius(self):
      center=self._center
      A=self.a
      C=center*-A
      B=C.conjugate()
      D=(center*center.conjugate()-self._radiusSquared)*A
      self._hermitian= Hermitian([[A,B],[C,D]])


class _zPointArray(Element):
   """
:definition: an array of `class _zPoint`_ s on the `complex plane`_ with a defined 
             geometric relationship
:inherits:  `class Element`_ 
:site ref: http://mathworld.wolfram.com/Array.html
:attributes:  

   - zpoints: positioned complex points of the array

:keywords: 

   inherited keywords from `class Element`_ :
   
   ===========   ============================     =================  =====================
   Keyword       Definition                        Type               Default 
   ===========   ============================     =================  =====================
   color         drawn color of object            list of 3 numbers  [0, 1, 1] (CYAN) 
   level         visibility "level" - see GUI     integer            1
   trace         toggle for tracing function      boolean            False 
   texture       texture for Povray output        string             None
   ===========   ============================     =================  =====================
   
   class keywords:  
   
   ============  ==========================   ========       =====================
   pointsize     size of drawn points         numeric         .4
   density       points in the array          integer         50 
   ============  ==========================   ========       =====================
   """
   __opts__= Element.__opts__[:] + ["pointsize","density"]

   def __init__(self,*args,**kws):
      Element.__init__(self,*args,**kws)
      self.density=kws.get('density',50)
      self.pointsize=kws.get('pointsize',.1)
      self.color = kws.get("color",CYAN)
      self.zpoints=[]
      self.deps=[]

   def __iter__(self):
      for zpoint in self.zpoints:
         yield zpoint

   def __len__(self):
       return len(self.zpoints)

   def povout(self,buf):
       print >> buf,"\n //BEGIN zPointARRAY//"

       for zpoint in self.zpoints:
          zpoint.povout(buf)

   def _redraw(self):
       for zpoint in self.zpoints:
         zpoint._redraw()
 
   def draw(self):
       p_append=self.zpoints.append
       i=0
       while i < self.density:
           n=_zPoint(pointsize=self.pointsize,color=self.
                 color,level=self.level,append=False)
           n.draw()
           p_append(n)
           i+=1
       self.init_draw=True
 
class _zLineArray(Element):
   """
:definition: an array of `class _zLine`_ s on the `complex plane`_
:inherits:  `class Element`_ 
:site ref: http://mathworld.wolfram.com/Array.html
:attributes:  

   - zlines: positioned lines of the complex plane

:keywords: 

   inherited keywords from `class Element`_ :
   
   ===========   ============================     =================  =====================
   Keyword       Definition                        Type               Default 
   ===========   ============================     =================  =====================
   color         drawn color of object            list of 3 numbers  [1, 1, 0] (YELLOW) 
   level         visibility "level" - see GUI     integer            1
   trace         toggle for tracing function      boolean            False 
   texture       texture for Povray output        string             None
   ===========   ============================     =================  =====================

   class keywords:  
   
   ============  ==========================   ========       =====================
   linewidth     linewidth of drawn circles   numeric         .015
   density       lines in the array           integer           50 
   ============  ==========================   ========       =====================
   """
   __opts__= Element.__opts__[:] + ["density","linewidth"]

   def __init__(self,*args,**kws):
      Element.__init__(self,*args,**kws)
      self.density=kws.get('density',50)
      self.linewidth=kws.get('linewidth',.015)
      self.color = kws.get("color",YELLOW)
      self.zlines=[]
      self.deps=[]

   def __iter__(self):
      for zline in self.zlines:
         yield zline

   def __len__(self):
       return len(self.zlines)

   def povout(self,buf):
       print >> buf,"\n //BEGIN zLineARRAY//"

       for zline in self.zlines:
          zline.povout(buf)

   def _redraw(self):
       for zline in self.zlines:
         zline._redraw()
 
   def draw(self):
       p_append=self.zlines.append
       i=0
       while i < self.density:
           n=_zLine(linewidth=self.linewidth,color=self.
                 color,level=self.level,append=False)
           n.draw()
           p_append(n)
           i+=1
       self.init_draw=True
 

class _zCirclePencil(Element):
   """
:definition: an array_ of `class _zCircle`_ s on the `complex plane`_
:inherits:  `class Element`_ 
:site ref: http://mathworld.wolfram.com/Array.html
:attributes:  

   - zcircles: positioned circles of the complex plane

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
   linewidth     linewidth of drawn circles   numeric         .015
   precision     precision of drawn circles   integer         70
   density       lines in the array           integer         30 
   scale         drawing scale of planes      numeric         1
   ============  ==========================   ========       =====================
   """
   __opts__= Element.__opts__[:] + ["linewidth","style","density","precision"]
   def __init__(self,*args,**kws):
      self.precision=kws.get("precision",70)
      self.linewidth=kws.get("linewidth",.015)
      self.style=kws.get("style",LINES)
      self.density=kws.get("density",30)
      Element.__init__(self,*args,**kws)
      self.color=kws.get("color",RED)

      self.deps=[]
      self.zcircles=[]

   def __len__(self):
      return len(self.circles)

   def __iter__(self):
      for zcircle in self.zcircles:
         yield zcircle

   def _redraw(self):
      for zcircle in self.zcircles:
          zcircle.level=self.level
          zcircle.setshow()

   def povout(self,buf):
      print >> buf,"\n //BEGIN CIRCLEPENCEL//"
      for zcircle in self.zcircles:
         zcircle.povout(buf)


   def draw(self):
      c_append=self.zcircles.append
      i=0
      while i < self.density:
         n=_zCircle(color=self.color,level=self.level,
                   precision=self.precision,style=self.style)
         n.update()
         c_append(n)
         i+=1
      self.init_draw=True

class _zTransformation(Element):
   """
:definition: a `Mobius transformation`_ of geometric objects of the `complex plane`_
:inherits:  `class Element`_ 
:site ref: http://mathworld.wolfram.com/LinearFractionalTransformation.html
:attributes:  

   - _mobius: the Mobius tranformation matrix defining the transformation

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

   class keywords:  
   
   ============  =============================   ========       =====================
   normal_form   convert matrix to normal form    boolean        False
   ============  =============================   ========       =====================
   """
   __opts__= Element.__opts__[:] + ["normal_from"]
   def __init__(self,*args,**kws):
      Element.__init__(self,*args,**kws)
      self.color = kws.get("color",None)
      self.level = kws.get("level",None)
      self.deps=[]

   def _findSelf(self):
      if self._getMobius():
         return True
      else:
         return False
         
   def _redraw(self):
      for e,t in zip(self.elements,self.transforms):
          if e.transform(self._mobius,t):
             t._redraw()

  
   def povout(self,buf):
      print >> buf,"\n //BEGIN TRANSFORAMTION//"
      for t in self.transforms:
         t.povout(buf)

   def __iter__(self):
      for transform in self.transforms:
         yield transform

   def _getMobius(self):
       pass


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
           if isinstance(e,_zPoint):
               self.transforms.append(_zPoint(pointsize=e.pointsize,
                                               color=color,level=level,export = self.export))
           elif isinstance(e,_zCircle):
               self.transforms.append(_zCircle(linewidth=e.linewidth,
                                               color=color,level=level,export = self.export))
           elif isinstance(e,_zLine):
               self.transforms.append(_zCircle(linewidth=e.linewidth,
                                                color=color,level=level,export = self.export))
           elif isinstance(e,_zCirclePencil):
               for circle in e:
                   self.transforms.append(_zCircle(linewidth=e.linewidth,
                                                   color=color,level=level,export = self.export))
       for t in self.transforms:
           t.update()
       self.init_draw=True


