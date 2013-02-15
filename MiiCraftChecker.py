from __future__ import absolute_import
VER = "v0.4"
'''
 MiiCraft Check Slice Images 
 v0.1    2012-May-4th  [P.K.] Initial version
 v0.2    2012-May-31th [T.W.] Remove the "Three Images" button
         2012-May-31th [T.W.] Change the behavior of "Two Image" button
         2012-June-4th [P.K.] Change to non-class
                       [P.K.] Remove the "Print" Button"
                       [P.K.] Read HOMEPATH$\.miicraft\laststl file for the STL model name
                       [P.K.] Change the output path to HOMEPATH$\.miicraft\output
 
 v0.3    2012-July-5th [P.K.] Change the output path to reading from MiiCraftSuite.ini
 
 v0.4    2012-July-16th [P.K.] Change the initdir of askopenfilename to .\output
 
 ToDo: Zoom in the preview image 
 
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

import os, os.path
import sys
import struct
import subprocess

from   Tkinter        import *
from   tkMessageBox   import *
from   tkCommonDialog import Dialog
from   tkColorChooser import askcolor              
from   tkFileDialog   import askopenfilename 

from   PIL            import Image, ImageTk, ImageOps, ImageEnhance

PANEL_WIDTH            = 900
PANEL_HEIGHT           = 600
PANEL_LEFT_UP          = 100
PANEL_RIGHT_DOWN       = 100

def null():
    return

def ReadOutputPath(): # Read and Parse the INI file
    
    iniFileName     = 'miicraftsuite.ini'
    # Check if the INI file exists
    if not os.path.isfile('./'+iniFileName):
        print 'Error: '+'./'+iniFileName+ " doesn't exist"        
        return False
        
    iniFile = open('./'+iniFileName, 'r')
          
    # Check the Signature in the first line      
    FileSignature  = iniFile.readline()
    if 'Signature' not in FileSignature:
        print 'Error: '+'./'+iniFileName+" doesn't has the valid signature!"
        iniFile.close()
        return False

    # Read the next line from the INI file, it specifies the output path 
    LineRead = iniFile.readline()
    OutputPath = LineRead.split()[1]
    
    return OutputPath
            
def read_last_stl():
    
    HOMEPATH = os.environ['HOMEDRIVE']+os.environ['HOMEPATH']
    try:
        laststl = open(HOMEPATH+"\\.miicraft\\"+'laststl')
    except:
        showinfo("Error", "Failed to open"+HOMEPATH+"\\.miicraft\\"+"laststl file.")
        return False
    
    inputline = laststl.readline()
    laststl.close()
    
    inputsplit = inputline.split()
    longfilename =""
    if len(inputsplit) > 0 and inputsplit[0] == "LAST_STL_File_NAME":

        for i in range(1, len(inputsplit)):
            longfilename = longfilename + inputsplit[i]+" "
          
        return longfilename[:-1]
    else:
        print HOMEPATH+"\\.miicraft\\"+"laststl file is invalid!"
        #showinfo("Error",HOMEPATH+"\\.miicraft\\"+"laststl file is invalid!")
        return False

def CountImages(stlfilename, ImageFolder):
    global FileputPath
    try:
        dirList = os.listdir(ImageFolder)
    except:
        showinfo("Error", "Path: "+ImageFolder+" doesn't exist!")
        return -1, -1
        
    if len(dirList)==0:
        showinfo("Error", "Path: "+ImageFolder+" doesn't have images!")
        return -1, -1
        
    #print len(dirList), os.getcwd()
        
    min_image_num = 2000
    max_image_num = 0
        
    for imgFile in dirList:
        if 'png' in imgFile:
            if stlfilename[:-4] in imgFile:
                try:
                    file_num = int(imgFile[-8:-4])
                except:
                    return -1, -1    
                if file_num > max_image_num: max_image_num = file_num
                if file_num < min_image_num: min_image_num = file_num
    
    if max_image_num > 0:
        FileputPath = ImageFolder
    return min_image_num, max_image_num
    
def changeImage(slice_num):
    
    global PreViewImage, PreviewName, stlfilename
    global image_tk

    PreviewName.set("Preview Images - "+stlfilename[:-4]+str(slice_num)+".png")

    OperationValue = OperationVar.get()
    
    imageBlank  = Image.new("RGB", (768,480),0)
    
    image_im_m1        = imageBlank
        
    if (OperationValue == 1):      
        imageFile   = FileputPath+stlfilename[:-4]+str(int(slice_num))  +".png"
        try:
            image_im    = Image.open(imageFile)
        except:
            print imageFile+" error"
            showinfo("Error:", imageFile+" Open Error!")
            #checkslice_ui.destroy()
            return            
      
    if (OperationValue == 2):
        imageFile   = FileputPath+stlfilename[:-4]+str(int(slice_num))  +".png"
        try:
            image_im    = Image.open(imageFile)
        except:
            print imageFile+" error"
            showinfo("Error:", imageFile+" Open Error!")
            #checkslice_ui.destroy()
            return
                
        imageFilem1 = FileputPath+stlfilename[:-4]+str(int(slice_num)-1)+".png"
        try:
            image_im_m1 = Image.open(imageFilem1)
        except:
            image_im_m1 = imageBlank
    
        image_im    = image_im.convert("L")    
        image_im    = ImageOps.colorize(image_im, (0,0,0), (255,0,0)) 
        image_im    = image_im.convert("RGB") 
                                  
        image_im_m1 = image_im_m1.convert("L")    
        image_im_m1 = ImageOps.colorize(image_im_m1, (0,0,0), (255,255,255))
        image_im_m1 = image_im_m1.convert("RGB") 
        
        try:          
            image_im = Image.blend(image_im, image_im_m1, 0.3)
        except:
            null()
                
        image_im_enhance = ImageEnhance.Brightness(image_im)
        image_im = image_im_enhance.enhance(2.0)                       
                                        
    image_tk = ImageTk.PhotoImage(image_im)
        
    PreViewImage.configure(image = image_tk)
            
    return

def get_stlname_from_image():
    global stlfilename
    
    HOMEPATH = os.environ['HOMEDRIVE']+os.environ['HOMEPATH']
    longfilename = askopenfilename(title='Open file', filetypes=[('PNG files', '*.png')], initialdir = "output")            
    long_split = longfilename.split('/')
    imgfilename = long_split[len(long_split)-1]
    stlfiledir = '\\'.join(long_split[:-1])
    
    if imgfilename[:-8]=="":
        print "No file is selected!"
        return False
    
    stlfilename = imgfilename[:-8]+".stl"
    SliceImgPath = stlfiledir + '\\'
    
    #check outputs images
    fileNum_min, fileNum_max = CountImages(stlfilename, SliceImgPath)
    if fileNum_max == -1:
        print "Error"
        return False
    
    Scale_ImageSelect.configure(from_=fileNum_max)
    Scale_ImageSelect.configure(to=fileNum_min)
    Scale_ImageSelect.configure(command=changeImage)
    Scale_ImageSelect.configure(state=NORMAL)
    Scale_ImageSelect.set(fileNum_min)
    
    changeImage(fileNum_min)  
    return stlfilename
    
################ Main program below ##################################
  
global PreViewImage, PreviewName, stlfilename
global image_tk

# Setup GUI
image_tk =""   
           
checkslice_ui = Tk()
checkslice_ui.geometry("%dx%d" % (PANEL_WIDTH, PANEL_HEIGHT))
checkslice_ui.title("MiiCraft Checker " + VER)
        
PreviewName    = StringVar()
PreviewName.set("Preview Images - ")
        
f = Frame(checkslice_ui, width=880, height=600)
        
#PreView Image Frame
PreViewFrame = Frame(f, relief=GROOVE, borderwidth=2)
PreViewFrame.place(x=0, y=22, anchor=NW)
Label(f, textvariable=PreviewName, font=("Helvetica", 12, 'bold')).place(x=20, y=20,anchor=W)
imageBlank  = Image.new("RGB", (768,480),0)
imageBlank_tk  = ImageTk.PhotoImage(imageBlank)
PreViewImage = Label(PreViewFrame, image=imageBlank_tk)
PreViewImage.pack(pady=10) 
 
#Check Frame
CheckFrame = Frame(f, relief=GROOVE, borderwidth=2)
CheckFrame.place(x=800, y=22, anchor=NW)        
label_ImageSelect = Label(CheckFrame, text='Slice', font=("Helvetica", 12, 'bold'))
label_ImageSelect.grid(row=0, column=0,sticky=W, padx=5,pady=5)
Scale_ImageSelect = Scale(CheckFrame, from_=100, to=0, length=453, orient=VERTICAL, state=DISABLED)
Scale_ImageSelect.grid(row=1, column=0, columnspan=2, sticky=W, padx=5,pady=5)
        
#Operate Frame
OperationVar = IntVar()
OperationVar.set(1)
        
OperateFrame = Frame(f, relief=GROOVE, borderwidth=2)
OperateFrame.place(x=200, y=540, anchor=NW)                
     
Radiobutton(OperateFrame, width=26, text="Single Image", variable=OperationVar, value=1, indicatoron=0, font=("Helvetica", 12, 'bold')).grid(row=0, column=0, sticky=NW, padx=5,pady=5)
Radiobutton(OperateFrame, width=27, text="Two Images Compare",   variable=OperationVar, value=2, indicatoron=0, font=("Helvetica", 12, 'bold')).grid(row=0, column=1, sticky=NW, padx=5,pady=5)

#Load Frame
LoadFrame = Frame(f, relief=GROOVE, borderwidth=2)
LoadFrame.place(x=0, y=540, anchor=NW)        
Button(LoadFrame, width=15, text="Load Image", command=get_stlname_from_image,font=("Helvetica", 12, 'bold')).grid(row=0, column=3, sticky=NW, padx=5,pady=5)
        
f.pack()

# End of GUI

HOMEPATH = os.environ['HOMEDRIVE']+os.environ['HOMEPATH']+"\\.miicraft\\"
SliceImgPath = ReadOutputPath()

if os.path.isfile(HOMEPATH+'laststl') and read_last_stl() != False:
    longfilename = read_last_stl()
    long_split = longfilename.split('\\')
    stlfilename = long_split[len(long_split)-1].replace("%32", " ")
    stlfiledir = '\\'.join(long_split[:-1])
    print stlfilename, longfilename
    #check outputs images
    SliceImgPath = ReadOutputPath() + stlfilename[0:len(stlfilename)-4]+"\\";
    if os.path.isdir(SliceImgPath):
        fileNum_min, fileNum_max = CountImages(stlfilename, SliceImgPath)
    else:
        SliceImgPath = stlfiledir + '\\'
        fileNum_min, fileNum_max = CountImages(stlfilename, SliceImgPath)
    if fileNum_max > 0:
        Scale_ImageSelect.configure(from_=fileNum_max)
        Scale_ImageSelect.configure(to=fileNum_min)
        Scale_ImageSelect.configure(command=changeImage)
        Scale_ImageSelect.configure(state=NORMAL)
        Scale_ImageSelect.set(fileNum_min)
        changeImage(fileNum_min)
else:
    print HOMEPATH+"laststl file doesn't exist!"
                     
    
checkslice_ui.mainloop()
        
