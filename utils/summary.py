def generate_summary(activity, feature_df, bug_df, sentiment_summary):

    # 最热门功能
    top_feature = feature_df.iloc[0]["Feature"]
    top_feature_count = feature_df.iloc[0]["Count"]

    # 最常见 Bug
    top_bug = bug_df.iloc[0]["Bug"]
    top_bug_count = bug_df.iloc[0]["Count"]

    # 情绪统计
    positive = sentiment_summary.loc[
        sentiment_summary["Sentiment"] == "positive",
        "Count"
    ].sum()

    neutral = sentiment_summary.loc[
        sentiment_summary["Sentiment"] == "neutral",
        "Count"
    ].sum()

    negative = sentiment_summary.loc[
        sentiment_summary["Sentiment"] == "negative",
        "Count"
    ].sum()

    summary = f"""
## 📋 Community Daily Summary

- Total Posts: {activity['posts']}
- Total Comments: {activity['comments']}
- Active Users: {activity['users']}

### 🔥 Top Feature Request
**{top_feature}** ({top_feature_count} mentions)

### 🐞 Most Reported Bug
**{top_bug}** ({top_bug_count} mentions)

### 😊 Community Sentiment
Positive: {positive}
Neutral: {neutral}
Negative: {negative}
"""

    return summary