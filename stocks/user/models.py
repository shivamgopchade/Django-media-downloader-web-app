from django.db import models
from django.contrib.auth.models import User
import django.utils.timezone as tz
from PIL import Image
# Create your models here.
class media(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=20,default="NA")
    file=models.FileField(upload_to="downloads")
    data=models.IntegerField(default=0)
    date_time=models.DateTimeField(default=tz.now)
    thumbnail=models.CharField(default="https://picsum.photos/200",max_length=50)
    def __str__(self):
        return f"{self.user.username}"
