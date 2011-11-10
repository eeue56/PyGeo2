
import Numeric
import visual

class wiresphere:
   def __init__(self,density):
      self.density=density
      self.stack_increment = Numeric.pi /(density+1)
      self.slice_increment = Numeric.pi /density
   def getstacks(self):
      stackAngle = self.stack_increment
      wireStack=[0]*self.density
      for i in range(self.density):
         sliceAngle = 0.0;
         newstack = [0]*self.density
         for j in range(self.density):
            newstackvect = (Numeric.sin(stackAngle) * Numeric.sin(sliceAngle),
                            Numeric.sin(stackAngle) * Numeric.cos(sliceAngle),
                            Numeric.cos(stackAngle))

            newstack[j] = newstackvect
            sliceAngle -= self.slice_increment * 2.0
         newstack.append(newstack[0])
         wireStack[i] = newstack
         stackAngle +=self.stack_increment
      return Numeric.array(wireStack,'d')

   def getslices(self):
      sliceAngle = 0.0;
      wireSlice=[0]*self.density
      for i in range(self.density):
         stackAngle = 0.0
         newslice=[1]*(self.density+1)
         for j in range(self.density+1):
            newslicevect=visual.vector(Numeric.sin(stackAngle) * Numeric.sin(sliceAngle),
                         Numeric.sin(stackAngle) * Numeric.cos(sliceAngle),
                         Numeric.cos(stackAngle))
            newslice[j] =newslicevect
            stackAngle -= self.slice_increment
         wireSlice[i] = newslice
         sliceAngle += self.slice_increment * 2.0
      return Numeric.array(wireSlice,'d')
