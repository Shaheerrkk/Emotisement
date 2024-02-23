
from django.urls import path
from .views import upload_video
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.homePage,name='home'),
    path("upload/", views.upload_video,name="upload"),
    path("generate-report/", views.generateReport),
    path('signin/', views.signin, name="signin"),
    path('signup/', views.signup, name="signup"),
    path('signout/', views.signout, name="signout"),
    path('upload/', upload_video, name='upload_video'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)