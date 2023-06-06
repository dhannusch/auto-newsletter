from datetime import datetime
from content import Content
import guidance
from debug import debug, debug_guidance
from loadingbar import LoadingBar
from spinner import Spinner
import json
from colorama import Fore, Style
import os
from simple_term_menu import TerminalMenu

file_path="debug/debug_newsletter_writer.txt"

spinner = Spinner()
                                                      
# set the default language model used to execute guidance programs
guidance.llm = guidance.llms.OpenAI("text-davinci-003")
guidance.llms.OpenAI.cache.clear()

newsletter_writer_prompt = os.environ.get("NEWSLETTER_WRITER_PROMPT")
if newsletter_writer_prompt is None:
    raise ValueError("Missing env variable NEWSLETTER_WRITER_PROMPT")

# define the prompts
newsletter_llm = guidance(newsletter_writer_prompt + """
You will be provided news_content and the url. You are to write the newsletter_blurb about this news article as well as a section_title.
You must only use the provided news_content as reference for the blurb. 
Do not copy any of the news_content word for word when writting the newsletter_blurb.
```json
{
    "news_content": "{{news_content}}",
    "url": "{{url}}",
    "section_title": "{{gen 'section_title' temperature=0.1}}",
    "newsletter_blurb": "{{gen 'newsletter_blurb' temperature=0.1}}"
}```""")
                          
newsletter_title_llm = guidance(newsletter_writer_prompt + """
You will be provided a list of section titles included in a newsletter. You are to generate 3 title options for the whole newsletter. The title should be attention grabbing and reference 1-2 of the most interesting sections from this edition.
Section Title: {{titles}}
---
Title option 1: "{{gen "title1"}}"
Title option 2: "{{gen "title2"}}"
Title option 3: "{{gen "title3"}}"
""")
                                
def generate_newsletter_title(content: 'list[Content]'):
    """
    This function takes a list of string newsletter section "titles" and using an LLM will return some options for the title of the newsletter.
    """
    # Convert Content to dict
    titles = []
    for item in content:
        titles.append(item.title)

    out = newsletter_title_llm(titles=titles)
    print("Newsletter Title Options:")
    print(out["title1"])
    print(out["title2"])
    print(out["title3"])


def write_to_file(title: str, final_content: 'list[Content]'):
    """
    This function writes the final content of a newsletter to a text file.
    Parameters:
    - final_content: A list of Content objects representing the sections of the newsletter to be written to the file.
    """
    # Write the final newsletter out to a txt file
    current_date = datetime.now()
    folder = "newsletters/"
    filepath = (current_date.strftime("%B-%d-%Y") + '.txt').lower()  # Replace with the desired file path
    
    base, ext = os.path.splitext(filepath)
    counter = 1
    while os.path.exists(folder + filepath):
        filepath = f"{base}-v{counter}{ext}"
        counter += 1

    file = open(folder + filepath, 'w')

    print("Writing newsletter to file ", folder + filepath)

    file.write(title + "\n\n")

    for section in final_content:
        file.write(section.title + "\n")
        file.write(section.url + "\n")
        file.write(section.text + "\n\n")

def generate(content: Content) -> Content:
    """
    generate with newsletter_llm
    """
    out = newsletter_llm(news_content=content.text, url=content.url)
    json_string = json.dumps({k:v for k,v in out.variables().items() if k != "llm"})
    deserialized_out = json.loads(json_string)
    response = Content(deserialized_out["section_title"], content.url)
    response.add_text(deserialized_out["newsletter_blurb"])
    debug_guidance(deserialized_out, file_path) 
    return response

def write(news: 'list[Content]') -> 'list[Content]':
    """
    This function writes the content of a newsletter by processing each item in the input list. 
    It takes a list of Content objects as input, where each Content object represents a section of the newsletter with a title, URL, and text. 
    The function iterates over the items, performs some processing, and updates the content accordingly. 
    The modified content is stored in a new list and returned as the final result.
    """
    print("Time to write the newsletter!")
    # len(news)+1 to include generating titles
    # loading_bar = LoadingBar(total=len(news)+1, length=50)
    # loading_bar.draw()
    final_content = []
    titles = []
    for item in news:
        regenerate = True
        while (regenerate):
            spinner.start()
            content = generate(item)
            spinner.stop()
            print("\nGenerated Newsletter Section: \n\n"+ Fore.GREEN + content.title+ "\n\n",content.text)
            print(Style.RESET_ALL)
            print("\nDo you like it?")
            options = ["yes","no - regenerate"]
            terminal_menu = TerminalMenu(options)
            menu_entry_index = terminal_menu.show()
            response = options[menu_entry_index]
            if (response == "yes"):
                # loading_bar.update()
                regenerate = False
            else:
                guidance.llms.OpenAI.cache.clear()
        titles.append(content.title)
        final_content.append(content)
    
    # generate newsletter title options
    out = newsletter_title_llm(titles=titles)
    # loading_bar.update()
    print("\n\n"+ Fore.YELLOW +"Newsletter Title Options (select the one you like):")
    print(Style.RESET_ALL)

    options = get_title_options(out)
    terminal_menu = TerminalMenu(options)
    menu_entry_index = terminal_menu.show()
    title_selection = options[menu_entry_index]
    print(f"You have selected {title_selection}!")


    print("\n" + Fore.GREEN + "Newsletter writing complete!\n")
    print(Style.RESET_ALL)
    
    # write the final generated content to a file
    write_to_file(title_selection, final_content)

def get_title_options(out) -> 'list[str]':
    options = []
    if (out["title1"] is not None):
        options.append(out["title1"])
    if (out["title2"] is not None):
        options.append(out["title2"])
    if (out["title3"] is not None):
        options.append(out["title3"])
    return options