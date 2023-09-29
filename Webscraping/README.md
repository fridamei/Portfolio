# Webscraping and regular expressions
I ran the code in Anaconda Spyder 5 with python 3.8, tested on VMWare Horizon remote from ifi workspace with python 3. Necessary packages: 


## Task 5.1

### Dependencies
requests

### Functionality
Takes an URL argument and returns a string containing the HTML code from the URL.
Optional to pass URL parameters as argument.
The output argument is a filename, and if supplied, the text string is saved with that name locally

### Usage
Run the file from either terminal or in an IDE. 

## Task 5.2
Functions to find urls and save them to file. find_articles filters out the wikipedia articles among the returned urls from 
find_urls. 
   
### Dependencies
requests <br>
(Uses get_html from requesting_urls for testing the functions (when running as main) and a copy of this file is added to the same directory as filter_urls
for simplicity of use) <br>

re (regex) <br>
### Functionality
For find_urls:
   Takes an HTML string and returns a list of all the found URLs in the string. 
   Adds a base URL if the found URL is either a semi absolute URL (missing https:) 
   or partial URL (missing http://somewebpage.com)
   Saves to file if output is supplied
   
For find_articles:
   Takes an HTML string and returns a list of wikipedia articles contained in the string. Uses the find_url function
   If output is supplied, the found URLs are saved to file. 
   Takes base_url as optional argument to be passed to find_urls
   The list from find_urls is written to file locally in that function, find_articles appends to this file.
  
   Checks whether the url starts with either /wiki ... or http(s)//:xx.wikipedia.org ..., and adds https//:wikipedia.org if 
   it lacks. 

### Usage
Run filter_urls.py as main from either terminal or IDE

## Missing functionality
For the find_articles: does not check if the url start with anything else than stated above, and 
will be missed if that is the case


## Task 5.3

### Dependencies
re (regex) <br>
datetime <br>
get_html from requesting_urls (supplied in directory) <br>

### Functionality
Finds dates in argument string and saves them to file if output argument is supplied.
Captured date formats:
   DD MM YYYY
   MM DD(,) YYYY (comma is optional)
   YYYY MM DD
   YYYY-MM-DD
   
   The spaces between the components are required for all except the last where the hyphens are required
   
The returned dates are formatted to YYYY/MM/DD and sorted in ascending order

The output file contains both the list of dates in its entirety (as the text stated) and the dates printed individually

(I used datetime for sorting the list as I could not see any requirements in regards to method for that specific subtask)

### Usage
Run file as main from directory collect_dates_regex. The necessary file, requesting_urls, is copied to the folder 

## Missing functionality
For year 0-1000, leading zeros are necessary to  be captured (eg 0001)
Captures up to year 2999 (probably also too extensive, dates later than current year are almost never denoted as full dates)
Does not capture any other date formats than those specified above. 

## Task 5.4

### Dependencies
BeautifulSoup <br>
get_html from requesting_urls

### Functionality
Finds the calendar table of a Wikipedia page for a FIS Alpine Ski World Cup (I used https://en.wikipedia.org/wiki/2021%E2%80%9322_FIS_Alpine_Ski_World_Cup)
and returns a list of tuples with the event number, venue and discipline. 
For the implementation of cancelled events: I used the 2021-2022 page where there are no cancelled events, but as far as 
I can see on the 2020-2021 page, the cancellations are handled by 1. A large majority of them do not have rows within the specified number (between full_row_lenght and short_row_length)
and 2. The event number is removed, setting found_event to None and thereby by not triggering the last if which leads to the append

Creates a new directory, unless it already exists, called datetime_filter_results, whereas the file itself is located in datetime_filter

### Usage
Run file as main.

## Missing functionality
Is specifically designed for the 2021-2022 page, cannot guarantee compatibility with other pages
(though it seems to work with the 2020-2021 version as well)


## Task 5.5

### Dependencies
get html from requesting_urls (supplied in directory) <br>
(find_articles from filter_urls if the alternative way of extracting the urls is used, per now commented out) <br>
BeautifulSoup <br>
re <br>
matplotlib.pyplot as plt <br>
random <br>

### Functionality
extract_teams() takes an url of the 2021 NBA playoffs (https://en.wikipedia.org/wiki/2021_NBA_playoffs) and extracts 
the names and urls (2020-21 season for the team) of all the teams that entered the seminfinals (or further).
extract_players() takes an url of the 2020-2021 season for a team and extracts all the players and the url to their wikipedia page in their rosters for that year
and 
extract_player_statistics() takes a player url and extracts the stats of that player for the NBA 2021-21 season
(The supplied try/excepts showed sufficient to catch any combination the extracted players had of headers and tables in the html code)
Returns the point per game (ppg), blocks per game (bpg) and rebounds per game (rpg) for the player. 
plot_NBA_player_statistics() takes a team dictionary containing team names as keys and lists of player dictionaries as values. 
Extracts the stats and plots them. 
make_team_dictionary() builds the dictionary to send as argument to plot_NBA_player_statistics by using the other functions.
Sorts out the three best players for every team (based on ppg) and removes the rest from the dictionary


### Usage
Run as main from terminal or IDE

## Missing functionality
Only works for the 2020-21 season. 



## Task 5.6

### Dependencies
BeautifulSoup if using the find_urls function
Requests 
find_articles from filter_urls
get_html from requesting_urls


### Functionality
Finds the shortest path from one link to another following the found links on each page, using breadth first search

### Usage
Run as main

## Missing functionality
The found url has to match the goal url exactly, so if there are any discrepancies in writing, the path will not be found
Tried using the main title of each of the wikipedia pages, but the parsing of every link took way too long.
