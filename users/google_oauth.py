import urllib.request
import urllib.parse
import json
from django.utils import timezone
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from users.models import User

@api_view(['POST'])
def google_oauth_callback(request):
    # Получаем код авторизации из запроса
    code = request.data.get('code')
    if not code:
        return Response({'error': 'Code is required'}, status=status.HTTP_400_BAD_REQUEST)

    # Получаем токен Google
    token_url = 'https://oauth2.googleapis.com/token'
    data = {
        'code': code,
        'client_id': settings.GOOGLE_CLIENT_ID,
        'client_secret': settings.GOOGLE_CLIENT_SECRET,
        'redirect_uri': settings.GOOGLE_REDIRECT_URI,
        'grant_type': 'authorization_code',
    }
    encoded_data = urllib.parse.urlencode(data).encode()
    req = urllib.request.Request(token_url, data=encoded_data)
    req.add_header('Content-Type', 'application/x-www-form-urlencoded')
    try:
        with urllib.request.urlopen(req) as response:
            token_resp = response.read()
            token_data = json.loads(token_resp)
    except Exception:
        return Response({'error': 'Failed to get token'}, status=status.HTTP_400_BAD_REQUEST)
    access_token = token_data.get('access_token')

    # Получаем профиль пользователя
    user_info_url = 'https://www.googleapis.com/oauth2/v2/userinfo'
    req = urllib.request.Request(user_info_url)
    req.add_header('Authorization', f'Bearer {access_token}')
    try:
        with urllib.request.urlopen(req) as response:
            user_info_resp = response.read()
            user_info = json.loads(user_info_resp)
    except Exception:
        return Response({'error': 'Failed to get user info'}, status=status.HTTP_400_BAD_REQUEST)

    email = user_info.get('email')
    given_name = user_info.get('given_name')
    family_name = user_info.get('family_name')

    # Создаём или обновляем пользователя
    user, created = User.objects.get_or_create(email=email)
    user.first_name = given_name
    user.last_name = family_name
    user.registration_source = 'google'
    user.is_active = True
    user.last_login = timezone.now()
    user.save()

    return Response({'message': 'Google OAuth successful', 'email': email}, status=status.HTTP_200_OK)
