from transformers import pipeline
import streamlit as st
import pandas as pd

@st.cache_resource
def load_sentiment_model():
    return pipeline(
        "sentiment-analysis",
        model="cardiffnlp/twitter-roberta-base-sentiment-latest"
    )

classifier = load_sentiment_model()

def sentiment_analysis(df):

    df = df.copy()

    sentiments = []

    for _, row in df.iterrows():

        text = (
            str(row["text"])
        )

        try:
            result = classifier(text[:512])[0]

            label = result["label"].lower()

        except Exception:
            label = "neutral"

        sentiments.append(label)

    df["sentiment"] = sentiments

    # ==========================
    # ① Pie Chart 数据
    # ==========================

    summary = (
        df["sentiment"]
        .value_counts()
        .reset_index()
    )

    summary.columns = [
        "Sentiment",
        "Count"
    ]

    # ==========================
    # ② Timeline 数据
    # ==========================

    timeline = (
        df.groupby(
            ["created_date", "sentiment"]
        )
        .size()
        .reset_index(name="Count")
    )

    timeline = df.copy()

    timeline["week"] = (
        pd.to_datetime(
            timeline["created_date"]
        ).dt.to_period("W").astype(str)
    )

    timeline = (
        timeline
        .groupby(
            ["week", "sentiment"]
        )
        .size()
        .reset_index(name="Count")
    )
    # ==========================
    # ③ Negative Posts
    # ==========================

    negative_posts = (
        df[df["sentiment"] == "negative"]
        .sort_values(
            "num_comments",
            ascending=False
        )
    )

    return {
        "df": df,
        "summary": summary,
        "timeline": timeline,
        "negative_posts": negative_posts
    }