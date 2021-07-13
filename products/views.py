import json
from django.http import JsonResponse
from django.views import View
from products.models import Product, Category, ProductType, Option, Review
from utils           import authorization

class ProductView(View):
    def get(self, request):
        products   = Product.objects.all()
        categories = Category.objects.all()

        products_info = [{
            "name"          : product.name,
            "price"         : product.price,
            "main_image_url"  : product.main_image_url,
            "hover_image_url" : product.hover_image_url,
            "view_count"    : product.view_count,
        } for product in products]

        category_info = [{
            "name" : category.name,
        } for category in categories]

        return JsonResponse({
            "message"       : "SUCCESS",
            "products_info" : products_info,
            "category_info" : category_info}, status=201)


class ProductDetailView(View):
    def get(self, request, product_id):
        product_info = []
        option_info  = []
        product      = Product.objects.get(id=product_id)
        option       = Option.objects.get(id=1)

        product.view_count += 1 
        product.save()

        product_info.append({
            "name"           : product.name,
            "price"          : product.price,
            "main_image_url" : product.main_image_url,
            "description"    : product.description
        })

        option_info.append({
            "option_name"  : option.name,
            "option_price" : option.prices
        })

        return JsonResponse({
            "message"      : "SUCCESS",
            "product_info" : product_info,
            "option_info"  : option_info}, status=201)

class ProductReview(View):
    @authorization
    def post(self, request):
        data = json.loads(request.body)
        try:
            Review.objects.create(
                user       = request.user,
                product_id = data['product_id'],
                comment    = data['comment'],
                score      = data['score'] 
            )

            return JsonResponse({'MESSAGE':'SUCCESS'}, status=201)
        except KeyError:
            return JsonResponse({'MESSAGE':'KEYERROR'}, status=400)