"""
Contains the code used to visualize data as histograms, word clouds, and
individual user "ID Cards".
"""
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
    cloud = WordCloud(background_color="white", width=1920, \
        height=1080).generate_from_frequencies(frequency_dict)
    plt.figure(figsize=(10, 10))
    plt.imshow(cloud, interpolation='bilinear')
    plt.axis(False)
    plt.show()


def create_profile_image(user_id_list, save_path):
    """
    Creates an 'id card' representing an individual users' gamer sub-internet
    analysis results.

    Args:
        user_id_list: A list of the values needed to create the ID card for an
            individual user.
        save_path: A string representing a path to save the ID card images to.
    Returns:
        None
    """
    imarray = np.random.rand(4, 4, 3) * 255
    pfp_img = Image.fromarray(imarray.astype("uint8")).convert("RGBA")
    pfp_img = pfp_img.resize((165, 165))

    # Text contents
    username = str(user_id_list[0])
    if user_id_list[1] is True:
        gamer_status = "GAMER"
    else:
        gamer_status = "NOT A GAMER"
    gamer_z = "Gamer Z-Score - " + str(round((user_id_list[2]), 4))
    normal_z = "Normal Z-Score - " + str(round((user_id_list[3]), 4))
    gamer_to_all = "Gamer:All Words Ratio - " + str(round(user_id_list[4], 4))
    top_words = "Most common gamer words - \n"+", ".join([str(elem) for elem
                                                          in user_id_list[5]])

    # Font settings
    fonts = [ImageFont.truetype("Dosis-Bold.ttf", 16), \
        ImageFont.truetype("Dosis-Bold.ttf", 40), \
        ImageFont.truetype("Dosis-Bold.ttf", 14)]

    # Create background image
    img = Image.new('RGB', (475, 200), color=(250, 250, 250))

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
    draw.text((10, 175), username, font=fonts[0], fill=(0, 0, 0))
    draw.text((190, 10), gamer_status, font=fonts[1], fill=(255, 0, 0))
    draw.text((195, 70), gamer_z, font=fonts[2], fill=(0, 0, 0))
    draw.text((195, 95), normal_z, font=fonts[2], fill=(0, 0, 0))
    draw.text((195, 120), gamer_to_all, font=fonts[2], fill=(0, 0, 0))
    draw.text((190, 150), top_words, font=fonts[2], fill=(0, 0, 0))

    img.save(f"{save_path}/{username}.png")


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
    min_x, max_x = plt.xlim()
    plt.xlim(min_x, max_x)
    plt.ylabel("Frequency")
    plt.xlabel(x_label)
    plt.title(plt_title)


def stacked_histogram(data_list, num_bins, labels):
    """
    Given a list containing two lists of data, creates a histogram with both
    datasets stacked on top of each other.

    Does not funtion for a list containing more than two lists of data.

    Args:
        data_list: A list of two lists containing integers or floats
            representing the data to plot.
        num_bins: An integer representing the number of bins that the data
            should be sorted into.
        labels: A list containing strings necessary to label the histogram
            properly.
    """
    plt.hist(data_list[0], num_bins, alpha=0.33, label=labels[0])
    plt.hist(data_list[1], num_bins, alpha=0.33, label=labels[1])
    plt.legend(loc='upper right')
    plt.xlabel(labels[2])
    plt.ylabel("Frequency")
    plt.title(labels[3])
    plt.show()
