#import pygeo.base.abstract_elements_real as Real
import pygeo.base.abstract_elements_usphere as USphere

from pygeo.base.abstract_elements_real import method_get


from pygeo.base.pygeoexceptions import Argument_Type_Error
from pygeo.base.pygeoconstants import *
from pygeo.base.pygeomath import *
from pygeo.base.pygeoprimitives import *

from pygeo.base.pygeoopts import *



TransformClasses = ['uStereoProject']

TransformDefs = ['uTransform']


__all__= TransformClasses+TransformDefs

class uStereoProject(USphere._uTransformation):
   """
:constructors: 

     - uTransform(<list of objects of the zplane>)
     - uStereoProject(<list of objects of the zplane>) 
 
:returns: `stereographic projection`_ of given objects of the `complex plane`_ to the 
          `Riemann sphere`_ 
:site ref: http://en.wikipedia.org/wiki/User:Pmurray_bigpond.com/Complex_Numbers_as_a_3_Vector
   """
   def __init__(self,elements,**kws):
      self.elements=[]
      for e in elements:
         for t in e:
            self.elements.append(t)
      args=[elements]
      for element in elements:
         if not element in args:
            args.append(element)
      USphere._uTransformation.__init__(self,*args,**kws)
      self.update()

def  uTransform(*args,**kws):
   """
:constructors: 

  - uTransform(<list of objects of the zplane>);  calls: `class uStereoProject`_
  
:returns: `stereographic projection`_ of given objects of the `complex plane`_ to the 
          `Riemann sphere`_  
    
:site ref: http://en.wikipedia.org/wiki/User:Pmurray_bigpond.com/Complex_Numbers_as_a_3_Vector
   """
   __sigs__=[[list]]
   
   t,i = method_get(__sigs__,args)

   if t is None:
      raise Argument_Type_Error(__sigs__,args)
   else:
      if i==0:
         return uStereoProject(t[0],**kws)
      else:
         raise Argument_Type_Error(__sigs__,args)
