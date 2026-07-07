import pandas as pd
import streamlit as st

@st.cache_data
def activity_analysis(df):
    """
    Community Activity Analysis
    """

    posts = len(df)

    comments = df["num_comments"].sum()

    users = df["author"].nunique()

    avg_comments = round(comments / posts, 2)

    # ===== 按天统计 =====
    posts_per_day = (
        df.assign(day=df["created_date"].dt.date)
          .groupby("day")
          .size()
          .reset_index(name="Posts")
          .rename(columns={"day": "created_date"})
          .sort_values("created_date")
    )

    return {
        "posts": posts,
        "comments": comments,
        "users": users,
        "avg_comments": avg_comments,
        "posts_per_day": posts_per_day
    }