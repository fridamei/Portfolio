from bs4 import BeautifulSoup
from requesting_urls import get_html
import re
import os

from IPython import embed 

def extract_events(url):
    """ 
    Extract date, venue and discipline from Calendar table in the 2021–22 FIS Alpine Ski World Cup Wikipedia page
     Args :
         url (str): The url to extract the table from
     Returns :
         events (list of 3-tuples): A list of 3-tuples where the rows represent each race date, and the 3-tuples are (date, venue, discipline)
  
    """
    # Dictionary to search for the full name when an abbreviation is found in the table
    disciplines = {
        "DH": " Downhill ",
        "SL": " Slalom ",
        "GS": " Giant Slalom ",
        "SG": " Super Giant Slalom ",
        "AC": " Alpine Combined ",
        "PG": " Parallel Giant Slalom ",}
    
    # get the html string
    html = get_html(url)
    
    # make soup
    soup = BeautifulSoup(html, "html.parser")
    
    # Find the tag that contains the Calendar heading span
    calendar_header = soup.find(id="Calendar")
    
    # Find the following table
    calendar_table = calendar_header.find_all_next("table")[0]
    
    # Find the rows in the first table
    # Rows is a list with every row of the table as entries
    rows = calendar_table.find_all("tr")

    # The first entry of the row contains all the headers
    # Put them in their own list for easier handling (headers is a list of the individual columns from the first row of the table, so the cells of the first row then)
    headers = rows[0].find_all("th")
    # Extract text and strip of new-line symbols
    headers = [h.text.strip() for h in headers]

    # Save the indices of the event, venue and type (discipline) column
    index_event = headers.index('Event')
    index_venue = headers.index('Venue')
    index_type = headers.index('Type')
    
    found_event = None
    found_venue = None
    found_discipline = None
    
    # Saving all the necessary values in the list 
    events = []
    
    # Find the maximum number of columns a row can have
    full_row_length = 0
    for row in rows:
        # if the length of the row (the number of columns) is larger than full_row_length, update full_row_length 
        full_row_length = max(len(row.find_all('td')), full_row_length)        
        
    # some rows have fewer because the 'venue' spans multiple rows,
    # short_row_length means a repeated venue , which should be re-used from the previous iteration
    short_row_length = full_row_length-2

    for row in rows :
        # Finds every entry in the row
        # So cells is now a list containing each column in the current row
        cells = row.find_all("td")
    
        # Check if the number of columns NOT either the shortest number of columns a result row can have, the largest number or the one in between (for the results where the venue is repeated 3 times (row 23 and 36))
        if len(cells) not in range(short_row_length, full_row_length+1):
        # If the number of columns are fewer, the row is a 'header' row (not acutally a header, but divides the results into different championships)
            continue
        
        # Using the indices found earlier
        event = cells[index_event]
        # An event seems to always be a 1-3 digit number, so we can check that we have an event with a simple regex
        if re.match (r"\d{1,3}", event.text.strip()):
            found_event = event.text.strip()
        
        else:
            found_event = None
            continue # Break loop if no event is foundto avoid consuming time and resources unnecessarily
        
        if len(cells) == full_row_length:
        # If event is cancelled, the event number will return a non digit and break, not necessary to handle here
            #When full length (max number of columns), the venue is in its ordinary place
            venue_cell = cells[index_venue]
            found_venue = venue_cell.text.strip()
            discipline_index = index_type
        
        # For row 23 and 36 where the venue is repeated for the third time, the number of rows is one less than max
        elif len(cells) == full_row_length-1:
            # repeated venue, discipline is different column
            discipline_index = index_type-1
          
        # for every row with 9 columns (as defined in first if-test, the rows with other numbers of columns than defined here are not captured at all as all result rows are within this range)
        else:
            # repeated venue, discipline is in a different column
            discipline_index = index_type-2

        # Find the discipline
        discipline = cells[discipline_index]

        # find the discipline id

        # Regex that match the discipline abbreviations
        discipline_regex = r"\b(DH|SL|GS|SG|AC|PG)\b"
        
        # strip the discipline text before matching. Checks which of the abbreviations occur in the discipline cell
        discipline_match = re.search(discipline_regex, discipline.text.strip())
        
        if discipline_match :
            # The discipline abbr captured in the cell often have a trailing number. The slicing removes these if they exist
            found_discipline = disciplines[discipline.text.strip()[0:2]]
        else :
            found_discipline = None
            print("No discipline found")
            continue


        if found_venue and found_event and found_discipline :
            # if we found something
            events.append((found_event, found_venue, found_discipline))

    return events


def create_betting_slip(events, save_as):
    """
    Saves a markdown format betting slip to the location './datetime_filter/<save_as>.md'
    
    Args
        events (list):  list of 3-tuples containing date, venue and type for each event
        save_as (string): filename to save the markdown betting slip as
    
    """
    os.makedirs("datetime_filter_results", exist_ok=True)
    
    with open(f"./datetime_filter/{save_as}.md", 'w') as f:
        f.write(f"# BETTING SLIP ({save_as})\n\nName:\n\n")
        f.write(" Date | Venue | Discipline | Who wins?\n")
        f.write(" --- | --- | --- | --- \n")
        for e in events:
            date, venue, discipline = e
            f.write(f"{date} | {venue} | {discipline}\n")
   
if __name__ == '__main__':
    url = "https://en.wikipedia.org/wiki/2021-22_FIS_Alpine_Ski_World_Cup"
    
    events = extract_events(url)
    create_betting_slip(events, "FIS_21_22")