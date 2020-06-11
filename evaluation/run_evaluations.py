#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 16:23:33 2020

@author: ombretta
"""

import os
import math 

video_types = ["TVSum", "SumMe"]

features_type = "i3d" #"google"

regularization_factors = [0.05, 0.1, 0.15, 0.3, 0.5]

lr = 1e-5

for video_type in video_types:
    
    for regularization_factor in regularization_factors:
        
        str_regularization_factors = str(regularization_factor).replace(".","")
        str_lr = str(int(abs(math.log10(lr))))
        save_dir = "reg"+str_regularization_factors+"_lr"+str_lr+"_"+features_type
        os.system("python check_fscores_tvsum_with_gts.py " + save_dir)
        os.system("python check_fscores_tvsum.py " + save_dir)
        os.system("python check_fscores_summe_with_gts.py " + save_dir)
        os.system("python check_fscores_summe.py " + save_dir)

