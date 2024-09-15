import pandas as pd
def modifyCSV():
    arr = pd.read_csv("analysedEpisodesDupe.csv").values
    series = []
    episode = []
    negative = []
    neutral = []
    positive = []
    sentiment = []

    for a in arr:
        if int(a[0][0:-3]) < 10 and int(a[0][0:-3]) != 1:
            series.append("0" + str(a[0][0:-3]))
            episode.append(a[0][-2::])
        elif int(a[0][0:-3]) == 1:
            series.append("14")
            episode.append(a[0][-2::])
        else:
            series.append(a[0][0:-3])
            episode.append(a[0][-2::])
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
        "Series": series,
        "Episode": episode,
        "Negative": negative,
        "Neutral": neutral,
        "Positive": positive,
        "Sentiment": sentiment
    })
    df.to_csv("analysedEpisodes.csv", index=False)

modifyCSV()