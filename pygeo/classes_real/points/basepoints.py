import pygeo.base.abstract_elements_real as Real

from pygeo.base.pygeoconstants import *
from pygeo.base.pygeomath import *
from pygeo.base.pygeoprimitives import *


from pygeo.base.pygeoopts import *

BasePointsClasses = [ 'Point', 'FreePoint']


__all__= BasePointsClasses


class Point(Real._Point):
   """
:constructors:

   - Point()
   - Point( numeric, numeric <,numeric> )
   - Point( [numeric, numeric <,numeric> ] )
   - Point( (numeric, numeric <,numeric> ) )

:returns: the point_ fixed at the indicated x,y,z coordinates, i.e. tuple[0],tuple[1],tuple[2]

:default: point_ at origin, if no coordinate arguments given

:site ref: http://mathworld.wolfram.com/Point.html
   """

   def __init__(self,*args,**kws):
      Real._Point.__init__(self,*args,**kws)
      self.update()

class FreePoint(Real._FreePosition):
   """
:constructors:

  - FreePoint():
  - FreePoint(numeric, numeric <,numeric> ):
  - FreePoint([numeric, numeric <,numeric> ] ):
  - FreePoint((numeric, numeric <,numeric> ) ):

:returns: a point_ that can be picked and moved freely in space

:site ref: http://mathworld.wolfram.com/Point.html
   """
   def __init__(self,*args,**kws):
      Real._FreePosition.__init__(self,*args,**kws)
      self.update()
