import streamlit as st
from utils.data_loader import load_data

from utils.activity_analysis import activity_analysis
import plotly.express as px

from utils.feature_analysis import feature_analysis

from utils.bug_analysis import bug_analysis

from utils.sentiment_analysis import sentiment_analysis

from utils.summary import generate_summary

from utils.topic_analysis import topic_analysis

from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

from utils.reports_generator import community_report
from utils.reports_generator import product_report
from utils.reports_generator import qa_report

from utils.group_analysis import group_analysis

from utils.user_analysis import user_analysis

st.set_page_config(
    page_title="Reddit Community Dashboard",
    layout="wide"
)


#build dashboard
source = st.sidebar.selectbox(
    "Data Source",
    ["reddit", "wechat"]
)

# ==========================
# Heavy Analysis
# ==========================
st.sidebar.markdown("---")
st.sidebar.subheader("⚙️ Heavy Analysis")

run_sentiment = st.sidebar.checkbox(
    "Sentiment Analysis",
    value=(source == "reddit")
)

if source == "reddit":
    df = load_data(
        "data/reddit_rokid_glasses_data.json",
        source="reddit"
    )
else:
    df = load_data(
        "data/all_wechat_data.json",
        source="wechat"
    )

if source == "reddit":
    st.title("📊 Reddit Community Dashboard")

else:
    st.title("📊 WeChat Community Dashboard")

color_discrete_sequence=[
    "#00B5FF"
]

left, right = st.columns(2)

activity = activity_analysis(df)
feature_df = feature_analysis(df)
bug_df = bug_analysis(df)

if run_sentiment:

    sentiment = sentiment_analysis(df)

    sentiment_df = sentiment["df"]

    sentiment_summary = sentiment["summary"]

    sentiment_timeline = sentiment["timeline"]

    negative_posts = sentiment["negative_posts"]

else:

    sentiment = None

group_df = group_analysis(df)


topic_df = topic_analysis(df)

if run_sentiment:

    summary = generate_summary(
        activity,
        feature_df,
        bug_df,
        topic_df,
        sentiment
    )

else:

    summary = """
### 📋 AI Summary

Sentiment Analysis is disabled.

Enable it from the sidebar.
"""

if run_sentiment:

    community = community_report(
        activity,
        sentiment,
        topic_df
    )

    product = product_report(
        feature_df,
        topic_df
    )

    qa = qa_report(
        bug_df,
        sentiment
    )


user_df = user_analysis(df)

#community overtime
st.subheader("📈 Community Overview")

c1, c2, c3, c4 = st.columns(4)

if source == "reddit":

    c1.metric("Posts", activity["posts"])
    c2.metric("Comments", activity["comments"])
    c3.metric("Active Users", activity["users"])
    c4.metric("Avg Comments/Post", activity["avg_comments"])

else:

    c1.metric("Messages", activity["posts"])
    c2.metric("Groups", df["group"].nunique())
    c3.metric("Active Users", activity["users"])
    c4.metric("Avg Messages/User",
              round(activity["posts"]/activity["users"],2))
    

# ==========================
# WeChat Only
# ==========================
if source == "wechat":

    st.divider()
    st.header("💬 WeChat Community Analysis")

    # ==========================
    # KPI
    # ==========================
    c1, c2, c3 = st.columns(3)

    c1.metric("Groups", df["group"].nunique())
    c2.metric("Messages", len(df))
    c3.metric("Users", df["author"].nunique())

    # ==========================
    # Group Data
    # ==========================
    group_users = (
        df.groupby("group")["author"]
          .nunique()
          .reset_index(name="Users")
    )

    # ==========================
    # 两列布局
    # ==========================
    col1, col2 = st.columns(2)

    with col1:

        st.subheader("💬 各群消息数")

        fig_group = px.bar(
            group_df,
            x="Messages",
            y="group",
            orientation="h",
            text="Messages",
            template="plotly_dark",
            title="Messages by Group"
        )

        fig_group.update_layout(
            height=max(350, len(group_df) * 45),
            yaxis=dict(categoryorder="total ascending")
        )

        fig_group.update_yaxes(
            tickmode="linear",
            automargin=True
        )

        st.plotly_chart(
            fig_group,
            use_container_width=True
        )

    # ==========================
    # 右边
    # ==========================
    with col2:

        st.subheader("👥 各群活跃人数")

        fig_users = px.bar(
            group_users,
            x="Users",
            y="group",
            orientation="h",
            text="Users",
            template="plotly_dark",
            title="Users by Group"
        )

        fig_users.update_layout(
            height=max(350, len(group_users) * 45),
            yaxis=dict(categoryorder="total ascending")
        )

        fig_users.update_yaxes(
            tickmode="linear",
            automargin=True
        )

        st.plotly_chart(
            fig_users,
            use_container_width=True
        )

    st.subheader("👤 Top Active Users")

    user_df = (
        df.groupby("author")
        .size()
        .reset_index(name="Messages")
        .sort_values("Messages", ascending=False)
    )

    user_df["display_name"] = (
        user_df["author"]
        .str.slice(0,10)
    )

    fig_user = px.bar(
        user_df.head(20),
        x="Messages",
        y="display_name",
        orientation="h",
        text="Messages",
        hover_name="author",
        template="plotly_dark",
        title="Top 20 Active Users"
    )

    fig_user.update_layout(
        height=700,
        yaxis=dict(
            categoryorder="total ascending"
        )
    )

    fig_user.update_yaxes(
        tickmode="linear",
        automargin=True
    )

    st.plotly_chart(
        fig_user,
        use_container_width=True
    )


#posts over time
st.divider()
st.subheader("📈 Posts Over Time")

title = (
    "Daily Posts"
    if source=="reddit"
    else "Daily Messages"
)

fig = px.bar(
    activity["posts_per_day"],
    x="created_date",
    y="Posts",
    title=title,
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

#Hot topics
st.divider()
st.subheader("🔥 Hot Topics")

fig_topic = px.bar(

    topic_df,

    x="Score",

    y="Topic",

    orientation="h",

    template="plotly_dark",

    text_auto=".2f",

    title="Top Discussion Topics"
)


fig_topic.update_layout(

    yaxis=dict(
        categoryorder="total ascending"
    ),

    xaxis_title="TF-IDF Score",

    yaxis_title=""

)

fig_topic.update_yaxes(
    categoryorder="total ascending",
    tickmode="linear",
    automargin=True
)

st.plotly_chart(
    fig_topic,
    use_container_width=True
)


#PNN
if run_sentiment:

    st.divider()
    st.subheader("🧠 Community Sentiment")

    fig_sentiment = px.pie(
        sentiment_summary,
        names="Sentiment",
        values="Count",
        template="plotly_dark"
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


else:

    st.info("Sentiment Analysis is disabled.")


if run_sentiment:

    st.divider()

    st.subheader("📋 AI Community Summary")

    st.markdown(summary)


if run_sentiment:

    st.divider()

    st.subheader("📅 Community Daily Report")

    st.markdown(community)

    st.subheader("🚀 Product Report")

    st.markdown(product)

    st.subheader("🐞 QA Report")

    st.markdown(qa)


st.subheader("🚀 Product Report")
st.markdown(product)

st.subheader("🐞 QA Report")
st.markdown(qa)