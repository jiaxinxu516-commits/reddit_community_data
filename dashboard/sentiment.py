import streamlit as st
import plotly.express as px


def sentiment_dashboard(sentiment):

    sentiment_summary = sentiment["summary"]

    st.divider()
    st.header("🧠 Community Sentiment")

    # ==================================================
    # KPI
    # ==================================================
    positive = sentiment_summary.loc[
        sentiment_summary["Sentiment"] == "positive",
        "Count"
    ].sum()

    neutral = sentiment_summary.loc[
        sentiment_summary["Sentiment"] == "neutral",
        "Count"
    ].sum()

    negative = sentiment_summary.loc[
        sentiment_summary["Sentiment"] == "negative",
        "Count"
    ].sum()

    c1, c2, c3 = st.columns(3)

    c1.metric("😊 Positive", positive)
    c2.metric("😐 Neutral", neutral)
    c3.metric("😞 Negative", negative)

    # ==================================================
    # Pie Chart
    # ==================================================

    color_map = {
        "positive": "#00cc96",
        "neutral": "#636efa",
        "negative": "#ff4b4b"
    }

    fig_pie = px.pie(
        sentiment_summary,
        names="Sentiment",
        values="Count",
        color="Sentiment",
        color_discrete_map=color_map,
        template="plotly_dark",
        title="Sentiment Distribution"
    )

    st.plotly_chart(
        fig_pie,
        use_container_width=True
    )

    # ==================================================
    # Timeline
    # ==================================================

    if "timeline" in sentiment:

        st.subheader("📈 Weekly Sentiment Trend")

        fig_line = px.line(
            sentiment["timeline"],
            x="week",
            y="Count",
            color="sentiment",
            markers=True,
            template="plotly_dark"
        )

        st.plotly_chart(
            fig_line,
            use_container_width=True
        )

    # ==================================================
    # Negative Posts
    # ==================================================

    if "negative_posts" in sentiment:

        st.subheader("🚨 Top Negative Posts")

        st.dataframe(
            sentiment["negative_posts"].head(10),
            use_container_width=True,
            hide_index=True
        )