import json
import pandas as pd


def load_data(path, source="reddit"):

    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)

    rows = []

    # Reddit
    if source == "reddit":

        for item in raw["data"]["children"]:

            post = item["data"]

            rows.append({

                "title": post.get("title", ""),

                "body": post.get("selftext", ""),

                "text": post.get("title", "") + " " + post.get("selftext", ""),

                "author": post.get("author", ""),

                "group": "reddit",

                "created_date": post.get("created_utc"),

                "score": post.get("score", 0),

                "num_comments": post.get("num_comments", 0)

            })

        df = pd.DataFrame(rows)

        df["created_date"] = pd.to_datetime(
            df["created_date"],
            unit="s"
        )

    # WeChat
    elif source == "wechat":

        for msg in raw:

            rows.append({

                "title": "",

                "body": msg.get("chatContent", ""),

                "text": msg.get("chatContent", ""),

                "author": msg.get("senderName", ""),

                "group": msg.get("groupName", ""),

                "created_date": msg.get("receivedAt"),

                "score": 0,

                "num_comments": 0

            })

        df = pd.DataFrame(rows)

        df["created_date"] = pd.to_datetime(
            df["created_date"]
        )

    return df