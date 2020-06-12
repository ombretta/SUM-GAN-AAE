import os
import math 

video_types = ["TVSum", "SumMe"]

features_type = "i3d" #"google"

regularization_factors = [0.05, 0.1, 0.15, 0.3, 0.5]

learning_rates = [1e-4, 1e-5]

for video_type in video_types:
    
    for regularization_factor in regularization_factors:
        
        for lr in learning_rates:
            str_regularization_factors = str(regularization_factor).replace(".","")
            str_lr = str(int(abs(math.log10(lr))))
            save_dir = "reg"+str_regularization_factors+"_lr"+str_lr+"_"+features_type
            os.system("python plot_fscores.py " + save_dir + " " + video_type)

