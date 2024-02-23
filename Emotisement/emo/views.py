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

# views.py
# views.py
# views.py
# views.py
# views.py
from django.shortcuts import render, redirect, get_object_or_404
import os

def view_videos(request):
    if request.method == 'POST':
        video_id = request.POST.get('delete_video')
        if video_id:
            video = get_object_or_404(Video, id=video_id)
            
            try:
                # Get the file path before deleting the video from the database
                file_path = video.video_file.path

                # Delete the video from the database
                video.delete()

                # Now, the file should be closed, and we can safely delete it from the media folder
                os.remove(file_path)
                
                return redirect('view_videos')
            except Exception as e:
                print(f"Error: {e}")
                # Handle any exception that might occur during the deletion process

    videos = Video.objects.all()
    return render(request, 'view_videos.html', {'videos': videos})






# views.py
# views.py
from django.shortcuts import render, redirect
from .forms import VideoForm

def upload_video(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('view_videos')  # Redirect after successful form submission
    else:
        form = VideoForm()

    return render(request, 'uploadVideos.html', {'form': form})


