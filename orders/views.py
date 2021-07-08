import json

from django.views  import View
from django.http   import JsonResponse
from orders.models import Cart

class CartView(View):
    def get(self, request):
        try:
            data = json.loads(request.body)  # 토큰 적용시 삭제
            if Cart.objects.filter(user_id=data['user']):  # 토큰유저 수정
                user  = data['user']
                carts = Cart.objects.filter(user_id=user)
                user  = {'user_id' : user} # 토큰유저 수정
                
                cart_list = [{
                    'product' : cart.product.name,
                    'quantity': cart.quantity,
                    'option'  : cart.option.option,  # name으로 변경
                    'price'   : cart.product.price,
                } for cart in carts]

                return JsonResponse({'user':user, 'cart_list':cart_list}, status=200)
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
        except TypeError:
            return JsonResponse({'message':'TYPE_ERROR'}, status=400)
        except  ValueError:
            return JsonResponse({'message':'UNAUTHORIZED'}, status=401)
