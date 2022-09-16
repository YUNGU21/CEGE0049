# split images and matching labels into three sets: training set, validation set, and testing set
import os
import random
import shutil

'''
├── There are six sub-folders in a folder called 'data'.
│   ├── train: store images for training 
│   ├── trainmask: store masks for training
│   ├── val: store images for validation
│   ├── valmask: store masks for validation
│   ├── test: store images for testing
│   ├── testmask: store masks for testing
'''

# create new folders
dirpath_list = ['data/train', 'data/trainmask', 'data/val', 'data/valmask', 'data/test', 'data/testmask']
for dirpath in dirpath_list:
    if os.path.exists(dirpath):
        shutil.rmtree(dirpath)  # delete folder with the same filename if possible
        os.makedirs(dirpath)    # create new folders
    elif not os.path.exists(dirpath):
        os.makedirs(dirpath)

# set the percentage for each dataset -> train:valid:test=8:1:1
train_percent = 0.8
val_percent = 0.1
test_percent = 0.1

# There are two sub-folders containing original images and masks in a folder called 'data_mask'
imagefilepath = 'data_mask/images'
total_img = os.listdir(imagefilepath)
# get the names of all the images
total_name_list = [row.split('.')[0] for row in total_img]
num = len(total_name_list)
num_list = range(num)
# count the number of each dataset
train_tol = int(num * train_percent)
val_tol = int(num * val_percent)
test_tol = int(num * test_percent)

# index of the training dataset in total_name_list
train_numlist = random.sample(num_list, train_tol)
# index of the validation dataset in total_name_list
val_test_numlist = list(set(num_list) - set(train_numlist))
val_numlist = random.sample(val_test_numlist, val_tol)
# index of the testing dataset in total_name_list
test_numlist = list(set(val_test_numlist) - set(val_numlist))

# copy the images and labels to the associated folders
for i in train_numlist:
    img_path = 'data_mask/images/'+total_name_list[i]+'.png'
    new_path = 'data/train/'+total_name_list[i]+'.png'
    shutil.copy(img_path, new_path)
    img_path = 'data_mask/masks/' + total_name_list[i] + '.png'
    new_path = 'data/trainmask/' + total_name_list[i] + '.png'
    shutil.copy(img_path, new_path)
for i in val_numlist:
    img_path = 'data_mask/images/'+total_name_list[i]+'.png'
    new_path = 'data/val/'+total_name_list[i]+'.png'
    shutil.copy(img_path, new_path)
    img_path = 'data_mask/masks/' + total_name_list[i] + '.png'
    new_path = 'data/valmask/' + total_name_list[i] + '.png'
    shutil.copy(img_path, new_path)
for i in test_numlist:
    img_path = 'data_mask/images/'+total_name_list[i]+'.png'
    new_path = 'data/test/'+total_name_list[i]+'.png'
    shutil.copy(img_path, new_path)
    img_path = 'data_mask/masks/' + total_name_list[i] + '.png'
    new_path = 'data/testmask/' + total_name_list[i] + '.png'
    shutil.copy(img_path, new_path)
