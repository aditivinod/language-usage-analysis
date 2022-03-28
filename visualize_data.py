from PIL import Image, ImageDraw, ImageFont
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

def create_profile_image(name, has_bitches, gamer_freq, normal_freq, most_used):
    # Text contents
    username = str(name)
    bitches = str(has_bitches)
    gamer_frequency = str(gamer_freq)
    normal_frequency = str(normal_freq)
    top_words = "Most common words: "+', '.join([str(elem) for elem in most_used])

    # Font settings
    username_font = ImageFont.truetype("Dosis-Bold.ttf", 16)
    is_gamer_font = ImageFont.truetype("Dosis-Bold.ttf", 40)
    frequency_font = ImageFont.truetype("Dosis-Bold.ttf", 14)
    common_words_font = frequency_font

    # Create background image
    img = Image.new('RGB', (450, 200), color = (250, 250, 250))
    
    draw = ImageDraw.Draw(img)
    
    # Draw rectangles that mark out ID subsections
    draw.rectangle((0, 0, 180, 200), outline="grey", fill="grey")
    draw.rectangle((175, 175, 10, 10), outline="black")
    draw.rectangle((185, 10, 440, 60), outline="black")
    draw.rectangle((185, 65, 440, 120), outline="black")
    draw.rectangle((190, 70, 435, 90), outline="black")
    draw.rectangle((190, 95, 435, 115), outline="black")
    draw.rectangle((185, 125, 440, 190), outline="black")

    # Add in ID text
    draw.text((10,175), username, font=username_font, fill=(0, 0, 0))
    draw.text((190, 10), bitches, font=is_gamer_font, fill=(255, 0, 0))
    draw.text((195, 70), gamer_frequency, font=frequency_font, fill=(0, 0, 0))
    draw.text((195, 95), normal_frequency, font=frequency_font, fill=(0, 0, 0))
    draw.text((190, 125), top_words, font=common_words_font, fill=(0, 0, 0))

    img.show()
