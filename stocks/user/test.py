import os
from django.conf import settings
size=0
for i in os.listdir(os.path.join("C:/Users/91751/PycharmProjects/django_NT/stocks/media/downloads/shivam_admin","")):
    size += os.path.getsize("C:/Users/91751/PycharmProjects/django_NT/stocks/media/downloads/shivam_admin/"+ str(i))
    #print(os.path.getsize("C:/Users/91751/PycharmProjects/django_NT/stocks/media/downloads/shivam_admin/"+str(i)))
