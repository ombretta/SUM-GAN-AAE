from os import listdir
import json
import numpy as np
import h5py
from generate_summary import generate_summary
from evaluation_metrics import evaluate_summary

paths = ['../model/reg05_lr5_i3d/TVSum/results/split0', \
         '../model/reg05_lr5_i3d/TVSum/results/split1', \
         '../model/reg05_lr5_i3d/TVSum/results/split2', \
        '../model/reg05_lr5_i3d/TVSum/results/split3', \
        '../model/reg05_lr5_i3d/TVSum/results/split4'] # path to the json files with the computed importance scores for each epoch

for path in [p for p in paths if "f_scores_gts.txt" not in listdir(p) and len(listdir(p))>90]:
    print(path)
    results = [r for r in listdir(path) if "f_scores" not in r and ".json" in r]
    results.sort(key=lambda video: int(video[6:-5]))
    PATH_TVSum = '../data/TVSum/tvsum_i3d_mixed5c_aligned.h5'
    eval_method = 'avg' # the proposed evaluation method for TVSum videos
    
    # for each epoch, read the results' file and compute the f_score
    f_score_epochs = []
    for epoch in results:
        print(epoch)
        all_scores = []
        with open(path+'/'+epoch) as f:
            data = json.loads(f.read())
            keys = list(data.keys())
    
            for video_name in keys:
                scores = np.asarray(data[video_name])
                all_scores.append(scores)
    
        all_gt_scores, all_shot_bound, all_nframes, all_positions = [], [], [], []
        with h5py.File(PATH_TVSum, 'r') as hdf:
            for video_name in keys:
                video_index = video_name[6:] 
                
                # Using ground truth scores instead of user summary
                gt_score = np.array( hdf.get('video_'+video_index+'/gtscore') )
                sb = np.array( hdf.get('video_'+video_index+'/change_points') )
                n_frames = np.array( hdf.get('video_'+video_index+'/n_frames') )
                positions = np.array( hdf.get('video_'+video_index+'/picks') )
                
                # print("gtscore", len(gt_score))
                # print("position", len(positions))
                all_gt_scores.append(gt_score)
                all_shot_bound.append(sb)
                all_nframes.append(n_frames)
                all_positions.append(positions)
    
        # generate summary based on the auto-generated scores
        all_summaries = generate_summary(all_shot_bound, all_scores, all_nframes, all_positions)
        
        # generate summary based on the ground-truth scores
        all_gt_summary = generate_summary(all_shot_bound, all_gt_scores, all_nframes, all_positions)
    
        all_f_scores = []
        
    	# Compare the resulting summary with the ground truth one, for each video
        for video_index in range(len(all_summaries)):
            summary = all_summaries[video_index]
            gt_summary = all_gt_summary[video_index]
            f_score = evaluate_summary(summary, np.expand_dims(gt_summary, axis=0), eval_method)	
            all_f_scores.append(f_score)
    
        f_score_epochs.append(np.mean(all_f_scores))
        print("f_score: ",np.mean(all_f_scores))
    
    with open(path+'/f_scores_gts.txt', 'w') as outfile:  
        json.dump(f_score_epochs, outfile)   
