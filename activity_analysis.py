from collections import Counter
from datetime import datetime


def activity_analysis(data):
    """
    Community Activity Analysis
    """

    total_posts = len(data)

    total_comments = sum(
        post["num_comments"]
        for post in data
    )

    users = set(
        post["author"]
        for post in data
    )

    posts_per_day = Counter()

    for post in data:

        date = datetime.fromtimestamp(
            post["created_utc"]
        ).strftime("%Y-%m-%d")

        posts_per_day[date] += 1

    return {
        "posts": total_posts,
        "comments": total_comments,
        "users": len(users),
        "posts_per_day": posts_per_day
    }