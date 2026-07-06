import streamlit as st

# ==========================
# Utils
# ==========================
from utils.data_loader import load_data
from utils.activity_analysis import activity_analysis
from utils.feature_analysis import feature_analysis
from utils.bug_analysis import bug_analysis
from utils.topic_analysis import topic_analysis
from utils.sentiment_analysis import sentiment_analysis
from utils.summary import generate_summary
from utils.reports_generator import (
    community_report,
    product_report,
    qa_report,
)
from utils.group_analysis import group_analysis
from utils.user_analysis import user_analysis
from utils.user_sentiment_analysis import user_sentiment_analysis

# ==========================
# Dashboard
# ==========================
from dashboard.overview import show_overview
from dashboard.reddit import reddit_dashboard
from dashboard.wechat import wechat_dashboard
from dashboard.sentiment import sentiment_dashboard
from dashboard.reports import report_dashboard


# ==========================
# Page Config
# ==========================
st.set_page_config(
    page_title="Community Dashboard",
    layout="wide"
)

# ==========================
# Sidebar
# ==========================
source = st.sidebar.selectbox(
    "Data Source",
    ["reddit", "wechat"]
)

st.sidebar.divider()

run_sentiment = st.sidebar.checkbox(
    "Run Sentiment Analysis",
    value=(source == "reddit")
)

# ==========================
# Load Data
# ==========================
if source == "reddit":

    df = load_data(
        "data/reddit_rokid_glasses_data.json",
        source="reddit"
    )

else:

    df = load_data(
        "data/all_wechat_data.json",
        source="wechat"
    )

# ==========================
# Title
# ==========================
title = (
    "📊 Reddit Community Dashboard"
    if source == "reddit"
    else "💬 WeChat Community Dashboard"
)

st.title(title)

# ==========================
# Run Analysis
# ==========================
activity = activity_analysis(df)

if source == "reddit":

    feature_df = feature_analysis(df)
    bug_df = bug_analysis(df)
    topic_df = topic_analysis(df)

else:

    group_df = group_analysis(df)
    user_df = user_analysis(df)
    topic_df = topic_analysis(df)

# ==========================
# Sentiment Analysis
# ==========================
if source == "wechat":
    sentiment = None
    user_sentiment_df = None

    if run_sentiment:

        sentiment = sentiment_analysis(df)

        sentiment_df = sentiment["df"]

        user_sentiment_df = user_sentiment_analysis(
            sentiment_df
        )

# ==========================
# Overview
# ==========================
show_overview(
    df,
    activity,
    source
)

# ==========================
# Reddit Dashboard
# ==========================
if source == "reddit":

    reddit_dashboard(
        activity,
        feature_df,
        bug_df,
        topic_df
    )

# ==========================
# WeChat Dashboard
# ==========================
else:

    wechat_dashboard(
        df,
        activity,
        group_df,
        user_df,
        user_sentiment_df
    )

# ==========================
# Sentiment
# ==========================
if run_sentiment:

    sentiment = sentiment_analysis(df)

    summary = generate_summary(
        activity,
        feature_df if source == "reddit" else None,
        bug_df if source == "reddit" else None,
        topic_df,
        sentiment
    )

    community = community_report(
        activity,
        sentiment,
        topic_df
    )

    if source == "reddit":

        product = product_report(
            feature_df,
            topic_df
        )

        qa = qa_report(
            bug_df,
            sentiment
        )

    sentiment_dashboard(sentiment)

    report_dashboard(
        summary,
        community,
        product if source == "reddit" else None,
        qa if source == "reddit" else None,
        source
    )

else:
    # sentiment = sentiment_analysis(df)

    # sentiment_df = sentiment["df"]

    # user_sentiment_df = user_sentiment_analysis(
    # sentiment_df)

    st.info("Sentiment Analysis is disabled.")
