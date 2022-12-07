from django.urls import path
from upimg import views

urlpatterns = [
    path('', views.to_img_load),  # 跳转至上传图片页面
    path('image_upload/', views.image_upload),  # 上传图片
]

