import jwt
from django.conf import settings
from datetime import datetime, timedelta
from .models import CustomUser

def generate_access_token(user):
    access_token_payload = {
        'user_id': user.id,
        'exp': datetime.utcnow() + timedelta(seconds=settings.ACCESS_TOKEN_EXPIRATION),
        'iat': datetime.utcnow()
    }
    access_token = jwt.encode(access_token_payload, settings.SECRET_KEY, algorithm='HS256')
    return access_token

def generate_refresh_token(user):
    refresh_token_payload = {
        'user_id': user.id,
        'exp': datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRATION),
        'iat': datetime.utcnow()
    }
    refresh_token = jwt.encode(refresh_token_payload, settings.SECRET_KEY, algorithm='HS256')
    user.refresh_token = refresh_token
    user.save()
    return refresh_token

def decode_token(token):
    try:
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        return decoded_token
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def get_user_from_token(token):
    decoded_token = decode_token(token)
    if decoded_token:
        user_id = decoded_token.get('user_id')
        try:
            user = CustomUser.objects.get(id=user_id)
            return user
        except CustomUser.DoesNotExist:
            return None
    return None
