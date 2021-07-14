import json

from django.views     import View
from django.db.models import Q, Count
from django.http      import JsonResponse

from products.models  import Product

class SearchView(View):
    def post(self, request):
        try:
            page        = int(request.GET.get('page', 1))
            page_size   = 24
            limit       = int(page_size * page)
            offset      = int(limit - page_size)

            word        = request.GET.get('word', None)
            if not word:
                return JsonResponse({'message':'VALUE_ERROR'}, status=404)
            search_list = Product.objects.filter(Q(name__icontains=word) | Q(description__icontains=word)).annotate(review_count=Count('review')).order_by('-review_count')[offset:limit]
            context     = [{
                'name'           :search.name,
                'price'          :search.price,
                'main_image_url' :search.main_image_url,
                'hover_image_url':search.hover_image_url
            } for search in search_list]

            return JsonResponse({'search_list':context, 'search_word':word}, status = 200)
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
        except TypeError:
            return JsonResponse({'message':'TYPE_ERROR'}, status=400)
        except ValueError:
            return JsonResponse({'message':'UNAUTHORIZED'}, status=401)