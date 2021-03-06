from os import listdir
import sys
import json
import numpy as np
import h5py
from generate_summary import generate_summary
from evaluation_metrics import evaluate_summary

results_folder = str(sys.argv[1])

paths = ['../model/'+results_folder+'/SumMe/results/split0', \
         '../model/'+results_folder+'/SumMe/results/split1', \
         '../model/'+results_folder+'/SumMe/results/split2', \
        '../model/'+results_folder+'/SumMe/results/split3', \
        '../model/'+results_folder+'/SumMe/results/split4'] # path to the json files with the computed importance scores for each epoch

for path in [p for p in paths if "f_scores.txt" not in listdir(p) and len(listdir(p))>90]:
    print(path)
    results = [r for r in listdir(path) if "f_scores" not in r and ".json" in r]
    results.sort(key=lambda video: int(video[6:-5]))
    # PATH_SumMe = '../data/SumMe/eccv16_dataset_summe_google_pool5.h5'
    PATH_SumMe = '../data/SumMe/summe_i3d_mixed5c_aligned.h5'
    eval_method = 'max' # the proposed evaluation method for SumMe videos
    
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
    
        all_user_summary, all_shot_bound, all_nframes, all_positions = [], [], [], []
        with h5py.File(PATH_SumMe, 'r') as hdf:
            for video_name in keys:
                video_index = video_name[6:]
                
                #print(video_name, video_index)
                
                user_summary = np.array( hdf.get('video_'+video_index+'/user_summary') )
                sb = np.array( hdf.get('video_'+video_index+'/change_points') )
                n_frames = np.array( hdf.get('video_'+video_index+'/n_frames') )
                positions = np.array( hdf.get('video_'+video_index+'/picks') )
    
                all_user_summary.append(user_summary)
                all_shot_bound.append(sb)
                all_nframes.append(n_frames)
                all_positions.append(positions)
    
                #print(n_frames)
                
        all_summaries = generate_summary(all_shot_bound, all_scores, all_nframes, all_positions)
    
        all_f_scores = []
    	# compare the resulting summary with the ground truth one, for each video
        for video_index in range(len(all_summaries)):
            summary = all_summaries[video_index]
            user_summary = all_user_summary[video_index]
            f_score = evaluate_summary(summary, user_summary, eval_method)	
            all_f_scores.append(f_score)
    
        f_score_epochs.append(np.mean(all_f_scores))
        print("f_score: ",np.mean(all_f_scores))
    
    with open(path+'/f_scores.txt', 'w') as outfile:  
        json.dump(f_score_epochs, outfile)
