
import pygeo.base.abstract_elements_usphere as USphere


rPointClasses = ['rPoint', 'rFreePoint',
                   'rPole']

__all__ = rPointClasses



class rPoint(USphere._rPoint):
   def __init__(self,*args,**kws):
      USphere._rPoint.__init__(self,*args,**kws)
      self.update()

class rFreePoint(USphere._uFreePosition):
   def __init__(self,*args,**kws):
      USphere._uFreePosition.__init__(self,*args,**kws)
      self.update()

class rPole(USphere._rPoint):
  def __init__(self,uCircle,**kws):
      self.uCircle=uCircle
      USphere._rPoint.__init__(self,*[uCircle]**kws)
      self.update()

  def _findSelf(self):
     try:
        self.set(vector(self.uCircle._u/self.uCircle._d))
     except ZeroDivisionError:
        self.set(vector(COMPLEX_MAX,COMPLEX_MAX,COMPLEX_MAX))
     return True


