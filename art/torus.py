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

#rotation in R^n is described through one plane that stays constant during rotation
#so in 3D, we use plane xy instead of axis z
#numpy vectors g1, g2 are orthogonal to each other with g1*g2=0 and |g1|=|g2|=1
def n_rotational_matrix(g1, g2, dimensions, radians):
    V = np.tensordot(g1,g1,axes=0)+np.tensordot(g2,g2,axes=0)
    W = np.tensordot(g1,g2,axes=0)-np.tensordot(g2,g1,axes=0)
    r = np.eye(dimensions) \
            + (math.cos(radians) - 1) * V \
            + math.sin(radians) * W
    return r

default_rot_mat = rotational_matrix(0, math.pi * 0.2, math.pi * 0.2)

#R is the torus radius
#r is the torus thickness
def torus_image(R, r, rot_mat=default_rot_mat, color=primary, Rsteps=500, rsteps=50, scalar=1, margin=0):
    # cv2 maps [0-1] into [0-255] (>1 is mapped to 255)
    dim = (R+r)*2+1+margin
    img = np.zeros([dim,dim,3])
    #Torus formula
    #[x] (R + r * Math.cos(p)) * Math.cos(t)
    #[y] (R + r * Math.cos(p)) * Math.sin(t)
    #[z] r * Math.sin(p)
    Rstepsize = 2 * math.pi / Rsteps
    rstepsize = 2 * math.pi / rsteps

    wadd = dim / 2
    hadd = dim / 2

    for t in range(0, Rsteps):
        for p in range(0, rsteps):
            x = (R + r * math.cos(p * rstepsize)) * math.cos(t * Rstepsize)
            y = (R + r * math.cos(p * rstepsize)) * math.sin(t * Rstepsize)
            z = r * math.sin(p * rstepsize)
            res = np.dot(rot_mat, np.asarray((x,y,z)))
            img[int(round(res[0]+wadd)),int(round(res[1]+hadd))] = color

    img = img / 255.0
    img = np.transpose(img, [1,0,2])
    img = cv2.resize(img, (int(round(img.shape[0] * scalar)), int(round(img.shape[1] * scalar))))
    return img

#t is R coordinate
#p is r coordinate
#Rather than painting the torus as several slices we now paint a path over the whole torus
def path_over_torus_image(R, r, a, b, width, height, rot_mat=default_rot_mat, color=primary, steps=10000, scalar=1):
    # cv2 maps [0-1] into [0-255] (>1 is mapped to 255)
    img = np.zeros([width,height,3])
    #used in previous project
    #[x] (R + r * Math.cos(a * t)) * Math.cos(b * t)
    #[y] (R + r * Math.cos(a * t)) * Math.sin(b * t)
    #[z] r * Math.sin(a * t)

    wadd = width / 2
    hadd = height / 2

    for t in range(1, steps):
        x = (R + r * math.cos(a * t)) * math.cos(b * t)
        y = (R + r * math.cos(a * t)) * math.sin(b * t)
        z = r * math.sin(a * t)
        res = np.dot(rot_mat, np.asarray((x,y,z)))
        img[int(round(res[0]+wadd)),int(round(res[1]+hadd))] = color


    img = img / 255.0
    img = np.transpose(img, [1,0,2])
    img = cv2.resize(img, (int(round(img.shape[0] * scalar)), int(round(img.shape[1] * scalar))))
    return img

#a is changed with y, b is changed with x coordinate in resulting image
def flock_of_strange_toruses(R=40, r=30, astart=1, bstart=1, amax=10, bmax=16, astep=3, bstep=3, dist=10, rot_mat=default_rot_mat, color=primary, steps=10000):
    dim = int(round((R+r)*2.1))
    
    acount = math.floor((amax-astart) / astep) + 1
    bcount = math.floor((bmax-bstart) / bstep) + 1
    
    img = np.ones([acount*dim+(acount-1)*dist, bcount*dim+(bcount-1)*dist, 3])
    for a in range(astart,amax+1,astep):
        for b in range(bstart,bmax+1,bstep):
            tmp = path_over_torus_image(R,r,a,b,dim,dim,rot_mat,color,steps)
            #draw tmp to img
            x_offset = (dim+dist)*int(a/astep)#1 4 7 10 13 ... to 0 1 2 3 4 5 ...
            y_offset = (dim+dist)*int(b/bstep)
            img[x_offset:x_offset+tmp.shape[0], y_offset:y_offset+tmp.shape[1]] = tmp
    
    return img
    
def save_img(img, filename, dir="D:\Onedrive\OneDrive - rwth-aachen.de\Bilder\DigitalArt"):
    img = img * 255
    cv2.imwrite(dir + "\\" + filename, img)

def show_img(img):
    cv2.imshow("Torus", img)
    cv2.waitKey()

#conversion to gif:
#imageio.mimsave(filename without special caracters, images, format="GIF", fps=30)

#code for my torusflock.gif with nice colors and rotations
if __name__ == '__main__':
    imgs = []
    frames = 150
    #color transitions from violett to cyan
    for i in range(0, int(frames/2)):
        print(str(i) + " of " + str(frames))
        #I found this rotation to be quite asthetically pleasing
        rot = rotational_matrix(0, i * math.pi * 2 / frames, i * math.pi * -2 / frames)
        
        imgs.append(flock_of_strange_toruses(rot_mat=rot, steps=1000, dist=0, bmax=10,
                color=np.asarray(((255/frames)*i*2,255-(255/frames)*i*2, 235))))
        #imgs.append(path_over_torus_image(40,30,1,1,150,150,rot_mat=rot))
        #imgs.append(torus_image(100,60,rot,Rsteps=50,rsteps=30,
        #        color=np.asarray(((255/frames)*i*2,255-(255/frames)*i*2, 235))))

    #color transitions back to beginning
    for i in range(int(frames/2), frames):
        print(str(i) + " of " + str(frames))
        #I found this rotation to be quite asthetically pleasing
        rot = rotational_matrix(0, i * math.pi * 2 / frames, i * math.pi * -2 / frames)
        
        imgs.append(flock_of_strange_toruses(rot_mat=rot, steps=1000, dist=0, bmax=10,
                color=np.asarray((255-(255/frames)*(i-frames/2)*2,(255/frames)*(i-frames/2)*2, 235))))
        #imgs.append(path_over_torus_image(40,30,1,1,150,150,rot_mat=rot))
        #imgs.append(torus_image(100,60,rot,Rsteps=50,rsteps=30,
        #        color=np.asarray((255-(255/frames)*(i-frames/2)*2,(255/frames)*(i-frames/2)*2, 235))))

    imageio.mimsave("torusflock.gif", imgs, format="GIF", fps=30)