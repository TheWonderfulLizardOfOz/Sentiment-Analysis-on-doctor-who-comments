import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("analysedEpisodes.csv")

def boxPlotPerEpisode(sentiment = "Positive"):
    negativeByEpisode = df.groupby('Episode')[sentiment].apply(list)
    print(negativeByEpisode.head())
    data = [group for group in negativeByEpisode]
    positions = range(1, len(data) + 1)  # Unique positions for each episode

    plt.figure(figsize=(40, 10))
    plt.boxplot(data, positions=positions)
    plt.xticks(positions, negativeByEpisode.index)  # Set x-tick labels to episode names
    plt.xlabel(sentiment)
    plt.ylabel('{} Sentiment'.format(sentiment))
    plt.title('Boxplot of {} Sentiment per Episode'.format(sentiment))
    plt.tight_layout()
    plt.show()

def sentimentPieChart(episode = "1x01"):
    labels = ["positive", "neutral", "negative"]
    sizes = []
    for l in labels:
        sizes.append(portionSentiment(episode, l))
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%.0f%%')
    plt.title("Pie chart of sentiment for {}".format(episode))
    plt.show()

def plotSentimentPerEpisode(sentiment = "positive"):
    sentiment = sentiment.lower()
    episodes = df.groupby('Episode')["Sentiment"].apply(list)
    portions = []
    for e in episodes.index:
        print(int(e[0:-3] + e[-2::]))
        portions.append(portionSentiment(e, sentiment))
    plt.figure(figsize=(40, 10))
    plt.plot(episodes.index, portions, linestyle='--', marker='o')
    plt.title("Plot of portion of {} comments per episode".format(sentiment))
    plt.xlabel("Episode")
    plt.ylabel("Percentage {}".format(sentiment))
    plt.tight_layout()
    plt.show()

def portionSentiment(episode, sentiment):
    episodes = df.groupby('Episode')["Sentiment"].apply(list)
    return episodes[episode].count(sentiment)/len(episodes[episode])

#Sentiments: Positive, Neutral, Negative
#boxPlotPerEpisode("Positive")

#sentimentPieChart("12x03")
plotSentimentPerEpisode("negative")