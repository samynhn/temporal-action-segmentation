"""
Description:
    Calculate:
        - The percentage of each action label in the ground truth.
        - The number of each action label in the ground truth.
        - The sequence of each action label in the ground truth.
Example:
    # Output
    total: action1: 20.0%, action2: 30.0%, action3: 50.0%
    seq: [(action1,30), (action2,20), (action3,50), (action1,40), ...]
"""
from collections import defaultdict
from pathlib import Path
from tqdm import tqdm
import pandas as pd
import numpy as np
import cv2
import csv
import sys
import os

FILE = Path(__file__).resolve()
ROOT = Path(FILE.parents[1]) #get root path ./TAS 
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  

groundTruth_name = "15000_cut_groundTruth_Anthony_Sinisuka_GINTING_CHOU_Tien_Chen_Hong_Kong_Open_2019_Quarter_Finals.mp4.csv"
groundTruth_path = ROOT / "result" / "groundTruth" / groundTruth_name

def count_actions(csv_file_path):
    action_counts = defaultdict(int)

    with open(csv_file_path, mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        
        next(csv_reader, None)
        
        for row in csv_reader:
            action_label = row[0]  
            action_counts[action_label] += 1 

    action_counts = count_actions(groundTruth_path)

    print("動作標籤統計結果：")
    for action, count in action_counts.items():
        print(f'{action}: {count}個')

def count_sequential_actions(csv_file_path):
    action_sequence = []
    # 開啟CSV檔案並讀取
    with open(csv_file_path, mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        
        # 跳過標題行（如果有的話）
        next(csv_reader, None)
        
        # 初始化前一個標籤和計數器
        prev_label = None
        count = 1
        
        # 逐行讀取CSV檔案
        for row in csv_reader:
            # 如果前一個標籤是"Player A"或"Player B"，則將它們視為同一個標籤
            if row[0] == "Player A" or row[0] == "Player B":
                current_label = "PlayerA&B"
            else:
                current_label = row[0]  # 假設動作標籤在每行的第一個欄位

            if current_label == prev_label:
                count += 1  # 如果當前標籤和前一個標籤相同，則累加計數器
            else:
                # 如果遇到不同的標籤，且前一個標籤不為None，則將前一個標籤和它的計數加入列表
                if prev_label is not None:
                    action_sequence.append((prev_label, count))

                prev_label = current_label  # 更新前一個標籤為當前標籤
                count = 1  # 重置計數器

        # 確保最後一個標籤和它的計數也被加入列表
        if prev_label is not None:
            action_sequence.append((prev_label, count))
    
    sequential_actions = count_sequential_actions(groundTruth_path)

    # 打印結果
    for action, count in sequential_actions:
        print(f'({action}, {count})')