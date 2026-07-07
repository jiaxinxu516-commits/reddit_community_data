import pandas as pd
import streamlit as st

@st.cache_data
def user_analysis(df):

    user_df = (
        df.groupby("author")
          .size()
          .reset_index(name="Messages")
          .sort_values("Messages", ascending=False)
    )

    return user_df