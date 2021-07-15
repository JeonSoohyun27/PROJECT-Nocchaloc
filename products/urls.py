from django.urls import path
from products.views import ProductView, ProductDetailView, ProductReview, SearchView
urlpatterns = [
    path('', ProductView.as_view()),
    path('/<int:product_id>', ProductDetailView.as_view()),
    path('/review', ProductReview.as_view()),
    path('/search', SearchView.as_view())
]
