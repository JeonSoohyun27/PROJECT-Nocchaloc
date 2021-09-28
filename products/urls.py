from django.urls import path
from products.views import ProductView, ProductDetailView, ProductReviewView, SearchView
urlpatterns = [
    path('', ProductView.as_view()),
    path('/<int:product_id>', ProductDetailView.as_view()),
    path('/review', ProductReviewView.as_view()),
    path('/search', SearchView.as_view()),
    path('/<int:product_id>/review', ProductReviewView.as_view(), name='get_review'),
    path('/review/<int:review_id>', ProductReviewView.as_view(), name='delete_review'),
    path('/review/<int:review_id>', ProductReviewView.as_view(), name='patch_review')
]