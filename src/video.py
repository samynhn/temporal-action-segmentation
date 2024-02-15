from pathlib import Path
from tqdm import tqdm
import pandas as pd
import cv2
import sys

FILE = Path(__file__).resolve()
ROOT = Path(FILE.parents[1]) #get root path ./TAS 
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  

def show_video_frames(video_path):
    # 打開影片
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    frame_count = 0

    while True:
        # 讀取下一幀
        ret, frame = cap.read()

        # 檢查是否成功讀取
        if not ret:
            break

        frame_count += 1

        # 將幀數顯示在畫面上
        cv2.putText(frame, f'Frame: {frame_count}', (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # 顯示幀
        cv2.imshow('Video', frame)

        # 按 'q' 鍵退出
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 釋放攝影機資源並關閉視窗
    cap.release()
    cv2.destroyAllWindows()

def save_video(input_video_path, groundTruth_path, output_video_path, cut=False, putText=True):

    df = pd.read_csv(groundTruth_path, header=None)
    # 打開影片
    cap = cv2.VideoCapture(input_video_path)

    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    # 獲取視頻的基本資訊
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    # 定義編碼器並創建 VideoWriter 物件
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 或者 'XVID'
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))

    # frame_count = 10452
    frame_count = 0 
    total_frames = get_total_frames(input_video_path)

    if cut == True:#如果要切割影片 就用groundTruth csv的長度當作進度條
        pbar = tqdm(total=len(df), desc="Processing Video")  # 初始化進度條 
    else:
        pbar = tqdm(total=total_frames, desc="Processing Video")  # 初始化進度條pbar = tqdm(total=len(df), desc="Processing Video")

    while True:
        # 讀取下一幀
        ret, frame = cap.read()

        # 檢查是否成功讀取
        if not ret:
            break
        frame_count += 1
        if frame_count <= len(df):
            action_name = df.loc[frame_count].item()
        else:
            if cut ==True:
                break
            else:
                action_name = None

        # 將幀數顯示在畫面上
        if putText == True:
            cv2.putText(frame, f'Frame: {frame_count}', (10, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            cv2.putText(frame, f'Action: {action_name}', (10, 60), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # 寫入幀到輸出文件
        out.write(frame)
        pbar.update(1)

        # 顯示幀（可選）
        # cv2.imshow('Video', frame)

        # 按 'q' 鍵退出（如果啟用了顯示）
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break

    # 釋放資源
    pbar.close()
    cap.release()
    out.release()
    cv2.destroyAllWindows()

def get_total_frames(video_path):
    # 打開影片檔案
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error: Could not open video.")
        return None

    # 獲取影片的總幀數
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # 釋放 VideoCapture 物件
    cap.release()

    return total_frames
# 使用範例
def get_percentage_of_each_action():
    game_start, game_end, rally_start, rally_end, playerA, playerB, break_ = range(7)
    actions = ["game_start", "game_end", "rally_start", "rally_end", "Player A", "Player B", "break"]
    df = pd.read_csv('groundtruth.csv', header=None)
    pbar = tqdm(total=len(df), desc="Processing Video")  # 初始化進度條

    for i in range(len(df)):
        if df.loc[i].item() == actions[0]:
            game_start +=1
        elif df.loc[i].item() == actions[1]:
            game_end +=1
        elif df.loc[i].item() == actions[2]:
            rally_start +=1
        elif df.loc[i].item() == actions[3]:
            rally_end +=1
        elif df.loc[i].item() == actions[4]:
            playerA +=1
        elif df.loc[i].item() == actions[5]:
            playerB +=1
        elif df.loc[i].item() == actions[6]:
            break_ +=1
        pbar.update(1)
    pbar.close()
    print("game_start: " , game_start/len(df)*100 , "%")
    print("game_end: " , game_end/len(df)*100 , "%")
    print("rally_start: " , rally_start/len(df)*100 , "%")
    print("rally_end: " , rally_end/len(df)*100 , "%")
    print("playerA: " , playerA/len(df)*100 , "%")
    print("playerB: " , playerB/len(df)*100 , "%")
    print("break: " , break_/len(df)*100 , "%")

# 使用範例
if __name__ == '__main__':
    frame_count = 0
    game_name = 'Kento_MOMOTA_CHOU_Tien_Chen_Fuzhou_Open_2019_Finals.mp4'
    game_base_path = str(ROOT)+'/data/'+game_name+'/'
    videoPath = game_base_path + game_name
    groundTruth_path = str(ROOT)+'/result/groundTruth/'+game_name+'_groundtruth.csv'
    output_video_path = str(ROOT)+'/result/video/'+game_name
    save_video(videoPath, groundTruth_path, output_video_path, cut=True, putText=False)