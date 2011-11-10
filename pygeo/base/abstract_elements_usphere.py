
from position3 import Position3
from pygeoconstants import *
from pygeomath import *
from pygeoexceptions import Argument_Len_Error,Argument_Type_Error
import vdraw as Draw
import abstract_elements_real as Real
from abstract_elements_real import _Point
from pygeo.base.element import Element,freepoints
from abstract_elements_complex import _zPoint,_zLine,_zCircle



AbstractUClasses = ['_rPoint', '_uFreePosition','_rLine', '_uPoint',
                    '_uSphere','_uCircle', '_uCirclePencil']



__all__=AbstractUClasses

class _rPoint(Real._Point):
   """
:definition: an O dimensional object with a defined position in space. 
:inherits:  `class Real._Point`_ 
:site ref: http://mathworld.wolfram.com/Point.html
:attributes: 

   - x: x coord
   - y: y coord
   - z: z coord

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

   inherited keywords: from `class Real._Point`_ :

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
      Real._Point.__init__(self,*args,**kws)
      self.pointsize=kws.get("pointsize",.1)
      self.color=kws.get("color",RED)
      if self.trace:
         self.tmparray=Position3()
         self.tmparray.set(self)
         self.mintrace=kws.get("mintrace",.01)
         self.maxtrace=kws.get("maxtrace",500.)
         self.tracewidth=kws.get("tracewidth",self.pointsize/2.0)
         self.tracecolor=kws.get("tracecolor",self.color)
      self.fontXoffset=kws.get("fontXoffset",0)
      self.fontYoffset=kws.get("fontYoffset",0)


class _uPoint(_rPoint):
   """    
:definition: an O dimensional object on the unit sphere. 
:inherits:  `class Real._Point`_ 
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

   inherited keywords: `class _rPoint`_  :

   ===========   ==========================   ========       =====================
   pointsize     size of drawn point          numeric         .5 
   label         label rendered for point     string          None 
   fontsize      fontsize of label            constant        NORMALFONT
   fontcolor     color of label font          constant        BLACK
   fontXoffset   horizontal offset of label   numeric         pointsize/10.+ 3.0
   fontYoffset   vertical offset of label     numeric         pointsize/10.+ 3.0
   ===========   ==========================   ========       =====================
   """
   # so points on unit sphere have a unique signature
   def __init__(self,*args,**kws):
      _rPoint.__init__(self,*args,**kws)

class _uFreePosition(_uPoint):
   """
:definition: an O dimensional object that can be picked and moved either 
             freely on the unit sphere or on an object of the unit sphere 
:inherits:  `class _uPoint`_ 
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

   inherited keywords: `class _uPoint`_  :

   ===========   ==========================   ========       =====================
   pointsize     size of drawn point          numeric         .5 
   label         label rendered for point     string          None 
   fontsize      fontsize of label            constant        NORMALFONT
   fontcolor     color of label font          constant        BLACK
   fontXoffset   horizontal offset of label   numeric         pointsize/10.+ 3.0
   fontYoffset   vertical offset of label     numeric         pointsize/10.+ 3.0
   ===========   ==========================   ========       =====================
   """
   def __init__(self,*args,**kws):
      _uPoint.__init__(self,*args,**kws)
      self.pointsize=kws.get("pointsize",.15)
      self.color=kws.get("color",RED)
      self.initcolor =self.color
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
      _uPoint.update(self)

class _uCircle(Real._Circle):
   """
:definition: a spheric section of the unit sphere
:inherits:  `class Real._Circle`_                   
:site ref: http://mathworld.wolfram.com/SphericSection.html
:attributes:  

   - _u : the unit normal of the circle's plane
   - _d : the distance from origin of the circle's plane
   - _s : unit vector perp to normal of the circle's plane
   - _center: the circle's center point
   - _cpoint: a point of the circle's circumference
   - _radius: the circle's radius
   - _radiusSquared: the square of circle's radius

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

   inherited keywords from `class Real._Circle`_ :
   
   ============  ==========================   ========       =====================
   style         drawing style                constant        LINES
   linewidth     width of drawn lines         numeric        .2 
   precision     drawing precision            integer         40 
   show_normal   draw normal                  boolean         False
   normal_width  width of drawn normal        numeric         .4
   fixed         fix to initial position      boolean         False   
   ============  ==========================   ========       =====================
   """
   def __init__(self,*args,**kws):
      Real._Circle.__init__(self,*args,**kws)
      self.linewidth=kws.get("linewidth",.02)


class _uSphere(Real._Sphere):
   """
:definition: the orign centered Riemann (unit) sphere representing the extended complex plane
:inherits:  `class Real._Sphere`_ 
:site ref: http://mathworld.wolfram.com/UnitSphere.html
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

   inherited keywords from `class Real._Sphere`_ :

   ============  ==========================   ========       =====================
   style         drawing style                constant        LINES
   linewidth     width of drawn lines         numeric        .1 
   precision     drawing precision            integer         10 
   fixed         fix to initial position      boolean         False   
   ============  ==========================   ========       =====================
   """
   def __init__(self,*args,**kws):
      Real._Sphere.__init__(self,*args,**kws)
      self.precision=kws.get("precision",20)
      self.color=kws.get("color",WHITE)
      self.linewidth=kws.get("linewidth",.01)
      self._center=_rPoint(append=False)
      self._radius=1
      self._radiusSquared=1
      self.N=_rPoint(0,0,1,append=False)

   def rmatrix(self):
      mat=Element.rmatrix(self)
      mat[3:]=array([[0.0,0.0,0.0,1.0]])
      return mat



class _uCirclePencil(Real._CirclePencil):
   """
:definition: an array_ of circle_ s on the `Riemann sphere`_
:inherits:  `class Real._CirclePencil`_ 
:site ref: http://mathworld.wolfram.com/SphericSection.html
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

   inherited keywords from `class Real._CirclePencil`_  :
   
   ============  ==========================   ========       =====================
   style         drawing style for circles    CONSTANT        LINES
   linewidth     linewidth of drawn circles   numeric         .05
   precision     precision of drawn circles   integer         40
   density       lines in the array           integer         25 
   scale         drawing scale of planes      numeric         1
   ============  ==========================   ========       =====================
   """
   def __init__(self,*args,**kws):

      Real._CirclePencil.__init__(self,*args,**kws)
      self.linewidth=kws.get("linewidth",.02)



class _uTransformation(Element):
   """
:definition: a stereographic mapping of geometric objects of the complex plane to the unit sphere
:inherits:  `class Element`_ 
:site ref: http://mathworld.wolfram.com/StereographicProjection.html
:attributes:  

   - transforms: the transformed positions of the given objects

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
       return True
         
   def _redraw(self):
      for e,t in zip(self.elements,self.transforms):
          if e.to_uSphere(t):
             t._redraw()

  
   def povout(self,buf):
      print >> buf,"\n //BEGIN TRANSFORAMTION//"
      for t in self.transforms:
         t.povout(buf)

   def __iter__(self):
      for transform in self.transforms:
         yield transform


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
               self.transforms.append(_uPoint(
                                               color=color,level=level,pointsize=.03))
           elif isinstance(e,_zCircle):
               self.transforms.append(_uCircle(
                                               color=color,level=level,linewidth=.01))
           elif isinstance(e,_zLine):
               self.transforms.append(_uCircle(
                                                color=color,level=level,linewidth=.01))
           elif isinstance(e,_zCirclePencil):
               for circle in e:
                   self.transforms.append(_uCircle(
                                                   color=color,level=level,linewidth=.01))
       for t in self.transforms:
           t.update()
       self.init_draw=True

class _rLine(Real._Line):
   """
:definition: an 1 dimensional object representing "breathless length"
:inherits:  `class Real._Line`_ 
:site ref: http://mathworld.wolfram.com/Line.html
:attributes:  

   - p1: point on line 
   - p2: point on line

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

   inherited keywords from `class _Line`_ :

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
   def __init__(self,*args,**kws):
      Real._Line.__init__(self,*args,**kws)
      self.linewidth=kws.get("linewidth",.03)

   def _findSelf(self):
      return True

