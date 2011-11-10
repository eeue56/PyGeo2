
"""
 much of this is from the PyPy complex number implmenentation
"""



import string

from pygeo.base.pygeoexceptions import Assignment_Error
from pygeo.base.pygeoconstants import *
from pygeo.base.pygeomath import *
from pygeo.base.pygeoprimitives import *

from pygeo.base.pygeoopts import *

#from pygeo.base.complex import Complex

VECT_TYPE=type(vector())
COMPLEX_TYPE=type(1+0j)
TUPLE_TYPE=type(())
LIST_TYPE=type([])

COORDSLIST = ['x','y']



class CPosition(object):
    """
    Create a Complex number from a real part and an optional imaginary part.
    This is equivalent to (real + imag*1j) where imag defaults to 0."""
    PREC_REPR = 17
    PREC_STR = 12

    __slots__ = ['real', 'imag']

    # XXX this class is not well tested

    # provide __new__to prevent the default which has no parameters
    def __new__(typ, *args,**kws):
        if args:
           if isinstance(args[0],complex):
              real=args[0].real
              imag=args[0].imag
           elif isinstance(args[0],(float,int)):
                  real=args[0]
                  try:
                     if isinstance(args[1],(float,int)):
                        imag=args[1]
                  except IndexError:
                     imag=0 
           else:
              real=0
              imag=0
        else:
           real=0
           imag=0
        ret = object.__new__(typ)
        ret._init(real, imag)
        return ret

    def __getnewargs__(self):
        return (complex(self.real, self.imag),)
    
    def __reduce__(self):
        return (self.__class__, (self.real, self.imag),
                getattr(self, '__dict__', None))

    def _init(self, re, im):
        real_slot.__set__(self, re)
        imag_slot.__set__(self, im)

    def __getitem__(self, index):
        return self.vector[index]

    def get_name(self):
        return self.__class__.__name__

    def set_x(self,value):
        self.real=value

    def set_y(self,value):
        self.imag=value

    def get_x(self):
        return self.real

    def get_y(self):
        return self.imag

    def get_z(self):
        return 0.


    def get_vector(self):
        return vector(self.real,self.imag)

    def set_vector(self,value=None):
        if value:
           if isinstance(value,VECT_TYPE):
               self._vector=value
           elif len(value) == 3 or len(value)==2 :
              #try:
              self._vector=vector(value)
            #except:
            #   raise self._assignerror(attr,value)
           else:
              print "assignment error: %s" %self.__class__.__name__
            #raise self._assignerror(attr,value)
        else:
           self._vector=vector()
        self.real=self._vector.x
        self.imag=self._vector.y


    def get_pos(self):
        v=self.vector
        if TEST_MAX:
           m=max(absolute(v))
           if m > MAX:
              return (v/m)*MAX
           else:
              return v
        else:
           return v

    pos= property(get_pos,None,None,"The 3 (z=0) coordinate drawing position vector")

    vector = property(get_vector, set_vector,
                       None,
                       "The 3 (z=0) coordinate geometric position vector")

    x= property(get_x,set_x,None,"The real coordinate ")

    y= property(get_y,set_y,None,"The imag coordinate ")

    z= property(get_z,None,None,"The complex plane x position")


    def __description(self, precision):
        if self.real != 0.:
            return self.__class__ + "(%.*g%+.*gj)"%(precision, self.real, precision, self.imag)
        else:
            return "%.*gj"%(precision, self.imag)


    def __repr__(self):
        return self.__description(self.PREC_REPR)


    def __str__(self):
        return self.__description(self.PREC_STR)

        
    def __hash__(self):
        hashreal = hash(self.real)
        hashimag = hash(self.imag)

        # Note:  if the imaginary part is 0, hashimag is 0 now,
        # so the following returns hashreal unchanged.  This is
        # important because numbers of different types that
        # compare equal must have the same hash value, so that
        # hash(x + 0*j) must equal hash(x).

        return hashreal + 1000003 * hashimag


    def __add__(self, other):
        result = self.__coerce__(other)
        if result is NotImplemented:
            return result
        self, other = result
        real = self.real + other.real
        imag = self.imag + other.imag
        return complex(real, imag)

    __radd__ = __add__

    def __sub__(self, other):
        result = self.__coerce__(other)
        if result is NotImplemented:
            return result
        self, other = result
        real = self.real - other.real
        imag = self.imag - other.imag
        return complex(real, imag)
    
    def __rsub__(self, other):
        result = self.__coerce__(other)
        if result is NotImplemented:
            return result
        self, other = result
        return other.__sub__(self)

    def __mul__(self, other):
        result = self.__coerce__(other)
        if result is NotImplemented:
            return result
        self, other = result
        real = self.real*other.real - self.imag*other.imag
        imag = self.real*other.imag + self.imag*other.real
        return complex(real, imag)

    __rmul__ = __mul__

    def __div__(self, other):
        result = self.__coerce__(other)
        if result is NotImplemented:
            return result
        self, other = result
        if abs(other.real) >= abs(other.imag):
            # divide tops and bottom by other.real
            try:
                ratio = other.imag / other.real
            except ZeroDivisionError:
                raise ZeroDivisionError, "Complex division"
            denom = other.real + other.imag * ratio
            real = (self.real + self.imag * ratio) / denom
            imag = (self.imag - self.real * ratio) / denom
        else:
            # divide tops and bottom by other.imag
            assert other.imag != 0.0
            ratio = other.real / other.imag
            denom = other.real * ratio + other.imag
            real = (self.real * ratio + self.imag) / denom
            imag = (self.imag * ratio - self.real) / denom

        return complex(real, imag)

    def __rdiv__(self, other):
        result = self.__coerce__(other)
        if result is NotImplemented:
            return result
        self, other = result
        return other.__div__(self)

    def __floordiv__(self, other):
        result = self.__divmod__(other)
        if result is NotImplemented:
            return result
        div, mod = result
        return div

    def __rfloordiv__(self, other):
        result = self.__coerce__(other)
        if result is NotImplemented:
            return result
        self, other = result
        return other.__floordiv__(self)

    __truediv__ = __div__
    __rtruediv__ = __rdiv__

    def __mod__(self, other):
        result = self.__divmod__(other)
        if result is NotImplemented:
            return result
        div, mod = result
        return mod

    def __rmod__(self, other):
        result = self.__coerce__(other)
        if result is NotImplemented:
            return result
        self, other = result
        return other.__mod__(self)

    def __divmod__(self, other):
        result = self.__coerce__(other)
        if result is NotImplemented:
            return result
        self, other = result

        import warnings, math
        warnings.warn("complex divmod(), // and % are deprecated", DeprecationWarning)

        try:
            div = self/other # The raw divisor value.
        except ZeroDivisionError:
            raise ZeroDivisionError, "Complex remainder"
        div = complex(math.floor(div.real), 0.0)
        mod = self - div*other
        return div, mod

    def __rdivmod__(self, other):
        result = self.__coerce__(other)
        if result is NotImplemented:
            return result
        self, other = result
        return other.__divmod__(self)


    def __pow__(self, other, mod=None):
        if mod is not None:
            raise ValueError("Complex modulo")
        result = self.__coerce__(other)
        if result is NotImplemented:
            return result
        a, b = result
        import math

        if b.real == 0. and b.imag == 0.:
            real = 1.
            imag = 0.
        elif a.real == 0. and a.imag == 0.:
            if b.imag != 0. or b.real < 0.:
                raise ZeroDivisionError, "0.0 to a negative or Complex power"
            real = 0.
            imag = 0.
        else:
            vabs = math.hypot(a.real,a.imag)
            len = math.pow(vabs,b.real)
            at = math.atan2(a.imag, a.real)
            phase = at*b.real
            if b.imag != 0.0:
                len /= math.exp(at*b.imag)
                phase += b.imag*math.log(vabs)
            real = len*math.cos(phase)
            imag = len*math.sin(phase)

        result = complex(real, imag)
        return result

    def __rpow__(self, other, mod=None):
        result = self.__coerce__(other)
        if result is NotImplemented:
            return result
        self, other = result
        return other.__pow__(self, mod)

    def __neg__(self):
        return complex(-self.real, -self.imag)


    def __pos__(self):
        return complex(self.real, self.imag)


    def __abs__(self):
        import math
        result = math.hypot(self.real, self.imag)
        return float(result)


    def __nonzero__(self):
        return self.real != 0.0 or self.imag != 0.0


    def __coerce__(self, other):
        if isinstance(other, complex):
            return self, other
        if isinstance(other, (int, long, float)):
            return self, complex(other)
        if isinstance(other,CPosition):
            return self,complex(other.real,other.imag)
        return NotImplemented

    def conjugate(self):
        return complex(self.real, -self.imag)

    def __eq__(self, other):
        result = self.__coerce__(other)
        if result is NotImplemented:
            return id(self) == id(other)
        self, other = result
        return ((abs(self.real-other.real)) < EPS 
                 and abs((self.imag-other.imag)) < EPS) 

    def __ne__(self, other):
        result = self.__coerce__(other)
        if result is NotImplemented:
            return result
        self, other = result
        return ((self.real-other.real) >= EPS 
                 or (self.imag-other.imag) >= EPS) 


    # unsupported operations
    
    def __lt__(self, other):
        result = self.__coerce__(other)
        if result is NotImplemented:
            return result
        raise TypeError, "cannot compare Complex numbers using <, <=, >, >="

    __le__ = __gt__ = __ge__ = __lt__


    def __int__(self):
        raise TypeError, "can't convert Complex to int; use e.g. int(abs(z))"


    def __long__(self):
        raise TypeError, "can't convert Complex to long; use e.g. long(abs(z))"


    def __float__(self):
        raise TypeError, "can't convert Complex to float; use e.g. float(abs(z))"

    def arg(self):
        return arctan2(self.imag,self.real)

    def mod2(self):
        return abs(self)**2
   
    def mod(self):
        return abs(self)

    def distance(self,other):
        import math
        real=self.real-other.real
        imag=self.imag-other.imag
        result = math.hypot(real, imag)
        return float(result)
  
    def distanceSquared(self,other):
        return self.distance(other)**2

    def homogenous(self):
        return array([complex(self.real,self.imag),1+0j])




    def set(self,other):
        CPosition.real.__set__(self, other.real)
        CPosition.imag.__set__(self, other.imag)
      
        
    def toComplex(self):
        return complex(self.real,self.imag)



real_slot = CPosition.real
imag_slot = CPosition.imag
