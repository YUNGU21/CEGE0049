# Realize data augmentation to enlarge the images

# Please install the following packages in advance
from osgeo import gdal
import os
import cv2
import numpy as np


# Create a function called 'readtiff' to read TIFF files
def readtiff(filename, x_off=0, y_off=0, data_width=0, data_height=0):
    file = gdal.Open(filename)
    if file == None:
        print('cannot open' + filename)
    width = file.RasterXSize   # Column
    height = file.RasterYSize  # Row
    bands = file.RasterCount   # Bands
    if (data_width == 0 and data_height == 0):
        data_width = width
        data_height = height
    data = file.ReadAsArray(x_off, y_off, data_width, data_height)  # Get data
    transformation = file.GetGeoTransform()  # Get transformation information
    projection = file.GetProjection()        # Get projection information
    return width, height, bands, data, transformation, projection


# Create a function called 'savetiff' to save TIFF files
def savetiff(data, transformation, projection, path):
    # Determine the data type
    if 'int8' in data.dtype.name:     # 8-bit
        datatype = gdal.GDT_Byte
    elif 'int16' in data.dtype.name:  # 16-bit
        datatype = gdal.GDT_UInt16
    else:
        datatype = gdal.GDT_Float32   # 32-bit
    # Determine the array dimension
    if len(data.shape) == 3:          # For multiple bands
        bands, height, width = data.shape
    elif len(data.shape) == 2:        # For single band
        data = np.array([data])
        bands, height, width = data.shape
    # Create a file
    driver = gdal.GetDriverByName("GTiff")  # GeoTIFF
    dataset = driver.Create(path, int(width), int(height), int(bands), datatype)
    if (dataset != None):
        dataset.SetGeoTransform(transformation)   # Set transformation information
        dataset.SetProjection(projection)         # Set projection information
    for i in range(bands):                  # Write array data
        dataset.GetRasterBand(i + 1).WriteArray(data[i])
    del dataset

# For images
train_image_path = r"E:\planetapi\train"  # Set image location
imagelist = os.listdir(train_image_path)
transform_num = len(imagelist) + 1
# For labels
train_label_path = r"E:\planetapi\label"  # Set label location
labellist = os.listdir(train_label_path)

for i in range(len(imagelist)):
    # For images
    image_file = train_image_path + "\\" + imagelist[i]
    width, height, bands, data, transformation, projection = readtiff(image_file)
    # For labels
    label_file = train_label_path + "\\" + labellist[i]
    label = cv2.imread(label_file)
    # Perform data augmentation
    # For images: horizontal flip
    image_hor = np.flip(data, axis=2)
    path_hor = train_image_path + "\\" + str(transform_num) + imagelist[i][-4:]
    savetiff(image_hor, transformation, projection, path_hor)
    # For labels: horizontal flip
    label_hor = cv2.flip(label, 1)
    path_hor = train_label_path + "\\" + str(transform_num) + labellist[i][-4:]
    cv2.imwrite(path_hor, label_hor)
    transform_num += 1

    # For images: vertical flip
    image_ver = np.flip(data, axis=1)
    path_ver = train_image_path + "\\" + str(transform_num) + imagelist[i][-4:]
    savetiff(image_ver, transformation, projection, path_ver)
    # For labels: vertical flip
    label_vec = cv2.flip(label, 0)
    path_vec = train_label_path + "\\" + str(transform_num) + labellist[i][-4:]
    cv2.imwrite(path_vec, label_vec)
    transform_num += 1

    # For images: diagonal flip
    image_dia = np.flip(image_ver, axis=2)
    path_dia = train_image_path + "\\" + str(transform_num) + imagelist[i][-4:]
    savetiff(image_dia, transformation, projection, path_dia)
    # For labels: diagonal flip
    label_dia = cv2.flip(label, -1)
    path_dia = train_label_path + "\\" + str(transform_num) + labellist[i][-4:]
    cv2.imwrite(path_dia, label_dia)
    transform_num += 1