import pygeo.base.abstract_elements_usphere as USphere



rLineClasses = ['rLine']

__all__ = rLineClasses


class rLine(USphere._rLine):
   def __init__(self,p1,p2,**kws):
      USphere._rLine.__init__(self,*[p1,p2],**kws)
      self.p1=p1
      self.p2=p2
      self.update()

   def _findSelf(self):
      return True


