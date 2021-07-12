from django.urls import path
from products.views import ProductMain, ProductView, ProductDetailView
urlpatterns = [

    path('', ProductMain.as_view()),
    path('/productslist', ProductView.as_view()),
    path('/productslist/<int:product_id>', ProductDetailView.as_view())
]