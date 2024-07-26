from PIL import Image, ImageDraw
import math

def nextXY(x0,y0,len,deg):
    deg = (deg % 360) * (math.pi/180)
    xshift = math.cos(deg)*len
    yshift = math.sin(deg)*len
    return (x0+xshift, y0+yshift)
    
def draw(lines, xmin, ymin, xmax, ymax,thickness=1,scale=1,supersampling=1):
    if supersampling > 1:
        scale *= supersampling
    xmin *= scale
    ymin *= scale
    xmax *= scale
    ymax *= scale
    lines = map(lambda x: map(lambda y: y*scale, x), lines)
    img = Image.new('RGBA', (xmax-xmin, ymax-ymin), color="white")
    p = ImageDraw.Draw(img)
    for (a,b,c,d) in lines:
        p.line(
            (a-xmin, b-ymin,c-xmin,d-ymin),
            fill=128,
            width=thickness)
    del p
    img = img.rotate(90,expand=True)
    if(supersampling>1):
        img = img.resize( (int(img.size[0]/supersampling), int(img.size[1]/supersampling)), resample = Image.BICUBIC)
    img.show()
    return img

def generateStructure(rule, iterations, start="F"):
    for i in range(1,iterations):
        start = start.replace("F", rule)
    return start

"""
Different replacement pattern:
F[+FF][--F]F n=6 l=10 r=17 for FoSAP Slide 13
F[+F]F[-F]F n=6 l=5 r=25 for FoSAP Slide 15
F[+F]F[-F][F] n=7 l=5 r=20 for FoSAP Slide 16
FF-[-F+F+F]+[+F-F-F] n=5 l=10 r=22 for FoSAP Slide 17
f[-*F]f[-*F][+*F] n=7 l=200 r=22 lf = 0.5 for FoSAP Slide 18 Left
f[+*F][-*F]f[*F] n=7 l=200 r=22 lf = 0.5 for FoSAP Slide 18 Mid
ff[**+F**+F]ff[**-F**-F]ff[*F] n=8 l=20 r=40 lf=0.83 for tree-like

The structure starts with "F" and then F is replaced by rule n times.
rot_step defines how much a line is rotated for a +/- in rule
l_factor defines how much the linelength is decreased for a *
l is the initial length
if save the images is saved to Images\DigitalArt\text.png
thickness is the linewidth in pixels
scale is also regarding the finished image
supersampling will generate the image on a higher resolution, then downsample
supersampling results in smoother edges
"""
def Tree(rule="FF-[-F+F+F]+[+F-F-F]", n=6, rot_step=22, l_factor=0.5, l=10, save=False, thickness=1, scale=1, supersampling=1):    
    x = 0
    y = 0
    deg = 0
    xmax = 0
    ymax = 0
    xmin = 0
    ymin = 0
    
    order = generateStructure(rule,n)

    lines = list()#list of lines where one given as (x1,y1,x2,y2)

    states = list()
    for c in order:
        if c=="F" or c=="f":
            if(l<1):
                continue
            a,b = nextXY(x,y,l,deg)
            a = int(round(a))
            b = int(round(b))
            xmin = min(x,xmin)
            xmax = max(x,xmax)
            ymin = min(y,ymin)
            ymax = max(y,ymax)
            lines.append((x,y,a,b))
            x=a
            y=b
        elif c=="-":
            deg -= rot_step
        elif c=="+":
            deg += rot_step
        elif c=="*":
            l *= l_factor
        elif c=="[":
            states.append((x,y,deg,l))
        elif c=="]":
            x,y,deg,l = states.pop()

    img = draw(lines,xmin,ymin,xmax,ymax,thickness,scale,supersampling)
    if(save):
        img.save("D:\Onedrive\OneDrive - rwth-aachen.de\Bilder\DigitalArt\\test.png")
    return img