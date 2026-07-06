import streamlit as st


def report_dashboard(
    summary,
    community,
    product=None,
    qa=None,
    source="reddit"
):
    """
    Display AI-generated reports
    """

    st.divider()
    st.header("🤖 AI Reports")

    # ==========================
    # AI Summary
    # ==========================

    st.subheader("📋 AI Community Summary")
    st.markdown(summary)

    # ==========================
    # Community Report
    # ==========================

    st.subheader("📅 Community Report")
    st.markdown(community)

    # ==========================
    # Reddit Only
    # ==========================

    if source == "reddit":

        if product is not None:

            st.subheader("🚀 Product Report")
            st.markdown(product)

        if qa is not None:

            st.subheader("🐞 QA Report")
            st.markdown(qa)