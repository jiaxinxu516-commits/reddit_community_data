def generate_summary(activity, features, bugs, topics, sentiment):

    # Top Feature
    top_feature = (
        features.iloc[0]["Feature"]
        if len(features) > 0
        else "N/A"
    )

    # Top Bug
    top_bug = (
        bugs.iloc[0]["Bug"]
        if len(bugs) > 0
        else "N/A"
    )

    # Top Topic
    top_topic = (
        topics.iloc[0]["Topic"]
        if len(topics) > 0
        else "N/A"
    )

    # Sentiment
    summary_df = sentiment["summary"]

    positive = summary_df.loc[
        summary_df["Sentiment"] == "positive",
        "Count"
    ].sum()

    neutral = summary_df.loc[
        summary_df["Sentiment"] == "neutral",
        "Count"
    ].sum()

    negative = summary_df.loc[
        summary_df["Sentiment"] == "negative",
        "Count"
    ].sum()

    report = f"""
### 📌 Community Daily Summary

Today the Reddit community remained active.

• 📄 **Posts:** {activity["posts"]}

• 💬 **Comments:** {activity["comments"]}

• 👥 **Active Users:** {activity["users"]}

---

### 🔥 Key Insights

• Most requested feature: **{top_feature}**

• Most discussed topic: **{top_topic}**

• Most reported bug: **{top_bug}**

---

### 😊 Community Sentiment

Positive: {positive}

Neutral: {neutral}

Negative: {negative}

---

### 🎯 Recommendation

Product Team:
Focus on **{top_feature}** related feature requests.

QA Team:
Investigate **{top_bug}** related issues.

Community Team:
Monitor discussions around **{top_topic}**.
"""

    return report