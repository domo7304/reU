# -*- coding: utf-8 -*-
"""
Created on Wed Nov 17 20:09:42 2021

@author: ksh76
"""

import numpy as np
import glob
import csv
import os


if __name__ == "__main__":
    # Load classes
    classes = sorted(glob.glob('/Users/ksh76/project_ksh/datasets/train_new_ksh/*'))
    classes_sort = []
    for i in range(len(classes)):
        classes_sort.append(classes[i].split('\\')[-1])
    classes = classes_sort
        
    
    ## Training
    path_full = []
    for j in range(len(classes)):
        path = sorted(glob.glob('/Users/ksh76/project_ksh/datasets/train_new_ksh/'+classes[j]+'/*'), key=os.path.getmtime)
        path.sort()
        
        for i in range(len(path)):
            _path = path[i].replace('\\', '/', 10).split('/')[-3:]
            full_path = _path[0] + '/' + _path[1] + '/' + _path[2]
            path_full.append(full_path)
        
        if j == 0:
            label = np.zeros(shape=(len(path),))
        else:
            label = np.hstack([label, np.ones(shape=(len(path),))*j])
    
    
    mylist = [['subDirectory_filePath', 'class']]
    for i in range(len(path_full)):
        mylist.append([path_full[i], int(label[i])])
    
    
    # Save training path
    with open('/Users/ksh76/project_ksh/datasets/training.csv', 'w', newline='') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerows(mylist)
        
    
    ## Evaluation
    path_full = []
    for j in range(len(classes)):
        path = sorted(glob.glob('/Users/ksh76/project_ksh/datasets/val_new_ksh/'+classes[j]+'/*'), key=os.path.getmtime)
        path.sort()
        
        for i in range(len(path)):
            _path = path[i].replace('\\', '/', 10).split('/')[-3:]
            full_path = _path[0] + '/' + _path[1] + '/' + _path[2]
            path_full.append(full_path)
        
        if j == 0:
            label = np.zeros(shape=(len(path),))
        else:
            label = np.hstack([label, np.ones(shape=(len(path),))*j])
    
    
    mylist = [['subDirectory_filePath', 'class']]
    for i in range(len(path_full)):
        mylist.append([path_full[i], int(label[i])])
    
    
    # Save training path
    with open('/Users/ksh76/project_ksh/datasets/validation.csv', 'w', newline='') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerows(mylist)
