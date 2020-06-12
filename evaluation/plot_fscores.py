#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  5 13:39:50 2020

@author: ombretta
"""

import sys
import os
from matplotlib import pyplot as plt
import numpy as np

folder = str(sys.argv[1])
dataset = str(sys.argv[2])

print(folder, dataset)

f_scores = {}
f_scores_gts = {}

for score in ["f_scores", "f_scores_gts"]:
    
    valid_splits = [] # Count how many splits have valid fscore files
    average_scores = [0 for i in range(100)]
    
    figure = plt.figure(score)
    for split in range(5):
        fscores_path = "../model/"+folder+"/"+dataset+"/results/split"+str(split)+"/"+score+".txt"
        
        if os.path.exists(fscores_path):
            valid_splits.appen(split)
            with open(fscores_path, "r") as f:
                scores_per_epoch = f.read()
            scores_per_epoch = [float(s) for s in scores_per_epoch[1:-1].split(", ")]
            print("Split", score, str(split), str(round(max(scores_per_epoch), 2)), "at epoch", np.argmax(scores_per_epoch)+1)
            
            for i in range(len(scores_per_epoch[1:])): average_scores[i] += scores_per_epoch[i]
            
            plt.plot(scores_per_epoch)
    
    print("Average", score, str(round(max(average_scores)/len(valid_splits), 2)), "at epoch", np.argmax(average_scores)+1)
    plt.plot([a/len(valid_splits) for a in average_scores])

    plt.legend(["split " + str(i) for i in valid_splits]+["average"])    
    plt.title(dataset+" - "+score)
    plt.xlabel("epoch")
    plt.ylabel("f-score")
    plt.savefig("../model/"+folder+"/"+dataset+"/results/"+score+".png")