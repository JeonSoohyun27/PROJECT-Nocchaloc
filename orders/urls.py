from django.urls import path

from orders.views import CartView, OrderView, OrderItemView

urlpatterns = [
    path('/cart', CartView.as_view()),
    path('', OrderView.as_view()),
    path('/<int:order_id>', OrderItemView.as_view())
]
