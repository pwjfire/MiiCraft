VERSION = 'V02'
'''
 MiiCraft Suite 
 v0.1    2012-May-18th 
         Initial Version
         
 V0.2    2012-June-5th
         Add writing HOMEPATH$\.miicraft\laststl in STLWrite()
        
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

#from   visual import *
import os
import sys
import struct
from   tkMessageBox import *
from   tkFileDialog import asksaveasfilename 


def STLWrite(triangles, triangle_normals):
    if len(triangles)==0:
        print "No triangles"
        return False
    
    stlfilename = asksaveasfilename(
    title="Save STL File",
    initialfile="sample",
    defaultextension=".stl",
    filetypes=[('STL files', '*.stl')])
    
    print stlfilename
    
    if stlfilename == "":
        print "Invalid File"
        return False
    
    fw=open(stlfilename, 'w')
    #fw.write("This is a sample\n")
    fw.write("solid From MiiCraftPrint\n")
    
    print len(triangles), len(triangle_normals)
    for i in range(len(triangle_normals)/3):
        normal_x = "%e" % triangle_normals[i*3][0]
        normal_y = "%e" % triangle_normals[i*3][1]
        normal_z = "%e" % triangle_normals[i*3][2]
        v1_x =     "%e" % triangles[i*3][0]
        v1_y =     "%e" % triangles[i*3][1]
        v1_z =     "%e" % triangles[i*3][2] 
        v2_x =     "%e" % triangles[i*3+1][0]
        v2_y =     "%e" % triangles[i*3+1][1]
        v2_z =     "%e" % triangles[i*3+1][2]  
        v3_x =     "%e" % triangles[i*3+2][0]
        v3_y =     "%e" % triangles[i*3+2][1]
        v3_z =     "%e" % triangles[i*3+2][2]                         
        fw.write("  facet normal "+normal_x+" "+normal_y+" "+normal_z+"\n")
        fw.write("    outer loop\n")
        fw.write("      vertex "+v1_x+" "+v1_y+" "+v1_z+"\n")
        fw.write("      vertex "+v2_x+" "+v2_y+" "+v2_z+"\n")
        fw.write("      vertex "+v3_x+" "+v3_y+" "+v3_z+"\n")
        fw.write("    endloop\n")
        fw.write("  endfacet\n")           
                         
    fw.write("endsolid From MiiCraftPrint\n")    
    fw.close()

    return stlfilename
