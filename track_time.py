import os
import pandas as pd
from lxml import html
import requests

from typing import List


class TimeTracker:
    def __init__(self, text: List[str] = [''], time: List[str] = ['']) -> None:
        self.text = text
        self.time = time
        
        self.parsed_time = []

    def parse_read_time(self):
        # Reads through time tracking files and returns a list of [time, chars] per file
        # 3 types of lines: time and text and comments

        # 3 states in for loop: 1. beginning block (no start text), 2. regular block, 3. ending block (no end block)
        for time_file, text_file in zip(self.time, self.text):
            state = 1
            last_index = 0 # next index must be bigger; useful for error checking in case of multiple matches
            elapsed_time = 0

            parsed_time_per_file = []
            for line in time_file:
                line = line.strip() # FUCK YOUUU
                # NOTE: lazy checking because checking if there are chinese characters is hard due to multiple unicode blocks
                if line[0] == '#':
                    continue
                elif line[0].isnumeric():
                    split = [int(x) for x in line.split(' ')]
                    assert len(split) == 2, f'Time block not in 2 chunks!, f{time_file}'
                    start, end = split
                    elapsed = end - start
                    # NOTE: assuming never more than 60
                    if start >= end: elapsed += 60 #add 60min for hour
                    elapsed_time += elapsed
                else:  # assuming otherwise = text and NO EXCEPTIONS!
                    # Find chars and sanity check index
                    index = text_file.find(line)
                    total_chars = index - last_index + len(line)
                    if index < last_index: raise Exception(f'Index is less than last index, probably multiple matches or no match! Searched string: {line} found at: {index}')
                    else: last_index = index

                    parsed_time_per_file.append([elapsed_time, total_chars, total_chars/elapsed_time])
                    elapsed_time = 0 # reset time
                    # if state == 1:
                    #     total_chars = 
                    # elif state == 2:
                    # elif state == 3:
                    # else: raise Exception('Invalid State')
            self.parsed_time.append(parsed_time_per_file)

def get_text(filenames: List[str], lines = False) -> List[str]:
    text = []
    for f in filenames:
        with open(f, 'r', encoding='utf-8') as handle:
            if lines:
                text.append(handle.readlines())
            else:
                text.append(handle.read())
    return text


def main():
    BOOK = 'shz'
    DIRECTORY = '/mnt/c/Users/sabot/Desktop'
    WEBSITE = 'http://purepen.com/shz/'
    CHAPTERS = [4, 5, 6]
    # BEFORE CHANGING DIR
    read_text = get_text([f'{x:03d}.txt' for x in CHAPTERS])

    # os.chdir(DIRECTORY)
    # files = os.listdir()
    read_filenames = [f'shz{x}.txt' for x in CHAPTERS]  # Hardcoded
    read_urls = [f'{WEBSITE}{x:03d}.htm' for x in CHAPTERS]

    # TODO: web scraping
    # https://docs.python-guide.org/scenarios/scrape/
    # read_pages = [html.fromstring(requests.get(url).content) for url in read_urls]

    read_time_files = get_text(read_filenames, True)

    time_tracker = TimeTracker(read_text, read_time_files)
    time_tracker.parse_read_time()
    print(time_tracker.parsed_time)


if __name__ == "__main__":
    main()
