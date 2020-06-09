#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 16:23:33 2020

@author: ombretta
"""

import os

text = "#!/bin/sh\n\
#SBATCH --partition=general\n\
#SBATCH --qos=short\n\
#SBATCH --time=4:00:00\n\
#SBATCH --ntasks=1\n\
#SBATCH --cpus-per-task=2\n\
#SBATCH --mem=32000\n\
#SBATCH --gres=gpu:1\n\
module use /opt/insy/modulefiles\n\
module load cuda/10.0 cudnn/10.0-7.6.0.64\n\
srun python main.py --split_index "

video_types = ["TVSum", "SumMe"]

features_type = "i3d", #"google"

regularization_factor = 0.5

for video_type in video_types:
    for split_index in range(5):
        full_text = text + str(split_index) + " --video_type=" + video_type + \
        " --features_type=" + features_type + " --regularization_factor=" + \
        str(regularization_factor)
    
        print(full_text)
        
        filename = video_type + str(split_index) + ".sbatch"
    
        with open(filename, "w") as file:
            file.write(full_text)
    
        os.system("sbatch " + filename)
