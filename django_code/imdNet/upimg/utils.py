import os
# 图像篡改检测模型所在文件夹
model_path = os.path.join('/mnt/hgfs/Learning-Rich-Features-for-Image-Manipulation-Detection/', 'default', 'gene_2007_trainval', 'default')


## Image Tool
import json
import random
import time
from .models import Image
from PIL import Image as PILImage

SUPPORT_IMG_TYPE=["PNG", "JPG", "JPEG"]
class ImgTypeError(Exception):
    def __init__(self, ErrorInfo):
        super().__init__(self)
        self.errorinfo=ErrorInfo
    def __str__(self):
        return self.ErrorInfo


def random_str():
    rstr = ""
    while rstr is None or rstr == "" or Image.objects.filter(name = rstr):
        num_set = [chr(i) for i in range(48, 58)]
        char_set = [chr(i) for i in range(97, 123)]
        total_set = num_set + char_set
        bits = 14
        value_set = "".join(random.sample(total_set, bits))
        rstr = value_set + str(int(time.time()))
    return rstr

def get_new_random_file_name(file_name):
    new_file_name = "IMD"+random_str().upper()
    find_type = False
    for c in file_name:
        if c == '.':
            find_type = True
    if find_type:
        suffix = file_name.split('.')[-1]
        if suffix.upper() not in SUPPORT_IMG_TYPE:
            raise ImgTypeError("Only support {}.".format(", ".join(SUPPORT_IMG_TYPE)))
        return new_file_name + '.' + suffix
    else:
        # return new_file_name
        raise ImgTypeError("Only support {}.".format(", ".join(SUPPORT_IMG_TYPE)))

## Just for test
def gen_new_img(image_s):
    img = PILImage.open(image_s)
    img_new = img.convert("L")
    img_new.format = img.format
    return img_new

