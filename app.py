import streamlit as st
from utils.data_loader import load_data

from utils.activity_analysis import activity_analysis
import plotly.express as px

from utils.feature_analysis import feature_analysis


st.set_page_config(
    page_title="Reddit Community Dashboard",
    layout="wide"
)

st.title("📊 Reddit Community Intelligence Dashboard")

df = load_data("data/reddit_rokid_glasses_data.json")
activity = activity_analysis(df)
feature_df = feature_analysis(df)

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