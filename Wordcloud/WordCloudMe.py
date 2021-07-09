from wordcloud import WordCloud
import matplotlib.pyplot as plt
from functools import reduce
import itertools
import numpy as np

A = "ML Python"
B = "JavaScript Tensorflow Theory DL AI C++"
C = "LaTeX Networks Java Bioinformatics SQL Keras"
D = "Teaching Haskell Prolog Matplotlib MSOffice Rosalind Arduino Numpy Git Computer-Graphics"

"""
A = "Calm Smart Rational Ambitious"
B = "Silent Reserved Gentle Direct Organized Tidy"
C = "Altruism Perfectionist Anxious Nihilist Catholic Clean Honest"
"""

txt = reduce(lambda x,y: x + " " + y, [A,A,A,A,B,B,B,C,C,D])

generate = True

x, y = np.ogrid[:200, :400]
mask = (x - 100) ** 2 + 0.25*(y - 200) ** 2 > 100 ** 2
mask = 255 * mask.astype(int)

if(generate):

    for (fs, rs, ph, i) in itertools.product([1,2,3,4], [0.5,0.7,0.9,1], [0.5,0.7,0.9,1], range(1,2)):
        wc = WordCloud(
            max_font_size=50,
            max_words=100,
            background_color="rgb(231, 231, 231)",
            font_step = fs,
            relative_scaling = rs,
            prefer_horizontal = ph,
            color_func=lambda *args, **kwargs: (0,0,0),
            mask = mask
            ).generate(txt).to_file("cvwcfs{0}rs{1}ph{2}i{3}.png".format(fs,rs,ph,i))

else:
    wc = WordCloud(
            max_font_size=50,
            max_words=100,
            background_color="rgb(231, 231, 231)",
            font_step = 3,
            relative_scaling=1,
            prefer_horizontal = 1,
            color_func=lambda *args, **kwargs: (0,0,0),
            mask = mask
            ).generate(txt)
    plt.figure()
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.show()