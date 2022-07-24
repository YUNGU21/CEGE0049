# Divide one large satellite image into multiple small images

# Please install the following packages in advance
from osgeo import gdal
import os
import numpy as np

# Create a function called 'readtiff' to read TIFF files


def readtiff(filename):
    file = gdal.Open(filename)
    if file == None:
        print('cannot open' + filename)
    return file


# Create a function called 'savetiff' to save TIFF files
def savetiff(data, transformation, projection, path):
    # Determine the data type
    if 'int8' in data.dtype.name:     # 8-bit
        datatype = gdal.GDT_Byte
    elif 'int16' in data.dtype.name:  # 16-bit
        datatype = gdal.GDT_UInt16
    else:                             # 32-bit
        datatype = gdal.GDT_Float32
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
        dataset.SetGeoTransform(transformation)  # Set transformation information
        dataset.SetProjection(projection)        # Set projection information
    for i in range(bands):                       # Write array data
        dataset.GetRasterBand(i + 1).WriteArray(data[i])
    del dataset


"""
Create a function called 'TiffDivide' to divide the satellite image
Parameters:
tiffpath -> read location
savepath -> save location
size     -> required size (2^n)
rate     -> repetition rate
"""


def TiffDivide(tiffpath, savepath, size, rate):
    data = readtiff(tiffpath)                      # Import TIFF file
    width = data.RasterXSize                       # Get width information
    height = data.RasterYSize                      # Get height information
    projection = data.GetProjection()              # Get projection information
    transformation = data.GetGeoTransform()        # Get transformation information
    image = data.ReadAsArray(0, 0, width, height)  # Get data
    # Get the number of files in the save folder
    new_name = len(os.listdir(savepath))
    for i in range(int((height - size * rate) / (size * (1 - rate)))):
        for j in range(int((width - size * rate) / (size * (1 - rate)))):
            # For single band
            if (len(image.shape) == 2):
                divided = image[
                          int(i * size * (1 - rate)): int(i * size * (1 - rate)) + size,
                          int(j * size * (1 - rate)): int(j * size * (1 - rate)) + size]
            # For multiple bands
            else:
                divided = image[:,
                          int(i * size * (1 - rate)): int(i * size * (1 - rate)) + size,
                          int(j * size * (1 - rate)): int(j * size * (1 - rate)) + size]
            # Save TIFF files
            savetiff(divided, transformation, projection, savepath + "/%d.tif" % new_name)
            new_name = new_name + 1

    #  Forward pruning the last column
    for i in range(int((height - size * rate) / (size * (1 - rate)))):
        if (len(image.shape) == 2):
            divided = image[int(i * size * (1 - rate)): int(i * size * (1 - rate)) + size,
                      (width - size): width]
        else:
            divided = image[:,
                      int(i * size * (1 - rate)): int(i * size * (1 - rate)) + size,
                      (width - size): width]
        savetiff(divided, transformation, projection, savepath + "/%d.tif" % new_name)
        new_name = new_name + 1

    #  Forward pruning the last row
    for j in range(int((width - size * rate) / (size * (1 - rate)))):
        if (len(image.shape) == 2):
            divided = image[(height - size): height,
                      int(j * size * (1 - rate)): int(j * size * (1 - rate)) + size]
        else:
            divided = image[:,
                      (height - size): height,
                      int(j * size * (1 - rate)): int(j * size * (1 - rate)) + size]
        savetiff(divided, transformation, projection, savepath + "/%d.tif" % new_name)
        new_name = new_name + 1

    #  For right bottom corner
    if (len(image.shape) == 2):
        divided = image[(height - size): height,
                  (width - size): width]
    else:
        divided = image[:,
                  (height - size): height,
                  (width - size): width]
    savetiff(divided, transformation, projection, savepath + "/%d.tif" % new_name)
    new_name = new_name + 1


# Test the function
TiffDivide(r"E:\planetapi\field_reclass1.tif", r"E:\planetapi\label", 256, 0)
