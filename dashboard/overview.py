import streamlit as st

def show_overview(df, activity, source):

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
        c4.metric(
            "Avg Messages/User",
            round(activity["posts"]/activity["users"],2)
        )