from transformers import pipeline
import pandas as pd

# 加载模型（第一次运行会下载）
classifier = pipeline(
    "sentiment-analysis",
    model="cardiffnlp/twitter-roberta-base-sentiment-latest"
)


def sentiment_analysis(df):

    sentiments = []

    for _, row in df.iterrows():

        text = str(row["title"]) + " " + str(row["body"])

        try:

            result = classifier(text[:512])[0]

            label = result["label"]

        except:

            label = "neutral"

        sentiments.append(label)

    df = df.copy()

    df["sentiment"] = sentiments

    summary = (
        df["sentiment"]
        .value_counts()
        .reset_index()
    )

    summary.columns = ["Sentiment", "Count"]

    return df, summary