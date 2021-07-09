from django.db.models import Q
from django.http import JsonResponse
from django.views import View
from products.models import Product, Category, ProductType, Option

class ProductView(View):
    def get(self, request):
        products_info = []
        category_info = []
        categories    = Category.objects.all()
        sort_dic ={'1':'-is_new', '2':'price', '3':'-price'}

        product_type = request.GET.getlist('product_type', None)
        category     = request.GET.get('category', None)
        sort         = request.GET.get('sort', None) # 1~3

        q = Q()
        if category:
            q &= Q(category_id=category)
        if product_type:
            q &= Q(product_type_id__in=product_type)

        products = Product.objects.filter(q).order_by(sort_dic[sort])

        for product in products:
            products_info.append({
                "pk"              : product.pk,
                "name"            : product.name,
                "price"           : product.price,
                "main_image_url"  : product.main_image_url,
                "hover_image_url" : product.hover_image_url,
                "view_count"      : product.view_count,
                "is_new"          : product.is_new
            })
        for category in categories:
            category_info.append({
                "name" : category.name
            })
        return JsonResponse({
            "message"       : "SUCCESS",
            "products_info" : products_info,
            "category_info" : category_info}, status=201)


class ProductDetailView(View):
    def get(self, request, product_id):
        product_info = []
        option_info  = []
        product = Product.objects.get(id=product_id)
        option  = Option.objects.get(id=1)
        product_info.append({
            "name"           : product.name,
            "price"          : product.price,
            "main_iamge_url" : product.main_image_url,
            "description"    : product.description
        })
        option_info.append({
            "option_name"  : option.name,
            "option_price" : option.price
        })
        return JsonResponse({
            "message"       : "SUCCESS",
            "product_info"  : product_info,
            "option_info"   : option_info}, status=201)