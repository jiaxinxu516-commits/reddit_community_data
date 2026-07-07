import pandas as pd
import re
import streamlit as st

BUG_KEYWORDS = {

    "Display": [
        "display",
        "screen",
        "black screen",
        "brightness",
        "flicker"
    ],

    "Connection": [
        "connection",
        "disconnect",
        "bluetooth",
        "wifi",
        "hdmi",
        "usb"
    ],

    "Battery": [
        "battery",
        "charging",
        "charge",
        "power"
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

@st.cache_data
def bug_analysis(df):

    bug_counts = {}

    for bug in BUG_KEYWORDS:
        bug_counts[bug] = 0

    for _, row in df.iterrows():

        text = (
            str(row["text"]).lower()
        )

        for bug, keywords in BUG_KEYWORDS.items():

            for keyword in keywords:

                if re.search(
                    rf"\b{re.escape(keyword)}\b",
                    text
                ):
                    bug_counts[bug] += 1
                    break

    bug_df = (
        pd.DataFrame({
            "Bug": bug_counts.keys(),
            "Count": bug_counts.values()
        })
        .sort_values("Count", ascending=False)
    )

    return bug_df