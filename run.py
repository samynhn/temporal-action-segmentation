from pathlib import Path
import logging
import json
import sys
import os

FILE = Path(__file__).resolve()
ROOT = Path(FILE.parents[0]) #get root path ./TAS 
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  

logging.basicConfig(level=logging.INFO)

import src.groundTruth as groundTruth # groundTruth.py
import src.cut_frame as cut_frame # cut_frame.py
import src.video as video # video.py

if __name__ == "__main__":
    with open(str(ROOT)+'/data/data.json', 'r', encoding='utf-8') as json_file:
        json_data = json.load(json_file)

    # 使用for循環遍歷每個video對象
    for game_info in json_data:
        game_id = game_info["id"]
        game_name = game_info["video"]
        remained_lines = game_info["cut"]

        rallySeg_name = "RallySeg.csv"
        game_base_path = str(ROOT)+'/data/'+game_name+'/'
        groundTruth_path = str(ROOT)+'/result/groundTruth/'+'groundTruth_'+game_name+'.csv'
        videoPath = game_base_path + game_name

        setFile_names =['label/set1.csv', 'label/set2.csv', 'label/set3.csv']
        for setFile_name in setFile_names:
            setFile_path = os.path.join(game_base_path, setFile_name)
            if not os.path.exists(setFile_path):
                setFile_names.remove(setFile_name)
        setFiles_path = [os.path.join(game_base_path, setFile_name) for setFile_name in setFile_names]

        actions = ["break", "break", "rally_start", "rally_end", "playerA", "playerB", "break"]
        target = "break"
        output_video_path = str(ROOT)+'/result/video/'+str(remained_lines)+'_'+game_name
        cut_groundTruth_path = str(ROOT)+'/result/groundTruth/'+str(remained_lines)+'_cut_groundTruth_'+game_name+'.csv'

        logging.info("Start getting groundTruth: {}".format(game_name))
        groundTruth.get_groundTruth(setFiles_path, game_base_path, groundTruth_path, videoPath, rallySeg_name, actions)

        logging.info("Start cutting groundTruth: {}".format(game_name))
        cut_frame.cut_groundTruth(groundTruth_path, remained_lines, cut_groundTruth_path, target)

        logging.info("Start saving video: {}".format(game_name))
        video.save_video(videoPath, cut_groundTruth_path, output_video_path, cut=True, putText=False)