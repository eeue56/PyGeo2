#import pychecker.checker

"""
   * 12/01/2001 - 17:18:39
   *
   * PyFrame.py - PyGeo user interface
   * Copyright (C) 2001 Arthur J. siegel
   * ajs@ix.netcom.com
   * pygeo.sourceforge.net
   *
   * This program is free software; you can redistribute it and/or
   * modify it under the terms of the GNU General Public License
   * as published by the Free Software Foundation; either version 2
   * of the License, or any later version.
   *
   * This program is distributed in the hope that it will be useful,
   * but WITHOUT ANY WARRANTY; without even the implied warranty of
   * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   * GNU General Public License for more details.
   *
   * You should have received a copy of the GNU General Public License
   * along with this program; if not, write to the Free Software
   * Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
"""


import visual
import time
from threading import *
import sys
import os
from pygeo.base.element import elements,freepoints
from pygeo.base.pygeoconstants import *
from pygeo.base.pygeomath import *
from pygeo.base.pygeoprimitives import *


class display( visual.ui.display):

   __opts__ = ["width","height","background","scale","title","center","panel","instruction",
              "explanation","reference","trace_on","observe_on","test_real","view_drag","panel_x",
              "panel_y","scene_x","scene_y","axis","povout","frames","delay","pov_name","pov_directory",
              "camera_vector"]

   def __init__( self, **kws):
       visual.ui.display.__init__(self)
       self.select(self)

       #take a long way around since display.height,display width not
       #readable attributes
       self.w=kws.get("width",800)
       self.h=kws.get("height",600)
       self.width=self.w
       self.height=self.h



       self.background=kws.get("background",(.85,1,1))
       self.scale_factor=scale= kws.get("scale",30)
       self.title=kws.get("title","PyGeo")
       self.center=kws.get("center",(0,0,0))
       self.panel= kws.get("panel",True)
       self.instruction= kws.get("instruction",None)
       self.explanation= kws.get("explanation",None)
       self.reference= kws.get("reference",None)
       self.trace_on=kws.get("trace_on",0)
       self.observe_on=kws.get("observe_on",True)
       self.test_real=kws.get("test_real",True)
       self.view_drag=kws.get("view_drag",True)
       self.no_pov_shadows=kws.get("no_pov_shadows",True)
       self.aspect=float(self.width)/self.height

       panel_x= kws.get("panel_x",5)
       panel_y= kws.get("panel_y",5)
       scene_x= kws.get("scene_x",100)
       scene_y= kws.get("scene_y",100)
       self.axis= kws.get("axis",False)
       self.axis_2d= kws.get("axis_2d",False)
       self.forward=kws.get("camera_vector",[0,0,-1])
       self.range=vector(scale,scale,scale)
       self.x=scene_x
       self.y=scene_y
       self.ambient=kws.get("ambient",.2)
       self.autoscale =kws.get("autoscale",False)
       self.exit=True
       if self.trace_on:
          TRACE_ON['active']=True
       if self.view_drag:
          DRAG_VIEW['active']=True
       if self.panel:
          self.cs=Thread(target=geo3d,args=(self,panel_x,panel_y,
                        self.instruction,
                        self.explanation,
                        self.reference))
          
          self.cs.start()              
       if self.axis:
          self.drawaxis()
       else:
          self.axis_on=0




   def animate(self,**kws):
      frames= kws.get("frames",36)
      delay= kws.get("delay",.1)
      povout=kws.get("povout",False)
      for i in range(frames):
         time.sleep(delay)
         for e in elements:
              e.update()
              if e.trace:
                 e.do_trace()
         if self.mouse.clicked:
            time.sleep(.1)
            break
         if povout:
            pov_name=kws.get("pov_name","geopov")
            if i < 10:
                num = "0" + `i`
            else:
                num=`i`
            filename = pov_name + num + ".pov"
            self.Povexport(filename)
 
   def drawaxis(self):
      scale=int(self.scale_factor)
      marker=10/(scale*1.5)
      axis=visual.frame()
      self.y_axis=visual.curve(frame=axis,pos=[(0.0,scale,0.0),
                       (0.0,-scale,0.0)],color=RED)
      self.y_markers=[]
      for i in range(-scale,scale+1):
         self.y_markers.append(visual.curve(frame=axis,pos=[(-marker,i,0),
                              (marker,i,0)],color=RED))
      self.x_axis=visual.curve(frame=axis,pos=[(scale,0.0,0.0),
                       (-scale,0.0,0.0)],color=BLUE)
      self.x_markers=[]
      for i in range(-scale,scale+1):
         self.x_markers.append(visual.curve(frame=axis,pos=[(i,-marker,0),
                              (i,marker,0)],color=BLUE))
      if not self.axis_2d:
         self.z_axis=visual.curve(frame=axis,pos=[(0.0,0.0,scale),
                       (0.0,0.0,-scale)],color=GREEN)
         self.z_markers=[]
         for i in range(-scale,scale+1):
            self.z_markers.append(visual.curve(frame=axis,pos=[(0,-marker,i),
                              (0,marker,i)],color=GREEN))
         self.axis_on=True

   def hideaxis(self):
      self.x_axis.visible=False
      for i in self.x_markers:
        i.visible=False
      self.y_axis.visible=False
      for i in self.y_markers:
        i.visible=False
      self.z_axis.visible=False
      for i in self.z_markers:
        i.visible=False
      self.axis_on=False

   def _do_update(self,i):
       if self.observe_on:
          do=i.dependants
       else:
          do=elements
       for e in do:
         if self.test_real:
            e._allreal()
         e.update()
         if TRACE_ON['active']:
            if e.trace:
               e.do_trace()

   def pickloop(self):
      dragpoint = None
      pickup = self.scale_factor/10.**2
 
      while 1:
 
         if self.mouse.events:
            c = self.mouse.getevent()
            if c.release:
               if dragpoint:   # drop the selected object
                  dragpoint.color = dragpoint.initcolor
                  dragpoint.radius-=pickup
                  if not DRAG_VIEW['active']:
                      self._do_update(self.i)
                  dragpoint = None
            elif c.pick:   # pick up the object
               for f in freepoints:
                   if c.pick in f.rend:
                      c.pick.color = visual.color.green
                      c.pick.radius+=pickup
                      if c.drag:
                         self.i=f
                         dragpoint = c.pick
                         dragpoint.color = visual.color.green
                         if self.panel:
                            if self.i.label:
                               self.controlpanel.pickedlabel.config(text=self.i.label)
                            else:
                               self.controlpanel.pickedlabel.config(text="No label")
                      else:
                          time.sleep(.2)

                          c.pick.color = c.pick.initcolor
                          c.pick.radius-=pickup

                      break
            else:
               for f in freepoints:
                   f.rend[0].color = visual.color.blue
                   f.rend[0].radius+=pickup
                   time.sleep(.1)
                   f.rend[0].color = f.initcolor
                   f.rend[0].radius-=pickup
	                    


         if dragpoint:
              dp=self.mouse.pos
              if dp:
                if DRAGXYZ['active']=='xy':
                  # self.i.vector=c.pos
                  self.i.x=dp.x
                  self.i.y=dp.y
                elif DRAGXYZ['active']=='xz':
                  self.i.x=dp.x
                  self.i.z=dp.y
                elif DRAGXYZ['active']=='yz':
                  self.i.y=dp.y
                  self.i.z=dp.x
                elif DRAGXYZ['active']=='x':
                  self.i.x=dp.x
                elif DRAGXYZ['active']=='y':
                  self.i.y=dp.y
                elif DRAGXYZ['active']=='z':
                  self.i.z=dp.x
                if self.panel:
                   self.controlpanel.positionlabel.config(text='%5.2f , %5.2f , %5.2f'
                                                %(round(self.i.x,2),
                                                  round(self.i.y,2),
                                                  round(self.i.z,2)))
                visual.rate(20)
                self.i.update()
                if DRAG_VIEW['active']:
                   self._do_update(self.i)

   def Povexport(self,filename=None):
       import os
       import string
       #import subprocess

       #os.path.join("..","..","povray")

       buf = file(filename, 'w')
       print "start export"

#       inclist = ['colors.inc', 'textures.inc', 'stones.inc', 'metals.inc','glass.inc']
       print >>buf,'#include "transforms.inc"\n'

       amb=self.ambient*10
       print >>buf,"""
global_settings { ambient_light rgb <%f, %f, %f> }
\n""" %(amb,amb,amb)

       print >>buf,"""background { color rgb <%f, %f, %f> }
\n"""  % (self.background[0],self.background[1],self.background[2])

       light_template = """
light_source { <%f, %f, %f>
color rgb <%f, %f, %f>
}
   """
       for light in self.lights:
           intensity = mag(light)*5./3 # intensity of light (all lights are white)
           pos = norm(light) * max(self.range) * 100.0 # far away to simulate parallel light
           light_code= light_template %(pos.x, pos.y, pos.z,
                                        intensity,intensity,intensity)
           if self.no_pov_shadows:
            # insert frame_code at end (these rot's must be done last)
              end = string.rfind(light_code, '}')
              light_code = light_code[:end] + 'shadowless\n' + light_code[end:]
           print >>buf,light_code


       print >>buf,"""
camera {
    right <%f, 0, 0>      //visual uses right-handed coord. system
    location <%f, %f, %f>
    sky <%f, %f, %f>
    look_at <%f, %f, %f>
    angle %f
}
"""  % (-self.aspect,
        self.mouse.camera.x,self.mouse.camera.y,self.mouse.camera.z,
        self.up.x, self.up.y,self.up.z,
        self.center.x,self.center.y, self.center.z,
        self.fov*180/PI )
       for element in elements:
          if element.visible and element.export:
             for e in element:
                if e.visible and e.export:
                   e.povout(buf)
       time.sleep(1)

       buf.close()
       print "finish export"
       time.sleep(1)

import Tkinter as TK
import tkFileDialog
#import tkMessageBox

DRAGOPTS=('xy','xz','yz','x','y','z')
LEVELMODE=('Specific','Cumulative')
LEVELOPTS=('1','2','3','4','5')
DRAGXYZ={'active':'xy'}
TRACE_ON={'active':0}
DRAG_VIEW={'active':0}

class geo3d:
   def __init__(self,display,x,y,instruction,explanation,reference):
      self.scene=display
      self.scene.controlpanel=self
      self.root=root=TK.Tk()
      self.instruction=instruction
      self.explanation=explanation
      self.reference=reference
      if TK._default_root:
         TK._default_root.withdraw()
      self.menubar = menubar =TK.Menu(root)
      self.TopFrame=TopFrame=TK.Toplevel(self.root,menu=menubar)
      self.x=x
      self.y=y
      self.TopFrame.wm_geometry("+%d+%d" % (self.x, self.y))
      TopFrame.protocol("WM_DELETE_WINDOW", self.TopFrame.destroy)
      TopFrame.title("Geometry")
      TopFrame.iconname("Geometry")
      options=TK.Menu(menubar,name="options")
      help=TK.Menu(menubar,name='help')
      menubar.add_cascade(label="Options",menu=options)
      menubar.add_cascade(label="Help",menu=help)
      options.add_command(label='Reset to intial',command=self.Reset)
      options.add_command(label='Remove trace elements',command=self.Reset_trace)
      options.add_command(label='Remove traced curves',command=self.Reset_trace_curves)
      options.add_command(label='Toggle trace on/off',command=self.Toggle_trace)
      options.add_command(label='Toggle axis visiblity',command=self.Toggle_axis)
      options.add_command(label='Toggle drag effect',command=self.Toggle_drag)

      options.add_command(label='Animate',command=self.scene.animate)
      options.add_command(label='Export Pov-ray file',command=self.Povexport)
      help.add_command(label='Navigation help',command = self.help_dialog)
      help.add_command(label='PyGeo Help', command=self.pygeo_docs)

      if self.instruction:
         help.add_command(label='Diagram instructions',command = self.instructions)
      if self.explanation:
         help.add_command(label='Diagram explantion',command = self.explanations)
      if self.reference:
         help.add_command(label='Diagram refernce',command = self.references)
      self.constraint=constraint=TK.StringVar()
      constraint.set('xy')
      self.level=TK.IntVar()
      self.level.set(1)
      self.SBar=SBar=TK.Frame(TopFrame,relief=TK.RAISED)
      self.UBar=UBar=TK.Frame(TopFrame,relief=TK.RAISED)
      SBar.pack(side='top')
      UBar.pack(side='bottom')

      levelholder = TK.Label(SBar, bd=True, relief='sunken', anchor='w',width=30)
      levelholder.pack(side='left')
      levelcaption=TK.Label(levelholder,width=20,text="Detail Level")
      levelcaption.pack(side='left')
      constraintholder = TK.Label(SBar, bd=True, relief='sunken', anchor='w',width=30)
      constraintholder.pack(side='right')
      constraintcaption=TK.Label(constraintholder,width=20,text="Drag Constraint")
      constraintcaption.pack(side='left')

      for opt in DRAGOPTS:
         b=TK.Radiobutton(constraintholder,text=opt,variable=self.constraint,
                          value=opt, command=self.setDragopt,anchor=TK.W)
         b.pack(side='left')

      self.pickedlabel = TK.Label(UBar, bd=True, relief='sunken', anchor='w',width=10)
      self.pickedlabel.pack(side='left')
      self.positionlabel = TK.Label(UBar, bd=True, relief='sunken', anchor='w',width=20)
      self.positionlabel.pack(side='left')
      self.tracelabel = TK.Label(UBar, bd=True, relief='sunken', anchor='w',width=15)
      self.tracelabel.pack(side='left')
      self.tracelabel.config(text=self.set_tracelabel())
      self.draglabel = TK.Label(UBar, bd=True, relief='sunken', anchor='w',width=15)
      self.draglabel.pack(side='left')
      self.draglabel.config(text=self.set_draglabel())

      self.level1=level1=TK.IntVar()
      self.level2=level1=TK.IntVar()
      self.level3=level1=TK.IntVar()
      self.level4=level1=TK.IntVar()
      self.level5=level1=TK.IntVar()
      self.level6=level1=TK.IntVar()
      self.level1.set(1)
      b=TK.Checkbutton(levelholder,text="1",variable=self.level1,command=self.curryLevel(self.level1,1))
      b.pack(side='left')
      b=TK.Checkbutton(levelholder,text="2",variable=self.level2,command=self.curryLevel(self.level2,2))
      b.pack(side='left')
      b=TK.Checkbutton(levelholder,text="3",variable=self.level3,command=self.curryLevel(self.level3,3))
      b.pack(side='left')
      b=TK.Checkbutton(levelholder,text="4",variable=self.level4,command=self.curryLevel(self.level4,4))
      b.pack(side='left')
      b=TK.Checkbutton(levelholder,text="5",variable=self.level5,command=self.curryLevel(self.level5,5))
      b.pack(side='left')
      b=TK.Checkbutton(levelholder,text="6",variable=self.level6,command=self.curryLevel(self.level6,6))
      b.pack(side='left')
      root.mainloop()

   help='help.txt'

   def help_dialog(self, event=None):
      try:
         helpfile = os.path.join(os.path.dirname(__file__), self.help)
      except NameError:
         helpfile = self.help
      HelpFrame=TK.Toplevel(self.root)
      self.helptext = helptext = TK.Text(HelpFrame, name='text', padx=5,
                                         background="white", wrap="none")
      f = open(helpfile)
      chars = f.read()
      f.close()
      self.helptext.delete("1.0", "end")
      self.helptext.insert("1.0", chars)
      self.helptext.mark_set("insert", "1.0")
      self.helptext.see("insert")
      self.helptext.pack()
      return True

   help_url = "http://pygeo.sourceforge.net/docs_html/index.html"
   if sys.platform[:3] == "win":
      fn = os.path.join(os.path.dirname(__file__), "docs_html", "index.html")
      fn = os.path.normpath(fn)
      if os.path.isfile(fn):
          help_url = fn
      del fn
      def pygeo_docs(self, event=None):
          os.startfile(self.help_url)
   else:
      def pygeo_docs(self, event=None):
          webbrowser.open(self.help_url)


   def instructions(self):
      HelpFrame=TK.Toplevel(self.root)
      instructiontext = TK.Text(HelpFrame, name='text', padx=5,
                                background="white", wrap="none")
      instructiontext.delete("1.0", "end")
      instructiontext.insert("1.0", self.instruction)
      instructiontext.mark_set("insert", "1.0")
      instructiontext.see("insert")
      instructiontext.pack()
      return True

   def explanations(self):
      HelpFrame=TK.Toplevel(self.root)
      explantiontext = TK.Text(HelpFrame, name='text', padx=5,
                               background="white", wrap="none")
      explantiontext.delete("1.0", "end")
      explantiontext.insert("1.0", self.explanation)
      explantiontext.mark_set("insert", "1.0")
      explantiontext.see("insert")
      explantiontext.pack()
      return True

   def references(self):
      HelpFrame=TK.Toplevel(self.root)
      referencetext = TK.Text(HelpFrame, name='text', padx=5,
                              background="white", wrap="none")
      referencetext.delete("1.0", "end")
      referencetext.insert("1.0", self.reference)
      referencetext.mark_set("insert", "1.0")
      referencetext.see("insert")
      referencetext.pack()
      return True

   def Reset(self,*dummy):
      for e in elements:
         e.reset()
      for e in elements:
         e.update()

   def Reset_trace(self,*dummy):
      for e in elements:
         e.reset_trace()

   def Reset_trace_curves(self,*dummy):
      for e in elements:
         e.reset_trace_curves()


   def Toggle_trace(self,*dummy):
      if TRACE_ON['active']:
         TRACE_ON['active']=0
         self.tracelabel.config(text="TRACE OFF")
      else:
         TRACE_ON['active']=True
         self.tracelabel.config(text="TRACE ON")

   def Toggle_drag(self,*dummy):
      if DRAG_VIEW['active']:
         DRAG_VIEW['active']=False
         self.draglabel.config(text="DRAG OFF")
      else:
         DRAG_VIEW['active']=True
         self.draglabel.config(text="DRAG ON")

   def set_tracelabel(self):
      if TRACE_ON['active']:
         return "TRACE ON"
      else:
         return "TRACE OFF"

   def set_draglabel(self):
      if DRAG_VIEW['active']:
         return "DRAG ON"
      else:
         return "DRAG OFF"



   def Povexport(self,filename=None,render=True,show=True):
       import os
       import string
       if not os.path.split(os.getcwd())[-1] == "povout":
           try:
              os.chdir(os.path.join("..","povout"))
           except OSError:
              try:
                 os.chdir(os.path.join("..","..","povout"))
              except OSError:
                 pass

       if not filename:
          filename = self.asksavefile()
       self.scene.Povexport(filename=filename)
       if render:

          print "start render"
          import sys
          if sys.platform == "win32":
             import _winreg
             key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, "Software\\POV-Ray\\CurrentVersion\\WINDOWS")
             os.environ["PATH"]=os.path.join(_winreg.EnumValue(key,0)[1],"bin"+ os.sep)
          renderfile=os.path.basename(filename)
          basefile = os.path.join("..","images",string.split(renderfile,'.')[0])
          imagefile=basefile + ".ppm"
          os.popen('pvengine -GD -GW -GS -GR +FP +GF%s +i%s +o%s +w%s +h%s /EXIT'
                     %(basefile + '.poverror', renderfile, basefile,
                       self.scene.w,self.scene.h ))
       if show:
          tf=TK.Toplevel(self.root)
          tf.title('POVRAY RENDERING')

          UI(tf,imagefile).pack()


   def asksavefile(self):
      self.savedialog = tkFileDialog.SaveAs(master=self.root)
      return self.savedialog.show()

   def setDragopt(self):
     # self.constraintlabel.config(text=self.constraint.get())
      DRAGXYZ['active']=self.constraint.get()


   def Toggle_axis(self):
      if self.scene.axis_on:
         self.scene.hideaxis()
      else:
         self.scene.drawaxis()


   def curryLevel(self,button,level):
       def changeLevel():
           for element in elements:
               if element.level==level:
                  if button.get():
                      if not element.show:
                          element.show=True
                  else:
                      if element.show:
                           element.show=False
               element.setshow()
       return changeLevel


#   def close(self):
#      self.scene.hide() # close visual
#      self.quit()

#   def quit(self):
#      self.root.quit()



class UI(TK.Button):
    def __init__(self,root,filename):
        self.image=TK.PhotoImage(file=filename)
        TK.Button.__init__(self, root, image=self.image, bd=0)
