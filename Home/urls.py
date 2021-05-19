from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

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
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='passwordReset/password_reset_form.html'), name='password_reset'),

    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='passwordReset/password_reset_done.html'), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='passwordReset/password_reset_confirm.html'), name='password_reset_confirm'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='passwordReset/password_reset_complete.html'), name='password_reset_complete'),
    path('<str:slug>/', views.userSettings, name="userSettings"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
