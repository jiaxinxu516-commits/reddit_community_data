from collections import Counter
import re


BUG_KEYWORDS = {

    "Display": [
        "display",
        "screen",
        "black screen",
        "brightness",
        "flicker"
    ],

    "Battery": [
        "battery",
        "charging",
        "charge",
        "power"
    ],

    "Connection": [
        "bluetooth",
        "wifi",
        "disconnect",
        "hdmi",
        "usb"
    ],

    "Audio": [
        "audio",
        "sound",
        "speaker",
        "microphone",
        "mic"
    ],

    "Crash": [
        "crash",
        "freeze",
        "stuck",
        "restart",
        "bug",
        "error"
    ],

    "Translation": [
        "translation",
        "translate",
        "translator"
    ]
}


def bug_analysis(data):

    counter = Counter()

    for post in data:

        text = (
            post["title"] + " " + post["body"]
        ).lower()

        for bug, keywords in BUG_KEYWORDS.items():

            for keyword in keywords:

                if re.search(
                        rf"\b{re.escape(keyword)}\b",
                        text):

                    counter[bug] += 1
                    break

    return counter