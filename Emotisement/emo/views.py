from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import Video
from .forms import VideoForm
from .models import Video

def homePage(request):
    return render(request,"home.html")
def aboutUs(request):
    return HttpResponse("About Us")
def upload(request):
    return HttpResponse("upload")
def generateReport(request):
    return HttpResponse("report")

def signin(request):
    context={"message":""}
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            context["message"]="Username or Password is not correct!!!"

    return render (request,'signin.html',context)

def signout(request):
    logout(request)
    return redirect('signin')

from django.contrib.auth.models import User

def signup(request):
    context = {"message": ""}
    
    if request.method == 'POST':
        uname = request.POST.get('username')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')
        
        if pass1 != pass2:
            context["message"] = "Passwords are not the same!!"
        else:
            # Create user without additional fields
            my_user = User.objects.create_user(uname, email, pass1)

            # Set additional fields
            my_user.first_name = fname
            my_user.last_name = lname
            my_user.save()

            return redirect('signin')
    
    return render(request, 'signup.html', context)


def view_videos(request):
    videos = Video.objects.all()
    return render(request, 'view_videos.html', {'videos': videos})

def upload_video(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Make sure to use the correct name 'video_list' here
            return redirect('view_videos')
    else:
        form = VideoForm()

    return render(request, 'uploadVideos.html', {'form': form})
