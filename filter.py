import pandas as pd
import numpy as np

filename = 'data.csv'
selected_columns = ['rally','frame_num','player', 'getpoint_player']
# NOTE: 有參考價值的欄位：rally, ball_round, time, roundscore_A, roundscore_B, player, type, lose_reason, win_reason, getpoint_player, flaw, db

# columns_to_drop = ['']

output_file = 'result/result.csv'


def extract_columns(df, columns_to_keep):
    new_df = df[columns_to_keep]
    return new_df

def save_to_csv(filename, data):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)

def drop_columns(df, columns_to_drop):
    new_df = df.drop(columns=columns_to_drop)
    return new_df

def segment(df):
    # init
    new_df = df.copy()
    new_df.insert(0, 'rally_bool', np.nan)
    new_df.insert(1, 'rally_player', np.nan)

    flag = False # 回合結束時切換為1
    rally_bool = False
    rally_player = new_df.loc[0]["player"] # 以第一個球的發球者當作該回合擁有者

    for index, row in new_df.iterrows():
        if flag :
            rally_bool = switch(rally_bool)
            rally_player = row['player']        

        new_df.at[index, 'rally_bool'] = rally_bool
        new_df.at[index, 'rally_player'] = rally_player

        if not pd.isna(row['getpoint_player']):  # 如果getpoint_player有值 代表此回合要結束了 新回合開始
            flag = True # 切換回合 並在下次迴圈開始時寫入
        else:
            flag = False

    return new_df


def rally_count(df):
    # init
    new_df = df.copy()
    new_df.insert(0, 'rally_count', np.nan)

    flag = False # 
    rally_count = 1

    for index, row in new_df.iterrows():
        if flag :
            rally_count += 1

        new_df.at[index, 'rally_count'] = str(rally_count)
        if index + 1 < len(df):
            next_row = df.iloc[index + 1]  # 获取下一行
            if not pd.isna(next_row['rally']):  # 如果rally_count有值 
                if next_row['rally'] != row['rally']:
                    flag = True # 切換回合 並在下次迴圈開始時寫入
                else:
                    flag = False

    return new_df


org_df = pd.read_csv(filename)
new_df_with_extract_columns = extract_columns(org_df, selected_columns)
segment_df = rally_count(new_df_with_extract_columns)
save_to_csv(output_file, segment_df)

# NOTE:
# 增加start, progress, end
# True/False法 好像不太好
# 遺失的frame 要補上
