import os

import pytz

import Server01.models as models
from webServer.settings import TIME_ZONE


# 更换时区
def convert_to_timezone(datetime_obj, timezone_str):
    target_timezone = pytz.timezone(timezone_str)
    converted_datetime = datetime_obj.astimezone(target_timezone)
    return converted_datetime.strftime('%Y-%m-%d %H:%M')


# 检查邮箱
def check_email(email):
    return models.User.objects.filter(email=email).exists()


# 整合主页帖子的信息
def combine_index_post(posts):
    for post in posts:
        imgs = post.imgs.all()
        info = {
            'title': post.title,
            'id': post.id,
            'img': imgs[0].imagePath,
            'img_info': {
                'height': imgs[0].height,
                'width': imgs[0].width,
            },
            'load': False,
            'user': {
                'id': post.user.id,
                'username': post.user.username,
                'avatar': post.user.avatar
            }
        }
        yield info


# 检查和删除图片，用于删除帖子时删除文件，以及删除用户上一次上传的头像
def check_and_delete(*, id, mainPath):
    # 获取目录下的文件
    file_list = os.listdir(mainPath)
    # 遍历文件列表，检查是否有对应的文件，如果有就删除
    for file_name in file_list:
        if file_name.startswith(f'{id}-'):
            file_path = os.path.join(mainPath, file_name)
            os.remove(file_path)


def filter_querySet(querySet, offset, limit=20):
    limit = limit  # 每页显示的帖子数量
    count = querySet.count()
    if 0 <= offset < count:
        start = offset
        end = offset + limit
        filterQuerySet = querySet.order_by('-id')[start:end]
        return filterQuerySet
    return []


def get_user_post_info(posts, offset):
    clear_posts = filter_querySet(posts, offset, 10)
    info = [{
        'date': convert_to_timezone(post.created_at, TIME_ZONE),
        'title': post.title,
        'likeCount': post.favoritePosts.count(),
        'collectCount': post.collectedPosts.count(),
        'commentCount': post.comments.count(),
        'content': post.content,
        'id': post.id,
        'username': post.user.username,
    } for post in clear_posts if post]
    return info


def get_user_info(users, offset):
    clear_users = filter_querySet(users, offset, 10)
    info = [
        {
            'username': user.username,
            'avatar': user.avatar,
            'id': user.id,
            'fans': user.beFocusOn.count(),
            'follow': user.following.count(),
            'note': user.posts.count()
        } for user in clear_users
    ]
    return info
