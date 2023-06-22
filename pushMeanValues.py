import pandas as pd

def pushMeanValues(df, colList):
    """Fill missing values in the dataset with mean values"""
    df = df[colList]
    # df['time stamp'] = pd.to_datetime(df['time stamp'])
    df_new = pd.DataFrame(columns = df.columns)
    len_df = len(df)
    df_new.loc[0] = df.loc[0] # df_new.append(df.loc[0])
    new_ind = 0
    for i in range(1, len_df):
        diff_minute = (df.iloc[i]['time stamp'].hour - df.iloc[i - 1]['time stamp'].hour) \
            * 60 + df.iloc[i]['time stamp'].minute - df.iloc[i - 1]['time stamp'].minute
        diff_day = df.iloc[i]['time stamp'].day - df.iloc[i - 1]['time stamp'].day
        if diff_day > 0 or diff_minute == 1:
            new_ind += 1
            df_new.loc[new_ind] = df.iloc[i]
        else:
            df_diff = (df.iloc[i] - df.iloc[i - 1]) / int(diff_minute)
            df_diff['volume'] = int(df_diff['volume'])
            for j in range(diff_minute):
                new_ind += 1
                df_new.loc[new_ind] = df_new.loc[new_ind - 1] + df_diff
    return df_new