import trafilatura
from content import Content
from debug import debug
from loadingbar import LoadingBar
from colorama import Fore, Style

loading_bar = LoadingBar(total=100, length=50)
file_path="debug/debug_scrape.txt"
file = open(file_path, 'w')

def scrape(news: 'list[Content]') -> 'list[Content]':
    """
    Given a list of Content objects with a fetchable URL, scrape the text and output a new list of Content with the 'text' fields populated.
    """
    print("Scraping the content from the websites..")
    loading_bar = LoadingBar(total=len(news), length=50)
    loading_bar.draw()
    content = []
    for item in news:
        downloaded = trafilatura.fetch_url(item.url)
        item.add_text(trafilatura.extract(downloaded))
        debug(item, file)
        content.append(item)
        loading_bar.update()
    print("\n" + Fore.GREEN + "I have all the content scraped!\n")
    print(Style.RESET_ALL)
    return content

