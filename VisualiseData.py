import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("analysedEpisodes.csv")

def boxPlotPerEpisode(sentiment = "Positive"):
    negativeByEpisode = df.groupby(["Series", 'Episode'])[sentiment].apply(list)
    data = [group for group in negativeByEpisode]
    positions = range(1, len(data) + 1)  # Unique positions for each episode

    plt.figure(figsize=(40, 10))
    plt.boxplot(data, positions=positions)
    plt.xticks(positions, negativeByEpisode.index)  # Set x-tick labels to episode names
    plt.xlabel("Episode")
    plt.ylabel('{} Sentiment'.format(sentiment))
    plt.title('Boxplot of {} Sentiment per Episode'.format(sentiment))
    plt.tight_layout()
    plt.show()

def sentimentPieChart(episode = (14, 1)):
    labels = ["positive", "neutral", "negative"]
    sizes = []
    for l in labels:
        sizes.append(portionSentiment(episode, l))
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%.0f%%')
    plt.title("Pie chart of sentiment for series {} episode {}".format(episode[0], episode[1]))
    plt.show()

def plotSentimentPerEpisode(sentiment = "positive"):
    sentiment = sentiment.lower()
    episodes = df.groupby(["Series", 'Episode'])["Sentiment"].apply(list)
    portions = []
    positions = range(0, len(episodes))
    for e in episodes.index:
        portions.append(portionSentiment(e, sentiment))
    plt.figure(figsize=(40, 10))
    plt.plot(portions, linestyle='--', marker='o')
    plt.xticks(positions, episodes.index)
    plt.title("Plot of portion of {} comments per episode".format(sentiment))
    plt.xlabel("Episode")
    plt.ylabel("Percentage {}".format(sentiment))
    plt.tight_layout()
    plt.show()

def plotOverallSentimentPerEpisode():
    episodePositive = df.groupby(["Series", 'Episode'])["Positive"].mean()
    episodeNegative = df.groupby(["Series", 'Episode'])["Negative"].mean()
    overall = episodePositive.to_numpy() - episodeNegative.to_numpy()
    seriesNumbers = []
    for e in episodeNegative.index:
        if e[0] not in seriesNumbers:
            seriesNumbers.append(e[0])
    plt.figure(figsize=(16, 40))
    for i in range(len(seriesNumbers)):
        overall = episodePositive[seriesNumbers[i]].to_numpy() - episodeNegative[seriesNumbers[i]].to_numpy()
        plt.subplot(len(seriesNumbers), 1, i+1)
        plt.plot(episodePositive[seriesNumbers[i]].index, overall, linestyle='--', marker='o')
        plt.title("Series {}".format(seriesNumbers[i]))
        plt.xlabel("Episode")
        plt.ylabel("Overall sentiment")
    plt.show()

def portionSentiment(episode, sentiment):
    episodes = df.groupby(["Series", 'Episode'])["Sentiment"].apply(list)
    return episodes[episode[0]][episode[1]].count(sentiment)/len(episodes[episode[0]][episode[1]])

#Sentiments: Positive, Neutral, Negative
#boxPlotPerEpisode("Negative")

#sentimentPieChart()
#plotSentimentPerEpisode("negative")
plotOverallSentimentPerEpisode()