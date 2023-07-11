"""webServer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from Server01.views import user, post, comment

urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/", user.login),
    path('register/', user.register),
    path('index/', user.query_user_index),
    path('upload/', post.upload_post),
    path('upload/info/', post.upload_post_info),
    path('post/detail/', post.get_post_detail),
    path('post/', post.query_post_index),
    path('comment/', comment.do_comment)
]
