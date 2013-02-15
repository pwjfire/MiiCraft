from __future__ import absolute_import
VER = "v0.5"
'''
 MiiCraft Modeler 
 v0.1    2012-May-17th  
         [P.K.] Integrated into MiiCraft Suite   
 
 v0.2    2012-June-7th
         [P.K.] Reading/Reloading STL and writing STL will write the STL file name 
                into HOMEPATH+\.miicraft\laststl
         [P.K.] If laststl file exist, load laststl
 
 v0.3    2012-July-5th
         [P.K.] Fix minor budges
         [P.K.] Add Viewer tips
 
 v0.4    2012-July-16th
         [P.K.] Add usage message of the right click

 v0.5    2012-Nov-21th
         [M.H.] Adjust function of LAST_STL_File_NAME 
         
 Part of the MiiCraft project
 Copyright(c) 2012 Paul Kang

 This program is free software; you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation; either version 2 of the License, or
 (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with this program; if not, write to the Free Software Foundation,
 Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
'''

import os, glob, os.path
import sys
import StringIO
import threading
from   visual         import *
from   Tkinter        import *
from   tkMessageBox   import *
from   tkColorChooser import askcolor              
from   tkFileDialog   import askopenfilename
import Image, ImageChops

from   STLRead         import *
from   STLWrite        import *

DebugMessage    = False

#constants
PANEL_WIDTH            = 420
PANEL_HEIGHT           = 500+66
PANEL_LEFT_UP          = 100
PANEL_RIGHT_DOWN       = 100

PYTHON_VIEW_WIDTH      = 500
PYTHON_VIEW_HEIGHT     = 534+66
PYTHON_VIEW_LEFT_UP    = PANEL_WIDTH + PANEL_LEFT_UP + 5
PYTHON_VIEW_RIGHT_DOWN = 100

class MiiCraftModeler:

    def null(self):
        return
    
    def draw_grid(self):
        self.scene3D.up = (0,0,1)
        self.scene3D.forward = (-1,1,-1)
                
        self.x_axis_min_at0   = curve(pos=[(-22.5,-14,  0), (-22.5, 14,  0)], radius=0.06, color=color.red)
        self.x_axis_max_at0   = curve(pos=[( 22.5,-14,  0), ( 22.5, 14,  0)], radius=0.06, color=color.red) 
        self.x_axis_min_atH   = curve(pos=[(-22.5,-14,180), (-22.5, 14,180)], radius=0.06, color=color.red)
        self.x_axis_max_atH   = curve(pos=[( 22.5,-14,180), ( 22.5, 14,180)], radius=0.06, color=color.red) 

        self.y_axis_min_at0   = curve(pos=[(-22.5,-14,  0), ( 22.5,-14,  0)], radius=0.06, color=color.red)
        self.y_axis_max_at0   = curve(pos=[(-22.5, 14,  0), ( 22.5, 14,  0)], radius=0.06, color=color.red)
        self.y_axis_min_atH   = curve(pos=[(-22.5,-14,180), ( 22.5,-14,180)], radius=0.06, color=color.red)
        self.y_axis_max_atH   = curve(pos=[(-22.5, 14,180), ( 22.5, 14,180)], radius=0.06, color=color.red)

        self.z_axis_LeftDown  = curve(pos=[(-22.5,-14,  0), (-22.5,-14,180)], radius=0.06, color=color.red)
        self.z_axis_LeftUp    = curve(pos=[(-22.5, 14,  0), (-22.5, 14,180)], radius=0.06, color=color.red)
        self.z_axis_RightDown = curve(pos=[( 22.5,-14,  0), ( 22.5,-14,180)], radius=0.06, color=color.red)
        self.z_axis_RightUp   = curve(pos=[( 22.5, 14,  0), ( 22.5, 14,180)], radius=0.06, color=color.red)

        self.x_axis_grid_m10  = curve(pos=[(-22.5,-10,  0), ( 22.5,-10,  0)], radius=0.06, color=color.gray(0.5))
        self.x_axis_grid_m5   = curve(pos=[(-22.5, -5,  0), ( 22.5, -5,  0)], radius=0.06, color=color.gray(0.5))
        self.x_axis_grid_0    = curve(pos=[(-22.5,  0,  0), ( 22.5,  0,  0)], radius=0.06, color=color.yellow)
        self.x_axis_grid_p5   = curve(pos=[(-22.5,  5,  0), ( 22.5,  5,  0)], radius=0.06, color=color.gray(0.5))
        self.x_axis_grid_p10  = curve(pos=[(-22.5, 10,  0), ( 22.5, 10,  0)], radius=0.06, color=color.gray(0.5))  

        self.y_axis_grid_m20  = curve(pos=[(  -20,-14,  0), (  -20, 14,  0)], radius=0.06, color=color.gray(0.5))
        self.y_axis_grid_m15  = curve(pos=[(  -15,-14,  0), (  -15, 14,  0)], radius=0.06, color=color.gray(0.5))
        self.y_axis_grid_m10  = curve(pos=[(  -10,-14,  0), (  -10, 14,  0)], radius=0.06, color=color.gray(0.5))
        self.y_axis_grid_m5   = curve(pos=[(   -5,-14,  0), (   -5, 14,  0)], radius=0.06, color=color.gray(0.5))
        self.y_axis_grid_0    = curve(pos=[(    0,-14,  0), (    0, 14,  0)], radius=0.06, color=color.yellow)        
        self.y_axis_grid_p5   = curve(pos=[(    5,-14,  0), (    5, 14,  0)], radius=0.06, color=color.gray(0.5))
        self.y_axis_grid_p10  = curve(pos=[(   10,-14,  0), (   10, 14,  0)], radius=0.06, color=color.gray(0.5))
        self.y_axis_grid_p15  = curve(pos=[(   15,-14,  0), (   15, 14,  0)], radius=0.06, color=color.gray(0.5))
        self.y_axis_grid_p20  = curve(pos=[(   20,-14,  0), (   20, 14,  0)], radius=0.06, color=color.gray(0.5))            
                       
    def look_at_XY(self):
        self.scene3D.forward = (0,0,-1)
        self.scene3D.up = (0,1,0)
        return
        
    def look_at_XZ(self):
        self.scene3D.forward = (0,1,0)
        self.scene3D.up = (0,0,1)     
        return         
          
    def look_at_YZ(self):
        self.scene3D.forward = (-1,0,0)
        self.scene3D.up = (0,0,1)   
        return

    def shift_x(self, val):
        self.model_x = int(val)
        self.V3DFrame.x= self.model_x
        return
      
    def shift_y(self, val):      
        self.model_y = int(val)
        self.V3DFrame.y= self.model_y

    def shift_z(self, val):
        self.model_z = int(val)
        self.V3DFrame.z= self.model_z
        return
    
    def rotate_x(self, val):
        new_xa = int(val) - self.model_x_a
        self.V3DFrame.rotate(angle=pi*new_xa/180, axis=(1,0,0), origin=(0,0,0))
        self.model_x_a = int(val)
        return
    
    def rotate_y(self, val):
        new_ya = int(val) - self.model_y_a
        self.V3DFrame.rotate(angle=pi*new_ya/180, axis=(0,1,0), origin=(0,0,0))
        self.model_y_a = int(val)
        return
            
    def rotate_z(self, val):
        new_za = int(val) - self.model_z_a
        self.V3DFrame.rotate(angle=pi*new_za/180, axis=(0,0,1), origin=(0,0,0))
        self.model_z_a = int(val)
        return
    
    def submit_scale(self):
        try:
            if self.triangles:
                dummy = 1
        except:
            showinfo("Warning", 'No Triangles loaded!')
            return
        
        self.model.visible=0 # http://vpython.org/webdoc/visual/delete.html says this will delete the old self.model.object          
        try:
            self.model_scale = float(self.Scale_num.get())
        except ValueError:
            self.model.visible=1
            self.scale_text.set('Not a Valid number')
            return

        print self.model_scale
        
        for i in range(len(self.triangles)):
            if self.scale_X.get() == 1: self.triangles[i][0] = self.triangles[i][0]* self.model_scale
            if self.scale_Y.get() == 1: self.triangles[i][1] = self.triangles[i][1]* self.model_scale            
            if self.scale_Z.get() == 1: self.triangles[i][2] = self.triangles[i][2]* self.model_scale        

        self.model = faces( pos = zeros( (len(self.triangles)/3,3), float) , frame = self.V3DFrame )
        self.model.pos=self.triangles 
        self.model.make_normals()
        self.model.make_twosided()

        self.scale_text.set('')
        print self.model_scale
        return
        
    def submit_xshift(self):       
        self.model.visible=0 # http://vpython.org/webdoc/visual/delete.html says this will delete the old self.model.object          
        shiftX = self.V3DFrame.x
        self.V3DFrame.x = 0
        self.model_shift_x.set(0)
        
        for triangle in self.triangles:
            triangle[0]+=shiftX
           
        self.model = faces( pos = zeros( (len(self.triangles)/3,3), float) , frame = self.V3DFrame )
        self.model.pos=self.triangles 
        self.model.make_normals()
        self.model.make_twosided()        
            
        return
    
    def submit_yshift(self):        
        self.model.visible=0 # http://vpython.org/webdoc/visual/delete.html says this will delete the old self.model.object          
        shiftY = self.V3DFrame.y
        self.V3DFrame.y = 0
        self.model_shift_y.set(0)
        
        for triangle in self.triangles:
            triangle[1]+=shiftY
          
        self.model = faces( pos = zeros( (len(self.triangles)/3,3), float) , frame = self.V3DFrame )
        self.model.pos=self.triangles 
        self.model.make_normals()
        self.model.make_twosided()         
        return
    
    def submit_zshift(self):
        self.model.visible=0 # http://vpython.org/webdoc/visual/delete.html says this will delete the old self.model.object          
        shiftZ = self.V3DFrame.z
        self.V3DFrame.z = 0
        self.model_shift_z.set(0)
        
        for triangle in self.triangles:
            triangle[2]+=shiftZ

        self.model = faces( pos = zeros( (len(self.triangles)/3,3), float) , frame = self.V3DFrame )
        self.model.pos=self.triangles 
        self.model.make_normals()
        self.model.make_twosided()           
        return
        
    def my_quit(self):
        self.model_ui.destroy()
        self.model_ui.quit()

    def submit_xrotate(self):
        rotateX = float(self.model_x_a)
        self.model_rotate_x.set(0)
        self.triangles = self.rotate_triangles(self.triangles, rotateX, 0, 0)
        self.model.visible=0 # http://vpython.org/webdoc/visual/delete.html says this will delete the old self.model.object          
        self.model = faces( pos = zeros( (len(self.triangles)/3,3), float) , frame = self.V3DFrame )
        self.model.pos=self.triangles 
        self.model.make_normals()
        self.model.make_twosided()                   
        return
    
    def submit_yrotate(self):
        rotateY = float(self.model_y_a)
        self.model_rotate_y.set(0)
        self.triangles = self.rotate_triangles(self.triangles, 0, rotateY, 0)
        self.model.visible=0 # http://vpython.org/webdoc/visual/delete.html says this will delete the old self.model.object          
        self.model = faces( pos = zeros( (len(self.triangles)/3,3), float) , frame = self.V3DFrame )
        self.model.pos=self.triangles 
        self.model.make_normals()
        self.model.make_twosided()                   
        return
    
    def submit_zrotate(self):
        rotateZ = float(self.model_z_a)
        self.model_rotate_z.set(0)
        self.triangles = self.rotate_triangles(self.triangles, 0, 0, rotateZ)
        self.model.visible=0 # http://vpython.org/webdoc/visual/delete.html says this will delete the old self.model.object          
        self.model = faces( pos = zeros( (len(self.triangles)/3,3), float) , frame = self.V3DFrame )
        self.model.pos=self.triangles 
        self.model.make_normals()
        self.model.make_twosided()                   
        return  
    
    def OpenFile(self, ask):        
        self.model.visible=0       
        if ask:
            self.filename = askopenfilename(title='Open file', filetypes=[('STL files', '*.stl')])
        
        try:    
            if self.filename =='':
                showinfo("Warning", "Failed to get STL file name...")
                self.model.visible=1
                return
        except:
            showinfo("Warning", "No STL file name selected...")
            self.model.visible=1
            return    

        [self.ASCII, self.stl_file] = STL_Type(self.filename)

        if self.ASCII == 0:
            [self.triangles, self.triangle_normals, self.max_pos, self.min_pos] = ReadBinary_STL(self.stl_file, gui=True)
        else:
            [self.triangles, self.triangle_normals, self.max_pos, self.min_pos] = ReadASCII_STL(self.stl_file, gui=True)

        
        if len(self.triangles) ==0:
            showinfo("Warning", "Invalid STL file!")           
    
        else:

            showinfo("Model Information", "X Min: "+'%(#)+.4f' % {"#":self.min_pos[0]} 
                                      + "\tX Max: "+'%(#)+.4f' % {"#":self.max_pos[0]} 
                                      + "\nY Min: "+'%(#)+.4f' % {"#":self.min_pos[1]} 
                                      + "\tY Max: "+'%(#)+.4f' % {"#":self.max_pos[1]} 
                                      + "\nZ Min: "+'%(#)+.4f' % {"#":self.min_pos[2]} 
                                      + "\tZ Max: "+'%(#)+.4f' % {"#":self.max_pos[2]} 
                                      + "\n\nTriangle number: " + str(len(self.triangles)/3)
                                      + "\n\nClick 'Model Info.' to see the Info. again."                                                                         
                    )       
        self.model.visible=0 # http://vpython.org/webdoc/visual/delete.html says this will delete the old self.model.object          
        del self.model
        del self.V3DFrame
        self.V3DFrame = frame()
        self.model = faces( pos = zeros( (len(self.triangles)/3,3), float) , frame = self.V3DFrame )

        self.model.pos=self.triangles 
        self.model.make_normals()
        self.model.make_twosided()
        
        self.model_ui.focus()
        
        self.model.visible=1   
        
        write_string = self.filename.replace('/', "\\")
        write_string = write_string.replace(' ', "%32")
        
        HOMEPATH = os.environ['HOMEDRIVE']+os.environ['HOMEPATH']       
        try:
            laststl = open(HOMEPATH+"\\.miicraft\\"+"laststl", "w") 
            laststl.write("LAST_STL_File_NAME  "+write_string) 
            laststl.close()
        except:
            showinfo("Error", "Failure to write laststl! ")    
                
        return
                
    def model_info(self):       
        #center_X = (max_pos[0] + min_pos[0])/2
        self.tri_num = StringVar()
        self.max_x = StringVar()
        self.min_x = StringVar()

        self.max_y = StringVar()
        self.min_y = StringVar()

        self.max_z = StringVar()
        self.min_z = StringVar()        
        
        self.ModelInfo = Toplevel(self.ModelerFrame)
        self.ModelInfo.title('Model Information')
        self.ModelInfo.geometry("%dx%d" % (PANEL_WIDTH, PANEL_HEIGHT))
               
        self.ModelInfo_info = Label(self.ModelInfo, text='Model Information:', font=("Helvetica", 12, 'bold'))
        self.ModelInfo_info.grid(row=0, column=0, sticky=W, padx=5,pady=5)

        self.ModelInfo_tri_num = Label(self.ModelInfo, textvariable = self.tri_num, font=("Helvetica", 12, 'bold'))
        self.ModelInfo_tri_num.grid(row=1, column=0, sticky=W, padx=5,pady=5)
        
        self.ModelInfo_max_x = Label(self.ModelInfo, textvariable = self.max_x, font=("Helvetica", 12, 'bold'))
        self.ModelInfo_max_x.grid(row=2, column=0, sticky=W, padx=5,pady=5)
        self.ModelInfo_min_x = Label(self.ModelInfo, textvariable = self.min_x, font=("Helvetica", 12, 'bold'))
        self.ModelInfo_min_x.grid(row=2, column=1, sticky=W, padx=5,pady=5)

        self.ModelInfo_max_y = Label(self.ModelInfo, textvariable = self.max_y, font=("Helvetica", 12, 'bold'))
        self.ModelInfo_max_y.grid(row=3, column=0, sticky=W, padx=5,pady=5)
        self.ModelInfo_min_y = Label(self.ModelInfo, textvariable = self.min_y, font=("Helvetica", 12, 'bold'))
        self.ModelInfo_min_y.grid(row=3, column=1, sticky=W, padx=5,pady=5)

        self.ModelInfo_max_z = Label(self.ModelInfo, textvariable = self.max_z, font=("Helvetica", 12, 'bold'))
        self.ModelInfo_max_z.grid(row=4, column=0, sticky=W, padx=5,pady=5)
        self.ModelInfo_min_z = Label(self.ModelInfo, textvariable = self.min_z, font=("Helvetica", 12, 'bold'))
        self.ModelInfo_min_z.grid(row=4, column=1, sticky=W, padx=5,pady=5)        

        try:
            self.max_pos, self.min_pos = self.bounday_triangles(self.triangles)
        except:
            showinfo("Warning", "No triangles")
            return
        
        if len(self.max_pos)==0:
            showinfo('Warning", "No triangles')
        else:
            self.tri_num.set('    Triangle numbers: '+ str(len(self.triangles)/3))
            self.max_x.set  ('    Max X: '+ str(self.max_pos[0]))
            self.min_x.set  ('Min X: '+ str(self.min_pos[0]))

            self.max_y.set  ('    Max Y: '+ str(self.max_pos[1]))
            self.min_y.set  ('Min Y: '+ str(self.min_pos[1]))

            self.max_z.set  ('    Max Z: '+ str(self.max_pos[2]))
            self.min_z.set  ('Min Z: '+ str(self.min_pos[2]))            

        return 

    def centerXY(self):
        max_pos, min_pos = self.bounday_triangles(self.triangles)
        center_X = (max_pos[0] + min_pos[0])/2
        center_Y = (max_pos[1] + min_pos[1])/2
        
        self.V3DFrame.x = -center_X
        self.V3DFrame.y = -center_Y
        
        self.model.visible=0 # http://vpython.org/webdoc/visual/delete.html says this will delete the old self.model.object          
        shiftX = self.V3DFrame.x
        shiftY = self.V3DFrame.y
        self.V3DFrame.x = 0
        self.V3DFrame.y = 0
        self.model_shift_x.set(0)
        self.model_shift_x.set(0)
        
        for triangle in self.triangles:
            triangle[0]+=shiftX
            triangle[1]+=shiftY
                     
        self.model = faces( pos = zeros( (len(self.triangles)/3,3), float) , frame = self.V3DFrame )
        self.model.pos=self.triangles 
        self.model.make_normals()
        self.model.make_twosided()
        
        return
        
    def ZeroZ(self):
        max_pos, min_pos = self.bounday_triangles(self.triangles)
        self.V3DFrame.z = -min_pos[2]         
        self.submit_zshift()     
        return      

    def WriteSTL(self): 
        self.stlfilename = STLWrite(self.triangles, self.triangle_normals) 
        
        write_string = self.filename.replace('/', "\\")
        write_string = write_string.replace(' ', "%32")
        
        HOMEPATH = os.environ['HOMEDRIVE']+os.environ['HOMEPATH']       
        try:
            laststl = open(HOMEPATH+"\\.miicraft\\"+"laststl", "w") 
            laststl.write("LAST_STL_File_NAME  "+write_string) 
            laststl.close()
        except:
            showinfo("Error", "Failure to write laststl! ")    
    
    def loadSTL(self):
                                 
        self.model_shift_x.set(0)
        self.model_shift_y.set(0)
        self.model_shift_z.set(0)
        self.model_rotate_x.set(0)
        self.model_rotate_y.set(0)
        self.model_rotate_z.set(0)
        self.model_scale = 1.0
        self.scale_text.set('')   
            
        self.OpenFile(ask=True)
        
        return     

    def reloadSTL(self):
        self.model_shift_x.set(0)
        self.model_shift_y.set(0)
        self.model_shift_z.set(0)
        self.model_rotate_x.set(0)
        self.model_rotate_y.set(0)
        self.model_rotate_z.set(0)
        self.model_scale = 1.0 
        self.scale_text.set('')         
                
        self.OpenFile(ask=False)
  
        return             
    
    def rotate_triangles(self, triangles, x_a, y_a, z_a):
        R_x= array( [[                 1,                  0,                0],
                     [                 0,  cos(x_a/180.0*pi), -sin(x_a/180.0*pi)],
                     [                 0,  sin(x_a/180.0*pi),  cos(x_a/180.0*pi)]])
    
        R_y= array( [[ cos(y_a/180.0*pi),                  0,  sin(y_a/180.0*pi)],
                     [                 0,                  1,                0],
                     [-sin(y_a/180.0*pi),                  0,  cos(y_a/180.0*pi)]])
    
        R_z= array( [[ cos(z_a/180.0*pi), -sin(z_a/180.0*pi),                0],
                     [ sin(z_a/180.0*pi),  cos(z_a/180.0*pi),                0],
                     [                 0,                  0,                1]])
            
        for i in range(len(triangles)):
            if x_a != 0: triangles[i] = vector(dot(R_x,triangles[i]))
            if y_a != 0: triangles[i] = vector(dot(R_y,triangles[i]))
            if z_a != 0: triangles[i] = vector(dot(R_z,triangles[i]))
        
        return triangles       

    def bounday_triangles(self, triangles):
        x_max = -100000
        y_max = -100000
        z_max = -100000   
        x_min =  100000
        y_min =  100000
        z_min =  100000
        
        if len(triangles) ==0: return False, False
        
        for triangle in triangles:
            if triangle[0] > x_max: x_max = triangle[0]
            if triangle[1] > y_max: y_max = triangle[1]
            if triangle[2] > z_max: z_max = triangle[2]
            if triangle[0] < x_min: x_min = triangle[0]               
            if triangle[1] < y_min: y_min = triangle[1]
            if triangle[2] < z_min: z_min = triangle[2]
    
        return [x_max, y_max, z_max], [x_min, y_min, z_min]    
    
    def load_last_stl(self):
        HOMEPATH = os.environ['HOMEDRIVE']+os.environ['HOMEPATH']
        try:
            laststl = open(HOMEPATH+"\\.miicraft\\"+'laststl')
        except:
            #showinfo("Error", "Failed to open"+HOMEPATH+"\\.miicraft\\"+"laststl file.")
            print "Warning:"+"Failed to open"+HOMEPATH+"\\.miicraft\\"+"laststl file."
            return False
        
        inputline = laststl.readline()
        laststl.close()
        
        inputsplit = inputline.split()

        longfilename =""
        if len(inputsplit) > 0 and inputsplit[0] == "LAST_STL_File_NAME":
    
            for i in range(1, len(inputsplit)):
                longfilename = longfilename + inputsplit[i]+" "
            
            longfilename = longfilename.replace("%32"," ")
            
            print longfilename
             
            if os.path.isfile(longfilename[:-1]):
                #print longfilename[:-1]
                if askyesno("Load STL", 'Would you like to load the last STL file?\n\nLarger model would take long time to load and Display.'):
                    self.filename = longfilename[:-1]
                    self.OpenFile(ask=False)   
                
        return     
        
    def ZoomShifttask(self): # Provide Zoom and Z-shift function in the VPython Viewer
        
        if self.scene3D.mouse.events:
            m1 = self.scene3D.mouse.getevent() # get event
            if m1.click == 'left':
                self.scene3D.center[2] = self.scene3D.mouse.pos[2]          
                #print self.scene3D.forward, self.scene3D.range
        
            elif m1.drag == 'middle':
                self.zoom = True
                self.lasty = m1.pos.y
                    
            elif m1.drop == 'middle':
                self.zoom = False            
        
        elif self.zoom:
            self.newy = self.scene3D.mouse.pos.y
            if self.newy != self.lasty:
                distance = (self.scene3D.center-self.scene3D.mouse.camera).mag
                scaling = 10**((self.lasty-self.newy)/distance)
                newrange = scaling*self.scene3D.range.y
                if self.rangemin < newrange < self.rangemax:
                    self.scene3D.range = newrange
                        
                    self.x_axis_min_at0.radius   = 0.0025*newrange
                    self.x_axis_max_at0.radius   = 0.0025*newrange                
                    self.x_axis_min_atH.radius   = 0.0025*newrange  
                    self.x_axis_max_atH.radius   = 0.0025*newrange
                    self.y_axis_min_at0.radius   = 0.0025*newrange
                    self.y_axis_max_at0.radius   = 0.0025*newrange                
                    self.y_axis_min_atH.radius   = 0.0025*newrange  
                    self.y_axis_max_atH.radius   = 0.0025*newrange               
                    self.z_axis_LeftDown.radius  = 0.0025*newrange 
                    self.z_axis_LeftUp.radius    = 0.0025*newrange  
                    self.z_axis_RightDown.radius = 0.0025*newrange 
                    self.z_axis_RightUp.radius   = 0.0025*newrange  
                        
                    self.x_axis_grid_m10.radius  = 0.0025*newrange
                    self.x_axis_grid_m5.radius   = 0.0025*newrange
                    self.x_axis_grid_0.radius    = 0.0025*newrange
                    self.x_axis_grid_p5.radius   = 0.0025*newrange                  
                    self.x_axis_grid_p10.radius  = 0.0025*newrange  
        
                    self.y_axis_grid_m20.radius  = 0.0025*newrange
                    self.y_axis_grid_m15.radius  = 0.0025*newrange                
                    self.y_axis_grid_m10.radius  = 0.0025*newrange
                    self.y_axis_grid_m5.radius   = 0.0025*newrange
                    self.y_axis_grid_0.radius    = 0.0025*newrange
                    self.y_axis_grid_p5.radius   = 0.0025*newrange                  
                    self.y_axis_grid_p10.radius  = 0.0025*newrange   
                    self.y_axis_grid_p15.radius  = 0.0025*newrange
                    self.y_axis_grid_p20.radius  = 0.0025*newrange                              
                                       
                    self.lasty = scaling*self.newy
                                 
        self.model_ui.after(10, self.ZoomShifttask)  # reschedule event in 10 milliseconds
    
        
        
    def __init__(self, parent, parent_window):
               
        self.parent = parent

        self.model_ui = Toplevel(parent_window)
        self.model_ui.geometry("%dx%d+%d+%d" % (PANEL_WIDTH, PANEL_HEIGHT, PANEL_LEFT_UP, PANEL_RIGHT_DOWN))
        
        if __name__ == '__main__':
            self.model_ui.title("MiiCraft Modeler "+VER) 
        else:
            self.model_ui.title("MiiCraft Modeler "+VER) 
                       
        self.status         = StringVar()
        self.scale_X        = IntVar()
        self.scale_Y        = IntVar()  
        self.scale_Z        = IntVar()
        self.model_shift_x  = IntVar()
        self.model_shift_y  = IntVar()
        self.model_shift_z  = IntVar()
        self.model_rotate_x = IntVar()
        self.model_rotate_y = IntVar()
        self.model_rotate_z = IntVar()    
        self.status.set(' ')    
        self.scale_X.set(1)
        self.scale_Y.set(1)
        self.scale_Z.set(1)   
        self.model_shift_x.set(0)   
        self.model_shift_y.set(0)   
        self.model_shift_z.set(0)     
        self.model_rotate_x.set(0) 
        self.model_rotate_y.set(0) 
        self.model_rotate_z.set(0)                        

            
        self.scale_text  = StringVar()
        self.model_scale = 1.0
        self.model_x   = 0              # x offset of the model
        self.model_y   = 0              # y offset of the model
        self.model_z   = 0              # z offset of the model
        self.model_x_a = 0              # rotate angle on x-axis of the model
        self.model_y_a = 0              # rotate angle on x-axis of the model
        self.model_z_a = 0              # rotate angle on x-axis of the model
        self.triangles = []
        self.triangle_normals = []

        self.max_pos=[]
        self.min_pos=[]

        self.scene3D = display(title='Viewer', x=PYTHON_VIEW_LEFT_UP, y=PYTHON_VIEW_RIGHT_DOWN,
                               width=PYTHON_VIEW_WIDTH, height=PYTHON_VIEW_HEIGHT)
        self.scene3D.select()
        self.V3DFrame = frame()
        self.model = faces( pos = zeros( (3,3), float) , frame = self.V3DFrame )
        
        self.scene3D.userzoom = False    
        self.scene3D.range=30
        
        self.draw_grid()

    
        self.ModelerFrame = Frame(self.model_ui, width=370, height=450)
                
        YSPACING = 5

        # Views
        Label(self.ModelerFrame, text='View at:', font=("Helvetica", 12, 'bold')).grid(row=0, column=0,sticky=W, padx=5,pady=YSPACING+3)
        # View XY button
        Button(self.ModelerFrame, text="X-Y Plane", command=self.look_at_XY, font=("Helvetica", 12, 'bold')).grid(row=0, column=1, sticky=W, padx=5,pady=YSPACING+3)
        # View XZ button
        Button(self.ModelerFrame, text="X-Z Plane", command=self.look_at_XZ, font=("Helvetica", 12, 'bold')).grid(row=0, column=2, sticky=W, padx=5,pady=YSPACING+3)      
        # View YZ button
        Button(self.ModelerFrame, text="Y-Z Plane", command=self.look_at_YZ, font=("Helvetica", 12, 'bold'), width=7).grid(row=0, column=3, sticky=W, padx=5,pady=YSPACING+3)

        # X, Y , Z Scale
        Label(self.ModelerFrame, text='Scale at:', font=("Helvetica", 12, 'bold')).grid(row=1, column=0,sticky=W, padx=5,pady=0)
        self.check_x     = Checkbutton(self.ModelerFrame, text="X", variable=self.scale_X, command=self.null, font=("Helvetica", 12, 'bold'))
        self.check_x.grid(row=1, column=1,sticky=W, padx=5,pady=0)
        self.check_y     = Checkbutton(self.ModelerFrame, text="Y", variable=self.scale_Y, command=self.null, font=("Helvetica", 12, 'bold'))
        self.check_y.grid(row=1, column=2,sticky=W, padx=5,pady=0)
        self.check_z     = Checkbutton(self.ModelerFrame, text="Z", variable=self.scale_Z, command=self.null, font=("Helvetica", 12, 'bold'))
        self.check_z.grid(row=1, column=3,sticky=W, padx=5,pady=0)        
        
        # Model Scale setting
        self.label_scale = Label(self.ModelerFrame, text='Scale:', font=("Helvetica", 12, 'bold'))
        self.label_scale.grid(row=2, column=0,sticky=W, padx=5,pady=YSPACING)
        self.Scale_num = Entry(self.ModelerFrame, width=22, textvariable=self.scale_text, font=("Helvetica", 12, 'bold'))
        self.Scale_num.grid(row=2, column=1, columnspan=2, sticky=W, padx=5,pady=YSPACING)        
        Button(self.ModelerFrame, text="Set", command=self.submit_scale,font=("Helvetica", 12, 'bold'), width = 8).grid(row=2, column=3, sticky=E, padx=5,pady=YSPACING)

        # Model X-direction shift slider
        self.label_shift_x = Label(self.ModelerFrame, text='Shift X:', font=("Helvetica", 12, 'bold'))
        self.label_shift_x.grid(row=3, column=0,sticky=W, padx=5,pady=YSPACING)
        self.model_shift_x = Scale(self.ModelerFrame, from_=-50, to=50, length = 200, command=self.shift_x, orient=HORIZONTAL)
        self.model_shift_x.grid(row=3, column=1, columnspan=2, sticky=W, padx=5,pady=YSPACING)
        Button(self.ModelerFrame, text="Set", command=self.submit_xshift,font=("Helvetica", 12, 'bold'), width = 8).grid(row=3, column=3, sticky=E, padx=5,pady=YSPACING)

        # Model Y-direction shift slider
        self.label_shift_y = Label(self.ModelerFrame, text='Shift Y:', font=("Helvetica", 12, 'bold'))
        self.label_shift_y.grid(row=4, column=0,sticky=W, padx=5,pady=YSPACING)
        self.model_shift_y = Scale(self.ModelerFrame, from_=-30, to=30, length = 200, command=self.shift_y, orient=HORIZONTAL)
        self.model_shift_y.grid(row=4, column=1, columnspan=2, sticky=W, padx=5,pady=YSPACING)
        Button(self.ModelerFrame, text="Set", command=self.submit_yshift,font=("Helvetica", 12, 'bold'), width = 8).grid(row=4, column=3, sticky=E, padx=5,pady=YSPACING)

        # Model Z-direction shift slider
        self.label_shift_z = Label(self.ModelerFrame, text='Shift Z:', font=("Helvetica", 12, 'bold'))
        self.label_shift_z.grid(row=5, column=0,sticky=W, padx=5,pady=YSPACING)
        self.model_shift_z = Scale(self.ModelerFrame, from_=-180, to=180, length = 200, command=self.shift_z, orient=HORIZONTAL)
        self.model_shift_z.grid(row=5, column=1, columnspan=2, sticky=W, padx=5,pady=YSPACING)
        Button(self.ModelerFrame, text="Set", command=self.submit_zshift,font=("Helvetica", 12, 'bold'), width = 8).grid(row=5, column=3, sticky=E, padx=5,pady=YSPACING)

        # Model X-axis rotate slider
        self.label_rotate_x = Label(self.ModelerFrame, text='Rotate X:', font=("Helvetica", 12, 'bold'))
        self.label_rotate_x.grid(row=6, column=0,sticky=W, padx=5,pady=YSPACING)
        self.model_rotate_x = Scale(self.ModelerFrame, from_=-180, to=180, length = 200, command=self.rotate_x, orient=HORIZONTAL)
        self.model_rotate_x.grid(row=6, column=1, columnspan=2, sticky=W, padx=5,pady=YSPACING)
        Button(self.ModelerFrame, text="Set", command=self.submit_xrotate,font=("Helvetica", 12, 'bold'), width = 8).grid(row=6, column=3, sticky=E, padx=5,pady=YSPACING)

        # Model Y-axis rotate slider
        self.label_rotate_y = Label(self.ModelerFrame, text='Rotate Y:', font=("Helvetica", 12, 'bold'))
        self.label_rotate_y.grid(row=7, column=0,sticky=W, padx=5,pady=YSPACING)
        self.model_rotate_y = Scale(self.ModelerFrame, from_=-180, to=180, length = 200, command=self.rotate_y, orient=HORIZONTAL)
        self.model_rotate_y.grid(row=7, column=1, columnspan=2, sticky=W, padx=5,pady=YSPACING)
        Button(self.ModelerFrame, text="Set", command=self.submit_yrotate,font=("Helvetica", 12, 'bold'), width = 8).grid(row=7, column=3, sticky=E, padx=5,pady=YSPACING)

        # Model Z-axis rotate slider
        self.label_rotate_z = Label(self.ModelerFrame, text='Rotate Z:', font=("Helvetica", 12, 'bold'))
        self.label_rotate_z.grid(row=8, column=0,sticky=W, padx=5,pady=YSPACING)
        self.model_rotate_z = Scale(self.ModelerFrame, from_=-180, to=180, length = 200, command=self.rotate_z, orient=HORIZONTAL)
        self.model_rotate_z.grid(row=8, column=1, columnspan=2, sticky=W, padx=5,pady=YSPACING)
        Button(self.ModelerFrame, text="Set", command=self.submit_zrotate,font=("Helvetica", 12, 'bold'), width = 8).grid(row=8, column=3, sticky=E, padx=5,pady=YSPACING)

        # Read STL button
        self.Read_STL = Button(self.ModelerFrame, text="Read STL", command=self.loadSTL, font=("Helvetica", 12, 'bold'))
        self.Read_STL.grid(row=9, column=1, sticky=W, padx=5,pady=YSPACING)

        # Model Info. button
        self.Model_Info = Button(self.ModelerFrame, text="Model Info.", command=self.model_info, font=("Helvetica", 12, 'bold'))
        self.Model_Info.grid(row=9, column=2, sticky=W, padx=5,pady=YSPACING)
        
        # Reload button
        self.Reload = Button(self.ModelerFrame, text="Reload", command=self.reloadSTL, font=("Helvetica", 12, 'bold'), width=8)
        self.Reload.grid(row=9, column=3, sticky=W, padx=5,pady=YSPACING)

        # Center
        Button(self.ModelerFrame, text="Center XY", command=self.centerXY, font=("Helvetica", 12, 'bold'), width=8).grid(row=10, column=1, sticky=W, padx=5,pady=YSPACING) 

        # 'Z'ero, put the bottom of the model on the Z=0 ground plane 
        Button(self.ModelerFrame, text="'Z'ero", command=self.ZeroZ, font=("Helvetica", 12, 'bold'), width=9).grid(row=10, column=2, sticky=W, padx=5,pady=YSPACING) 
        
        # Save STL File
        self.button_slicing = Button(self.ModelerFrame, text="Save STL", command=self.WriteSTL, font=("Helvetica", 12, 'bold'), width=8)
        self.button_slicing.grid(row=10, column=3, sticky=W, padx=5,pady=YSPACING) 
        
        # STL Viewer tips
        self.label_tip1 = Label(self.ModelerFrame, text='Viewer Tips: Left-Click to shift the Z of View-At.', font=("Helvetica", 10, 'bold'))
        self.label_tip1.grid(row=11, column=0, columnspan=4, sticky=W, padx=5,pady=YSPACING-5)
        self.label_tip2 = Label(self.ModelerFrame, text='                     Right buttons together to rotate the view.', font=("Helvetica", 10, 'bold'))
        self.label_tip2.grid(row=12, column=0, columnspan=4, sticky=W, padx=5,pady=YSPACING-5)
        self.label_tip3 = Label(self.ModelerFrame, text='                     Left & Right buttons together to scale.', font=("Helvetica", 10, 'bold'))
        self.label_tip3.grid(row=13, column=0, columnspan=4, sticky=W, padx=5,pady=YSPACING-5)
                                                                                         
        self.ModelerFrame.pack()

        self.drag     = None
        self.drag_pos = None
        self.zoom     = None
        self.newy     = None
        self.lasty    = None
        self.rangemin = 1
        self.rangemax = 100  
              
        self.load_last_stl()

        self.model_ui.after(10, self.ZoomShifttask)
           
        self.model_ui.mainloop()

if __name__ == '__main__':
    print "MiiCraftModeler is run from __main__"
    root = Tk()
    root.withdraw()
    MiiCraftModeler("",root)

