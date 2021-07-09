from django.urls import path

from orders.views import CartAddUpdateView, CartDeleteView, CartView

urlpatterns = [
    path('/cart', CartView.as_view()),
]
