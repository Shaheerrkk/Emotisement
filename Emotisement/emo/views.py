from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import Video,VideoEmotions
from .forms import VideoForm
from .models import Video
from django.conf import settings
from .inference import predict
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

def homePage(request):
    if request.user.is_authenticated:
        return render(request,"home.html")
    else:
        return redirect('signin')
def aboutUs(request):
    return HttpResponse("About Us")
def upload(request):
    return HttpResponse("upload")
def generateReport(request):
    return HttpResponse("report")

def signin(request):
    context = {"message": ""}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')  # Corrected to match input name
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            context["message"] = "Username or Password is not correct!!!"

    return render(request, 'signin.html', context)


def signout(request):
    logout(request)
    return redirect('signin')


from django.shortcuts import render, redirect
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
            context["message"] = "Passwords do not match!"
        else:
            # Check if username or email already exists
            if User.objects.filter(username=uname).exists() or User.objects.filter(email=email).exists():
                context["message"] = "Username or email already exists!"
            else:
                # Create user without additional fields
                my_user = User.objects.create_user(uname, email, pass1)

                # Set additional fields
                my_user.first_name = fname
                my_user.last_name = lname
                my_user.save()

                return redirect('signin')  # Redirect to the sign-in page
    
    return render(request, 'signup.html', context)


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




def emotionCapture(request):
    
    if request.user.is_authenticated and request.user.is_superuser:
    
        videos = Video.objects.all()
        context = {
            'MEDIA_URL': settings.MEDIA_URL,
            'videos': videos
        }
        return render(request,'emotionCapture.html', context)
    elif not request.user.is_superuser:
        return redirect('access_denied')
    else:
        # Redirect or display a forbidden message
        return redirect('adminsignin')


def prediction(request):
    if request.method == 'POST':
        video_chunks = [request.FILES[key] for key in request.FILES if key.startswith('video_chunk_')]
        
        uploaded_file = request.FILES.get('video')
        width = request.POST.get('width')
        height = request.POST.get('height')
        video_id=request.POST.get('id')
        # Perform inference
        results ={"c":"jg"}
        results = predict(video_chunks, width, height)
        results = {"emotions_and_timestamp": results}
        video_emotions, created = VideoEmotions.objects.get_or_create(video_id=video_id)
        if(results):
            video_emotions.emotions_and_timestamp = results
            video_emotions.save()
        # Return inference results as JSON response
        return JsonResponse(results)
    else:
        return render(request, 'upload.html')


def adminsignin(request):
    context={"message":""}
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None and user.is_superuser:
            login(request,user)
            return redirect('emotion_capture')
        elif not user.is_superuser:
            context["message"]="You are not authorized to view the page!!!"
        else:
            context["message"]="Username or Password is not correct!!!"

    return render (request,'adminsignin.html',context)


def unauthorized_access_handler(request):
    # You can render an access denied page or return a response with an error message
    return render(request, 'accessDenied.html', {'message': 'Access Denied'})
