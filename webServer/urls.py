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
# from django.contrib import admin
from django.urls import path

from Server01.views import user, post, comment

urlpatterns = [
    # path("admin/", admin.site.urls),
    # 用户相关
    path("login/", user.login),
    path('register/', user.register),
    path('index/', user.query_user_index),
    path('focus/', user.focusOn),
    path('user/focus/', user.get_user_focus),
    path('user/unfollow/', user.unfollow),
    path('user/update/', user.update_user_info),
    path('user/avatar/', user.update_avatar),
    path('user/post/', user.query_user_index_post),
    path('user/post/control/', user.user_control_index),
    path('user/remove/fan/', user.remove_fans),
    # 帖子相关
    path('upload/', post.upload_post),
    path('upload/info/', post.upload_post_info),
    path('post/detail/', post.get_post_detail),
    path('post/', post.query_post_index),
    path('post/control/', post.control_like_collect),
    path('post/delete/', post.post_delete),
    # 评论相关
    path('comment/', comment.do_comment),
    path('comment/main/', comment.get_comment),
    path('comment/reply/', comment.load_reply)
]
