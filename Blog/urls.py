from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.blogHome, name="BlogHome"),
    path('composeblog/', views.composeBlog, name="composeBlog"),
    path('deletepost/', views.deletePost, name="deletePost"),
    path('<str:owner>/editpost/<str:slug>/', views.editPost, name="editPost"),
    path('<str:slug>/', views.blogPost, name="BlogPost"),
]
