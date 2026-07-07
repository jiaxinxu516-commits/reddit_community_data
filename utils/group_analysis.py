import pandas as pd
import streamlit as st

@st.cache_data
def group_analysis(df):

    group_df = (
        df.groupby("group")
          .size()
          .reset_index(name="Messages")
          .sort_values("Messages", ascending=False)
    )

    return group_df