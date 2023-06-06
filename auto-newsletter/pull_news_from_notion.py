import requests
import os
from datetime import datetime, timedelta
from content import Content
from debug import debug
from spinner import Spinner
from colorama import Fore, Style

spinner = Spinner()
file_path="debug/debug_pull_news_from_notion.txt"
file = open(file_path, 'w')

def date_last_week():
    """
    Returns the date of a week ago from today in ISO 8601 format which is required for filters in the Notion API.
    """
    # Get the date of a week ago
    current_date = datetime.now()
    week_ago = current_date - timedelta(days=7)

    # Format the date in ISO 8601 format
    iso_date = week_ago.isoformat()

    return iso_date

def date_last_x_days(days: int):
    """
    Returns the date of 'x' days ago from today in ISO 8601 format which is required for filters in the Notion API.
    """
    # Get the date of a week ago
    current_date = datetime.now()
    week_ago = current_date - timedelta(days=days)

    # Format the date in ISO 8601 format
    iso_date = week_ago.isoformat()

    return iso_date


def pull_news_from_notion(date_filter: str) -> 'list[Content]':
    """
    Uses the Notion API along with a DB ID and an API key to pull news titles and their respective URLs from within the last week.
    The DB ID and API key are set by environment variables CONTENT_DB_ID & NOTION_API_KEY.
    Parameters:
    - date_filter: an ISO 8601 formatted str date. Can use functions date_last_week() or date_last_x_days()
    Returns a list of Content objects.
    """
    print("Pulling news from notion..")
    spinner.start()
    url = "https://api.notion.com/v1/databases/{}/query".format(os.environ.get("CONTENT_DB_ID"))

    headers = {
        "accept": "application/json",
        "Notion-Version": "2022-06-28",
        "content-type": "application/json",
        "Authorization": "Bearer {}".format(os.environ.get("NOTION_API_KEY"))
    }
    data = {
        "filter": {
            "property": "Date Added",
            "date": {
                "after": date_filter
            }
        },
    }

    response = requests.post(url, headers=headers, json=data)
    json_response = response.json()
    news = []
    for item in json_response["results"]:
        props = item["properties"]
        title = props["Title"]["title"][0]["plain_text"]
        article_url = props["URL"]["url"]
        content = Content(title, article_url)
        debug(content, file)
        news.append(content)
    spinner.stop()
    print(Fore.GREEN + "Got all the news from notion!\n")
    print(Style.RESET_ALL)
    return news