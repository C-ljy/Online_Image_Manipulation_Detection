from django.db import models

# Create your models here.

class Image(models.Model):
    img_path = 'upload/'
    img_new_path = 'download/'
    # Fields
    name = models.CharField(max_length=50, primary_key=True, help_text="image name")
    img = models.ImageField(upload_to=img_path)
    time = models.DateTimeField(auto_now_add=True)
    img_new = models.TextField(max_length=512)


