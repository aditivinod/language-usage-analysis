from PIL import Image, ImageDraw, ImageFont
import numpy as np
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def word_cloud(frequency_dict):
    """
    Given a dictionary containing words and their frequencies, creates a word
    cloud image representing said dictionary.

    Args:
        frequency_dict: A dictionary containing keys that are strings, or words
            and values that are integers, or frequencies of the corresponding
            words.
    Returns:
        None
    """
    wc = WordCloud(background_color="white", width=1920, height=1080).generate_from_frequencies( \
        frequency_dict)
    plt.figure(figsize = (10,10))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis(False)
    plt.show()


def create_profile_image(name, gamer_or_not, gamer_z_score, normal_z_score, \
    gamer_all_freq, most_used):
    """
    Creates an 'id card' representing an individual users' gamer sub-internet
    analysis results. 

    Args:
        name: 
        gamer_or_not: A boolean representing whether the individual is a gamer or
            not. 
        gamer_z: A float representing the gamer z score of the individual.
        normal_z: A float representing the normal z score of the individual.
        gamer_all_freq: A float representing the ratio of gamer words to all words
            in an individual's messages.
        most_used: A list of strings containing the top five most used gamer words
            by an individual.
    Returns:
        None
    """
    imarray = np.random.rand(4,4,3) * 255
    pfp_img = Image.fromarray(imarray.astype('uint8')).convert('RGBA')
    pfp_img = pfp_img.resize((165, 165))
    
    # Text contents
    username = str(name)
    if gamer_or_not is True:
        gamer_status = "GAMER"
    else:
        gamer_status = "NOT A GAMER"
    gamer_z = "Gamer Z-Score - " + str(round((gamer_z_score), 4))
    normal_z = "Normal Z-Score - " + str(round((normal_z_score), 4))
    gamer_to_all = "Gamer:All Words Ratio - " + str(round(gamer_all_freq, 4))
    top_words = "Most common gamer words - \n"+', '.join([str(elem) for elem \
        in most_used])

    # Font settings
    username_font = ImageFont.truetype("Dosis-Bold.ttf", 16)
    is_gamer_font = ImageFont.truetype("Dosis-Bold.ttf", 40)
    frequency_font = ImageFont.truetype("Dosis-Bold.ttf", 14)
    common_words_font = ImageFont.truetype("Dosis-Bold.ttf", 14)

    # Create background image
    img = Image.new('RGB', (475, 200), color = (250, 250, 250))


    draw = ImageDraw.Draw(img)
    
    # Draw rectangles that mark out ID subsections
    draw.rectangle((0, 0, 180, 200), outline="grey", fill="grey")
    img.paste(pfp_img, (10, 10))    # Add in pfp
    draw.rectangle((175, 175, 10, 10), outline="black")
    draw.rectangle((185, 10, 470, 60), outline="black")
    draw.rectangle((185, 65, 470, 145), outline="black")
    draw.rectangle((190, 70, 465, 90), outline="black")
    draw.rectangle((190, 95, 465, 115), outline="black")
    draw.rectangle((190, 120, 465, 140), outline="black")
    draw.rectangle((185, 150, 470, 190), outline="black")

    # Add in ID text
    draw.text((10,175), username, font=username_font, fill=(0, 0, 0))
    draw.text((190, 10), gamer_status, font=is_gamer_font, fill=(255, 0, 0))
    draw.text((195, 70), gamer_z, font=frequency_font, fill=(0, 0, 0))
    draw.text((195, 95), normal_z, font=frequency_font, fill=(0, 0, 0))
    draw.text((195, 120), gamer_to_all, font=frequency_font, fill=(0, 0, 0))
    draw.text((190, 150), top_words, font=common_words_font, fill=(0, 0, 0))

    img.show()

def single_histogram(data_list, num_bins, x_label, plt_title):
    """
    Given a list of data, creates a single histogram representing the data.

    Args:
        data_list: A list of integers or floats representing the data to plot.
        num_bins: An integer representing the number of bins that the data 
            should be sorted into.
        x_label: A string representing the label on the x axis of the
            histogram.
        plt_title: A string representing the title of the histogram.
    """
    plt.hist(data_list, density=True, bins=num_bins)
    mn, mx = plt.xlim()
    plt.xlim(mn, mx)
    plt.ylabel("Frequency")
    plt.xlabel(x_label)
    plt.title(plt_title)

def stacked_histogram(data_list, num_bins, label_1, label_2, x_axis, plt_title):
    """
    Given a list containing two lists of data, creates a histogram with both
    datasets stacked on top of each other.

    Does not funtion for a list containing more than two lists of data.

    Args:
        data_list: A list of two lists containing integers or floats
            representing the data to plot.
        num_bins: An integer representing the number of bins that the data
            should be sorted into.
        label_1: A string representing the label in the legend for the first 
            list of data.
        label_2: A string representing the label in the legend for the second
            list of data.
        x_axis: A string representing the label on the x axis of the
            histogram.
        plt_title: A string representing the title of the histogram.
    """
    plt.hist(data_list[0], num_bins, alpha=0.33, label=label_1)
    plt.hist(data_list[1], num_bins, alpha=0.33, label=label_2)
    plt.legend(loc='upper right')
    plt.xlabel(x_axis)
    plt.ylabel("Frequency")
    plt.title(plt_title)
    plt.show()