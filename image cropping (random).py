# Divide the whole imagery into multiple chips randomly with assigned number
import random
from osgeo import gdal
import numpy as np
import os


#  Read TIFF files
def readTif(fileName):
    dataset = gdal.Open(fileName)
    if dataset == None:
        print(fileName + "cannnot open the file")
    return dataset


#  Save TIFF files
def writeTiff(im_data, im_geotrans, im_proj, path):
    if 'int8' in im_data.dtype.name:
        datatype = gdal.GDT_Byte
    elif 'int16' in im_data.dtype.name:
        datatype = gdal.GDT_UInt16
    else:
        datatype = gdal.GDT_Float32
    if len(im_data.shape) == 3:
        im_bands, im_height, im_width = im_data.shape
    elif len(im_data.shape) == 2:
        im_data = np.array([im_data])
        im_bands, im_height, im_width = im_data.shape
    # Create files
    driver = gdal.GetDriverByName("GTiff")
    dataset = driver.Create(path, int(im_width), int(im_height), int(im_bands), datatype)
    if (dataset != None):
        dataset.SetGeoTransform(im_geotrans)  # Read transformation parameters
        dataset.SetProjection(im_proj)  # Read projection information
    for i in range(im_bands):
        dataset.GetRasterBand(i + 1).WriteArray(im_data[i])
    del dataset


'''
ImagePath: original path for the whole imagery
LabelPath: original path for the matching label
IamgeSavePath: save path for images
LabelSavePath: save path for labels
CropSize: the size of cropped chips
CutNum: the number of cropped chips 
'''


def RandomCrop(ImagePath, LabelPath, IamgeSavePath, LabelSavePath, CropSize, CutNum):
    dataset_img = readTif(ImagePath)
    width = dataset_img.RasterXSize
    height = dataset_img.RasterYSize
    proj = dataset_img.GetProjection()
    geotrans = dataset_img.GetGeoTransform()
    img = dataset_img.ReadAsArray(0, 0, width, height)  # get the image data
    dataset_label = readTif(LabelPath)
    label = dataset_label.ReadAsArray(0, 0, width, height)  # get the mask data

    #  get the number of all the files and rename the cropped image as len+1
    fileNum = len(os.listdir(IamgeSavePath))
    new_name = fileNum + 1
    while (new_name < CutNum + fileNum + 1):
        #  generate the coordinates on the top left corner of the cropped chips
        UpperLeftX = random.randint(0, height - CropSize)
        UpperLeftY = random.randint(0, width - CropSize)
        if (len(img.shape) == 2):
            imgCrop = img[UpperLeftX: UpperLeftX + CropSize,
                      UpperLeftY: UpperLeftY + CropSize]
        else:
            imgCrop = img[:,
                      UpperLeftX: UpperLeftX + CropSize,
                      UpperLeftY: UpperLeftY + CropSize]
        if (len(label.shape) == 2):
            labelCrop = label[UpperLeftX: UpperLeftX + CropSize,
                        UpperLeftY: UpperLeftY + CropSize]
        else:
            labelCrop = label[:,
                        UpperLeftX: UpperLeftX + CropSize,
                        UpperLeftY: UpperLeftY + CropSize]
        writeTiff(imgCrop, geotrans, proj, IamgeSavePath + "/%d.tif" % new_name)
        writeTiff(labelCrop, geotrans, proj, LabelSavePath + "/%d.tif" % new_name)
        new_name = new_name + 1


#  crop 8,000 chips with size as 256*256
RandomCrop(r"D:\09_09_final.tif",
           r"E:\planetapi\reclass_3125.tif",
           r"E:\planetapi\images",
           r"E:\planetapi\masks",
           256, 8000)
