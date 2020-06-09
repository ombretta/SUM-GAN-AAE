#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  5 13:39:50 2020

@author: ombretta
"""

from matplotlib import pyplot as plt
import numpy as np

dataset = "SumMe"

f_scores = {}
f_scores_gts = {}

for score in ["f_scores", "f_scores_gts"]:
    
    average_scores = [0 for i in range(100)]
    
    figure = plt.figure(score)
    for split in range(5):
        fscores_path = "../model/exp0/"+dataset+"/results/split"+str(split)+"/"+score+".txt"
        
        with open(fscores_path, "r") as f:
            scores_per_epoch = f.read()
        scores_per_epoch = [float(s) for s in scores_per_epoch[1:-1].split(", ")]
        print("Split", score, str(split), str(round(max(scores_per_epoch), 2)), "at epoch", np.argmax(scores_per_epoch)+1)
        
        for i in range(100): average_scores[i] += scores_per_epoch[i] 
        
        plt.plot(scores_per_epoch)
    
    print("Average", score, str(round(max(average_scores)/5, 2)), "at epoch", np.argmax(average_scores)+1)
    plt.plot([a/5 for a in average_scores])

    plt.legend(["split " + str(i) for i in range(5)]+["average"])    
    plt.title(dataset+" - "+score)
    plt.xlabel("epoch")
    plt.ylabel("f-score")
    plt.savefig("../model/exp0/"+dataset+"/results/"+score+".png")