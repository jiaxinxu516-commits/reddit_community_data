import pandas as pd


def group_analysis(df):

    group_df = (
        df.groupby("group")
          .size()
          .reset_index(name="Messages")
          .sort_values("Messages", ascending=False)
    )

    return group_df