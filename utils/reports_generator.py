#社区日报
def community_report(activity, sentiment, topics):

    summary = sentiment["summary"]

    positive = summary.loc[
        summary["Sentiment"]=="positive",
        "Count"
    ].sum()

    neutral = summary.loc[
        summary["Sentiment"]=="neutral",
        "Count"
    ].sum()

    negative = summary.loc[
        summary["Sentiment"]=="negative",
        "Count"
    ].sum()

    report = f"""
# 📅 Community Daily Report

## Community Activity

Posts: {activity["posts"]}

Comments: {activity["comments"]}

Users: {activity["users"]}

## Community Sentiment

Positive: {positive}

Neutral: {neutral}

Negative: {negative}

## Hot Topics

"""

    for _, row in topics.head(5).iterrows():

        report += f"- {row['Topic']}\n"

    return report


#产品日报
def product_report(features, topics):

    report = "# 🚀 Product Daily Report\n\n"

    report += "## Top Requested Features\n\n"

    for _, row in features.head(5).iterrows():

        report += f"- {row['Feature']} ({row['Count']})\n"

    report += "\n## Trending Topics\n\n"

    for _, row in topics.head(5).iterrows():

        report += f"- {row['Topic']}\n"

    return report


#QA日报
def qa_report(bugs, sentiment):

    report = "# 🐞 QA Daily Report\n\n"

    report += "## Top Bugs\n\n"

    for _, row in bugs.head(5).iterrows():

        report += f"- {row['Bug']} ({row['Count']})\n"

    report += "\n## Negative Posts\n"

    negative = sentiment["negative_posts"]

    for _, row in negative.head(5).iterrows():

        report += f"- {row['title']}\n"

    return report