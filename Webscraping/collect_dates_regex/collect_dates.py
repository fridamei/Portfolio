import re
from requesting_urls import get_html
from datetime import datetime
from IPython import embed # for debugging

def find_dates(html_string, output=None):
    """
    Takes a HTML_string and filters out every date in the formats DMY, MDY, YMD, ISO.
    Formats the dates to YYYY/MM/DD
    
    Args
        html_string (string)    String to search for dates in, typically a HTML-string from a webpage
        output (string)  Name of file to write the dates to. No file is created if output is None
    Returns
        formatted_dates: A list of strings of dates in format YYYY/MM/DD
        
    """
    # Regex for every month, regardless of abbreviation and capitalization
    jan = r"\b[jJ]an(?:uary)?\b"
    feb = r"\b[fF]eb(?:ruary)?\b"
    mar = r"\b[mM]ar(?:ch)?\b"
    apr = r"\b[aA]pr(?:il)?\b"
    may = r"\b[mM]ay\b"
    june = r"\b[jJ]une\b"
    jul = r"\b[jJ]ul(?:y)?\b"
    aug = r"\b[aA]ug(?:ust)?\b"
    sep = r"\b[sS]ep(?:tember)?\b"
    octb = r"\b[oO]ct(?:ober)?\b"
    nov = r"\b[nN]ov(?:ember)?\b"
    dec = r"\b[dD]ec(?:ember)?\b"
    
    # matches every month from 1 to 12 (in a non-capture group to get the entire date in same list entry)
    iso_month_format = r"\b(?:0[1-9]|1[0-2])\b" 
    
    # Regex for day (1-31) and year (0000-2999) in non-capture groups
    day = r"\b(?:[0-2][1-9]|3[0-1])\b"
    year = r"\b(?:[0-2]\d{3})\b"
    
    # regex that match any of the months in a non-capture group
    months = rf"(?:{jan}|{feb}|{mar}|{apr}|{may}|{june}|{jul}|{aug}|{sep}|{octb}|{nov}|{dec})"
    
    # The formats to consider
    dmy = rf"{day}\s{months}\s{year}"
    mdy = rf"{months}\s{day},?\s{year}" # Optional comma in cases where it is omitted
    ymd = rf"{year}\s{months}\s{day}"
    iso = rf"{year}-{iso_month_format}-{day}"
    
    # matches any of the formats
    date_formats = f"{dmy}|{mdy}|{ymd}|{iso}"
    
    #finds the matches and saves them in a list, dates. Since every component of the entire regex were non-capture groups, the date is instead captured in its entirety as one single match
    dates = re.findall(date_formats, html_string)
    
    # List to save the formatted dates in
    formatted_dates = []
    
    # Loop to format every element
    for date_element in dates:
        # Run format_date() to get elemtent_date in YYYY/MM/DD format
        date_element = format_date(date_element, day, months, year, iso_month_format)
        
        # Substitute the months given in word character with corresponding number
        date_element = format_month(date_element, months)
        
        # Add to list
        formatted_dates.append(date_element)
    
    # Use the strptime function of datetime to sort the list in ascending order (from 'oldest' to 'newest')
    # sort takes a callable as a parameter, here the lambda function which converts every date to a datetime object
    formatted_dates.sort(key = lambda date: datetime.strptime(date, '%Y/%m/%d'))
    
    # Save to file if output is supplied    
    if output:
        # Open a file with name output
        # utf-8 encoding to avoid UnicodeEncodeError 
        with open(output, 'w', encoding="utf-8") as f:
            f.write(f"{formatted_dates}\n\n")
            [f.write(f"{date_element}\n") for date_element in formatted_dates]
        
    return formatted_dates


def format_date(date_element, day_regex, month_regex, year_regex, iso_month_regex):
    """
    Formats date to YYYY/MM/DD
    
    Args
        date_element (string) date to be converted
        day_regex (string)  regex matching the day
        month_regex (string)  regex matching the month
        year_regex (string)  regex matching the year
        iso_month_regex (string)  regex matching the month in iso format
        
        
    Returns
        date_element (string): the formatted date element in YYYY/MM/DD format
    """
    # DMY
    date_element = re.sub(rf"({day_regex})\s({month_regex})\s({year_regex})", r"\3/\2/\1", date_element)
        
    # MDY
    date_element = re.sub(rf"({month_regex})\s({day_regex}),\s({year_regex})", r"\3/\1/\2", date_element)
        
    # YMD
    date_element = re.sub(rf"({year_regex})\s({month_regex})\s({day_regex})", r"\1/\2/\3", date_element)
        
    # ISO
    date_element = re.sub(rf"({year_regex})-({iso_month_regex})-({day_regex})", r"\1/\2/\3", date_element)

    return date_element


def format_month(date_element, months):
    """
    Substitutes the month, if written in characters, to the number representation
    
    Args
        date_element (string)  Date to check for and replace character representation of month
        months (string)  The regex to match the character month
    
    Returns
        date_element (string): The formatted date_element
    """
    # Define a month dictionary to find the correct number to replace the month with
    month_dict = {'january':'01', 'february':'02', 'march':'03', 'april':'04', 
                  'may':'05', 'june':'06', 'july':'07', 'august':'08', 
                  'september':'09', 'october':'10', 'november':'11', 'december':'12'}
    
    # Must slice the months regex to get rid of the (?: ... ) as this is a non-capture group and would not return anything 
    months = months[3:-1]
    
    # Check if the month is represented in characters
    month = re.findall(months, date_element)
    
    # If the above regex returned something other than None:
    if month:
        """
        Lambda iterates through the dictionary like a for-loop, checking if any of the keys 
        contain part of or the enitre month. Returns a function object
        
        Filter takes that function, and only keeps entries where the lambda evaluated to true given the parameter passed to the lambda function (month in dict_key)
        (ie the dictionary key that the month was contained in)
        
        Filter returns an iterator, which is then converted to a list
        Access the element of the list as a string using [0]
        """

        month_dict_key = list(filter(lambda dict_key: month[0].lower() in dict_key, month_dict.keys()))[0]
        
        # Slicing 1 represent the year/ part of the original date_element, slicing 2 the /day part. The month is replaced by the corresponding value from the dictionary
        date_element = date_element[0:5] + month_dict[month_dict_key] + date_element[-3:]
        
    return date_element

if __name__ == '__main__':
    html1 = get_html("https://en.wikipedia.org/wiki/J._K._Rowling")
    find_dates(html1, output="dates_rowling.txt")
    
    html2 = get_html("https://en.wikipedia.org/wiki/Richard_Feynman")
    find_dates(html2, output="dates_feynman.txt")
    
    html3 = get_html("https://en.wikipedia.org/wiki/Hans_Rosling")
    find_dates(html3, output="dates_rosling.txt")