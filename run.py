import sys
import os
from pathlib import Path

FILE = Path(__file__).resolve()
ROOT = Path(FILE.parents[0]) #get root path ./TAS 
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  

import src.groundTruth as groundTruth # groundTruth.py
import src.cut_frame as cut_frame # cut_frame.py
import src.video as video # video.py

if __name__ == "__main__":
    game_name = 'Kento_MOMOTA_CHOU_Tien_Chen_Fuzhou_Open_2019_Finals.mp4'
    rallySeg_name = "RallySeg.csv"
    game_base_path = str(ROOT)+'/data/'+game_name+'/'
    groundTruth_path = str(ROOT)+'/result/groundTruth/'+'groundTruth_'+game_name+'.csv'
    videoPath = game_base_path + game_name
    setFile_names = ['label/set1.csv', 'label/set2.csv', 'label/set3.csv']
    setFiles_path = [os.path.join(game_base_path, setFile_name) for setFile_name in setFile_names]
    actions = ["break", "break", "rally_start", "rally_end", "playerA", "playerB", "break"]

    remained_lines = 15000
    target = "break"

    output_video_path = str(ROOT)+'/result/video/'+str(remained_lines)+'_'+game_name
    cut_groundTruth_path = str(ROOT)+'/result/groundTruth/'+str(remained_lines)+'_cut_groundTruth_'+game_name+'.csv'

    groundTruth.get_groundTruth(setFiles_path, game_base_path, groundTruth_path, videoPath, rallySeg_name, actions)
    cut_frame.cut_groundTruth(groundTruth_path, remained_lines, cut_groundTruth_path, target)
    video.save_video(videoPath, cut_groundTruth_path, output_video_path, cut=True, putText=True)