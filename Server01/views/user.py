import json

from django.http import JsonResponse

import Server01.models as models
from Server01.util.auxiliaryFuction import check_email, combine_index_post, check_and_delete
from Server01.util.verifyJWT import create_token, authenticate_request
from webServer.settings import SYSTEM_PATH


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


# 获取用户主页信息
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
                'focusOn': user.following.count(),
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


# 获取用户关注用户id
@authenticate_request
def get_user_focus(request, payload):
    user_id = payload['user_id']
    user = models.User.objects.filter(id=user_id).first()
    following = user.following.all()
    ids = [u.id for u in following]
    return JsonResponse({'info': ids}, status=200)


# 用户关注
@authenticate_request
def focusOn(request, payload):
    # 做关注操作的用户id
    id1 = payload['user_id']
    user1 = models.User.objects.filter(id=id1).first()
    # 被关注的用户id
    id2 = json.loads(request.body)['id']
    user2 = models.User.objects.filter(id=id2).first()
    if user1 and user2:
        user1.following.add(user2)
        return JsonResponse({'info': '成功关注'}, status=200)
    return JsonResponse({'error': '非法的操作'}, status=401)


@authenticate_request
def unfollow(request, payload):
    # 取消关注操作的用户id
    user_id = payload['user_id']
    user = models.User.objects.filter(id=user_id).first()
    # 被取消关注的用户id
    unfollow_id = json.loads(request.body)['id']
    unfollow_user = models.User.objects.filter(id=unfollow_id).first()
    if user and unfollow_user:
        user.following.remove(unfollow_user)
        return JsonResponse({'info': '成功取消关注'}, status=200)
    return JsonResponse({'error': '非法的操作'}, status=401)


@authenticate_request
def update_user_info(request, payload):
    data = json.loads(request.body)
    user_id = payload['user_id']
    user = models.User.objects.filter(id=user_id).first()
    user.username = data['username']
    user.signature = data['signature']
    user.save()
    return JsonResponse({'info': '修改成功'}, status=200)


@authenticate_request
def update_avatar(request, payload):
    file = request.FILES['file']
    id = payload['user_id']
    file_path = SYSTEM_PATH + '/webServer/Server01/static/img/avatar/' + str(id) + '-' + file.name
    check_and_delete(id, SYSTEM_PATH + '/webServer/Server01/static/img/avatar/')
    with open(file_path, 'wb') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    result = {
        'filename': file.name,
        'filepath': 'http://localhost:8000/static/img/avatar/' + str(id) + '-' + file.name,
    }
    user = models.User.objects.filter(id=id).first()
    user.avatar = 'http://localhost:8000/static/img/avatar/' + str(id) + '-' + file.name
    user.save()
    return JsonResponse({'info': result}, status=200)
