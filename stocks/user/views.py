import json
import os.path
from datetime import datetime
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render,redirect
from .forms import UserRegisterForm
import requests
from django.contrib.auth.decorators import login_required
from bs4 import BeautifulSoup
from pytube import YouTube
import mimetypes
from django.conf import settings
from .models import media
from django.contrib.auth.models import User

# Create your views here.


def get_storage(user):
    try:
        path = os.path.join(settings.MEDIA_ROOT, "downloads/" + str(user))
        size = 0
        for i in os.listdir(path):
            size += os.path.getsize(os.path.join(path, str(i))) // (1024 * 1024)
        return size
    except Exception:
        return 0

def home(request):


    if request.user!="AnonymousUser":

        size=get_storage(request.user)

        if size>10:
                info="You exceeded Max value of storage assign!! Try deleting your data in HISTORY"
        else:
                info=""

        return render(request,template_name="user/home1.html",context={"info":info,"storage":size})

    else:
           info = "SignIn!!"
           return render(request, template_name="user/home1.html", context={"info": info})

def Register(request):
    info=""
    if request.method=="POST":
        form=UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
        else:
            info="Invalid Credentials Try Again!!"
    else:
        form=UserRegisterForm()
        info = "Register using proper credentials!!"
    return render(request,template_name="user/register.html",context={"form":form,"ret":info})

@login_required
def delete_acc(request,name):
    User.objects.filter(username=name).delete()
    return redirect("home1")

def download_video(link,client,path=settings.MEDIA_ROOT+"/downloads/",res=None):
        context = {}
        try:
            yt=YouTube(url=link)
        except Exception:
            context["ret"] = "Error in download try:correcting url address"
            context["type"] = "warning"
            context["val"]=0
            return context
        else:

            #stream=yt.streams.filter(resolution=res,progressive=True,file_extension="mp4")
            stream = yt.streams.filter(resolution=res, progressive=True)
            try:
                    context['ext'] =str(stream[0].mime_type).split("/")[-1]
                    n=datetime.now().strftime("%S")+"."+context['ext']
                    p1=stream[0].download(output_path=path+str(client),filename=n)
                    #context['ext']="."+p1.split('.')[-1]

            except Exception :
                    context["ret"]="Error in loading video. Try correcting input fields"
                    context["type"]="danger"
                    context["val"] = 0
            else:
                    #saving new file in server
                    file_path=str(yt.title)

                    obj=media(user=client,title=yt.title,file="downloads/"+str(client)+"/"+n,thumbnail=yt.thumbnail_url)
                    obj.save()

                    # extracting link from server
                    context['link']=str(obj.file).split("/")[-1]
                    #download(context['link'])
                    context["ret"]="Your video is Ready:"
                    context["type"]="success"
                    context["title"]=yt.title
                    context["val"] = 1
            return context

def download_audio(link,client,abr,path=settings.MEDIA_ROOT+"/downloads"):
    context = {}
    try:
        yt = YouTube(url=link)
    except Exception:
        context["ret"] = "Error in Loading Audio try:correcting url address"
        context["type"] = "danger"
        context["val"] = 0
        return context
    else:

        stream = yt.streams.filter(only_audio=True, abr=abr)
        try:
            context['ext']=str(stream[0].mime_type).split("/")[-1]
            n = datetime.now().strftime("%S") + "."+context['ext']
            stream[0].download(output_path=path+str(client),filename=n)
        except Exception:
            context["ret"] = "Error in Loading audio. Try correcting input fields"
            context["type"] = "danger"
            context["val"] = 0
        else:
            # saving new file in server

            obj=media(user=client,title=yt.title,file="downloads/"+str(client)+"/"+n,thumbnail=yt.thumbnail_url)
            obj.save()

            # extracting link from server
            context['link'] = str(obj.file).split("/")[-1]
            context["ret"] = "Your Audio Ready:"
            context["type"] = "success"
            context["title"] = yt.title
            context["val"] = 1
        return context

def download(request,client,fl_path1):
    # fill these variables with real values
    #fl_path ="D:/python_media/downloads/Avicii - Hey Brother (Lyric).mp4"
    fl_path=os.path.join(settings.MEDIA_ROOT,"downloads/"+str(client)+"/"+fl_path1)

    fl = open(fl_path, "rb")
    mime_type, _ = mimetypes.guess_type(fl_path)
    response = HttpResponse(fl, content_type=mime_type)

    filename = "YOUTUBE Media downloader" + "." +str(fl_path1).split(".")[-1]
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response


@login_required
def get_video(request):
    if get_storage(request.user)<10:
        if request.method=="POST":
            link_address=request.POST['link']
            res=request.POST['res']
            context=download_video(link=link_address,res=res,client=request.user)
            return render(request,template_name="user/video_downloader.html",context=context)
        else:
            return render(request,template_name="user/video_downloader.html",context={"ret":"Downlaod video","type":"secondary"})
    else:
        info = "You exceeded Max value of storage assign!! Try deleting your data in HISTORY"
        return render(request,template_name="user/home1.html",context={"info":info,"storage":10})

@login_required
def get_audio(request):
    if get_storage(request.user) < 10:
        if request.method=="POST":
            link_address=request.POST['link']
            abr=request.POST['abr']
            context=download_audio(link=link_address,client=request.user,abr=abr)
            return render(request,template_name="user/audio_downloader.html",context=context)
        else:
            return render(request,template_name="user/audio_downloader.html",context={"ret":"Downlaod Audio in mp4!!","type":"secondary"})
    else:
        info = "You exceeded Max value of storage assign!! Try deleting your data in HISTORY"
        return render(request,template_name="user/home1.html",context={"info":info,"storage":10})

@login_required
def get_history(request):
    if request.method=="POST":


        url = request.POST['delete']
        media.objects.filter(user=request.user).filter(file=url).delete()
        os.remove(os.path.join(settings.MEDIA_ROOT, url))


    user=request.user
    history_list=media.objects.filter(user=user).order_by("-date_time")
    l=[]
    for history in history_list:
        l.append(history)

    return render(request,template_name="user/history.html",context={"list":l})
