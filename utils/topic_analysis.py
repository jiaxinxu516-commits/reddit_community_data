import pandas as pd
import streamlit as st

from sklearn.feature_extraction.text import (
    TfidfVectorizer,
    ENGLISH_STOP_WORDS
)

# 自定义停用词
CUSTOM_STOPWORDS = {
    # 品牌
    "rokid", "glasses", "glass", "app",

    # Reddit常见
    "reddit", "official", "community",

    # URL
    "https", "http", "www", "com", "amp", "png",

    # 无意义动词
    "need", "use", "used", "using", "want", "wanted",
    "like", "really", "just", "good", "great",
    "know", "think", "make", "trying", "try",

    # 礼貌词
    "hi", "hello", "thanks", "thank", "please",

    # 购买
    "buy", "bought", "order", "ordered", "purchase",

    # 其它
    "lens", "new", "one", "would", "could", "can",
    "got", "getting",

}

@st.cache_data
def topic_analysis(df, top_n=20):

    texts = (
        df["text"].fillna("")
    )

    # 合并 sklearn 默认停用词 + 自定义停用词
    stop_words = list(
        ENGLISH_STOP_WORDS.union(CUSTOM_STOPWORDS)
    )

    vectorizer = TfidfVectorizer(

        stop_words=stop_words,

        max_features=1000,

        ngram_range=(1, 2)

    )

    X = vectorizer.fit_transform(texts)

    words = vectorizer.get_feature_names_out()

    scores = X.sum(axis=0).A1

    topic_df = pd.DataFrame({

        "Topic": words,

        "Score": scores

    })

    topic_df = (
        topic_df
        .sort_values(
            "Score",
            ascending=False
        )
        .head(top_n)
    )

    return topic_df