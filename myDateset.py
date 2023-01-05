import os
from copy import deepcopy
from functools import partial
from glob import glob
from hashlib import sha1
from typing import Callable, Iterable, Optional, Tuple

import cv2
import numpy as np
from glog import logger
from joblib import Parallel, cpu_count, delayed
from skimage.io import imread
from torch.utils.data import Dataset
from tqdm import tqdm
import yaml

import aug


class MyDataset(Dataset):
    def __init__(self, config, transform_fn: Callable,
                 normalize_fn: Callable,
                 corrupt_fn: Optional[Callable] = None,
                 verbose=True):
        self.config = config
        self.b, self.s = self.get_path()
        self.transform_fn = transform_fn
        self.normalize_fn = normalize_fn
        self.corrupt_fn = corrupt_fn
        self.verbose = verbose

    def __len__(self):
        return len(self.b)

    def __getitem__(self, idx):
        img_blur = cv2.imread(self.b[idx])
        img_sharp = cv2.imread(self.s[idx])
        return img_blur, img_sharp

    def get_path(self):
        dataset_base_path = self.config['files_a']
        train_file_list = os.listdir(dataset_base_path)
        blur_img_path_list = []
        sharp_img_path_list = []
        for i in range(len(train_file_list)):
            base_img_path = os.path.join(dataset_base_path, train_file_list[i])
            blur_img_path = os.path.join(base_img_path, 'blur')
            sharp_img_path = os.path.join(base_img_path, 'sharp')
            sharp_img = os.listdir(sharp_img_path)
            blur_img = os.listdir(blur_img_path)
            for j in range(len(blur_img)):
                b_img = os.path.join(blur_img_path, blur_img[j])
                s_img = os.path.join(sharp_img_path, sharp_img[j])
                blur_img_path_list.append(b_img)
                sharp_img_path_list.append(s_img)

        return blur_img_path_list, sharp_img_path_list


def init_dataset(config):
    config = deepcopy(config)
    transform_fn = aug.get_transforms(size=config['size'], scope=config['scope'], crop=config['crop'])
    normalize_fn = aug.get_normalize()
    if config['corrupt'] is None:
        corrupt_fn = lambda x: x
    else:
        corrupt_fn = aug.get_corrupt_function(config['corrupt'])
    verbose = config.get('verbose', True)
    return MyDataset(config, transform_fn, normalize_fn, corrupt_fn, verbose)