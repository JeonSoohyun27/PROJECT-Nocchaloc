import re,json,bcrypt,jwt

from django.core.exceptions import MultipleObjectsReturned
from django.views           import View
from django.http            import JsonResponse
from django.shortcuts       import render

from users.models           import User
from users.validator        import validate_account, validate_password
from my_settings            import SECRET_KEY

# Create your views here.

class SignupView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            if not validate_password(data['password']) or validate_account(data['account']):
                return JsonResponse({'message':'INVALID_ERROR'},status=404)
            
            if User.objects.filter(account=data['account']).exists() or User.objects.filter(phone_number=data['phone_number']).exists():
                return JsonResponse({'message':'DUPLICATE'},status=409)

            encoded_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())

            User.objects.create(
                phone_number = data['phone_number'],
                name         = data['name'],
                birthday     = data['birthday'],
                account      = data['account'],
                password     = encoded_password.decode('utf-8'),
                point        = 50000,
            )
            return JsonResponse({'message':'SUCCESS'},status=200)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'},status=400)

class SigninView(View):
    def post(self, request):
        try:
            data     = json.loads(request.body)
            account  = data['account']
            password = data['password']
            user     = User.objects.get(account=data['account'])

            if bcrypt.checkpw(data['password'].encode('utf-8'),user.password.encode('utf-8')):
                encoded_jwt = jwt.encode({'account':user.account},SECRET_KEY,algorithm='HS256')
                return JsonResponse({'message':'SUCCESS','TOKEN':encoded_jwt},status=200)
            
            return JsonResponse({'message':'INPUT_ERROR'},status=406)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'},status=400)

        except MultipleObjectsReturned:
            return JsonResponse({'message':'INVALID_ERROR'},status=404)