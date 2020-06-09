# -*- coding: utf-8 -*-

import torch
from torch.utils.data import Dataset, DataLoader
import h5py
import numpy as np
import json

class VideoData(Dataset):
    def __init__(self, mode, name, features_type, split_index):
        self.mode = mode
        self.name = name.lower() #'tvsum'
        self.features_type = features_type
        self.datasets = ['../data/SumMe/eccv16_dataset_summe_google_pool5.h5',
                         '../data/TVSum/eccv16_dataset_tvsum_google_pool5.h5',
                         '../data/SumMe/summe_i3d_mixed5c.h5',
                         '../data/SumMe/tvsum_i3d_mixed5c.h5']
        self.splits_filename = ['../data/splits/' + self.name + '_splits.json']
        self.splits = []
        self.split_index = split_index # it represents the current split (varies from 0 to 4)
        temp = {}

        if 'summe' in self.splits_filename[0]:
            if features_type == "google":
                self.filename = self.datasets[0]
            if features_type == "i3d":
                self.filename = self.datasets[2]
        elif 'tvsum' in self.splits_filename[0]:
            if features_type == "google":
                self.filename = self.datasets[1]
            if features_type == "i3d":
                self.filename = self.datasets[3]
        self.video_data = h5py.File(self.filename, 'r')

        with open(self.splits_filename[0]) as f:
            data = json.loads(f.read())
            for split in data:
                temp['train_keys'] = split['train_keys']
                temp['test_keys'] = split['test_keys']
                self.splits.append(temp.copy())

    def __len__(self):
        self.len = len(self.splits[0][self.mode+'_keys'])
        return self.len

    # In "train" mode it returns the features; in "test" mode it also returns the video_name
    def __getitem__(self, index):
        video_name = self.splits[self.split_index][self.mode + '_keys'][index]
        frame_features = torch.Tensor(np.array(self.video_data[video_name + '/features']))
        if self.mode == 'test':
            return frame_features, video_name
        else:
            return frame_features


def get_loader(mode, name, features_type, split_index):
    if mode.lower() == 'train':
        vd = VideoData(mode, name, features_type, split_index)
        return DataLoader(vd, batch_size=1)
    else:
        return VideoData(mode, name, features_type, split_index)


if __name__ == '__main__':
    pass
