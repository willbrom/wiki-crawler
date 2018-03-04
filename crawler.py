import time

def continue_crawl(search_history, target_url, max_step=25):
    """A function that checks if crawl should continue or stop based on given args

    search_history: A list of urls that have been crawled
    target_url: A url that when reached, crawl should stop
    max_step: Max number of urls that can be crawled before stoping the crawler, default value 25
    """
    if search_history[-1] == target_url or len(search_history) > max_step or search_history[-1] in search_history[:-1]:
        return False
    else:
        return True

article_chain = []

while continue_crawl(search_history, target_url):
    # download html of last article in article chain
    # find the first link in the article
    first_link = find_first_link(article_chain[-1])
    # add the first link to article chain
    article_chain.append(first_link)
    # delay for about 2 sec
    time.sleep(2)
