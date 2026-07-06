import streamlit as st
import plotly.express as px
import pandas as pd


def wechat_dashboard(df, activity, group_df, user_df, user_sentiment_df):

    st.divider()
    st.header("💬 WeChat Community Analysis")

    # ==================================================
    # Top Active Users
    # ==================================================

    st.subheader("👤 Top Active Users")

    display_df = user_df.copy()

    display_df["display_name"] = (
        display_df["author"]
        .astype(str)
        .str.slice(0, 10)
    )

    fig_user = px.bar(
        display_df.head(20),
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

    if user_sentiment_df is not None:

        st.subheader("😊 User Sentiment Ranking")

        st.dataframe(
            user_sentiment_df[
                [
                    "author",
                    "Positive %",
                    "Neutral %",
                    "Negative %",
                    "Sentiment Score"
                ]
            ],
            width="stretch"
        )

    else:
        st.info("Enable 'Run Sentiment Analysis' to view user sentiment.")

    # ==================================================
    # Group Users
    # ==================================================

    group_users = (
        df.groupby("group")["author"]
        .nunique()
        .reset_index(name="Users")
    )

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("💬 Messages by Group")

        fig_group = px.bar(
            group_df,
            x="Messages",
            y="group",
            orientation="h",
            text="Messages",
            template="plotly_dark"
        )

        fig_group.update_layout(
            height=max(350, len(group_df) * 45),
            yaxis=dict(
                categoryorder="total ascending"
            )
        )

        fig_group.update_yaxes(
            tickmode="linear",
            automargin=True
        )

        st.plotly_chart(
            fig_group,
            use_container_width=True
        )

    with col2:

        st.subheader("👥 Users by Group")

        fig_users = px.bar(
            group_users,
            x="Users",
            y="group",
            orientation="h",
            text="Users",
            template="plotly_dark"
        )

        fig_users.update_layout(
            height=max(350, len(group_users) * 45),
            yaxis=dict(
                categoryorder="total ascending"
            )
        )

        fig_users.update_yaxes(
            tickmode="linear",
            automargin=True
        )

        st.plotly_chart(
            fig_users,
            use_container_width=True
        )

    # ==================================================
    # Messages Over Time
    # ==================================================

    st.divider()
    st.subheader("📈 Messages Over Time")

    fig = px.bar(
        activity["posts_per_day"],
        x="created_date",
        y="Posts",
        template="plotly_dark",
        title="Daily Messages"
    )

    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Messages",
        hovermode="x unified"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )