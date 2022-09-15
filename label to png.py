# transform labels from TIFF to PNG
import os
imgdir = r"E:/planetapi/masks/"
savedir =  r"E:/planetapi/masks_png/"

from PIL import Image
file_name_list = os.listdir(imgdir)
for name in file_name_list:
    filename = os.path.splitext(name)[0]
    img_path = os.path.join(imgdir, name)
    img = Image.open(img_path)
    img.save(savedir + "/" + filename + ".png")
