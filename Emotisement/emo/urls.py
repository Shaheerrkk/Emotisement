
from django.urls import path
from .views import upload_video
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import view_videos, upload_video

urlpatterns = [
    path("aftersign/", views.homePage,name='home'),   #page wherer you upload or view videos
    path("upload/", views.upload_video,name="upload"), 
    path("generate-report/", views.generateReport),
    path('signin/', views.signin, name="signin"),
    path("", views.signup, name="signup"),
    path('signout/', views.signout, name="signout"),
    path('upload/', upload_video, name='upload_video'),
    path('view/', view_videos, name='view_videos'),
    #path('videos/', video_list, name='video_list'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)