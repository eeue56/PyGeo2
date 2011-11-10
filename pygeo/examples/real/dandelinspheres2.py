
from pygeo.base.abstract_elements_real import _Sphere, _Point
from pygeo import *
from pygeo.base.position3 import Position3

# build a class for the sphere inscribed in/ exscribed by 4 arbitrary planes
# inherits from the _Sphere abstract class
class SphereFromPlanes(_Sphere):
   def __init__(self,plane1,plane2,plane3,plane4,inscribed=True,**kws):
      self.plane1=plane1
      self.plane2=plane2
      self.plane3=plane3
      self.plane4=plane4
      self.inscribed=inscribed
      self._center=Position3()
      self.deps=[self._center]
      
      #initialize parent with list of arguments to register
      _Sphere.__init__(self,*[plane1,plane2,plane3,plane4],**kws)
      
      #update to complete initialization
      self.update()

   # find the point of intersection of 3 given planes
   def findPoint(self,plane1,plane2,plane3):
     # _u attribute is normal to plane
     # _d attribute is distance of plane from origin
     return vector(solve(
               array([plane1._u,plane2._u,plane3._u]),
               array([plane1._d,plane2._d,plane3._d])
               ))

   #calculate center, and radius of sphere, return 'True' for success
   def _findSelf(self):
      plane1=self.plane1
      plane2=self.plane2
      plane3=self.plane3
      plane4=self.plane4
      
      v0=self.findPoint(plane1,plane2,plane3)
      v3=self.findPoint(plane1,plane2,plane4)
      e2=v3-v0
      n1=plane2._u
      n2=plane1._u*-1
      n0=plane4._u
      if not self.inscribed:
         # get exscribed sphere
         n0=-n0
      n3=plane3._u*-1
      A=array((n1-n0,n2-n0,n3-n0))
      B=array((0.,0.,-dot(n3,e2)))
      k=vector(solve(A,B))
      self._center.set(v3+k)
      self._radius=-k.dot(n0)
      self._radiusSquared=self._radius**2
      return True

# simply class making the sphere center a dynamic element
class SphereCenter(_Point):
   def __init__(self,sphere,**kws):
      self.sphere=sphere
      self.deps=[]
      _Point.__init__(self,*[sphere],**kws)
      self.update()

   def _findSelf(self):
      self.set(self.sphere._center)
      return True

#construct main window
def construct():
 
   #3 arbitrary points in space
   p1=FreePoint(57,-30,-13,level=4,color=CYAN)
   p2=FreePoint(2,-25,27,level=4,color=CYAN)
   p3=FreePoint(-34,-30,4,level=4,color=CYAN)
   
   #the circle inscribed in the triangle of the 3 points
   circle=Circle(p1,p3,p2,INSCRIBED,level=1,color=BLUE,precision=200)

   #the center of the inscribed circle
   center=Center(p1,p2,p3,INSCRIBED,level=3)
   
   # the plane determined by the 3 points
   plane =Plane(p1,p3,p2,level=5)
   
   #line from the  given point perpendicular to the given plane
   axis=Line(center,plane,level=3)
   
   # a point that slide that can be picked and moved, constrained to the given line
   O=Slider(axis,ratio=3.5)
   
   #3 arbitrary points in space
   p4=FreePoint(25,-20,13,level=1,export=False)
   p5=FreePoint(-18,-7,-18,level=1,export=False)
   p6=FreePoint(-20,-8,16,level=1,export=False)


   #the 4 planes determined by the sliding point and the 3 addtioanl points
   plane1=Plane(O,p1,p2,level=5)
   plane2=Plane(O,p1,p3,level=5)
   plane3=Plane(O,p2,p3,level=5)
   plane4=Plane(p4,p5,p6)
   
   #perspective projection of the circle from the given point to the 
   #given plane.  
   
   #This is the conic whose foci we seek by the construction.
   
   Transform(O,[circle],plane4,color=YELLOW)
   
   #an array of points equidistant on the circumference of the circle
   pa=PointArray(circle,level=3)
  
   #an array of lines connecting the point and the points of the given array
   LineArray(O,pa,linewidth=.05,color=BLACK)


   # the sphere inscribed in the given planes
   sphere1=SphereFromPlanes(plane1,plane2,plane3,plane4,style=FILL)
   

   # the sphere exscribed in the given planes, opposite to the point of 
   # intersection of the first 3 given planes
   sphere2=SphereFromPlanes(plane1,plane2,plane3,plane4,inscribed=False,style=FILL)

   # the centers of the given sphere
   s1=SphereCenter(sphere1)
   s2=SphereCenter(sphere2)
   
   # the centers of the given sphere
   Foot(s1,plane4,color=RED,label="s1",pointsize=1.2)
   Foot(s2,plane4,color=RED,label="s2",pointsize=1.2)



  #construct detail window
   display(scale=30,center=(0,-15,0),scene_x=650,scene_y=350, camera_vector=[.5,-.5,-.5],
        width=350,height=350,panel=False,title="Conic Detail",background=(.9,.9,1))
   Transform(O,[circle],plane4,color=YELLOW)
   Foot(s1,plane4,color=RED,label="s1")
   Foot(s2,plane4,color=RED,label="s2")


v=display(scale=55,title="Dandelin Sphere",scene_x=5,scene_y=5,width=450,panel=False)
construct()
v.pickloop()

