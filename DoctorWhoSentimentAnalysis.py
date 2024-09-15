import json
import re
import praw
import urllib.request
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax
import pandas as pd

tokenizer = AutoTokenizer.from_pretrained("cardiffnlp/twitter-roberta-base-sentiment-latest")
model = AutoModelForSequenceClassification.from_pretrained("cardiffnlp/twitter-roberta-base-sentiment-latest")

file = open("secret.txt", "r")
lines = [line.strip() for line in file.readlines()]
file.close()

reddit = praw.Reddit(
    client_id=lines[2],
    client_secret=lines[3],
    user_agent=lines[0],
    password=lines[1],
    username=lines[0]
)

doctorWho = reddit.subreddit("DoctorWho")
def setDiscussions():
    episodes = {}
    file = open("discussionThreads.txt", "w")
    searchRange = [1] + [i for i in range(8, 14)]
    results = set()
    for i in searchRange:
        searchString = "Doctor Who {}x{}:"
        for j in range(1, 18):
            print(i, j)
            if j < 10:
                searchResult = doctorWho.search(searchString.format(i, "0" + str(j)), limit=2)
            else:
                searchResult = doctorWho.search(searchString.format(i, j), limit=2)
            for r in searchResult:
                while 1:
                    try:
                        request_url = urllib.request.urlopen("https://www.reddit.com/comments/{}/.json".format(r)).read()
                        break
                    except:
                        continue

                if "Post-Episode Discussion Thread" not in re.search("\"title\":(.*?\".*?\"),", str(request_url))[1]:
                    continue
                if r not in results:
                    file.write("https://www.reddit.com/comments/{}/.json\n".format(str(r)))
                    episode = re.search("\"title\":.*?([0-9]+x[0-9]+).*?,", str(request_url))[1]
                    while 1:
                        try:
                            r.comments.replace_more(limit=0)
                            comments = []
                            for comment in r.comments.list():
                                print(comments)
                                comments.append(comment.body)
                            episodes[episode] = comments
                            break
                        except:
                            print("waiting")
                            continue
                results.add(r)

    with open('episodes.json', 'w') as fp:
        json.dump(episodes, fp)
    file.close()

def analyseComments():
    analysedEpisodes = {}
    with open('episodes.json', 'r') as file:
        episodes = json.load(file)
    analysedComments = []
    for episode in episodes:
        print(episode)
        # [episode name, negative, neutral, positive]
        for comment in episodes[episode]:
            encodedInput = tokenizer(comment, truncation=True, max_length=512, return_tensors='pt')
            output = model(**encodedInput)
            scores = output[0][0].detach().numpy()
            scores = softmax(scores)
            c = [episode] + list(scores)
            analysedComments.append(c)
        df = pd.DataFrame(analysedComments, columns =['Episode', 'Negative', "Neutral", "Positive"])
        df.to_csv("analysedEpisodes.csv")
