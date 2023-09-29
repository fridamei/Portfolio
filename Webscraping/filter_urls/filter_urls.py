import re
from requesting_urls import get_html

from IPython import embed # For debugging

def find_urls(html_string, base_url=None, output=None):
    """
    Function that takes an HTML-string and finds the URLs in the text.
    Base_url is for use with relative paths found. 
    
    Args
        html_string (string) The HTML code to be searched for URLs, represented as a string
        base_url (string) The base URL to add the relative paths to, if any
        output (string) Name of the output file to save the URLs
    Returns
        url_list: A list of strings containing the found urls
  
    """
    
    """
    Explanation of the regex string: 
        

    Matches a '<' followed by an 'a', then one or more spaces. 
    Then follows an optional group ('?' behind closing parentheses) which is non-captured ('?:')
    and contains any number of any character unless its '>' (denoting the end of the <a) followed by spaces
    
    After this group it matches 'href="' literally, 
    then a captured group, so this is the text that is actually saved in the list. 
    This group includes every character which is not either '"' or '#', as the normal paths end in " and the relative
    paths start with and end in # and we do not want these characters in the url string.
    
    The captured group captures every character until it reaches a literal ", denoting then end of the url
    """

    regex = r'<a\s+(?:[^>]*?\s+)?href="([^"#]*)"'
    
    # Find all strings that match the regex and save in a set (to remove duplicates)
    url_list = set(re.findall(regex, html_string))

    # Make sure there are no empty entries in the list 
    url_list = (list(filter(None, url_list)))
    
    # If base url is supplied then append the relative paths in place to this
    if base_url:
        for i in range(len(url_list)):
            #  Semi-absolute url, only add https
            if url_list[i][0:2] == '//':
                url_list[i] = base_url[0:6] + url_list[i]

            # Relative path, add entire base_url
            elif "http" not in url_list[i]:
                url_list[i] = base_url + url_list[i]

    # If output is supplied save to file
    if output:
        # Open a file with name output
        # utf-8 encoding to avoid UnicodeEncodeError 
        with open(output, 'w', encoding="utf-8") as f:
            # Write each of the urls to file
            [f.write(f"{url}\n") for url in url_list]
            
    return url_list
    

def find_articles(html_string, base_url=None, output=None):
    """
    Function that takes in an HTML string and searches for only urls to wikipedia articles,
    excluding the namespace articles. Saves the URLs to file if output is supplied
    
    Args
        html_string (string) The HTML code to be searched for URLs, represented as a string
        base_url (string) URL to add the partial and semi absolute URLs in find_urls to 
        output (string) Name of the output file to save the article URLs
        
    Returns
        article_url_list: A list of strings containing the URLs to the found Wikipedia articles
    
    """
    
    # Make filename to save the results from the find_urls function to get two different files. Is set to None if output is not supplied
    output_all_urls =f"all_urls_{output}" if output else None
    
    # Get all URLs from the HTML-string
    urls = find_urls(html_string, base_url=base_url, output=output_all_urls)
    
    """
    Regex explanation:

        The first (sub)group checks if the url starts with https://xx.wikipedia.org or ('|') /wiki without capturing it (this is captured later together with the entire url instead, if not done like this, this is returned as its own entry in the list without the suffix)
        (where /wiki is specified to be the first word in the url and not followed by other characters, to exclude cases such as http//:wikimedia and the last part of https//:someNonWikipediaUrl/wiki/)
        
        Then comes a group with a negativ lookahead, where if 'Wikipedia:' follows any number of any character, the
        url should not be matched (which excludes the wikipedia namespace pages). 
        
        Then match any number of any character that is not a whitespace character ('[^\s]+'), so the matching stops at the newline between the urls
        (works because the '\n'.join makes the urls a string separated by a newline)
        
        The outermost group captures the entire strings that meet the requirements stated above (starts with wikipedia.org or wiki, without Wikipedia: in the middle), 
        because of the .+ in the second group and the [^\s]+ at the end. 
    """
    regex = r"((?:https?:\/\/\w\w\.wikipedia.org|^/wiki\b)(?!.+\bWikipedia:\b)[^\s]+)"
    #regex = r"https?:\/\/\w\w\.wikipedia.org(?!.*\bWikipedia\b)[^\s]+"

    # The regex needs an actual stop to match the url, not just an space so traverse the url list to get each of the urls 'alone'
    article_url_list = []
    for article in urls:
        article = re.findall(regex, article)
        if article:
            article_url_list.append(article[0])
    
    # If base_url is set, the find_urls function will ensure every url has https//: ....
    # If not, add them here (also to ensure double entries do not accure as the same article can be written as both a relative and absolute url)
    if not base_url:
        for i in range(len(article_url_list)):
            #  Relative URL, add the wikipedia base
            if "http" not in article_url_list[i]:
                article_url_list[i] =  f"https://en.wikipedia.org{article_url_list[i]}"
   
    # To ensure no duplicates when the base_url is not passed to find_url (then many of the URLs will be in the format /wiki, which might point to the same page as another full wikipedia link)
    article_url_list = list(set(article_url_list))
    
    # Save to file if output is supplied
    if output:
        # Open a file with name output
        # utf-8 encoding to avoid UnicodeEncodeError 
        with open(output, 'w', encoding="utf-8") as f:
            # Write each of the urls to file
            [f.write(f"{url}\n") for url in article_url_list]
    
    return article_url_list
    
if __name__ == '__main__':
    html = get_html("https://en.wikipedia.org/wiki/Nobel_Prize")
    find_articles(html, base_url="https://en.wikipedia.org", output="nobel_prize.txt")
    
    html2 = get_html("https://en.wikipedia.org/wiki/Bundesliga")
    find_articles(html2, base_url="https://en.wikipedia.org", output="bundesliga.txt")
    
    html3 = get_html("https://en.wikipedia.org/wiki/2019%E2%80%9320_FIS_Alpine_Ski_World_Cup")
    find_articles(html3, base_url="https://en.wikipedia.org", output="alpine_world_cup.txt")