
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from emo.views import view_videos, upload_video

urlpatterns = [
    path("", views.homePage,name='home'),   #page wherer you upload or view videos
    path("generate-report/", views.generateReport),
    path('signin/', views.signin, name="signin"),
    path("signup/", views.signup, name="signup"),
    path('signout/', views.signout, name="signout"),
    path('upload/', views.upload_video, name='upload'),
    path('view/', views.view_videos, name='view_videos'),
    path('adminsignin/', views.adminsignin, name="adminsignin"),
    path('emotion-capture/', views.emotionCapture, name='emotion_capture'), 
    path('predict/', views.prediction, name='predict'),
    path('access-denied/', views.unauthorized_access_handler, name='access_denied'),

    #path('videos/', video_list, name='video_list'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)