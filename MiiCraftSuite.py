from __future__ import absolute_import
VER = 'V04'
'''
 MiiCraft Suite 
 v0.1    2012-May-18th 
         [P.K.] Modified from MiiCraftPrint V0.2, integrate
                     - Modeler
                     - Slicer
                     - Checker
                     - Printer

 v0.2    2012-June-4th
         [P.K.] Use SlicerV02 (non-OOP) miicraftslice.py to MiiCraftSlicer_V02.py
         2012-June-5th
         [P.K.] Use os.system(0 to call modeler, slicer, checker and printer
         [P.K.] Use gif icon instead of jpg icon
         [P.K.] Clean codes and add comments
 
 v0.3    2012-July-4th
         [P.K.] Prepare for 1st public release
         
ToDo: 1. Now MiiCraft Suit uses os.system to call individual Modeler, Slicer, 
         Checker and Printer. The same program could be called multiple times.
         Use pywin32 to get the titles of windows, when there is an instance of
         the program is already running. Warn the users.
         
 Part of the MiiCraft project
 Copyright(c) 2012 Thomas Wu, Paul Kang

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
# OS utilities
import os
import subprocess

# Tkinter
from   Tkinter        import *
from   tkMessageBox   import *            
from   tkFileDialog   import askopenfilename 

# Vpython
from   visual         import *

# STL Read/Write by Paul Kang
from   STLRead        import *
from   STLWrite       import *

# Constants
PANEL_WIDTH            = 420
PANEL_HEIGHT           = 500
PANEL_LEFT_UP          = 100
PANEL_RIGHT_DOWN       = 100
BUTTON_WIDTH           = 30

LastWorkingSTL         =""

class MiiCraftSuite():
        
    def not_yet(self):
        showinfo("Warning", "Function not implemented yet!")
        return
       
    def Modeler(self):          
        subprocess.Popen("Python MiiCraftModeler"+".py")
        return
     
    def Slicer(self):
        subprocess.Popen("Python MiiCraftSlicer"+".py")
        return
    
    def Checker(self):
        subprocess.Popen("python MiiCraftChecker"+".py")
           
    def Printer(self): 
        subprocess.Popen("python MiiCraftPrinter"+".py")
        return
                     
    def __init__(self):
                
        self.Suite_ui = Tk()
        self.Suite_ui.title("MiCraft(TM) Suite "+VER)
        self.Suite_ui.geometry("%dx%d+%d+%d" % (PANEL_WIDTH, PANEL_HEIGHT, PANEL_LEFT_UP, PANEL_RIGHT_DOWN))
 
        YSPACING = 10
                
        self.ArrowImage = PhotoImage(file = 'small_down_arrow.gif')
                  
        Label(self.Suite_ui, text = "MiiCraft(TM) Suite", font=("Helvetica", 14, 'bold'), justify=LEFT, width=26).pack(padx=5,pady=YSPACING)      
                
        self.Model_Info = Button(self.Suite_ui, text="Modeler: STL Viewer/Editor", command=self.Modeler, font=("Helvetica", 12, 'bold'), width=BUTTON_WIDTH)
        self.Model_Info.pack(padx=5,pady=YSPACING)

        Label(self.Suite_ui, image=self.ArrowImage).pack(padx=5,pady=YSPACING)
               
        self.Slice = Button(self.Suite_ui, text="Slicer: Slicing Model into Images", command=self.Slicer, font=("Helvetica", 12, 'bold'), width=BUTTON_WIDTH)

        self.Slice.pack(padx=5,pady=YSPACING)
        
        Label(self.Suite_ui, image=self.ArrowImage).pack(padx=5,pady=YSPACING)
        
        self.CheckSlice = Button(self.Suite_ui, text="Checker: Check Sliced Images", command=self.Checker, font=("Helvetica", 12, 'bold'), width=BUTTON_WIDTH)
        self.CheckSlice.pack(padx=5,pady=YSPACING)

        Label(self.Suite_ui, image=self.ArrowImage).pack(padx=5,pady=YSPACING)
        
        self.PrintOut = Button(self.Suite_ui, text="Printer: Print STL Model", command=self.Printer, font=("Helvetica", 12, 'bold'), width=BUTTON_WIDTH)
        self.PrintOut.pack(padx=5,pady=YSPACING)
                
        self.Suite_ui.mainloop()

if __name__ == '__main__':
    Suites = MiiCraftSuite()
