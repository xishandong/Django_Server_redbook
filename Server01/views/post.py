import json

from django.db.models import Q
from django.http import JsonResponse

import Server01.models as models
from Server01.util.auxiliaryFuction import convert_to_timezone, combine_index_post
from Server01.util.verifyJWT import authenticate_request
from webServer.settings import TIME_ZONE, SYSTEM_PATH


@authenticate_request
def upload_post(request, payload):
    file = request.FILES['file']
    id = request.POST.get('id')
    file_path = SYSTEM_PATH + 'post/' + str(id) + '-' + file.name
    with open(file_path, 'wb') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    result = {
        'filename': file.name,
        'filepath': 'http://localhost:8000/static/img/post/' + str(id) + '-' + file.name,
    }
    post = models.Post.objects.filter(id=id).first()
    if post:
        models.Image.objects.create(imagePath=result['filepath'], post=post)
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
            'comment': [
                {
                    'id': comment.id,
                    'content': comment.content,
                    'createTime': convert_to_timezone(comment.created_at, TIME_ZONE),
                    'user': {
                        'id': comment.user.id,
                        'username': comment.user.username,
                        'avatar': comment.user.avatar
                    }

                } for comment in post.comments.all()
            ],
            'user': {
                'id': post.user.id,
                'username': post.user.username,
                'avatar': post.user.avatar
            },
            'createTime': convert_to_timezone(post.created_at, TIME_ZONE)
        }
        return JsonResponse({'info': info}, status=200)
    return JsonResponse({'error': '错误的访问'}, status=404)


# 主页推送帖子
def query_post_index(request):
    data = json.loads(request.body)
    offset = data['offset']
    query = data.get('query')
    limit = 20  # 每页显示的帖子数量
    if query:
        posts = models.Post.objects.filter(
            Q(title__icontains=query) |
            Q(user__username__icontains=query) |
            Q(content__icontains=query)
        )
    else:
        posts = models.Post.objects.all()
    count = posts.count()

    if 0 <= offset < count:
        start = offset
        end = offset + limit
        posts = posts.order_by('-id')[start:end]
        return JsonResponse({'info': list(combine_index_post(posts))}, status=200)

    return JsonResponse({'info': []}, status=200)
