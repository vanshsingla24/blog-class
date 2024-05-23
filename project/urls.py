"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.contrib import admin
from blog.views import BlogList, BlogDetail, CommentList, CommentDetail, WelcomeView, LoginView, LogoutView, SignupView, HomeView, DeleteBlogView, CreateBlogView, ViewBlogView, LikeBlogView, DislikeBlogView, EditBlogView
import debug_toolbar


urlpatterns = [
    
    path('blogs/', BlogList.as_view(), name='blog-list'),
    path('blogs/<int:pk>/', BlogDetail.as_view(), name='blog-detail'),
    path('comments/', CommentList.as_view(), name='comment-list'),
    path('comments/<int:pk>/', CommentDetail.as_view(), name='comment-detail'), 
    
    path('admin/', admin.site.urls),
    path('__debug__/', include(debug_toolbar.urls)),
    path('', WelcomeView.as_view(), name='welcome'),
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('accounts/profile/', HomeView.as_view(), name='home'),
    path('create_blog/', CreateBlogView.as_view(), name='create_blog'),
    path('blog/<int:pk>/', ViewBlogView.as_view(), name='view_blog'),
    path('blog/<int:pk>/like/', LikeBlogView.as_view(), name='like_blog'),
    path('blog/<int:pk>/dislike/', DislikeBlogView.as_view(), name='dislike_blog'),
    path('blog/<int:pk>/edit/', EditBlogView.as_view(), name='edit_blog'),
    path('blog/<int:pk>/delete/', DeleteBlogView.as_view(), name='delete_blog'),
]
