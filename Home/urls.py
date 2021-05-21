from django.contrib import admin
from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.index, name="Home"),
    path('about/', views.about, name="About"),
    path('contact/', views.contact, name="Contact"),
    path('search/', views.search, name="Search"),
    path('deleteprofilepicture/', views.deleteProfilePicture, name="deleteProfilePicture"),
    path('signup/', views.handleSignUp, name="SignUp"),
    path('otp/', views.sendOtp, name="sendOtp"),
    path('login/', views.handleSignIn, name="SignIn"),
    path('logout/', views.handleLogout, name="SignIn"),
    path('usersettings/<str:slug>/', views.userSettings, name="userSettings"),
   
   

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
