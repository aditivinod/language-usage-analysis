
gamer-detector aims to create a list of most commonly used words in specific internet sub-communities, in this implementation’s case - gamers, and then identify whether individual users are part of that sub-community.

## Installation
The following libraries were utilized in python 3.9..7 in the Conda environment:
PRAW Reddit API - ``$ pip install praw``
Discord API - ``$ pip install -U discord.py``
WordCloud - ``$ pip install wordcloud``
Numpy - ``$ pip install numpy``
MatPlotLib - ``$ pip install matplotlib``

## Usage

Cloning from this repository to mess around with values is welcome. Changes that will be necessary to make to the code run are mostly folder paths that are given to the function in the computational essay, which calls all of the functions. 

In order to successfully run the code, a path for the folder containing all the CSVs with individual user data needs to be given to the functions present in gamer_words.py. While none of these functions have a hard coded path in them at any point in time, to switch from the already provided anonymous_user dataset to another data set, the function calls within the computational essay would have to be changed.

Within ``visualize_data.py``, the ID card generation automatically makes the text on the ID cards refer to a “Gamer Z-Score,” even though this project could easily be applicable to other sub-communities on the internet, so that string would have to be changed to make the final ID card output accurate. There additionally is a section within the same function that serves as the primary identifier on the ID card, “GAMER,” and “NOT GAMER,” that would also have to be changed if this project was being applied to non-gamer data. 

### Data Collection
In order to obtain similar data to that found in ``gaming.csv`` and ``normal.csv``, the ``scrape_subreddits`` function must be run with an input of a list of strings representing the subreddits to collect data form. For example, the input to create the gaming frequency dictionary was ``[“gaming”, “games”, “leagueoflegends”, “pokemon”, “minecraft”]``. The output of this function must then be put into the ``dict_to_csv`` function along with the desired name for the CSV file. 

To obtain user message data from Discord, the ``discord_message_collector.py`` file can be run from a local host when given the token for a bot initialized through the Discord Developer Portal website. Alternatively, this [invite](https://discord.com/api/oauth2/authorize?client_id=957422654070091826&permissions=1377007164528&scope=bot) link is functional for adding the collection bot to servers; however, once again, the collection is locally hosted so the former method is more effective. The file location within the ``collect`` function should be modified to be a sub-folder of the repository clone.

### Data Processing
Once the data has been collected into CSV form, it can be turned back into frequency dictionaries via ``csv_to_dictionary``. Running the ``parse_words`` function from ``gamer_words.py`` will then complete all the steps necessary to create the gamer (or other sub-community-specific) words list. 

In order to classify individuals as part of an internet sub-community or not, the ``analyze_users_language`` function turns the user CSV data into processable numbers. ``stats_and_z_info`` then converts the values from the previous function into z-scores, which are then used in ``is_gamer`` to determine whether a given user is part of the sub-community in question.

### Data Visualization
All of the visuals generated require outputs from the gamer_words.py file to be used as parameters for functions in the ``visualize_data.py file``. 
Word cloud: To make a word cloud, the output of ``determine_gamer_words_frequency`` must be fed into the ``wordcloud`` function from ``visualize_data.py``.
Histograms: To make a stacked histogram, the ``z_list`` returned by ``stats_and_z_info``, the number of bins to give the histogram, and various plot labels must be given to the ``stacked_histogram`` function from ``visualize_data.py``; to make a single histogram, the chosen statistic returned by ``analyze_users_language``, the number of bins to give the histogram, and various plot labels must be given to the single_histogram function from ``visualize_data.py``.
ID Cards: To make an ID card, each element from the output of ``generate_user_id_dict`` for a single user must be given to ``create_profile_imate from visualize_data.py``

