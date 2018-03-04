import time
import requests
import urllib

from bs4 import BeautifulSoup


start_url = "https://en.wikipedia.org/wiki/Special:Random"
target_url = "https://en.wikipedia.org/wiki/Greek_language"

def find_first_link(url):
    """Finds the first link in a wiki page and returns it. If no link found returns None.

    This function uses the requests library to get the response from the given wiki url,
    the BeautifulSoup library to get the link to the next article and the urllib library
    to create the url for the next article.
    url: A wiki url
    """
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    # This div contains the article's body
    content_div = soup.find(id="mw-content-text").find(class_="mw-parser-output")
    # stores the first link found in the article, if article containes no links
    # the value remains None
    article_link = None

    for element in content_div.find_all("p", recursive=False):
        if element.find("a", recursive=False):
            article_link = element.find("a", recursive=False).get('href')
            break

    if not article_link:
        return

    # Build full url from the relative url
    first_link = urllib.parse.urljoin('https://en.wikipedia.org/', article_link)

    return first_link

def continue_crawl(search_history, target_url, max_step=25):
    """A function that checks if crawl should continue or stop based on given args.

    search_history: A list of urls that have been crawled
    target_url: A url that when reached, crawl should stop
    max_step: Max number of urls that can be crawled before stoping the crawler, default value 25
    """
    print(search_history[-1])

    if search_history[-1] == target_url:
        print("We've found the {} article, aborting search!".format(target_url.split('/')[-1]))
        return False
    elif len(search_history) > max_step:
        print("The search has gone on suspiciously long, aborting search!")
        return False
    elif search_history[-1] in search_history[:-1]:
        print("We've arrived at an article we've already seen, aborting search!")
        return False
    else:
        return True

article_chain = [start_url]

while continue_crawl(article_chain, target_url, 40):
    # download html of last article in article chain
    # find the first link in the article
    first_link = find_first_link(article_chain[-1])

    if not first_link:
        print("We have reached an article with no links, aborting search!")
        break

    # add the first link to article chain
    article_chain.append(first_link)
    # delay for 2 sec
    time.sleep(2)
