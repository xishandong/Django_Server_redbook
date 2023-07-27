import datetime

import jwt
from django.http import JsonResponse
from jwt import exceptions

import Server01.models as models
from webServer.settings import SECRET_KEY


def authenticate_request(view_func):
    def wrapper(request, *args, **kwargs):
        # 从请求中获取 JWT 令牌
        try:
            token = request.headers.get('Authorization').split(' ')[1]
            verify_payload = jwt.decode(token, SECRET_KEY, ['HS256'], verify=True)
            return view_func(request, verify_payload, *args, **kwargs)
        except exceptions.ExpiredSignatureError:
            error_message = {'error': '登录身份过期'}
            return JsonResponse(error_message, status=401)
        except jwt.DecodeError:
            error_message = {'error': 'jwt认证失败'}
            return JsonResponse(error_message, status=401)
        except jwt.InvalidTokenError:
            error_message = {'error': '非法的token'}
            return JsonResponse(error_message, status=401)
    return wrapper


def create_token(user):
    # 构造头部
    headers = {
        'typ': 'jwt',
        'alg': 'HS256',
    }
    # 构造payload
    payload = {
        'user_id': user.id,
        'username': user.username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=3600, days=5)  # 设置过期时间
    }
    result = jwt.encode(payload=payload, key=SECRET_KEY, algorithm='HS256', headers=headers)
    return result
