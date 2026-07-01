import json
import pandas as pd


def load_data(path):

    with open(path, "r", encoding="utf-8") as f:

        raw = json.load(f)

    rows = []

    for item in raw["data"]["children"]:

        post = item["data"]

        rows.append({

            "title": post.get("title", ""),

            "body": post.get("selftext", ""),

            "author": post.get("author", ""),

            "created_utc": post.get("created_utc", 0),

            "score": post.get("score", 0),

            "num_comments": post.get("num_comments", 0)

        })

    df = pd.DataFrame(rows)

    df["created_date"] = (
    pd.to_datetime(df["created_utc"], unit="s")
    .dt.date
    )
    
    return df