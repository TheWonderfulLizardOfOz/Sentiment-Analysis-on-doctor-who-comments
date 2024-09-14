import pandas as pd
def modifyCSV():
    arr = pd.read_csv("analysedEpisodesDupe.csv").values
    episodes = []
    negative = []
    neutral = []
    positive = []
    sentiment = []

    for a in arr:
        if int(a[0][0:-3]) < 10 and int(a[0][0:-3]) != 1:
            episodes.append("0" + a[0])
        elif int(a[0][0:-3]) == 1:
            episodes.append("14" + a[0][-3::])
        else:
            episodes.append(a[0])
        negative.append(a[1])
        neutral.append(a[2])
        positive.append(a[3])
        if a[1] > a[2] and a[1] > a[3]:
            sentiment.append("negative")
        elif a[2] > a[3]:
            sentiment.append("neutral")
        else:
            sentiment.append("positive")

    df = pd.DataFrame({
        "Episode": episodes,
        "Negative": negative,
        "Neutral": neutral,
        "Positive": positive,
        "Sentiment": sentiment
    })
    df.to_csv("analysedEpisodes.csv", index=False)

modifyCSV()