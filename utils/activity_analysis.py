import pandas as pd


def activity_analysis(df):
    """
    Community Activity Analysis
    """

    posts = len(df)

    comments = df["num_comments"].sum()

    users = df["author"].nunique()

    avg_comments = round(comments / posts, 2)

    # 每天发帖数量
    posts_per_day = (
        df.groupby("created_date")
        .size()
        .reset_index(name="Posts")
        .sort_values("created_date")
    )

    return {
        "posts": posts,
        "comments": comments,
        "users": users,
        "avg_comments": avg_comments,
        "posts_per_day": posts_per_day
    }