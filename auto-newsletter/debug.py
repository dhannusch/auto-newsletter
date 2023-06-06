import json
import datetime
from content import Content

def debug(item: Content, file):
    """
    Use this function to write debug output to a txt file
    """
    file.write(str(datetime.datetime.now()))
    file.write("title: " + item.title + '\n')
    file.write("url: " + item.url + '\n')
    file.write("text: " + item.text + '\n\n')

def debug_guidance(out, file_path):
    """
    Use this function to write debug guidance-specific output to a txt file
    """
    with open(file_path, 'w') as json_file:
        json.dump(out, json_file)
        json_file.write(str(datetime.datetime.now()))
        json_file.write('\n')