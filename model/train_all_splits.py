#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 16:23:33 2020

@author: ombretta
"""

import os
import math 
import shutil

def prepare_folder(save_dir, video_type):
    if not os.path.exists("./"+save_dir): os.mkdir("./"+save_dir)
    if not os.path.exists("./"+save_dir+"/"+video_type): 
        os.mkdir("./"+save_dir+"/"+video_type)
    for sub_folder in ["/logs", "/results", "/models"]:
        if not os.path.exists("./"+save_dir+"/"+video_type+"/"+sub_folder): 
            os.mkdir("./"+save_dir+"/"+video_type+sub_folder)
        for split_index in range(5):
            if not os.path.exists("./"+save_dir+"/"+video_type+sub_folder+"/split"+str(split_index)):
                os.mkdir("./"+save_dir+"/"+video_type+sub_folder+"/split"+str(split_index))
            if sub_folder == "/results":
                shutil.copy("./exp0/"+video_type+"/results/split0/"+video_type+"_-1.json", \
                            "./"+save_dir+"/"+video_type+"/results/split"+str(split_index)+"/")         

text = "#!/bin/sh\n\
#SBATCH --partition=general\n\
#SBATCH --qos=long\n\
#SBATCH --time=6:00:00\n\
#SBATCH --ntasks=1\n\
#SBATCH --cpus-per-task=2\n\
#SBATCH --mem=16000\n\
#SBATCH --gres=gpu:1\n\
module use /opt/insy/modulefiles\n\
module load cuda/10.0 cudnn/10.0-7.6.0.64\n\
srun python main.py --split_index= "

video_types = ["TVSum", "SumMe"]

features_type = "i3d" #"google"

regularization_factors = [0.05, 0.1, 0.15, 0.3]

lr = 1e-5

for video_type in video_types:
    
    for regularization_factor in regularization_factors:
        
        str_regularization_factors = str(regularization_factor).replace(".","")
        str_lr = str(int(abs(math.log10(lr))))
        save_dir = "reg"+str_regularization_factors+"_lr"+str_lr+"_"+features_type
        
        prepare_folder(save_dir, video_type)
        
        for split_index in range(5):
            full_text = text + str(split_index) + " --video_type=" + video_type + \
            " --features_type=" + features_type + " --regularization_factor=" + \
            str(regularization_factor) + " --lr=" + str(lr) + " --save_dir=" + \
            save_dir
            
            print(full_text)
            
            filename = video_type + str(split_index) + ".sbatch"
        
            with open(filename, "w") as file:
                file.write(full_text)
        
            os.system("sbatch " + filename)
