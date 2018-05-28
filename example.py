import requests
import time
import pprint

SUICIDEWATCH = "https://api.pushshift.io/reddit/search/submission/?size=500&stickied=false&subreddit=pics&before={}"


def write_to_file(out_file, body):
    for row in body.split("\n"):
        row = row.rstrip()
        if len(row) > 0:
            row = "__label__suicidal {}\n".format(row)
            out_file.write(row)

def suicidewatch(before=int(time.time())):
    url = SUICIDEWATCH.format(before)

    return requests.get(url).json()


with open("data/suicidal.txt", "w") as out_file:
    last = int(time.time())
    while True:
        res = suicidewatch(last)

        for submission in res['data']:
            try:
                pprint.pprint(submission)
                last = submission['created_utc']
                #write_to_file(out_file, submission['selftext'])
                print("{} OK".format(submission['url']))

                #exit()
            except Exception as ex:
                print("{} FAIL".format(submission['url']), ex)


