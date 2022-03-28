#from PIL import Image
#import numpy as np
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def got_bitches(result):
    print("You have no bitches")

def word_cloud(frequency_dict):
    wc = WordCloud(background_color="white").generate_from_frequencies(frequency_dict)
    plt.figure(figsize = (10,10))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis(False)
    plt.show()