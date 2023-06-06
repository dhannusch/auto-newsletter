# auto-newsletter

The auto-newsletter is a powerful tool that automates the creation of engaging newsletters using AI (LLM, BART) and Notion.

## Features

- **Notion Integration:** Easily pull article links from your Notion database for newsletter content.
- **BART-based Summarization:** Generates concise and accurate summaries of the articles.
- **Language Model (LLM):** Utilizes OpenAI's `text-davinci-003` and [Microsoft's guidance language](https://github.com/microsoft/guidance) to analyze and understand articles.
- **Effortless Content Curation:** Streamline your newsletter creation process and focus on other tasks.

## How the program works

1. First it pulls news links added within the last week from a Notion DB.
2. Scrapes the urls
3. Uses a [HuggingFace pipeline with the bart-large-cnn model](https://huggingface.co/facebook/bart-large-cnn) to summarize the scraped webpage. This way we can pass less tokens into the LLM. This summarizer runs locally and does not come with API costs.
4. Finally, pass each summary into `guidance` which uses OpenAI's `text-davinci-003` to write the newsletter blurb. The newsletter is outputted to a file in the `newsletters/` folder.

## Requirements

- Notion API Key
- OPENAI API Key
- Dependencies (see Pipfile)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/dhannusch/auto-newsletter
```

2. Navigate to the project directory:

```bash
cd auto-generator
```

3. Install the dependencies using Pipenv:

```bash
pipenv install
```

4. Setup the environment variables or remove `test` from `test.env` and add your keys.

```bash

export NOTION_API_KEY=your-notion-api-key
export CONTENT_DB_ID=your Notion DB id
export OPENAI_API_KEY=your-openapi-api-key
```

5. Add a custom prompt in your `.env` file to fine-tune the model. An example has been added in `test.env` file.

```bash
NEWSLETTER_WRITER_PROMPT="You are a distinguished writer for a tech newsletter named 'Tech Gazette' on GitHub.
This newsletter focuses on delivering insightful and up-to-date tech news to its readers.
Your writing style should be engaging and informative, ensuring that readers stay well-informed about the latest developments in the world of technology through your well-crafted newsletter."
```

6. Activate the Pipenv shell:

```bash
pipenv shell
```

7. Run the application:

```bash
python main.py
```

## Usage

1. Follow [these steps](https://developers.notion.com/docs/create-a-notion-integration) from Notions API docs to create an integration and get an API key. Add the generated API key `NOTION_API_KEY` in the `.env` file
2. Make sure your Notion database contains article links in the desired format.
3. Run the `main.py` script to fetch the articles and generate newsletter summaries.
4. The program will output the generated newsletter blurb for each article. You can chose to either trigger a regeneration or accept the generated blurb.
5. Finally, you will be given 3 newsletter title options to select from.

## What your Notion DB should look like

Your database should include properties

- `Date Added` (Date property)
- `Title` (Text property)
- `URL` (URL property)

## Things to note

- The web scraper doesn't do a great job with Reddit or Twitter yet.
- Obviously the more articles you've added throughout the week, the longer it will take. Therefore, I added a separate method `date_last_x_days(days: int)` in which you can shorten your window if you prefer less than a week. Just replace the function in `main.py` like this:

  ```python
  news = pull_news_from_notion(date_last_week())
  # change to..
  news = pull_news_from_notion(date_last_x_days(3)) # last 3 days
  ```

## TODO

- only summarize if content text is long
- add regeneration option for newsletter titles
- pull links from other DBs
- add advanced filtering option for notion DBs
- improve scraping of reddit and twitter
- speed up the program

## Contributing

Contributions are welcome! If you have any suggestions, bug reports, or feature requests, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).
