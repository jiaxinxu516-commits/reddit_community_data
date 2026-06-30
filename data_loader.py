import json


def load_data(file_path):
    """
    Load Reddit JSON data and convert it into a simplified format.
    """

    with open(file_path, "r", encoding="utf-8") as f:
        raw = json.load(f)

    posts = []

    # Reddit Official JSON
    for item in raw["data"]["children"]:

        post = item["data"]

        posts.append(
            {
                "title": post.get("title", ""),
                "body": post.get("selftext", ""),
                "author": post.get("author", ""),
                "created_utc": post.get("created_utc", 0),
                "score": post.get("score", 0),
                "num_comments": post.get("num_comments", 0),
                "url": post.get("url", ""),
                "subreddit": post.get("subreddit", "")
            }
        )

    print(f"Loaded {len(posts)} posts")

    return posts