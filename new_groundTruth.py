#NOTE: change actions = ["game_start", "game_end", "rally_start", "rally_end", "playerA", "playerB", "break"] to actions = ["rally_start", "rally_end", "playerA", "playerB", "break"]
import pandas as pd
import numpy as np
import os
import cv2
import csv
import video # video.py
from tqdm import tqdm
game_name = 'Kento_MOMOTA_CHOU_Tien_Chen_Fuzhou_Open_2019_Finals.mp4'
base_path = './data/'+game_name+'/'
actions = ["break", "break", "rally_start", "rally_end", "playerA", "playerB", "break"]
groundTruth_path = './'+game_name+'groundtruth.csv'

frame_count = 0
#get path
setFile_names = ['label/set1.csv', 'label/set2.csv', 'label/set3.csv']
rallySeg_name = "RallySeg.csv"
setFiles_path = [os.path.join(base_path, setFile_name) for setFile_name in setFile_names]

def merge_setFiles(files):
    return pd.concat((pd.read_csv(file) for file in files), ignore_index=True)

def rally_count(df):
    # init
    new_df = df.copy()
    new_df.insert(0, 'rally_count', np.nan)

    flag = False # 
    rally_count = 1

    for index, row in new_df.iterrows():
        if flag :
            rally_count += 1

        new_df.at[index, 'rally_count'] = rally_count
        if index + 1 < len(df):
            next_row = df.iloc[index + 1]  # 获取下一行
            if not pd.isna(next_row['rally']):  # 如果rally_count有值 
                if next_row['rally'] != row['rally']:
                    flag = True # 切換回合 並在下次迴圈開始時寫入
                else:
                    flag = False

    return new_df

def write_actions_to_csv(setFiles_df_with_rally_count, rallySeg_df, total_frame_num, file_name, current_frame_num=1):
    pbar = tqdm(total=total_frame_num)
    first_frame = rallySeg_df.iloc[0]["Start"]
    last_frame = rallySeg_df.iloc[-1]["End"]


    with open(file_name, mode='w', newline='') as file:
        writer = csv.writer(file)
        
        # # 寫入列標題（如果需要）
        # writer.writerow(['Value'])

        # 從 start_value 開始寫入數值，直到達到或超過 max_value
        i,j=0,0
        while current_frame_num <= total_frame_num:
            #DONE:
                #此時frame number < 第一個 RallySeg Start 的frame number : 設定為game start
                #此時frame number > 最後一個 RallySeg Start 的frame number : 設定為game end

            #TODO:
                #set中的frame number >此時frame number > RallySeg Start 的frame number : 設定為rally start
                #set中的frame number <此時frame number < RallySeg Start 的frame number : 設定為rally end

                #讀取set中的A,B player
                #此時frame number 在RallySeg 範圍外 : 設定為Break
            first_exit_rally = False #讓一開始沒進while 也不會進if   
            current_rally_num = i+1 #rallySeg_df的index=0開始 但是rally_count=1開始
            #找出目前rally中 第一個row 和 最後一個row

            if(current_frame_num < first_frame): 
                writer.writerow([actions[0]]) #game_start
                current_frame_num += 1 
                pbar.update(1)
            elif(current_frame_num > last_frame):
                writer.writerow([actions[1]]) #game_end
                current_frame_num += 1 
                pbar.update(1)
            else:
                current_rally_df = setFiles_df_with_rally_count[setFiles_df_with_rally_count['rally_count'] == current_rally_num]
                first_row_in_current_rally = current_rally_df.iloc[0]
                last_row_in_current_rally = current_rally_df.iloc[-1]
                # if(current_rally_num==2):
                #     print("i=" , i)
                #     print("current_frame_num: ", current_frame_num)
                #     print("current_rally_num: ", current_rally_num)
                #     print("first_row_in_current_rally: ", first_row_in_current_rally)
                #     print("last_row_in_current_rally: ", last_row_in_current_rally)
                #     break
                index_of_current_rally_df = 0    

                while(current_frame_num >= rallySeg_df.iloc[i]["Start"] and current_frame_num <= rallySeg_df.iloc[i]["End"]): # in rally
                    first_exit_rally = True #之後出while時候 會進if
                    #進到rally範圍內 用current_rally_num check
                    if(current_frame_num < first_row_in_current_rally["frame_num"]): #rally範圍內 但是不在set範圍內
                        writer.writerow([actions[2]])  #rally_start
                    elif(current_frame_num > last_row_in_current_rally["frame_num"]):
                        writer.writerow([actions[3]]) 
                    else:
                        if(len(current_rally_df)>index_of_current_rally_df+1): #同rally內還沒到最後一個row
                            if(current_frame_num < current_rally_df.iloc[index_of_current_rally_df+1]["frame_num"]):
                                player = current_rally_df.iloc[index_of_current_rally_df]["player"]
                                writer.writerow(["Player " + str(player)])
                            else:
                                index_of_current_rally_df += 1
                                player = current_rally_df.iloc[index_of_current_rally_df]["player"]
                                writer.writerow(["Player " + str(player)])
                        else:
                            player = current_rally_df.iloc[index_of_current_rally_df]["player"]
                            writer.writerow(["Player " + str(player)])
                    
                    current_frame_num += 1
                    pbar.update(1)

                else:
                    writer.writerow([actions[6]]) #break  不在rally範圍內表示break i+=1後也可能不會in rally 就表示繼續
                    if(first_exit_rally): #當連續兩個break時候，i不會+1 不然一直往下看rally
                        i+=1 #當if成立時候 i 不能動 ，直到不在該rally範圍內才換下一個rally 所以i才要+1
                    first_exit_rally = False
                    current_frame_num += 1 
                    pbar.update(1)
    pbar.close()

def __init__():
# setFiles_df, rallySeg_df
    setFiles_df = merge_setFiles(setFiles_path)

    setFiles_df_with_rally_count = rally_count(setFiles_df)
    rallySeg_df = pd.read_csv(os.path.join(base_path, rallySeg_name))

    # setFiles_df_with_rally_count.to_csv('new_df.csv', index=False) #新增rally_count欄位 用於後續判斷是否在rally範圍內

    total_frame_num = video.get_total_frames(video.videoPath)
    
    # 使用範例
    write_actions_to_csv(setFiles_df_with_rally_count, rallySeg_df, total_frame_num, groundTruth_path)

if __name__ == "__main__":
    __init__()
