

class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class Assignment_Error(Error):
    """Exception raised for errors in the input.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self,e, value):
        self.value=value
        self.e = e
    def __str__(self):
       str = "\n attempted value is %s of type %s \n" %(self.value,type(self.value))
       return str


class Argument_Len_Error(Error):
    """Exception raised for errors in the input.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, e,args):
        self.e=e
        self.args = args

    def __str__(self):
       str = "tgest"
       return str

class Argument_Type_Error(Error):
    """Exception raised for errors in the input.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self,sigs,args):
        self.sigs = sigs
        self.args = args
        self.goodargs=[]
        for a in self.sigs:
           argset=[]
           for b in a:
               argset.append(b.__name__)
           self.goodargs.append(argset)


    def __str__(self):
        str="\n class requires arguments derived from one of: \n %s \n arguments given: \n %s \n" \
        %( self.goodargs,
         [x.__class__.__base__.__name__ for x in self.args])
        return str


#print str.