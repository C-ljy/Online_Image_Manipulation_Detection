from django.shortcuts import render

# Create your views here.

from .models import Image
from django.shortcuts import HttpResponse


def to_img_load(request):
    '''
    展示页面
    '''
    return render(request, 'img_upload.html')

        
from django.http import JsonResponse
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.conf import settings
import os
from .utils import *
from .imd import imd
from PIL import Image as PILImage

def image_upload(request):
    '''
    处理上传图片，存入数据库并返回相应信息
    '''
    ## 获取生成的图像，检查文件格式，重命名
    try:
        img_s = request.FILES['img']  # 获取文件对象
        img_s.name = get_new_random_file_name(img_s.name)   # 检查文件格式，重命名
    # 图片格式异常
    except ImgTypeError as err:
        return JsonResponse({"data":2, "info":err.errorinfo}, json_dumps_params={'ensure_ascii':False}, safe=False)
    # 上传失败
    except Exception as err:
        print(err)
        return JsonResponse({"data":0}, json_dumps_params={'ensure_ascii':False}, safe=False)

    ## 保存上传的图像，生成篡改检测图像，保存并返回
    try:
        # 保存数据
        image = Image(name = img_s.name, img = img_s)
        image.save()
        #img_rec = Image.objects.get(name = img_s.name)
        
        # 生成响应图片
        imd(imgs=[img_s.name],
            load_path = os.path.join(settings.MEDIA_ROOT, image.img_path),
            save_path = os.path.join(settings.MEDIA_ROOT, image.img_new_path),
            model_path = model_path
            )
        imd_new_file = os.path.join(image.img_new_path, img_s.name)
        
        # if os.path.exists(imd_new_file):
        #     img_new = PILImage.open(imd_new_file)
        #     # 转化为InMemoryUploadedFile数据
        #     img_new_io = BytesIO()
        #     img_new.save(img_new_io, img_new.format)
        #     img_d = InMemoryUploadedFile(
        #         file=img_new_io,
        #         field_name=None,
        #         name=img_s.name,
        #         content_type=img_s.content_type,
        #         size=img_s.size,
        #         charset=None
        #     )
        #     image.img_new = img_d
        #     image.save()
        if os.path.exists(os.path.join(settings.MEDIA_ROOT, imd_new_file)):
            image.img_new = imd_new_file
            image.save()
        # 图像篡改检测异常
        else:
            return JsonResponse({"data":3}, json_dumps_params={'ensure_ascii':False}, safe=False)
        
        return JsonResponse({"data":1, "info":str(image.img_new)}, json_dumps_params={'ensure_ascii':False}, safe=False)
    # 上传失败
    except Exception as err:
        print(err)
        return JsonResponse({"data":0}, json_dumps_params={'ensure_ascii':False}, safe=False)

