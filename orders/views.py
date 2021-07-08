import json

from django.views  import View
from django.http   import JsonResponse
from orders.models import Cart

class CartView(View):
    @authorization
    def get(self, request):
        try:
            if Cart.objects.filter(user_id=request.user).exists():
                carts = Cart.objects.filter(user_id=request.user)
                user  = {'user_id' : request.user}
                
                cart_list = [{
                    'product' : cart.product.name,
                    'quantity': cart.quantity,
                    'option'  : cart.option.option,  # name으로 변경
                    'price'   : cart.product.price,
                } for cart in carts]
                return JsonResponse({'user':user, 'cart_list':cart_list}, status=200)
#==============================================================
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
        except TypeError:
            return JsonResponse({'message':'TYPE_ERROR'}, status=400)
        except  ValueError:
            return JsonResponse({'message':'UNAUTHORIZED'}, status=401)

class CartDeleteView(View):
    @authorization
    def post(sele, request):
        try:
            data = json.loads(request.body)
            user = request.user_id

            if Cart.objects.filter(user_id=user, cart_id=data['cart']).exists:
                Cart.objects.get(user_id=user, cart_id=data['cart']).delete()
                return JsonResponse({'message':'SUCCESS'}, staus=200)
            return 