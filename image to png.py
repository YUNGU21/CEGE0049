# convert the images from TIFF to PNG
import numpy as np
import os
from PIL import Image
from osgeo import gdal

def readTif(imgPath, bandsOrder=[3, 2, 1]):
    """
    Read the first 3 bands in a TIFF file and store them in an array
    :param imgPath: image path
    :param bandsOrder: specific band order for Red, Green, and Blue For Sentinel-2 and PlanetScope, the original band order is Blue, Green, Red, and Near-infrared.
    :return: an array with three dimensions
    """
    dataset = gdal.Open(imgPath, gdal.GA_ReadOnly)
    cols = dataset.RasterXSize
    rows = dataset.RasterYSize
    data = np.empty([rows, cols, 3], dtype=float)
    for i in range(3):
        band = dataset.GetRasterBand(bandsOrder[i])
        oneband_data = band.ReadAsArray()
        data[:, :, i] = oneband_data
    return data


def stretchImg(imgPath, resultPath, lower_percent=0.5, higher_percent=99.5):
    """
    # map the original DN values to 0-255 and save the results
    :param imgPath: original TIFF files (***.tif)
    :param resultPath: result path (***.png)
    :param lower_percent: low stretch percentage
    :param higher_percent: high stretch percentage
    :return: images, no parameters
    """
    RGB_Array = readTif(imgPath)
    band_Num = RGB_Array.shape[2]
    PNG_Array = np.zeros_like(RGB_Array, dtype=np.uint8)
    for i in range(band_Num):
        minValue = 0
        maxValue = 255
        low_value = np.percentile(RGB_Array[:, :, i], lower_percent)
        high_value = np.percentile(RGB_Array[:, :, i], higher_percent)
        temp_value = minValue + (RGB_Array[:, :, i] - low_value) * (maxValue - minValue) / (high_value - low_value)
        temp_value[temp_value < minValue] = minValue
        temp_value[temp_value > maxValue] = maxValue
        PNG_Array[:, :, i] = temp_value
    outputImg = Image.fromarray(np.uint8(PNG_Array))
    outputImg.save(resultPath)


def Batch_Convert_tif_to_png(imgdir, savedir):
    # get all the filenames and store them into a list
    file_name_list = os.listdir(imgdir)
    for name in file_name_list:
        # get paths for images
        img_path = os.path.join(imgdir, name)
        # get filenames, excluding the extension
        filename = os.path.splitext(name)[0]
        savefilename = filename + ".png"
        # save files
        savepath = os.path.join(savedir, savefilename)
        stretchImg(img_path, savepath)
        print("image:[", filename, "] has been transformed successfullly.")
    print("Congratulations! All the images have been transformed successfully.")


# main function
if __name__ == '__main__':
        imgdir = r"E:/planetapi/images/"
        savedir = r"E:/planetapi/images_png/"
        Batch_Convert_tif_to_png(imgdir, savedir)
