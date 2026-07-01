import streamlit as st
from utils.data_loader import load_data

from utils.activity_analysis import activity_analysis
import plotly.express as px

from utils.feature_analysis import feature_analysis

from utils.bug_analysis import bug_analysis

from utils.sentiment_analysis import sentiment_analysis

from utils.summary import generate_summary


st.set_page_config(
    page_title="Reddit Community Dashboard",
    layout="wide"
)


#build dashboard
st.title("📊 Reddit Community Intelligence Dashboard")
color_discrete_sequence=[
    "#00B5FF"
]

left, right = st.columns(2)


df = load_data("data/reddit_rokid_glasses_data.json")
activity = activity_analysis(df)
feature_df = feature_analysis(df)
bug_df = bug_analysis(df)
sentiment_df, sentiment_summary = sentiment_analysis(df)
summary = generate_summary(
    activity,
    feature_df,
    bug_df,
    sentiment_summary
)


#community overtime
st.subheader("📈 Community Overview")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Posts",
        activity["posts"]
    )

with c2:
    st.metric(
        "Comments",
        activity["comments"]
    )

with c3:
    st.metric(
        "Active Users",
        activity["users"]
    )

with c4:
    st.metric(
        "Avg Comments/Post",
        activity["avg_comments"]
    )


#posts over time
st.divider()
st.subheader("📈 Posts Over Time")

fig = px.bar(
    activity["posts_per_day"],
    x="created_date",
    y="Posts",
    template="plotly_dark",
    title="Daily Posts"
)

st.sidebar.header("Filters")

start_date = st.sidebar.date_input(
    "Start Date",
    df["created_date"].min()
)

end_date = st.sidebar.date_input(
    "End Date",
    df["created_date"].max()
)

fig.update_layout(
    xaxis_title="Date",
    yaxis_title="Number of Posts",
    hovermode="x unified"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


#top feature requests
st.divider()
st.subheader("📦 Top Feature Requests")

fig_feature = px.bar(
    feature_df,
    x="Count",
    y="Feature",
    orientation="h",
    template="plotly_dark",
    text="Count",
    title="Most Requested Features"
)

fig_feature.update_layout(

    yaxis=dict(
        categoryorder="total ascending"
    ),

    xaxis_title="Mentions",

    yaxis_title=""
)

st.plotly_chart(
    fig_feature,
    use_container_width=True
)


#Bug analysis
st.divider()
st.subheader("🐞 Bug Analysis")

fig_bug = px.bar(

    bug_df,

    x="Count",

    y="Bug",

    orientation="h",

    template="plotly_dark",

    text="Count",

    title="Most Reported Bugs"

)

fig_bug.update_layout(

    yaxis=dict(
        categoryorder="total ascending"
    ),

    xaxis_title="Mentions",

    yaxis_title=""

)

st.plotly_chart(
    fig_bug,
    use_container_width=True
)

#PNN
st.divider()
st.subheader("🧠 Community Sentiment")

fig_sentiment = px.pie(

    sentiment_summary,

    names="Sentiment",

    values="Count",

    template="plotly_dark",

    title="Sentiment Distribution"

)

st.plotly_chart(
    fig_sentiment,
    use_container_width=True
)

c1, c2, c3 = st.columns(3)

positive = sentiment_summary.loc[
    sentiment_summary["Sentiment"]=="positive",
    "Count"
].sum()

neutral = sentiment_summary.loc[
    sentiment_summary["Sentiment"]=="neutral",
    "Count"
].sum()

negative = sentiment_summary.loc[
    sentiment_summary["Sentiment"]=="negative",
    "Count"
].sum()

c1.metric("😊 Positive", positive)

c2.metric("😐 Neutral", neutral)

c3.metric("😞 Negative", negative)

color_map = {
    "positive": "#00cc96",
    "neutral": "#636efa",
    "negative": "#ff4b4b"
}

fig_sentiment = px.pie(
    sentiment_summary,
    names="Sentiment",
    values="Count",
    color="Sentiment",
    color_discrete_map=color_map,
    template="plotly_dark",
    title="Sentiment Distribution"
)

st.divider()
st.subheader("📋 AI Community Summary")
st.markdown(summary)