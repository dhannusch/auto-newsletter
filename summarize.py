from transformers import pipeline
from content import Content
import os
from colorama import Fore, Style
from debug import debug
from spinner import Spinner

spinner = Spinner()

os.environ["TOKENIZERS_PARALLELISM"] = "false"
file_path="debug/debug_summarize.txt"
file = open(file_path, 'w')

def summarize(content: 'list[Content]') -> 'list[Content]':
    """
    Given a list of Content objects, this function takes the 'text' from each object and replaces them with a summary using BART AI model.
    """
    print("Summarizing the news from notion..\n")
    spinner.start()
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    spinner.stop()
    summaries = []
    count = 1
    for item in content:
        if item.text is not None:
            # override text with summarized text
            print(Fore.CYAN + "Summarizing article " + str(count) + " (" + item.title + ") ...")
            print(Style.RESET_ALL)
            spinner.start()
            summary = summarizer(item.text, max_length=130, min_length=30, do_sample=False, truncation=True)
            spinner.stop()
            item.text = ' '.join([str(elem["summary_text"]) for elem in summary])
            debug(item, file)
            if item.text == "":
                return SystemError("error! summarizer returned nothing.")
            summaries.append(item)
            count+=1
        else:
            return SystemError("error! item text was empty")
    print("\n" + Fore.GREEN + "Got all the summaries!\n")
    print(Style.RESET_ALL)
    return summaries
