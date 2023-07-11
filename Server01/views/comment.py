import json

from django.http import JsonResponse
from Server01.util.verifyJWT import authenticate_request
from Server01.models import Comment


@authenticate_request
def do_comment(request, verify_payload):
    data = json.loads(request.body)
    print(verify_payload)
    user_id = verify_payload['user_id']
    data['user_id'] = user_id
    comment = Comment.objects.create(**data)
    return JsonResponse({'info': '评论已发送！', 'id': comment.id}, status=200)