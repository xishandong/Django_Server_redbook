import json

from django.http import JsonResponse

from Server01.models import Comment, Post
from Server01.util.auxiliaryFuction import convert_to_timezone, filter_querySet
from Server01.util.verifyJWT import authenticate_request
from webServer.settings import TIME_ZONE


@authenticate_request
def do_comment(request, verify_payload):
    data = json.loads(request.body)
    user_id = verify_payload['user_id']
    data['user_id'] = user_id
    comment = Comment.objects.create(**data)
    return JsonResponse({'info': '评论已发送！', 'id': comment.id}, status=200)


def get_comment(request):
    data = json.loads(request.body)
    post_id = data['id']
    offset = data['offset']
    comments = Post.objects.filter(id=post_id).first().comments.all()
    filter_comments = filter_querySet(comments, offset, limit=5)
    if filter_comments:
        data = [
            {
                'id': comment.id,
                'content': comment.content,
                'createTime': convert_to_timezone(comment.created_at, TIME_ZONE),
                'user': {
                    'id': comment.user.id,
                    'username': comment.user.username,
                    'avatar': comment.user.avatar
                }
            } for comment in filter_comments if comment
        ]
        return JsonResponse({'info': data}, status=200)
    return JsonResponse({'info': []}, status=200)


