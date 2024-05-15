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
from blog.views import WelcomeView, LoginView, LogoutView, SignupView, HomeView, DeleteBlogView, CreateBlogView, BlogsView, ViewBlogView, LikeBlogView, DislikeBlogView, EditBlogView, ViewBlogsView
import debug_toolbar

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', WelcomeView.as_view(), name='welcome'),
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('accounts/profile/', HomeView.as_view(), name='home'),
    path('create_blog/', CreateBlogView.as_view(), name='create_blog'),
    path('blogs/', BlogsView.as_view(), name='blogs'),
    path('blog/<int:pk>/', ViewBlogView.as_view(), name='view_blog'),
    path('blogs/<int:pk>/', ViewBlogsView.as_view(), name='view_blogs'),
    path('blog/<int:pk>/like/', LikeBlogView.as_view(), name='like_blog'),
    path('blog/<int:pk>/dislike/', DislikeBlogView.as_view(), name='dislike_blog'),
    path('blog/<int:pk>/edit/', EditBlogView.as_view(), name='edit_blog'),
    path('blog/<int:pk>/delete/', DeleteBlogView.as_view(), name='delete_blog'),
    path('__debug__/', include(debug_toolbar.urls)),
]
