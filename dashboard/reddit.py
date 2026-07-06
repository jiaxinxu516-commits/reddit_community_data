import streamlit as st
import plotly.express as px


def reddit_dashboard(activity, feature_df, bug_df, topic_df):

    st.divider()
    st.header("📊 Reddit Analysis")

    # ==================================================
    # Posts Over Time
    # ==================================================
    st.subheader("📈 Posts Over Time")

    fig = px.bar(
        activity["posts_per_day"],
        x="created_date",
        y="Posts",
        template="plotly_dark",
        title="Daily Posts"
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

    # ==================================================
    # Feature Requests
    # ==================================================
    st.divider()
    st.subheader("📦 Top Feature Requests")

    fig_feature = px.bar(
        feature_df,
        x="Count",
        y="Feature",
        orientation="h",
        text="Count",
        template="plotly_dark",
        title="Most Requested Features"
    )

    fig_feature.update_layout(
        yaxis=dict(categoryorder="total ascending"),
        xaxis_title="Mentions",
        yaxis_title=""
    )

    st.plotly_chart(
        fig_feature,
        use_container_width=True
    )

    # ==================================================
    # Bug Analysis
    # ==================================================
    st.divider()
    st.subheader("🐞 Bug Analysis")

    fig_bug = px.bar(
        bug_df,
        x="Count",
        y="Bug",
        orientation="h",
        text="Count",
        template="plotly_dark",
        title="Most Reported Bugs"
    )

    fig_bug.update_layout(
        yaxis=dict(categoryorder="total ascending"),
        xaxis_title="Mentions",
        yaxis_title=""
    )

    st.plotly_chart(
        fig_bug,
        use_container_width=True
    )

    # ==================================================
    # Hot Topics
    # ==================================================
    st.divider()
    st.subheader("🔥 Hot Topics")

    fig_topic = px.bar(
        topic_df,
        x="Score",
        y="Topic",
        orientation="h",
        text_auto=".2f",
        template="plotly_dark",
        title="Top Discussion Topics"
    )

    fig_topic.update_layout(
        yaxis=dict(categoryorder="total ascending"),
        xaxis_title="TF-IDF Score",
        yaxis_title=""
    )

    fig_topic.update_yaxes(
        tickmode="linear",
        automargin=True
    )

    st.plotly_chart(
        fig_topic,
        use_container_width=True
    )