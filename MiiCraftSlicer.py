from __future__ import absolute_import
VER = "v0.6"
'''
 MiiCraft Slicer 
 v0.1    2012-Apr-22 Initial version
 v0.2    2012-Apr-25 Changes: 
         1. The center position of image is changed from (400,240) to (384, 240)
         2. Layer Thickness setting could be changed by users
         3. XScale and YScale settings could be changed by users
         4. Add PixelPerMillimeter_X and PixelPerMillimeter_Y to INI file
         5. Uniformity correction
         6. Remove -flip from option of executing mogrify.exe. Use negative number of X Scale and Y Scale for mirroring images 
         7. Add Z Scale
         8. Remove the File & Slice menu

 v0.3    2012-July-5th
         1. Merge MiiCraftSlice.ini into MiiCraftSuite.ini
         2. Skeinforge path is casted at the "skeinforge" directory under the MiiCraft installed directory
         3. carve_cvs path is casted at HOMEPATH\.skeinforge\profiles\extrusion\ABS\
         4. add GenIdx
 
 v0.4    2012-July-16th
         1. Change the message of "  ImageMagics Converting Sliced BMP files ..." to
            "  ImageMagics Converting Sliced PNG files ..."
            
 v0.5    2012-July-31st
         1. Correct the image size of mogrify to 768x480
         2. Sliced image numbering starts from 2000 instead 1000 before
         
         2012-Aug-9th
         1. [Bug Fix] MiiCraftSlicer.py     - Correct the image size of mogrify to 768x480
         2. [Improve] MiiCraftSlicer.py     - Sliced image numbering starts from 2000 instead 1000 before

 v0.6    2012-Aug=26th
         1. [Improve] MiiCraftSlicer.py     - Add base option
          
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

import os, glob
import sys
import StringIO
import threading
from   Tkinter        import *
from   tkMessageBox   import *
from   tkColorChooser import askcolor              
from   tkFileDialog   import askopenfilename

import Image, ImageChops, ImageDraw, ImageMath

DebugMessage    = False

#class InputDialog:
#    def __init__(self, parent, VariableName, Message):
#        global AddBase, BaseLayers
#        top = self.top = Toplevel(parent)    
#        Label(top, text=Message, width=25, anchor=W).grid(row=0, column=0, columnspan=2, sticky=W, padx=10,pady=5)
#        Label(top, text="Base Layers", anchor=W).grid(row=1, column=0, sticky=W, padx=10,pady=5)
#
#        BaseLayersVarStr = StringVar()
#        
#        self.e = Entry(top, textvariable=BaseLayersVarStr, width=8)
#        self.e.grid(row=1, column=1, sticky=W, padx=10,pady=5)
#        
#        BaseLayersVarStr.set(str(BaseLayers))
#
#        bOk = Button(top, text="Yes", width=8, command=lambda: self.yes(VariableName)).grid(row=2, column=0, sticky=W, padx=10,pady=5)
#        bCancel = Button(top, text="No", width=8, command=lambda: self.no(VariableName)).grid(row=2, column=1, sticky=W, padx=10,pady=5)
#        AddBase = True
#        
#    def yes(self, VariableName):
#        global BaseLayers
#        inputText = self.e.get()
#        self.top.destroy()  
#        cmd = inputText.split()
#        BaseLayers = int(cmd[0])
#        print "BaseLayers is", BaseLayers                 
#
#    def no(self, VariableName):
#        global AddBase
#        inputText = self.e.get()
#        self.top.destroy()  
#        print "Not to add Base"  
#        AddBase = False          
              
#def BaseDialog():
#    global root
#    d = InputDialog(root, "BaseLayers", "Recommend to add the Base.")
#    root.wait_window(d.top)
        
class SettingsDialog:
    VarName =""
    def __init__(self, parent, LabelText, VarStr):
        global root, LayerThickness, XScale, YScale, ZScale
        
        self.VarName = VarStr
        top = self.top = Toplevel(parent)

        if self.VarName =='LayerThickness':
            VarText = str(LayerThickness)
        elif self.VarName =='XScale':
            VarText = str(XScale)
        elif self.VarName =='YScale':  
                VarText = str(YScale)  
        elif self.VarName =='ZScale':  
                VarText = str(ZScale) 
        Label(top, text=LabelText+VarText, width=40,anchor=W).pack()
        
        self.e = Entry(top, width=40)
        self.e.pack(padx=5)

        Button(top, text="OK", command=self.ok).pack(pady=5)

    def ok(self):
        global LayerThickness, LayerThicknessStr, StatusStr
        global XScale, XScaleStr
        global YScale, YScaleStr
        global ZScale, ZScaleStr        
                
        inputText = self.e.get()
        if self.VarName =='LayerThickness':    
            try:    
                LayerThickness = float(inputText)
            except:
                print "Invalid input for LayerThickness"
                StatusStr.set("Invalid Input for LayerThickness") 
                self.top.destroy()
                return False
            
            if DebugMessage:              
                print "Thickness is", LayerThickness
                
            LayerThicknessStr.set("Layer Thickness:"+"\t"+str(LayerThickness)) 
            
        elif self.VarName =='XScale':
            try:    
                XScale = float(inputText)
            except:
                print "Invalid input for X Scale"
                StatusStr.set("Invalid Input for X Scale") 
                self.top.destroy()
                return False  
            
            if DebugMessage:           
                print "XScale is", XScale
            
            XScaleStr.set('X Scale: '+"\t\t"+str(XScale))  
                     
        elif self.VarName =='YScale':
            try:    
                YScale = float(inputText)
            except:
                print "Invalid input for Y Scale"
                StatusStr.set("Invalid Input for Y Scale") 
                self.top.destroy()
                return False  
                       
            if DebugMessage:
                    print "YScale is", YScale
            
            YScaleStr.set('Y Scale: '+"\t\t"+str(YScale))
            
        elif self.VarName =='ZScale':
            try:    
                ZScale = float(inputText)
            except:
                print "Invalid input for Z Scale"
                StatusStr.set("Invalid Input for Z Scale") 
                self.top.destroy()
                return False  
                       
            if DebugMessage:
                print "ZScale is", ZScale
            
            ZScaleStr.set('Z Scale: '+"\t\t"+str(ZScale))
        
        self.top.destroy()        
                              
def ReadIni(): # Read and Parse the INI file
    global LayerThickness, OutputPath
    global carve_csvFile, XScale, YScale, ZScale
    global PixelPerMillimeter_X, PixelPerMillimeter_Y
#    global UniformityCorrect, UniformityCorrectFile
    global DelSVG, GenIdx
    
    iniFileName     = 'miicraftsuite.ini'
    # Check if the INI file exists
    if not os.path.isfile('./'+iniFileName):
        print 'Error: '+'./'+iniFileName+ " doesn't exist"        
        return False
        
    iniFile = open('./'+iniFileName, 'r')

    # Cast the skeinforge directory at \\skeinforge
    SkeinforgePath = ".\\skeinforge\\skeinforge_application\\"
    print "SkeinforgePath:", SkeinforgePath    
       
    if SkeinforgePath not in sys.path:
        sys.path.insert(0, SkeinforgePath )
        
    if not os.path.isfile(SkeinforgePath+'\skeinforge.py'):     # Check if skeinforge.py exist
        print 'Error: '+"The skeinforge.py does not exist in " + SkeinforgePath +'\skeinforge.py' + "!"
        iniFile.close()
        return False          

    # Get the carve.cvs from HOMEPATH+"\\.skeinforge\\profiles\\extrusion\\ABS\\"
    HOMEPATH = os.environ['HOMEDRIVE']+os.environ['HOMEPATH']
    carve_csvPath = HOMEPATH+"\\.skeinforge\\profiles\\extrusion\\ABS\\"
    carve_csvFile = carve_csvPath +'carve.csv' 
    print "carve_csvFile:", carve_csvFile
      
    if not os.path.isfile(carve_csvFile): # Check carve.csv existence
        print 'Error: '+"The carve.csv does not exist in " + carve_csvPath + "!"
        iniFile.close()
        return False  
 
    csvFile = open(carve_csvFile, 'r') # Check if carve.csv valid
    csvRead = csvFile.readlines()
    csvFile.close()    
    LayerHeightFound = -1
    for i in range(len(csvRead)):
        if ('Layer' in csvRead[i])and ('Height' in csvRead[i]):
            LayerHeightFound = i
            break   

    if LayerHeightFound ==-1:
        print 'Invalid carve.csv! Please check the path or run skeinforge to generate one.'
        iniFile.close()
        carve_csvFile = ""
        return False
    
    csvFile.close()
          
    # Check the Signature in the first line      
    FileSignature  = iniFile.readline()
    if 'Signature' not in FileSignature:
        print 'Error: '+'./'+iniFileName+" doesn't has the valid signature!"
        iniFile.close()
        return False

    # Read the next line from the INI file, it specifies the output path 
    LineRead = iniFile.readline()
    OutputPath = LineRead.split()[1]
#    print "OutputPath in MiiCraftSuite.ini", OutputPath
    if not os.path.isdir(OutputPath):
        os.system('mkdir '+ OutputPath)
                
    # Read the next line from the INI file, it specifies the LayerThickness
    LineRead = iniFile.readline() 
    if LineRead.split()[0] != 'LayerThickness(mm)':
        print 'Error: '+'./'+iniFileName+" doesn't specify LayerThickness(mm)!"
        iniFile.close()
        return False
    
    LayerThickness = LineRead.split()[1]
   

                
    # Read the next line from the INI file, it specifies the X Scale           
    LineRead = iniFile.readline()
    XScale = float(LineRead.split()[1])   

    # Read the next line from the INI file, it specifies the Y Scale           
    LineRead = iniFile.readline()
    YScale = float(LineRead.split()[1]) 

    # Read the next line from the INI file, it specifies the Z Scale           
    LineRead = iniFile.readline()
    ZScale = float(LineRead.split()[1])     

    # Read the next line from the INI file, it specifies the PixelPerMillimeter_X           
    LineRead = iniFile.readline()
    PixelPerMillimeter_X = float(LineRead.split()[1])  
 
    # Read the next line from the INI file, it specifies the PixelPerMillimeter_Y           
    LineRead = iniFile.readline()
    PixelPerMillimeter_Y = float(LineRead.split()[1]) 
    
#    # Read the next line from the INI file, it specifies the Uniformity Correct File               
#    LineRead = iniFile.readline()
#    UniformityCorrect     = LineRead.split()[1]
#    UniformityCorrectFile = LineRead.split()[2]    

    # Read the next line from the INI file, it specifies if delete SVG files after slicing              
    LineRead = iniFile.readline()
    DelSVG   = LineRead.split()[1]

    # Read the next line from the INI file, it specifies if generate idx file after slicing              
    LineRead = iniFile.readline()
    GenIdx   = LineRead.split()[1]
 
  
    WriteThicknesstoCSV(float(LayerThickness)/ZScale)
                             
    iniFile.close()
        
    return True

def UpdateThickness():
    global root, ZScale
    d = SettingsDialog(root, "Input the Layer Thickness (mm): ", "LayerThickness")
    root.wait_window(d.top) 
    WriteThicknesstoCSV(float(LayerThickness)/ZScale)
    
def SetXScale():
    global root
    d = SettingsDialog(root, "Input the X Scale (0.9 ~ 1.1): ", "XScale")
    root.wait_window(d.top) 
    
def SetYScale():
    global root
    d = SettingsDialog(root, "Input the Y Scale (0.9 ~ 1.1): ", "YScale")
    root.wait_window(d.top)   
    
def SetZScale():
    global root
    d = SettingsDialog(root, "Input the Z Scale (0.9 ~ 1.1): ", "ZScale")
    root.wait_window(d.top) 
    WriteThicknesstoCSV(float(LayerThickness)/ZScale) 

def WriteThicknesstoCSV(ZThickness):
    global carve_csvFile, LayerThickness
    
    csvFile = open(carve_csvFile, 'r')
    csvRead = csvFile.readlines()
    csvFile.close()    
    LayerHeightFound = -1
    for i in range(len(csvRead)):
        if ('Layer' in csvRead[i])and ('Height' in csvRead[i]):
            LayerHeightFound = i
            break   

    if LayerHeightFound ==-1:
        print 'Invalid carve.csv! Please check the path or run skeinforge to generate one.'
        carve_csvFile = ""
        return False
    
    new_thickness_line = "Layer Height (mm):\t"+ str(ZThickness)+"\n"
    
    if DebugMessage:
        print ZThickness, new_thickness_line
    
    csvFile = open(carve_csvFile, 'w')
    for i in range(len(csvRead)): 
        if i == LayerHeightFound:
            csvFile.write(new_thickness_line)
        else:
            csvFile.write(csvRead[i])
        
    csvFile.close()         
    
    return True
       
def SkeinforgeSVG(STLFileName):  
    global root
      
    #from skeinforge import * # put import here because ReadIni() will read the path of Skeinforge
    
    repository = getNewRepository()
    root.update()
    repository.fileNameInput.value = STLFileName
    skeinforge_craft.writeSVGTextWithNounMessage(STLFileName, repository, False) 
    root.update()   

def Slice():
    global root, STLFileNameStr, StatusStr
    global STLFileName, OutputPath, StatusStr
    global XScale, YScale, PixelPerMillimeter_X, PixelPerMillimeter_Y
    global DelSVG
    
    # Dialog for adding base  
#    BaseDialog()
    
    CWD = os.getcwd()       # save the current working directory to CWD
    # OutputPath = os.environ['HOMEDRIVE']+os.environ['HOMEPATH']+"\\.miicraft\\output\\" 
    os.chdir(OutputPath)    # change to the output directory  
    
    # Check if STL File is valid, return False if not.
    if STLFileName =='NOVALID':
        STLFileNameStr.set("  No STL file Selected")
        StatusStr.set ("Invalid STL file name!")
        print 'Invalis STL File'
        os.chdir(CWD)
        return False
        
    # Retrieving Filename from Path
    fileSplit = STLFileName.replace("\\","/").split("/")
    stl_file_name = fileSplit[len(fileSplit)-1]
    
    
    print 'Model name:', stl_file_name[0:len(stl_file_name)-4]
    
    FileputPath = str(".\\"+stl_file_name[0:len(stl_file_name)-4]+"\\")
#    print FileputPath
#    print OutputPath
    print 'File path:', str(OutputPath+stl_file_name[0:len(stl_file_name)-4]+"\\")
    os.system('mkdir '+ FileputPath)
    os.chdir(FileputPath)    
            
    # Use Skeinforge to Slice the model to the Skeinforge SVG file
    StatusStr.set("  Slicing with Skeinforge ....")
    root.update()
    SkeinforgeSVG(STLFileName)
    StatusStr.set("  Skeinforge Slicing Done!")
    root.update()
    
    SVGFileName = STLFileName[0:len(STLFileName)-4]+'_skeinforge.svg'
    if DebugMessage:
        print SVGFileName
    
    try:
        inFile = open(SVGFileName, 'r')
    except:
        print 'Error: Open', './'+SVGFileName,'error'
        StatusStr.set('  Error: Open'+'./'+SVGFileName+'error')
        root.update()
        return
       
    TotalLayers = 0

    # Split the Skeinforge SVG file with a collection of layers into SVG files for each layer
    LineRead = inFile.readline()
    
    # Search how many layers in the Skeinforge SVG file
    while LineRead != '':
        if "<g id='z:" in LineRead:         # find the layer id
            TotalLayers = TotalLayers + 1   # TotalLayer increment
        LineRead = inFile.readline() 
    
    # Error if TotalLayer is 0 in the Skeinforge SVG file
    if TotalLayers == 0:
        print 'Warning: Total Layers is 0, something wrong in', './'+SVGFileName
        StatusStr.set('Warning: Total Layers is 0, something wrong in', './'+SVGFileName)
        root.update()
        return
        
    if DebugMessage:
        print 'Total Layers', str(TotalLayers).zfill(4)
    
    # Rewind the Skeinforge SVG file to the beginning
    inFile.seek(0)
    
    # Find the Layer Data header
    LineRead = inFile.readline()
    while LineRead != '':
        if "<g id='layerData'" in LineRead:
            break 
        LineRead = inFile.readline()
        
    if LineRead =='':
        print "'Error: layerData' tag not found, something wrong in", './'+SVGFileName
        return  
    
    LayerDataItems = LineRead.split()
    
    if DebugMessage:
        print LayerDataItems[0], LayerDataItems[1], "fill='#000000' fill-rule='evenodd' stroke='#000000' stroke-width='0px'>"   
    
    # Process each Layer data to an indivisual SVG file    
    for i in range(TotalLayers):   
#        if AddBase:
#            OutSVGFileName = stl_file_name[0:len(stl_file_name)-4]+str(2000+i+BaseLayers).zfill(4)+".svg"
#        else:  
#            OutSVGFileName = stl_file_name[0:len(stl_file_name)-4]+str(2000+i).zfill(4)+".svg"
      
        OutSVGFileName = stl_file_name[0:len(stl_file_name)-4]+str(2000+i).zfill(4)+".svg"  #new add
        
        StatusStr.set('  Generating '+OutSVGFileName)
        root.update()
        OutFile = open(OutSVGFileName, 'w')
        OutString  = StringIO.StringIO()
        
        print >> OutString, SVGHeader
        print >> OutString, LayerDataItems[0], LayerDataItems[1], "fill='#000000' fill-rule='evenodd' stroke='#000000' stroke-width='0px'>"
        
        LineRead = inFile.readline()
        while LineRead != '':
            if "<g id='z:" in LineRead:
                separatedItems = LineRead.split()
                print >> OutString, '    ', separatedItems[0], separatedItems[1], "transform='translate(384.0, 240.0)'>"
            
                LineRead = inFile.readline()
                LineRead = inFile.readline()
                LineRead = inFile.readline()
                if "<path d=" in LineRead:
                    separatedItems = LineRead.split("'")
                    #hard coded is like: separatedItems[3] = ' scale(17.68 17.64) translate(0.0, 0.0)'  #the unit in SVG file is mm, use scale to fit the image size.
                    xscale = XScale * PixelPerMillimeter_X
                    yscale = YScale * PixelPerMillimeter_Y
                    separatedItems[3] = ' scale('+str(xscale)+' '+ str(yscale)+') translate(0.0, 0.0)'
                    print >> OutString, separatedItems[0],"'", separatedItems[1], "'", separatedItems[2], "'", separatedItems[3], "'", separatedItems[4]
                    print >> OutString, '    ', "</g>"
                    break 
                        
            LineRead = inFile.readline()                          

        print >> OutString, "</g>" 
        print >> OutString, "</svg>"

        OutFile.write(OutString.getvalue())
        OutFile.close()
           
    inFile.close()   

    StatusStr.set("  ImageMagics Converting Sliced PNG files ...")
    root.update()

    #os.system('mogrify -size 864x480 -negate -flip -white-threshold 128 -format png *.svg')
    os.system('mogrify -size 768x480 -negate -white-threshold 128 -format png *.svg')

    StatusStr.set("  ImageMagik Conversions Done!")
    root.update()
        
    # Delete temp SVG Files 
    if DelSVG == 'True':
        os.system('del *.svg')    

    '''
    if UniformityCorrect =='True':
        im_filter = Image.open("CorrectRGB_MASK.png")# Read the Uniformity Correction Image 
        StatusStr.set("  Uniformity Correcting ...")
        root.update()   
             
        for PNG in glob.glob(stl_file_name[:-4]+"*.png"):
            StatusStr.set("  Uniformity Correcting "+PNG)
            im_in = Image.open(PNG)           
            im_in = im_in.convert("RGB")               
            im_out = ImageChops.multiply(im_in, im_filter)
            im_out.save(PNG)    
    
        StatusStr.set("  Uniformity Correcting Done!")
        root.update()    
    '''
        
    # Generate Index File
    if GenIdx == 'True':
        filename = stl_file_name[0:len(stl_file_name)-4]
        dirList = os.listdir(".\\")
        #print dirList
        file_num = 0
        for i in dirList:
            if (filename in i) and ('png' in i):
                file_num = file_num + 1
        
        idx_file = open(filename+".idx", 'w')
        idx_file.write("*** NVP Index file ***\n")
        idx_file.write("Prefix "+filename+"\n")
        idx_file.write("Ext png \n")

        idx_file.write("Model_Start 2000"+"\n")
        idx_file.write("Model_End "+str(2000+file_num-1)+"\n") #new add
        idx_file.write("Base_Start "+str(2000-BaseLayers-SupportLaters)+"\n")
        idx_file.close()

        image_base = Image.new("RGB",(768,480))
        draw_base = ImageDraw.Draw(image_base)
        draw_base.rectangle([1,1,766,478], fill=(255,255,255))
        draw_base.rectangle([1,1,21,21], fill=(0,0,0))
        draw_base.rectangle([1,458,21,478], fill=(0,0,0))
        draw_base.rectangle([746,1,766,21], fill=(0,0,0))
        draw_base.rectangle([746,458,766,478], fill=(0,0,0))
        draw_base.ellipse((1,1,41,41), fill=(255,255,255))
        draw_base.ellipse((1,438,41,478), fill=(255,255,255))
        draw_base.ellipse((726,1,766,41), fill=(255,255,255))
        draw_base.ellipse((726,438,766,478), fill=(255,255,255))


        modelFirstLayerFileName = stl_file_name[0:len(stl_file_name)-4]+"2000.png"
#        modelFirstLayerFileName = "test0001.png"  #Debug
        supportIm = addSupportLayer(modelFirstLayerFileName, 6, 15)

        for i in range(BaseLayers+SupportLaters):
            OutSVGFileName = stl_file_name[0:len(stl_file_name)-4]+str(2000+i-BaseLayers-SupportLaters).zfill(4)+".png"
            if i < BaseLayers:
                image_base.save(OutSVGFileName)
            else:
                supportIm.save(OutSVGFileName)

                          
    # Change back to Current Working Directory
    os.chdir(CWD)
    
    root.update()
    
def my_quit():
    root.destroy()
    root.quit()
    
def SelectSTLFile():
    global STLFileName, STLFileNameStr, StatusStr
    global BtnSlice
    
    offset = 32
            
    AskSTLFileName = askopenfilename(title='Open file', filetypes=[('STL files', '*.stl')])  
    Askfilelen = len(AskSTLFileName)   

    file_ext = AskSTLFileName[Askfilelen-4:]
    if file_ext != ".stl" and file_ext != ".STL":
        #STLFileNameStr.set("  No STL file Selected")
        StatusStr.set ("Invalid STL file Selected!")   
        #STLFileName ='NOVALID'     
        return False

    STLFileName = AskSTLFileName
    filelen = Askfilelen
    
    if  filelen < offset:
        STLFileNameStr.set("  "   +STLFileName)
    else:
        STLFileNameStr.set("  ..."+STLFileName[filelen-offset+3:])
        
    StatusStr.set (STLFileName+" is selected!")  

def load_last_stl():
    global STLFileName
    
    offset = 32
    
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
        
        longfilename = longfilename.replace("%32", " ")
             
        if os.path.isfile(longfilename[:-1]):
            print longfilename[:-1], " found!"
            STLFileName = longfilename[:-1]
            filelen = len(STLFileName)
            file_ext = STLFileName[filelen-4:]
            if file_ext != ".stl" and file_ext != ".STL":
                STLFileNameStr.set("  No STL file Selected")
                StatusStr.set ("Invalid STL file name!")   
                STLFileName ='NOVALID'     
                return False
                
            if  filelen < offset:
                STLFileNameStr.set("  "   +STLFileName)
            else:
                STLFileNameStr.set("  ..."+STLFileName[filelen-offset+3:])
                    
                BtnSlice.config(state=NORMAL)
                
    return

def getPixelValue(pixels, size, position):
    if position[0] >= size[0] or position[1] >= size[1]:
        return 0
    else:
        return pixels[position[1] * size[0] + position[0]]

def addSupportLayer(baseLayerFilename, radius, distance):
    baseIm = Image.open(baseLayerFilename)
    baseIm = baseIm.convert('L') # convert to 8-bits gray
    im = Image.new('L', baseIm.size, (0))
    draw = ImageDraw.Draw(im)
    c2c = radius * 2 + distance # maximum distance between the core of rect
    rate = c2c # thumbnail layer2 / thumbnail layer1
    th = 512 / c2c # use threshold to reduce noise
    
    # Create the thumbnail to define where is the best position of support
    # Thumbnail layer1
    w1, h1 = baseIm.size
    w1Shift = w1 % c2c
    h1Shift = h1 % c2c
    w1 = w1 / c2c
    h1 = h1 / c2c
    thumbnail1 = baseIm.resize((w1, h1), Image.ANTIALIAS)
    thumbnail1Pixels = list(thumbnail1.getdata())
    # Thumbnail layer2
    w2 = w1 * rate
    h2 = h1 * rate
    thumbnail2 = baseIm.resize((w2, h2), Image.ANTIALIAS)
    thumbnail2Pixels = list(thumbnail2.getdata())
    
    # Thumbnail layer1 define the initial position of support
    for i in range(len(thumbnail1Pixels)):
        w = i % w1
        h = i / w1
        # draw.rectangle((w * rate + w * w1Shift / w1, h * rate + h * h1Shift / h1, w * rate + w * w1Shift / w1, h * rate + h * h1Shift / h1), fill="white") # DEBUG
        if thumbnail1Pixels[i] > 0:
            # Search best position in Thumbnail layer2
            # The best position is the center of mass
            bestPosition = (w * rate, h * rate)
            dp = (0, 0)
            num = 0
            for dw in range (rate):
                for dh in range(rate):
                    newPosition = (bestPosition[0] + dw,  bestPosition[1] + dh)
                    if getPixelValue(thumbnail2Pixels, (w2, h2), newPosition) > th:
                        dp = (dp[0] + dw, dp[1] + dh)
                        num += 1
            if num == 0:
                continue
            bestPosition = (bestPosition[0] + dp[0] / num, bestPosition[1] + dp[1] / num)
            bestPosition = (
                            bestPosition[0] * c2c / rate + w1Shift * bestPosition[0] / w2,
                            bestPosition[1] * c2c / rate + h1Shift * bestPosition[1] / h2)
            # Paint support
            if c2c & 0x01:
                draw.ellipse((bestPosition[0] - radius, bestPosition[1] - radius,
                                 bestPosition[0] + radius, bestPosition[1] + radius), fill="white")
            else:
                draw.ellipse((bestPosition[0] - radius, bestPosition[1] - radius,
                                 bestPosition[0] + radius - 1 , bestPosition[1] + radius -1), fill="white")
    # im = Image.blend(baseIm, im, 0.8) # DEBUG
    return im


#=== Main Starts

# Global Variables
global STLFileName, StatusStr
global carve_csvFile
global AddBase, BaseLayers, SupportLaters
global root
root = Tk()
root.title("MiiCraft Slice " + VER)  

AddBase = True
BaseLayers = 5
SupportLaters = 5


SVGHeader = """<?xml version="1.0" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">

<svg xmlns="http://www.w3.org/2000/svg" version="1.1">
"""
#iniFileName             = 'skeinslice.ini'
LayerThickness          = '0.1'
OutputPath              = ".\\"
XScale                  = 1.0
YScale                  = 1.0
ZScale                  = 1.0
PixelPerMillimeter_X    = 17.68
PixelPerMillimeter_Y    = 17.64
#UniformityCorrect       = 'True'
#UniformityCorrectFile   = "CorrectRGB_MASK.png"
DelSVG                  = 'True'
GenIdx                  = 'True'

STLFileNameStr          = StringVar()
LayerThicknessStr       = StringVar()
XScaleStr               = StringVar()
YScaleStr               = StringVar()  
ZScaleStr               = StringVar()
StatusStr               = StringVar() 

if ReadIni() != True:
    exit()

from skeinforge import *

if DebugMessage:
    print carve_csvFile
    print XScale, YScale, ZScale, PixelPerMillimeter_X, PixelPerMillimeter_Y
#    print UniformityCorrect, UniformityCorrectFile

STLFileName ='NOVALID'
STLFileNameStr.set          ("  No STL file Selected")
LayerThicknessStr.set       ("Layer Thickness:"+"\t"+str(LayerThickness)) 
XScaleStr.set               ("X Scale:"+"\t"+"\t"+str(XScale)) 
YScaleStr.set               ("Y Scale:"+"\t"+"\t"+str(YScale)) 
ZScaleStr.set               ("Z Scale:"+"\t"+"\t"+str(ZScale))

StatusStr.set        ("")
#root.geometry("%dx%d+%d+%d" % (400, 400, 100, 100))

f = Frame(root, width=370, height=450)

#Setting Frame
SettingFrame = Frame(f,  relief=GROOVE, borderwidth=2)
SettingFrame.place(x=10, y=20, anchor=NW)
Label(SettingFrame, textvariable=LayerThicknessStr, font=("Helvetica", 12, 'bold'), width=20, anchor=W).grid(row=0, column=0, sticky=W, padx=2,pady=5)
BtnThick  = Button(SettingFrame, text="Set Thickness", font=("Helvetica", 12, 'bold'), command= UpdateThickness, width=12).grid(row=0, column=1,sticky=W, padx=5,pady=5)
Label(SettingFrame, textvariable=XScaleStr,         font=("Helvetica", 12, 'bold'), width=20, anchor=W).grid(row=1, column=0, sticky=W, padx=2,pady=5)
BtnXScale = Button(SettingFrame, text="Set X Scale", font=("Helvetica", 12, 'bold'), command= SetXScale, width=12).grid(row=1, column=1,sticky=W, padx=5,pady=5)
Label(SettingFrame, textvariable=YScaleStr,         font=("Helvetica", 12, 'bold'), width=20, anchor=W).grid(row=2, column=0, sticky=W, padx=2,pady=5)
BtnYScale = Button(SettingFrame, text="Set Y Scale", font=("Helvetica", 12, 'bold'), command= SetYScale, width=12).grid(row=2, column=1,sticky=W, padx=5,pady=5)
Label(SettingFrame, textvariable=ZScaleStr,         font=("Helvetica", 12, 'bold'), width=20, anchor=W).grid(row=3, column=0, sticky=W, padx=2,pady=5)
BtnZScale = Button(SettingFrame, text="Set Z Scale", font=("Helvetica", 12, 'bold'), command= SetZScale, width=12).grid(row=3, column=1,sticky=W, padx=5,pady=5)

#Slice Frame
SliceFrame = Frame(f,  relief=GROOVE, borderwidth=2)
#SliceFrame.place(x=10, y=170, anchor=NW)
SliceFrame.place(x=10, y=210, anchor=NW)
Label(SliceFrame, text="STL File Name:", font=("Helvetica", 12, 'bold'), width=34, anchor=W).grid(row=0, column=0, sticky=W, padx=2,pady=0)
Label(SliceFrame, textvariable=STLFileNameStr, font=("Courier New", 12), width=34, anchor=W).grid(row=1, column=0, sticky=W, padx=2,pady=5)
FileOpen = Button(SliceFrame, text="Select STL File", font=("Helvetica", 14, 'bold'), command= SelectSTLFile, width=27)
FileOpen.grid(row=2, column=0, sticky=W, padx=5,pady=5)
BtnSlice = Button(SliceFrame, text="Slice", font=("Helvetica", 14, 'bold'), command= Slice, width=27)
BtnSlice.grid(row=3, column=0, sticky=W, padx=5,pady=5)

# Status Frame
StatusFrame = Frame(f, relief=GROOVE, borderwidth=2)
#StatusFrame.place(x=10, y=350, anchor=NW)
StatusFrame.place(x=10, y=390, anchor=NW)
Label(f, text="Status", font=("Helvetica", 12, 'bold')).place(x=20, y=390,anchor=W)
Label(StatusFrame, textvariable=StatusStr, font=("Helvetica", 12), width=38, anchor=W, wraplength=400, justify=LEFT).grid(row=0, sticky=W, padx=2,pady=10)

f.pack()

load_last_stl()
       
root.mainloop()
    
