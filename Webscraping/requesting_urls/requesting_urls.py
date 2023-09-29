import requests as req

def get_html(url, params=None, output=None):
    """
    Function to fetch text from a provided URL. Saves to local file if output parameter is supplied
    
    Args
        param1 URL of webpage
        param2 dictionary of parameters to the URL (params={'key':'value', ...})
        param3 Name of the output file. If left empty, the HTML code is not saved to file
    
    Return
        Returns the text string containing the content of the URL
    
    """
    
    # Passing the optional parameters argument to the get function
    # Returns a Response object
    response = req.get(url, params=params)

    # Extract the text from the Response Object
    html_str = response.text

    # Save to file if output parameter is supplied
    # If output is provided, it evalutes to True:
    if output:
        # Open a file with name output
        # utf-8 encoding to avoid UnicodeEncodeError 
        with open(output, 'w', encoding="utf-8") as f:
            # Fetch the complete URLfrom response and write to file along with the html_str
            f.write(f"{response.url}\n\n{html_str}")

    # Return the html string
    return html_str

if __name__ == '__main__':
    get_html("https://en.wikipedia.org/wiki/Studio_Ghibli", output="studio_ghibli_wiki_html.txt")
    get_html("https://en.wikipedia.org/wiki/Star_Wars", output="star_wars_wiki_html.txt")
    get_html("https://en.wikipedia.org/w/index.php", params={'title' : 'Main_Page', 'action' : 'info'}, output='wiki_main_page_html.txt')
