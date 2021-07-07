import jwt

from django.http             import JsonResponse

from nocchaloc.settings      import SECRET_KEY
from users.models            import User

def authorization(func):
    def wrapper(self, request, *args, **kwargs):
        
        token = request.headers.get('Authorization', None)
        
        if token is None:
            return JsonResponse({'error':'Enter the token'}, status=401)
        
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms='HS256')
            
            if User.objects.get(id=payload['user_id']):
                request.user = User.objects.get(id=payload['user_id'])
                return func(self, request, *args, **kwargs)

        except jwt.InvalidSignatureError:
            return JsonResponse({'error':'Invalid token'}, status=401)
        
        except jwt.ExpiredSignatureError:
            return JsonResponse({'error':'Expried Signature'}, status=401)
        
        except jwt.DecodeError:
            return JsonResponse({'error':'Invalid token'}, status=401)
    
    return wrapper