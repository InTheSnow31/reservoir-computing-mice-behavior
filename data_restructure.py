import pandas as pd
from rich import print
from pygame_display import *
def import_data(dataset_name, dataset_sample):
    data_tracking = pd.read_parquet("data/train_tracking/"+dataset_name+"/"+dataset_sample+".parquet")
    data_annotation = pd.read_parquet("data/train_annotation/"+dataset_name+"/"+dataset_sample+".parquet")

    N_TIMEFRAME = 1000

    timeframes = {}
    for index, row in data_tracking.iterrows():
        if row.video_frame > N_TIMEFRAME :
            break
        if row.bodypart == "body_center":
            data = {"x": row.x, "y": row.y,"action":None}
            if row.video_frame not in timeframes :
                timeframes[row.video_frame] = {}
            timeframes[row.video_frame][row.mouse_id] = data

    #all_actions = []
    for index, row in data_annotation.iterrows():
        #if row.action not in all_actions :
        #    all_actions.append(row.action)
        if row.start_frame > N_TIMEFRAME :
            break
        for frame in range(row.start_frame, row.stop_frame+1):
            if frame in timeframes : 
                if row.agent_id in timeframes[frame]:
                    timeframes[frame][row.agent_id]['action'] = row.action
    return timeframes

AdaptableSnail_dataset = import_data("AdaptableSnail", "44566106")
display(AdaptableSnail_dataset, "AdaptableSnail", "44566106")
    