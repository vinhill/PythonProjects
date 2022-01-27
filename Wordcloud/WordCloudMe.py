from wordcloud import WordCloud
import matplotlib.pyplot as plt
from functools import reduce
from itertools import product, chain
import itertools
import numpy as np

A = "DL; Python; C++"
B = "JavaScript; Keras; ML; Angular; Biology"
C = "LaTeX; Java; Bioinformatics; SQL; Tensorflow; Node.js; Theory; AI; OpenCV"
D = "Teaching; Matplotlib; MSOffice; Numpy; Git; Computer Graphics; Computer Vision; cmake; Express; TypeScript; Software Architecture; Design Patterns"

"""
A = "ML Python"
B = "JavaScript Tensorflow Theory DL AI C++"
C = "LaTeX Networks Java Bioinformatics SQL Keras"
D = "Teaching Haskell Prolog Matplotlib MSOffice Rosalind Arduino Numpy Git Computer-Graphics"
"""

"""
A = "Calm Smart Rational Ambitious"
B = "Silent Reserved Gentle Direct Organized Tidy"
C = "Altruism Perfectionist Anxious Nihilist Catholic Clean Honest"
"""

A = A.split("; ")
B = B.split("; ")
C = C.split("; ")
D = D.split("; ")

freq = dict(chain(
    product(A, [50]),
    product(B, [45]),
    product(C, [40]),
    product(D, [35])
))

scale = 1

# circular drawing area
width, height = 400 * scale, 200 * scale
x, y = np.ogrid[:height, :width]
mask = (x - height/2) ** 2 + 0.25*(y - width/2) ** 2 > (height/2) ** 2
mask = 255 * mask.astype(int)

def make_wc(rs, ph):
    return WordCloud(
            max_font_size=50 * scale,
            min_font_size=9 * scale,
            max_words=100,
            background_color="rgb(231, 231, 231)",
            font_step = 1,
            relative_scaling = rs,
            prefer_horizontal = ph,
            color_func=lambda *args, **kwargs: (0,0,0),
            mask = mask
            ).generate_from_frequencies(freq)

def save_as_svg(wc, path):
    svg = wc.to_svg(embed_font=True)
    f = open(path, "w+")
    f.write(svg)
    f.close()

task = input("Gridsearch / iterate / show: ")

if task == "Gridsearch":
    for (rs, ph) in itertools.product([0.5,0.7,0.9,1], [0.5,0.7,0.9,1]):
        wc = make_wc(rs, ph).to_file("cvwcrs{0}ph{1}.png".format(rs,ph))
else:
    iterations = 1 if task == "show" else 5
    for i in range(0, iterations):
        wc = make_wc(0.3, 0.7)
        if task == "show":
            plt.figure()
            plt.imshow(wc, interpolation="bilinear")
            plt.axis("off")
            plt.show()
        elif task == "iterate":
            save_as_svg(wc, "cvwci{0}.svg".format(i))