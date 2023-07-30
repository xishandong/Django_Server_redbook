import json

from PIL import Image
from django.db.models import Q
from django.http import JsonResponse

import Server01.models as models
from Server01.util.auxiliaryFuction import convert_to_timezone, combine_index_post, filter_querySet
from Server01.util.verifyJWT import authenticate_request
from webServer.settings import TIME_ZONE, SYSTEM_PATH


@authenticate_request
def upload_post(request, payload):
    file = request.FILES['file']
    id = request.POST.get('id')
    file_path = SYSTEM_PATH + 'post/' + str(id) + '-' + file.name
    with Image.open(file) as img:
        image_height = img.height
        image_width = img.width
    with open(file_path, 'wb') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    result = {
        'filename': file.name,
        'filepath': 'http://localhost:8000/static/img/post/' + str(id) + '-' + file.name,
    }
    post = models.Post.objects.filter(id=id).first()
    if post:
        models.Image.objects.create(imagePath=result['filepath'], post=post, height=image_height, width=image_width)
        return JsonResponse({'data': 'success'}, status=200)
    return JsonResponse({'error': '错误的操作'}, status=401)


# 用户上传帖子
@authenticate_request
def upload_post_info(request, payload):
    data = json.loads(request.body)
    post = models.Post.objects.create(
        title=data.get('title'),
        content=data.get('content'),
        user_id=data.get('user_id')
    )
    return JsonResponse({'data': 'success', 'info': post.id}, status=200)


# 获取帖子详情，整合信息
def get_post_detail(request):
    data = json.loads(request.body)
    id = data.get('id')
    post = models.Post.objects.filter(id=id).first()
    if post:
        imgs = post.imgs.all()
        info = {
            'title': post.title,
            'id': post.id,
            'imgs': [img.imagePath for img in imgs],
            'user': {
                'id': post.user.id,
                'username': post.user.username,
                'avatar': post.user.avatar
            },
            'createTime': convert_to_timezone(post.created_at, TIME_ZONE),
            'likeCount': post.favoritePosts.count(),
            'collectCount': post.collectedPosts.count(),
            'commentCount': post.comments.count(),
            'content': post.content
        }
        return JsonResponse({'info': info}, status=200)
    return JsonResponse({'error': '错误的访问'}, status=404)


# 主页推送帖子
def query_post_index(request):
    data = json.loads(request.body)
    offset = data['offset']
    query = data.get('query')
    if query:
        posts = models.Post.objects.filter(
            Q(title__icontains=query) |
            Q(user__username__icontains=query) |
            Q(content__icontains=query)
        )
    else:
        posts = models.Post.objects
    posts = filter_querySet(posts, offset, limit=10)
    if posts:
        return JsonResponse({'info': list(combine_index_post(posts))}, status=200)
    # 没有内容了
    return JsonResponse({'info': []}, status=200)


@authenticate_request
def control_like_collect(request, payload):
    user_id = payload['user_id']
    data = json.loads(request.body)
    operation = data['operator']
    post_id = data['post_id']
    types = data['type']
    user = models.User.objects.filter(id=user_id).first()
    post = models.Post.objects.filter(id=post_id).first()
    if user and post:
        if types == 'like':
            if not operation:
                user.favorites.add(post)
                return JsonResponse({'info': '成功添加喜欢'}, status=200)
            user.favorites.remove(post)
            return JsonResponse({'info': '成功取消喜欢'}, status=200)
        elif types == 'collect':
            if not operation:
                user.collected.add(post)
                return JsonResponse({'info': '成功添加收藏'}, status=200)
            user.collected.remove(post)
            return JsonResponse({'info': '成功取消收藏'}, status=200)
    return JsonResponse({'error': '错误的操作'}, status=404)


@authenticate_request
def post_delete(request, payload):
    data = json.loads(request.body)
    id = data['id']
    post = models.Post.objects.filter(id=id).first()
    if post:
        if post.user.id == payload['user_id']:
            post.delete()
            return JsonResponse({'success': '帖子删除成功'}, status=200)
        return JsonResponse({'error': '错误'}, status=401)
    return JsonResponse({'error': '错误'}, status=401)