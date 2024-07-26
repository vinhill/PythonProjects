import numpy as np
import cv2
import math
import imageio
import random

#colors
primary = np.asarray((0, 255, 235)) # cyan
secondary = np.asarray((255, 0, 235)) # violett

#xy, xz, yz are degrees between 0 - 2pi
def rotational_matrix(xy, xz, yz):#z y x
    #see https://de.wikipedia.org/wiki/Drehmatrix
    rz = np.eye(3)
    rz[0,0] = math.cos(xy)
    rz[1,1] = rz[0,0]
    rz[1,0] = math.sin(xy)
    rz[0,1] = -1 * rz[1,0]

    ry = np.eye(3)
    ry[0,0] = math.cos(xz)
    ry[2,2] = ry[0,0]
    ry[0,2] = math.sin(xz)
    ry[2,0] = -1 * ry[0,2]
    
    rx = np.eye(3)
    rx[1,1] = math.cos(yz)
    rx[2,2] = rx[1,1]
    rx[2,1] = math.sin(yz)
    rx[1,2] = -1 * rx[2,1]

    rot_mat = np.dot(rx,ry)
    rot_mat = np.dot(rot_mat, rz)
    
    return rot_mat

default_rot_mat = rotational_matrix(0, math.pi * 0.2, math.pi * 0.2)

def save_img(img, filename, dir="D:\Onedrive\OneDrive - rwth-aachen.de\Bilder\DigitalArt"):
    img = np.transpose(img, [1,0,2])
    cv2.imwrite(dir + "\\" + filename, img)

def show_img(img):
    img = img / 255
    img = np.transpose(img, [1,0,2])
    cv2.imshow("Lissajorus", img)
    cv2.waitKey()

def lcm(a, b):
    return abs(a*b) // math.gcd(a,b)

def lissajorus3d(a_rad, b_rad, c_rad, a_steps, b_steps, c_steps, rot_mat, dim, color=primary):
    img = np.zeros([dim,dim,3])
    
    wadd = dim / 2
    hadd = dim / 2
    
    #greatest common divisor
    steps = lcm(a_steps ,lcm(b_steps,c_steps))
    
    for i in range(0, steps):
        x = a_rad * math.sin(i * math.pi * 2 / a_steps)
        y = b_rad * math.cos(i * math.pi * 2 / b_steps)
        z = c_rad * math.cos(i * math.pi * 2 / c_steps)
        
        res = np.dot(rot_mat, np.asarray((x,y,z)))
        img[int(round(res[0]+wadd)),int(round(res[1]+hadd))] = color
    
    return img

def lissajorus_flock_3d(rot_mat, color=primary):
    img = np.zeros([850,850,3])
    
    dim = 100
    
    c_x = c_y = 0
    for c in range(1, 5):
        for a in range(1, 5):
            for b in range(1, 5):
                tmp = lissajorus3d(25,25,25,
                        100 * a, 100 * b, 100 * c,
                        rot_mat, dim, color)
                img[(a-1)*dim+c_x:a*dim+c_x, (b-1)*dim+c_y:b*dim+c_y] = tmp
        if(c % 2 == 1):
            c_x = int(dim * 4.5)
        else:
            c_x = 0
            c_y = int(dim * 4.5)
            
    return img
    
if __name__ == "__main__":
    imgs = []
    frames = 90
    #color transitions from violett to cyan
    for i in range(0, int(frames/2)):
        print(str(i) + " of " + str(frames))
        
        rot = rotational_matrix(0, i * math.pi * 2 / frames, i * math.pi * -2 / frames)
        
        imgs.append(lissajorus_flock_3d(rot, 
                color=np.asarray(((255/frames)*i*2,255-(255/frames)*i*2, 235))))

    #color transitions back to beginning
    for i in range(int(frames/2), frames):
        print(str(i) + " of " + str(frames))
        
        rot = rotational_matrix(0, i * math.pi * 2 / frames, i * math.pi * -2 / frames)
        
        imgs.append(lissajorus_flock_3d(rot, 
                color=np.asarray((255-(255/frames)*(i-frames/2)*2,(255/frames)*(i-frames/2)*2, 235))))

    imageio.mimsave("lissajorustest.gif", imgs, format="GIF", fps=30)