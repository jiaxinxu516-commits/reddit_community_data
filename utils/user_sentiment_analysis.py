import pandas as pd


def user_sentiment_analysis(sentiment_df):
    """
    Calculate sentiment statistics for each user.
    sentiment_df 必须已经包含 sentiment 列
    """

    # 每个人各种情绪数量
    table = (
        sentiment_df
        .groupby(["author", "sentiment"])
        .size()
        .unstack(fill_value=0)
    )

    # 保证三列都存在
    for col in ["positive", "neutral", "negative"]:
        if col not in table.columns:
            table[col] = 0

    table["Total"] = (
        table["positive"] +
        table["neutral"] +
        table["negative"]
    )

    table["Positive %"] = (
        table["positive"] / table["Total"] * 100
    ).round(1)

    table["Neutral %"] = (
        table["neutral"] / table["Total"] * 100
    ).round(1)

    table["Negative %"] = (
        table["negative"] / table["Total"] * 100
    ).round(1)

    # 综合情绪评分
    table["Sentiment Score"] = (
        (
            table["positive"] -
            table["negative"]
        ) / table["Total"]
    ).round(2)

    table = (
        table
        .reset_index()
        .sort_values(
            "Negative %",
            ascending=False
        )
    )

    return table