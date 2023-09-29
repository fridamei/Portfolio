from requesting_urls import get_html
from filter_urls import find_articles
from bs4 import BeautifulSoup
import re 
from IPython import embed
import matplotlib.pyplot as plt
import random

def extract_teams(url):
    """ 
    Extract team names and urls from the NBA Playoff 'Bracket' section table.
    
    Args
        url (string): url of wikipedia page to find urls and team names in (specifically designed for the 2020-21 NBA Playoff page)
    Returns :
        team_names (list): A list of team names that made it to the conference semifinals.
        team_urls (list): A list of absolute Wikipedia urls corresponding to team_names.

    """

    # get the html string
    html = get_html(url)
    
    # make soup
    soup = BeautifulSoup(html, "html.parser")
    
    # Find the tag that contains the Calendar heading span
    bracket_header = soup.find(id="Bracket")
    
    # Find the following table
    bracket_table = bracket_header.find_all_next("table")[0]
    
    # Find the rows
    rows = bracket_table.find_all("tr")
    
    # Create list of teams
    team_list = []

    # For every row in list of all rows
    for i in range(1, len(rows)):
        # Store all the cells (/columns) of the row in a list
        cells = rows[i].find_all("td")
        
        # Make list with the cell text stripped of html syntax and newlines
        cells_text = [cell.get_text(strip=True) for cell in cells]
        
        # Filter out the empty cells
        cells_text = [cell for cell in cells_text if cell]

        # Find the rows that contain seeding, team name and games won
        if len(cells_text) > 1:
            # Regex to find the team name in the cell. Must contain letters with any capitalization followed by optional whitespace (to include New York and LA Clippers)
            team_regex = r"\b[A-Za-z]+\s?[A-Za-z]+\*?"
            team = re.findall(team_regex, ' '.join(cells_text))[0]
            
            # Seedings start with E or W, then a number (the seeding can be higher than 9)
            seeding_regex = r"\b[E|W]\d\d?\b"
            seed = re.findall(seeding_regex, ' '.join(cells_text))[0]
            
            # Single digit
            won_regex = r"\b\d\b"
            won = re.findall(won_regex, ' '.join(cells_text))[0]
            
            # If the found info is in the correct indices:
            if seed == cells_text[0] and team == cells_text[1] and won == cells_text[2]:
                team_url = str(cells[2].find_next("a").attrs["href"])
                team_url = "https://en.wikipedia.org" + team_url if 'http' not in team_url else team_url
                
                """
                # If the index of the url is not known/varies
                # Find the url of the team
                for cell in cells:
                    url = cell.find_all('a', href=True)

                    # If an url is found:
                    if len(url) != 0:
                        # Use the find_articles to extract the wikipedia link. This also checks if the links is complete or not and adds the wikipedia.org/ if it is not
                        team_url = find_articles(str(url))[0]

                """
                
                # Append the team and the url as a tuple for easier management when filtering out non-semifinalists later
                # Strip the team names of the asterisk if present
                team_list.append((team.strip('*'), team_url))

    # Fill team_list_filtered with every team that appears more than once. Will contain duplicates, which are removed with set()
    team_list_filtered = list(set([team for team in team_list if team_list.count(team) > 1]))
    
    # Extract name and url from the tuples
    team_names = [x[0] for x in team_list_filtered]
    team_urls = [x[1] for x in team_list_filtered]

    return team_names, team_urls


def extract_players (team_url):
    """
    Extract players that played for a specific team in the NBA playoffs.

    Args:
        team_url (str): URL to the Wikipedia article of the season of a given team.
    
    Returns:
        player_names (list): A list of players names corresponding to the team whos URL was passed semifinals .
        player_urls (list): A list of Wikipedia URLs corresponding to player_names of the team whos URL was passed .
    
    """
    
    # Keep base url
    base_url = "https://en.wikipedia.org"
    
    # get html for each page using the team url you extracted before
    html = get_html(team_url)

    # make soup
    soup = BeautifulSoup (html , "html.parser")
    
    # get the header of the Roster
    roster_header = soup.find (id="Roster")
    
    # identify table
    roster_table = roster_header.find_next("table")
    rows = roster_table.find_all("tr")

    # prepare lists for player names and urls
    player_names = []
    player_urls = []
    
    for i in range (0, len (rows)):
        cells = rows[i].find_all("td")
        cells_text = [cell.get_text(strip=True) for cell in cells]
        if len(cells_text) == 7:
            rel_url = cells[2].find_next("a").attrs["href"]
            name = cells[2].find_next("a").attrs["title"]
            
            # Regex to match every character until '(' or new_line (not strictly necessary as only one name is returned at a time))
            regex = r"^[^\(\n]+"
            # Strip name of trailing whitespaces
            name = re.findall(regex, name)[0].strip()
            
            # Add name to list
            player_names.append(name)
            
            # Add url to list
            url = base_url + rel_url if 'http' not in rel_url else rel_url
            player_urls.append(url)
            
    return player_names, player_urls


def extract_player_statistics(player_url):
    """ 
    Extract player statistics for NBA player .
    # Note : Make yourself familiar with the 2020 -2021 player statistics wikipedia page and adapt the code accordingly .
    Args :
        player_url (str): URL to the Wikipedia article of a player
        
    Returns :
        ppg (float): Points per Game .
        bpg (float): Blocks per Game .
        rpg (float): Rebounds per Game .
    
    """
    # As some players have incomplete statistic/information, you can set a default score , if you want .

    ppg = 0.0
    bpg = 0.0
    rpg = 0.0
    
    # get html
    html = get_html(player_url)
    
    # make soup
    soup = BeautifulSoup(html, "html.parser")

    # find header of NBA career statistics
    nba_header = soup.find(id="NBA_career_statistics")
    
    # check for alternative name of header
    if nba_header is None:
        nba_header = soup.find(id="NBA")

    try:
        # find regular season header
        # You might want to check for different spellings , e.g. capitalization
        # You also want to take into account the different orders of header and table
        
        regular_season_header = nba_header.find_next(id="Regular_season")
        # next we should identify the table
        nba_table = regular_season_header.find_next("table")
    
    except:
        try:
            # table might be right after NBA career statistics header
            nba_table = nba_header.find_next("table")
        except:
            """
            The supplied combinations seems to cover every combination. Tried printing every url where a table was not found, and all the results where due to a lack of table in the first place
            """
            # Return ppg, bpg and rpg without updating if no table is found
            return ppg, bpg, rpg
    
    # Find nba table header and extract rows
    table_header = nba_table.find_all("th")
    
    # Find the text for easier matching
    table_header_text = [header.get_text(strip=True) for header in table_header]
    
    # Find indicis of information to extract
    ppg_index = table_header_text.index('PPG')
    bpg_index = table_header_text.index('BPG')
    rpg_index = table_header_text.index('RPG')

    # Find every row of the table
    rows = nba_table.find_all("tr")
    
    # For every row, look for the 2020-21 season and extract ppg, bgp and rgp using the found indices
    for row in rows:
        # Find the individual cells of the row
        cells = row.find_all('td')
        if len(cells) > 1:
            cells_text = [cell.get_text(strip=True) for cell in cells]
            # Year should be stored at index 0. Strip † if any (denotes whether the player played for the winning team that season)
            year = cells_text[0].strip('†')
            if year == '2020–21':
                # Some players had a trailing asterisk after the score
                ppg = cells_text[ppg_index].strip('*')
                bpg = cells_text[bpg_index].strip('*')
                rpg = cells_text[rpg_index].strip('*')

    scores = [ppg, bpg, rpg]

    # Convert the scores extracted to floats
    # Note : In some cases the scores are not defined but only shown as '-'. In such cases you can just set the score to zero or not defined .
    for i in range(len(scores)):
        try:
            scores[i] = float(scores[i])
        
        # If the value cannot be converted to float:
        except ValueError:
            scores[i] = 0.0
    
    ppg = scores[0]
    bpg = scores[1]
    rpg = scores[2]
    
    return ppg,bpg, rpg
 
def plot_NBA_player_statistics(teams):
    """
    Takes a dictionary where the keys are the team names and the values are lists containing dictionaries with player stats
    Prints the stats as 3 bar plots, one for each of ppg, rpg and bpg
    Args
        teams (dictionary): Dictionary of lists of dictionaries containing the player stats
    """
    color_table = {}
    for team in teams:
        color = (random.random(), random.random(), random.random())
        while color in color_table.values():
            color = (random.random(), random.random(), random.random())
        color_table[team] = color
    
    count_so_far = 0
    all_names = []

    # iterate through each team and the
    for team, players in teams.items():
        # pick the color for the team , from the table above
       color = color_table[team]
       
       # collect the ppg and name of each player on the team
       # you 'll want to repeat with other stats as well
       ppg = []
       bpg = []
       rpg = []
       names = []
       
       for player in players:
           # Collect all stats
           names.append(player["name"])
           ppg.append(player["ppg"])
           bpg.append(player["bpg"])
           rpg.append(player["rpg"])
           
       # record all the names , for use later in x label
       all_names.extend(names)
           
       # the position of bars is shifted by the number of players so far
       x = range(count_so_far, count_so_far + len(players))
       count_so_far += len(players)
       
       # make bars for this team 's players ppg, bpg and rpg in separate figures
       # with the team name as the label
       plt.figure(1)
       bars_ppg = plt.bar(x, ppg, color=color, label=team)
       # Rotate to avoid overlap. Padding for space between end of bar and value label
       plt.bar_label(bars_ppg, rotation=90, padding=5)

       plt.figure(2)
       bars_bpg = plt.bar(x, bpg, color=color, label=team)
       plt.bar_label(bars_bpg, rotation=90, padding=5)

       plt.figure(3)
       bars_rpg = plt.bar(x, rpg, color=color, label=team)
       plt.bar_label(bars_rpg, rotation=90, padding=5)

    # Save ppg plot
    plt.figure(1)
    # use the names , rotated 90 degrees as the labels for the bars
    plt.xticks(range(len(all_names)), all_names, rotation=90)
    plt.legend(loc=0)
    plt.grid (False)
    plt.title("Points per game")
    # Set y-axis range to go above the max ppg to make space for legend without overlap
    plt.ylim(0, 45)
    plt.legend(loc='upper center', ncol=4)
    # tight_layout() to avoid the text being cut off
    plt.tight_layout()
    plt.savefig ("players_over_ppg.png")

    # Save bpg plot
    plt.figure(2)
    plt.xticks(range(len(all_names)), all_names, rotation=90)
    plt.legend(loc=0)
    plt.grid (False)
    plt.title("Blocks per game")
    plt.ylim(0, 3)
    plt.legend(loc='upper center', ncol=4)
    plt.tight_layout()
    plt.savefig ("players_over_bpg.png")

    # Save rpg plot
    plt.figure(3)
    plt.xticks(range(len(all_names)), all_names, rotation=90)
    plt.legend(loc=0)
    plt.grid (False)
    plt.title("Rebounds per game")
    plt.ylim(0, 20)
    plt.legend(loc='upper center', ncol=4)
    plt.tight_layout()
    plt.savefig ("players_over_rpg.png")


def make_team_dictionary(url):
    """
    Generates the team dictionary to use as argument in plot_NBA_player_statistics() to generate plots
    
    Return
        team_dict (dictionary): dictionary of lists containing dictionaries
    """
    # Returns the name and url of all the teams moving on to the semifinals
    team_names, team_urls = extract_teams(url)
    
    # Empy dictionary to fill with team names as keys and list of player dictionaries as values
    team_dict = {}
    
    # Traverse the teams found in the wikipedia url
    for i in range(len(team_urls)):
        # Extract the player names and urls
        player_names, player_urls = extract_players(team_urls[i])
        
        # Each team key should contain a list of player dictionaries. Make the for appending the dictionaries later
        team_dict[team_names[i]] = []
        
        #Traverse the player urls to gather the individual player statistics
        for j in range(len(player_urls)):
            ppg, bpg, rpg = extract_player_statistics(player_urls[j])
            
            # Make a dictionary for every player containing their stats
            player_dict = {}
            player_dict['name'] = player_names[j]
            player_dict['ppg'] = ppg
            player_dict['bpg'] = bpg
            player_dict['rpg'] = rpg
            
            # Append the dictionary to the team list
            team_dict[team_names[i]].append(player_dict)
    
        # For the current team, the ppg values is fetched for each player dictionary in the team list. 
        # These ppg values are then used to sort the player dictionaries in ascending order.
        # The best three are chosen as these have the highest values
        # (so the first argument to sorted() is a list of dictionaries. For each of these dictionaries, the second argument key = lambda ... extracts the ppg value of each of the players wihtout changing the original dictionaries. The ppg values are what the list of dictionaries is sorted on)
        team_dict[team_names[i]] = (sorted(team_dict[team_names[i]], key = lambda player: player['ppg']))[-3:]
        
    return team_dict

if __name__ == '__main__':
    teams = make_team_dictionary("https://en.wikipedia.org/wiki/2021_NBA_playoffs")
    plot_NBA_player_statistics(teams)
