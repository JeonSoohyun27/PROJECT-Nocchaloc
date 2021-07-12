import json

from django.views    import View
from django.http     import JsonResponse

from orders.models   import Cart
from products.models import Product, Option
from utils           import authorization

class CartView(View):
    @authorization
    def get(self, request):
        try:
            if Cart.objects.filter(user=request.user).exists():
                carts = Cart.objects.filter(user=request.user)

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
    def post(self, request):
        try:
            data       = json.loads(request.body)
            product_id = data['product_id']
            option_id  = data['option_id']
            quantity   = data['quantity']

            if Product.objects.filter(id=product_id).exists() and Option.objects.filter(id=option_id).exists():
                if Cart.objects.filter(product_id=product_id, option_id=option_id, user=request.user).exists():
                    add_cart = Cart.objects.get(product_id=product_id, option_id=option_id, user=request.user)
                    add_cart.quantity += quantity
                    add_cart.save()
                    return JsonResponse({'message':'SUCCESS'}, status=200)

                Cart.objects.create(
                    user       = request.user, 
                    product_id = product_id, 
                    quantity   = quantity, 
                    option_id  = option_id)

                return JsonResponse({'message':'SUCCESS'}, status=201)
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
            product_id = request.GET['product_id']
            option     = request.GET['option']

            if Cart.objects.filter(user=request.user, product=product_id).exists():
                change_cart = Cart.objects.get(user=request.user, product=product_id)
                if option == 'add':
                    change_cart.quantity += 1

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