#!/usr/bin/python3

import requests
import time
import pprint
import sys
import argparse
from urllib.parse import urlparse

parser = argparse.ArgumentParser()
parser.add_argument("subreddit", help="the subreddit to scrape")


LABEL = "suicidal"
URL = "https://api.pushshift.io/reddit/search/submission/?size=500&stickied=false&subreddit={}"
FILE_NAME = "data/{}.txt"

def write_to_file(out_file, body):
    for line in body.split("\n"):
        line = line.rstrip()
        if len(line) > 0:
            line = "__label__{} {}\n".format(LABEL, line)
            out_file.write(line)

def get_more(before=int(time.time())):
    url = URL.format(before)

    return requests.get(url).json()

if __name__ == "__main__":
    try:
        args = parser.parse_args()

        LABEL = None
        if args.subreddit:
            LABEL = args.subreddit
        else:
            raise Exception("subreddit not given")

        URL = URL.format(LABEL) + "&before={}"
        FILE_NAME = FILE_NAME.format(LABEL)


        # Open file and start scraping
        with open(FILE_NAME, "w") as out_file:
            last = int(time.time())
            while True:
                response = get_more(last)

                for submission in response['data']:
                    try:
                        # pprint.pprint(submission)
                        last = submission['created_utc']

                        body = None
                        if submission['is_self']:

                            # Skip [removed] and [deleted]
                            if submission['selftext'] == "[removed]" or submission == "[deleted]":
                                continue

                            body = submission['title'] + " " + submission['selftext']
                        else:
                            u = urlparse(submission['url'])
                            body = submission['title'] + " " + u.netloc

                        print(body)
                        write_to_file(out_file, body)

                        print("{} OK".format(submission['full_link']))

                        # exit()
                    except UnicodeEncodeError as ex:
                        print("UnicodeEncodeError", submission['id'])
                    except Exception as ex:
                        print("{} FAIL".format(submission['full_link']), ex)
    except KeyboardInterrupt:
        print("\nGoodbye!")


