import streamlit as st
import pandas as pd

# ==========================
# Utils
# ==========================
from utils.data_loader import load_data
from utils.activity_analysis import activity_analysis
from utils.feature_analysis import feature_analysis
from utils.bug_analysis import bug_analysis
from utils.topic_analysis import topic_analysis
from utils.sentiment_analysis import sentiment_analysis
from utils.user_sentiment_analysis import user_sentiment_analysis
from utils.group_analysis import group_analysis
from utils.user_analysis import user_analysis

from utils.summary import generate_summary
from utils.reports_generator import (
    community_report,
    product_report,
    qa_report,
)

# ==========================
# Dashboards
# ==========================
from dashboard.overview import show_overview
from dashboard.reddit import reddit_dashboard
from dashboard.wechat import wechat_dashboard
from dashboard.sentiment import sentiment_dashboard
from dashboard.reports import report_dashboard

# ==========================
# Page
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
st.title(
    "📊 Reddit Community Dashboard"
    if source == "reddit"
    else "💬 WeChat Community Dashboard"
)

# ==========================
# Basic Analysis
# ==========================
activity = activity_analysis(df)

topic_df = topic_analysis(df)

feature_df = None
bug_df = None

group_df = None
user_df = None

if source == "reddit":

    feature_df = feature_analysis(df)
    bug_df = bug_analysis(df)

else:

    group_df = group_analysis(df)
    user_df = user_analysis(df)

# ==========================
# Sentiment (只跑一次)
# ==========================
sentiment = None
user_sentiment_df = None

if run_sentiment:

    # 微信只分析最近30天
    if source == "wechat":

        recent_df = df[
            pd.to_datetime(df["created_date"])
            >= (
                pd.Timestamp.today().normalize()
                - pd.Timedelta(days=30)
            )
        ]

        sentiment = sentiment_analysis(recent_df)

    else:

        sentiment = sentiment_analysis(df)

    sentiment_df = sentiment["df"]

    if source == "wechat":

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
# Sentiment Dashboard
# ==========================
if run_sentiment:

    sentiment_dashboard(sentiment)

# ==========================
# Reports（Reddit）
# ==========================
if run_sentiment and source == "reddit":

    summary = generate_summary(
        activity,
        feature_df,
        bug_df,
        topic_df,
        sentiment
    )

    community = community_report(
        activity,
        sentiment,
        topic_df
    )

    product = product_report(
        feature_df,
        topic_df
    )

    qa = qa_report(
        bug_df,
        sentiment
    )

    report_dashboard(
        summary,
        community,
        product,
        qa,
        source
    )

# ==========================
# Reports（WeChat）
# ==========================
elif run_sentiment and source == "wechat":

    summary = generate_summary(
        activity,
        None,
        None,
        topic_df,
        sentiment
    )

    community = community_report(
        activity,
        sentiment,
        topic_df
    )

    report_dashboard(
        summary,
        community,
        None,
        None,
        source
    )

# ==========================
# No Sentiment
# ==========================
else:

    st.info(
        "Enable **Run Sentiment Analysis** to view sentiment insights."
    )
