import json
from django.db.models import Q, query
from django.http import JsonResponse
from django.views import View
from products.models import Product, Category, ProductType, Option

class ProductView(View):
    def get(self, request):
        sort_dic = {
            '1':'-is_new',
            '2':'price',
            '3':'-price',
            'm':'-view_count'}
        product_type = request.GET.getlist('product_type', None)
        category     = request.GET.get('category', None)
        sort         = request.GET.get('sort', '1')
        page         = request.GET.get('page', None)

        q = Q()
        if category:
            q &= Q(category_id=category)
        if product_type:
            q &= Q(product_type_id__in=product_type)
        if page == 'm':
            products = Product.objects.filter(q).order_by(sort_dic[page])[:10]
        else:
            products = Product.objects.filter(q).order_by(sort_dic[sort])
        products_info = [{
            "name"            : product.name,
            "price"           : product.price,
            "main_image_url"  : product.main_image_url,
            "hover_image_url" : product.hover_image_url,
            "pk"              : product.pk         if page != 'm' else None,
            "view_count"      : product.view_count if page != 'm' else None,
            "is_new"          : product.is_new     if page != 'm' else None
        } for product in products]

        categories = Category.objects.all()
        category_info = [{"name" : category.name} for category in categories]

        return JsonResponse({"products_info" : products_info, "category_info" : category_info}, status=200)

class ProductDetailView(View):
    def get(self, request, product_id):
        product = Product.objects.get(id=product_id)
        product_info = [{
            "name"           : product.name,
            "price"          : product.price,
            "main_image_url" : product.main_image_url,
            "description"    : product.description
        }]

        product.view_count += 1
        product.save()

        options = Option.objects.all()
        option_info = [{
            "option_name"  : option.name,
            "option_price" : option.price
        } for option in options]

        return JsonResponse({"product_info" : product_info, "option_info" : option_info}, status=200)