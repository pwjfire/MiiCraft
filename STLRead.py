VERSION = 'V02'
'''
 MiiCraft Suite 
 v0.1    2012-May-18th 
         Initial Version
 
 V0.2    2012-June-5th
         Binary STL handling with "Solid" header from Pre/E
                 
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

from   visual import *
import struct
import sys
from   tkMessageBox import *

# Convert the binary format of STL to floats.
def bin_to_float(b):
  
    exponent = (b[3] & 0x7F)*2 | (b[2] & 0x80)>>7
    sign = (b[3]&0x80)>>7
    exponent = exponent-127
    significand = 1 + (b[2]&0x7F)*pow(2,-7) + b[1]*pow(2,-15) + b[0]*pow(2,-23)  #throwing away precision for now...

    if(sign!=0): significand=-significand
    finalvalue = significand*pow(2,exponent);

    return finalvalue;

def scale_triangles(triangles, scale):
    # scale is a float
    for i in range(len(triangles)):
        triangles[i] = triangles[i] * scale

    return triangles

def shift_triangles(triangles, shift):
    # shift is a vector
    for i in range(len(triangles)):
        triangles[i] = triangles[i] + shift
        
    return triangles

def rotate_triangles(triangles, x_a, y_a, z_a):
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
    
# Judge STL type
def STL_Type(filename):

    ASCII = 0
    stl_file =open(filename)

    for i in range(4): # Some ASCII STL files have unwanted characters before "solid"
        head = stl_file.readline()
        if 'solid' in head:  
            facet_word  = stl_file.readline()
            if 'facet' in facet_word:
                print 'ASCII STL found'
                ASCII = 1                     
                stl_file.seek(-len(facet_word),1) # Unread facet                  
                return [ASCII, stl_file] 
        
    stl_file.close()
    print 'ASCII STL not found, open with binary'
    stl_file =open(filename, 'rb')
    
    return [ASCII, stl_file]


# kBinary STL

def ReadBinary_STL(fb, gui):
    # fb is the stl file opened with binary

    x_max = -100000
    y_max = -100000
    z_max = -100000

    x_min =  100000
    y_min =  100000
    z_min =  100000

    #fb=open(filename, 'rb')

    fb.seek(80) #skip the header

    a = fb.read(4)
    number_of_triangles = struct.unpack('L',a)
    
    if number_of_triangles[0] > 10000000 :
        if gui:
            showinfo("Warning", "Too many triangles or wrong binary file!")
        else:
            print "Too many triangles or wrong binary file"
        return [ [], [], [], [] ]

    triangle_normals = []
    triangles = []

    #print number_of_triangles[0]
    
    for i in range(number_of_triangles[0]):

        # read the normal of the next triangle
        n    = fb.read(12)
        nb   = struct.unpack('BBBBBBBBBBBB', n)

        n_x = bin_to_float(nb[0:4])
        n_y = bin_to_float(nb[4:8])    
        n_z = bin_to_float(nb[8:12])
        normal = [n_x, n_y, n_z]
        triangle_normals.append(normal)
        triangle_normals.append(normal)
        triangle_normals.append(normal)

        # read the tiangle vertex 
        for j in range(3):
            v     = fb.read(12)
            vb    = struct.unpack('BBBBBBBBBBBB', v)
            #print vb
            v_x   = bin_to_float(vb[0:4])
            v_y   = bin_to_float(vb[4:8])    
            v_z   = bin_to_float(vb[8:12])
            if v_x > x_max: x_max = v_x
            if v_y > y_max: y_max = v_y
            if v_z > z_max: z_max = v_z
            if v_x < x_min: x_min = v_x                 
            if v_y < y_min: y_min = v_y
            if v_z < z_min: z_min = v_z  
            #v_vec = [v_x, v_y, v_z]
            v_vec = vector(v_x, v_y, v_z)            
            triangles.append(v_vec)            

            
        fb.read(2)  #skip the 2bytes attribute byte count

        
    n    = fb.read(12)

    fb.close()
    return [triangles, triangle_normals, [x_max, y_max, z_max], [x_min, y_min, z_min]]
    
def ReadASCII_STL(fa, gui):
    # fa is the stl file opened with ASCII
    
    x_max = -100000
    y_max = -100000
    z_max = -100000

    x_min =  100000
    y_min =  100000
    z_min =  100000

    triangle_normals = []
    triangles = []

    f_all = fa.readlines()
    fa.close()

    vertex_to_go = 0
    i = 0

    f_all_len = len(f_all)


    print 'Reading the triangles ....',
    while i < f_all_len-7:
        error_num = 0
        if ('facet' in f_all[i]) and ('normal' in f_all[i]):
            aaa = f_all[i].split()
            normal = [float(aaa[2]), float(aaa[3]), float(aaa[4])]
            #normal = [float(aaa[2]), float(aaa[4]), float(aaa[3])]
            triangle_normals.append(normal)
            triangle_normals.append(normal)
            triangle_normals.append(normal)        

        if 'outer'    not in f_all[i+1]: error_num = error_num + 1
        if 'vertex'       in f_all[i+2]:
            aaa = f_all[i+2].split()
            point1 = vector(float(aaa[1]), float(aaa[2]), float(aaa[3]))
            #point1 = [float(aaa[1]), float(aaa[3]), float(aaa[2])]
            triangles.append(point1)
            if float(aaa[1]) > x_max: x_max = float(aaa[1])
            if float(aaa[2]) > y_max: y_max = float(aaa[2])
            if float(aaa[3]) > z_max: z_max = float(aaa[3])
            if float(aaa[1]) < x_min: x_min = float(aaa[1])                  
            if float(aaa[2]) < y_min: y_min = float(aaa[2])
            if float(aaa[3]) < z_min: z_min = float(aaa[3])                  
        else: error_num = error_num + 1
        if 'vertex'       in f_all[i+3]:
            aaa = f_all[i+3].split()
            point2 = vector(float(aaa[1]), float(aaa[2]), float(aaa[3]))
            #point2 = [float(aaa[1]), float(aaa[3]), float(aaa[2])]
            triangles.append(point2)
            if float(aaa[1]) > x_max: x_max = float(aaa[1])
            if float(aaa[2]) > y_max: y_max = float(aaa[2])
            if float(aaa[3]) > z_max: z_max = float(aaa[3])
            if float(aaa[1]) < x_min: x_min = float(aaa[1])                  
            if float(aaa[2]) < y_min: y_min = float(aaa[2])
            if float(aaa[3]) < z_min: z_min = float(aaa[3])        
        else: error_num = error_num + 1
        if 'vertex'       in f_all[i+4]: 
            aaa = f_all[i+4].split()
            point3 = vector(float(aaa[1]), float(aaa[2]), float(aaa[3]))
            #point3 = [float(aaa[1]), float(aaa[3]), float(aaa[2])]
            triangles.append(point3)
            if float(aaa[1]) > x_max: x_max = float(aaa[1])
            if float(aaa[2]) > y_max: y_max = float(aaa[2])
            if float(aaa[3]) > z_max: z_max = float(aaa[3])
            if float(aaa[1]) < x_min: x_min = float(aaa[1])                  
            if float(aaa[2]) < y_min: y_min = float(aaa[2])
            if float(aaa[3]) < z_min: z_min = float(aaa[3])        
            #triangles.append([point1, point2, point3])
        else: error_num = error_num + 1        
        if 'endloop'  not in f_all[i+5]: error_num = error_num + 1    
        if 'endfacet' not in f_all[i+6]: error_num = error_num + 1  
        i = i+7

    print 'done!'

    return [triangles, triangle_normals, [x_max, y_max, z_max], [x_min, y_min, z_min]]
