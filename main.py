from env import check_env_vars
from pull_news_from_notion import date_last_week, pull_news_from_notion
from scrape import scrape
from summarize import summarize
from newsletter_writer import write
from colorama import Fore, Style

def main():

    # verify that all env variables have been provided
    check_env_vars()

    # Pull news content urls from Notion
    news = pull_news_from_notion(date_last_week())

    # Scrape the text from the news content urls
    content = scrape(news)

    # Summarize each new content
    # TODO: only summarize if content text is long
    summaries = summarize(content)

    # Pass to LLM to write newsletter blob
    write(summaries)

    print(Fore.GREEN + "COMPLETE! :)")
    print(Style.RESET_ALL)

if __name__ == "__main__":
    main()