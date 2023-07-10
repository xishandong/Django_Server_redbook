import json

from django.http import JsonResponse

import Server01.models as models
from Server01.util.verifyJWT import create_token


# 用户登录
def login(request):
    data = json.loads(request.body)
    user = models.User.objects.filter(**data).first()
    if user:
        token = create_token(user)
        user = {
            'id': user.id,
            'username': user.username,
            'avatar': user.avatar,
            'signature': user.signature,
            'token': token
        }
        return JsonResponse(user, status=200)
    error_message = {'error': '邮箱或密码错误'}
    return JsonResponse(error_message, status=401)


# 用户注册
def register(request):
    data = json.loads(request.body)
    email = data['email']
    if check_email(email):
        return JsonResponse({'error': '该邮箱已被注册'}, status=401)
    try:
        models.User.objects.create(**data)
        return JsonResponse({'username': data})
    except Exception as e:
        print(e)
        return JsonResponse({'error': '创建用户失败'}, status=401)


def query_user_index(request):
    data = json.loads(request.body)
    if data.get('id'):
        user = models.User.objects.filter(id=data.get('id')).first()
        if user:
            author = {
                'id': user.id,
                'username': user.username,
                'avatar': user.avatar,
                'signature': user.signature,
                'fans': user.beFocusOn.count(),
                'focusOn': user.focusOn.count(),
                'postsCount': user.posts.count(),
            }
            info = {
                'user': author,
                'posts': list(combine_index_post(user.posts.all())),
                'collected': list(combine_index_post(user.collected.all())),
                'favorites': list(combine_index_post(user.favorites.all()))
            }
            return JsonResponse({'data': info}, status=200)
        return JsonResponse({'error': '错误的访问'}, status=401)
    return JsonResponse({'error': '非法访问'}, status=401)


def combine_index_post(posts):
    for post in posts:
        imgs = post.imgs.all()
        info = {
            'title': post.title,
            'id': post.id,
            'img': imgs[0].imagePath,
            'user': {
                'id': post.user.id,
                'username': post.user.username,
                'avatar': post.user.avatar
            }
        }
        yield info


def check_email(email):
    return models.User.objects.filter(email=email).exists()
