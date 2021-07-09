import json

from django.views  import View
from django.http   import JsonResponse

from orders.models import Cart
from utils         import authorization

class CartView(View):
    @authorization
    def get(self, request):
        try:
            if Cart.objects.filter(user_id=request.user.id).exists():
                carts = Cart.objects.filter(user_id=request.user.id)

                cart_list = [{
                    'product'    : cart.product.name,
                    'quantity'   : cart.quantity,
                    'option'     : cart.option.name,
                    'unit_price' : cart.product.price,
                    'price'      : cart.product.price * cart.quantity
                } for cart in carts]

                return JsonResponse({'user':request.user.id, 'cart_list':cart_list}, status=200)
            return JsonResponse({'message':'VALUE_ERROR'}, status=404)
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
        except TypeError:
            return JsonResponse({'message':'TYPE_ERROR'}, status=400)
        except  ValueError:
            return JsonResponse({'message':'UNAUTHORIZED'}, status=401)

    @authorization
    def delete(self, request):
        try:
            carts_id = request.GET.getlist('cart_id')

            for cart in carts_id:
                if not Cart.objects.filter(user=request.user, id=int(cart)).exists:
                    return JsonResponse({'message':'VALUE_ERROR'}, status=404)
                Cart.objects.get(user=request.user, id=int(cart)).delete()

            return JsonResponse({'message':'SUCCESS'}, status=200)
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
        except TypeError:
            return JsonResponse({'message':'TYPE_ERROR'}, status=400)
        except  ValueError:
            return JsonResponse({'message':'UNAUTHORIZED'}, status=401)

    @authorization
    def patch(self, request):
        try:
            cart_id = request.GET['cart_id']
            option  = request.GET['option']

            if Cart.objects.filter(user=request.user, id=cart_id).exists():
                change_cart= Cart.objects.get(id=cart_id)
                if option == 'add':
                    change_cart.quantity += 1
                    change_cart.save()
                if option == 'subtration':
                    change_cart.quantity -= 1
                    change_cart.save()
                
                return JsonResponse({'message':'SUCCESS'}, status=200)
            return JsonResponse({'message':'VALUE_ERROR'}, status=404)
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
        except TypeError:
            return JsonResponse({'message':'TYPE_ERROR'}, status=400)
        except  ValueError:
            return JsonResponse({'message':'UNAUTHORIZED'}, status=401)