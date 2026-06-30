from collections import Counter
import re


FEATURE_KEYWORDS = {

    "AI": [
        "ai",
        "gemini",
        "assistant",
        "chatgpt"
    ],

    "Translation": [
        "translation",
        "translate",
        "translator"
    ],

    "Photo Viewer": [
        "photo",
        "image",
        "gallery",
        "viewer"
    ],

    "Browser": [
        "browser",
        "chrome",
        "web"
    ],

    "Navigation": [
        "maps",
        "navigation",
        "gps"
    ],

    "APK": [
        "apk",
        "install",
        "sideload"
    ]
}


def feature_analysis(data):

    counter = Counter()

    for post in data:

        text = (
            post["title"] + " " + post["body"]
        ).lower()

        for feature, keywords in FEATURE_KEYWORDS.items():

            for keyword in keywords:

                if re.search(
                        rf"\b{re.escape(keyword)}\b",
                        text):

                    counter[feature] += 1
                    break

    return counter