from random import random,randint

__all__=['makecolor','permrange','permsets','subsets','isSubset','randomXYZ']

def makecolor(r=None,g=None,b=None):
  if not r:
    r=random()
  if not g:
    g=random()
  if not b:
    b=random()
  return (r,g,b)


# thanks to Phil Hunt's python-list response
# to my question on getting a permutation of
# a list excluding instance where list== list.reverse

def permrange(e,n=None):
   I=[]
   def perms(source,done,current=[]):
      if done == len(source):
         if current[0] < current[-1]:
            I.append(current)
      else:
         for s in source:
            if s not in current:
                perms(source,done+1,current+[s])
      if  len(I):
         return I
   source=range(e)
   if not n:
      done = 0
   else:
      done=e-n

   if n == 0:
      return []

   if n == 1:
      for s in source:
         I.append([s])
   else:
      perms(source,done)
   return I


def permsets(source,size):
   def permcalc(source,done,current=[]):
      if done == len(source):
         if current[0] < current[-1]:
            P.append(current)
      else:
         for i in source:
            if i not in current:
                permcalc(source,done+1,current+[i])
   P=[]
   done = len(source)-size
   permcalc(source,done)
   return P

# thanks to Danny Yoo's  Python edu-sig list response
# to my question on getting a permutation of
# a list excluding instance where list== list.reverse

def addhead(head,seq):
   I=[]
   for s in seq:
      I.append([head]+s)
   return I

def subsets(seq,n=None):
   s=list(seq)
   if not seq or n == 0:
      return []
   if n == 1:
      return map(lambda x: [x],seq)
   c1=addhead(s.pop(0),subsets(s,n-1))
   c2=subsets(s,n)
   return c1 + c2

def isSubset(a,b):
   t=a[:]
   s=b[:]
   while t:
      for i in t:
         if i in s:
             t.remove(i)
             isSubset(t,b)
         else: return False
   return True

# generate a random (integral) XYZ coordinates
# in space

def randomXYZ(max=50):
   def getsign():
      s=randint(0,1)
      if s: return False
      return True
   x=randint(0,max)*getsign()
   y=randint(0,max)*getsign()
   z=randint(0,max)*getsign()
   return (x,y,z)

