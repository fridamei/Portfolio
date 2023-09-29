
from collections import deque
from filter_urls import find_articles
from requesting_urls import get_html
from bs4 import BeautifulSoup
import requests as req 

def bfs(start, goal):
    """
    Breadth first search to find the shortest path between two Wikipedia urls using the urls found on the pages
    (https://stackoverflow.com/questions/8922060/how-to-trace-the-path-in-a-breadth-first-search)
    
    Works as follows: 
        Finds all the links from the start url. These links make up the first layer, the links found in the first layer make up the second layer and so on
        The BFS first checks if the goal url is in the first layer. If it is not, it moves on to the second layer and checks there.
        For every new link it checks, the path to it is documented for reference later when checking its 'children' 
        The layering mechanism works by storing the found links in a FIFO queueu. This way, all the links that where found in one layer,
        and therefore added to the queue after one another, are checked before the next layer is adressed. This should ensure, 
        if implemented correctly, that the BFS finds the shortest path
        
    Args
        start (string): The Wikipedia page to start from 
        goal (string):  The Wikipedia page to get to 

    Returns
        shortest_path (list): Returns the path in the graph with the shortest number of vertices from start to goal
        
    """
    # Normally when doing BFS, the graph is known. Here we build it as we find new urls (new 'vertices')
    graph = {}
    
    
    visited = []
    
    # Add the start url to our graph
    graph[start] = [start]
    
    # deque are faster in terms of popping and appending than lists
    # Add the start url to the queue
    queue = deque([start])

    # If using the is_match for matching
    #goal_header = is_match(goal)
    
    
    # While there are links in the queue:
    while len(queue) != 0:
        # Pop the first item in the queue (use the deque as a FIFO queque) and save as current_link
        current_link = queue.popleft()
        
        visited.append(current_link)
        
        # Get the html string from the current_link
        html = get_html(current_link)
    
        # Find all the wikipedia articles from the html string
        next_links = find_articles(html)
        
        #next_links = find_urls(current_link)
        
        # For every found link:
        for link in next_links:
            # Check if the link is the goal, in which case return the path followed to get here
            
            # if using is_match
            #link_header = is_match(link)
            
            if link == goal:
                #graph[current_link] + [link]
                shortest_path = graph[current_link] + [link]
                
                return shortest_path
            
            # If the link is not the goal:
            # Check if the link is not to itself, that the link is not already in path, that it's an english wikipedia page and thats it not been in the queue before
            if (link != current_link) and link not in graph and "en.wikipedia" in link and link not in visited:
                # The path to this link is the path to the url where it was found plus its own link
                graph[link] = graph[current_link] + [link]
                
                # Append the link to queue for inspection later
                queue.append(link)       
    return None
"""
# For checking if titles match instead of urls, but was very slow
def is_match(url1):
    
    # get the html string
    html1 = get_html(url1)
    
    # make soup
    soup1 = BeautifulSoup(html1, "html.parser")

    title1 = soup1.find(id="firstHeading")
    return title1.get_text()

"""
"""
#Could also use beautifulsoup for finding the links, but is not as thoroughly tested and does not handle semi-absolute urls for instance
def find_urls(url):
    ""
    Finding the urls listed on a page using BeautifulSoup
    
    Args
        url (string): url of the file to be scraped for urls
        
    Returns
        urls (list): list of strings of the found urls
    ""
    page = req.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    links = soup.select('a')
    
    base_url = "https://en.wikipedia.org"
    
    urls = []
    for link in links:
        if link.get('href') != None:
            if 'https://en.wikipedia.org' in link.get('href'):
                #print(link.get('href'))
                urls.append(link.get('href'))
            elif '/wiki/' in link.get('href') and not 'http' in link.get('href'):
                #print('https://en.wikipedia.org' + link.get('href'))
                urls.append(base_url + link.get('href'))
    return urls
"""

def shortest_path(start, goal, output=None):
    """
    Runs the BFS and saves results to file
    Args
        start (string): The Wikipedia page to start from 
        goal (string):  The Wikipedia page to get to 
        output (string): To save the path to disk
        
    Returns
        shortest_path (list): Returns the path in the graph with the shortest number of vertices from start to goal
    """
    path = bfs(start, goal)
    
    if output:
        # Open a file with name output
        # utf-8 encoding to avoid UnicodeEncodeError 
        with open(output, 'w', encoding="utf-8") as f:
            # Write each of the urls to file
            [f.write(f"{url}\n") for url in path]
        
    return path

if __name__ == '__main__':
    shortest_path("https://en.wikipedia.org/wiki/Parque_18_de_marzo_de_1938", "https://en.wikipedia.org/wiki/Bill_Mundell", output="shortest_way.txt")
