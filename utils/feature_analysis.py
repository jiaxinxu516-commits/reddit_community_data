import pandas as pd
import re
import streamlit as st

FEATURE_KEYWORDS = {
    "AI": [
        "ai",
        "assistant",
        "chatgpt",
        "gemini",
        "llm"
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
        "navigation",
        "maps",
        "gps"
    ],

    "APK": [
        "apk",
        "install",
        "sideload"
    ]
}

@st.cache_data
def feature_analysis(df):

    feature_counts = {}

    for feature in FEATURE_KEYWORDS:

        feature_counts[feature] = 0

    for _, row in df.iterrows():

        text = (
            str(row["text"]).lower()
        )

        for feature, keywords in FEATURE_KEYWORDS.items():

            for keyword in keywords:

                if re.search(
                    rf"\b{re.escape(keyword)}\b",
                    text
                ):
                    feature_counts[feature] += 1
                    break

    feature_df = (
        pd.DataFrame({
            "Feature": feature_counts.keys(),
            "Count": feature_counts.values()
        })
        .sort_values("Count", ascending=False)
    )

    return feature_df