from django.urls import path, include

urlpatterns = [
    path('orders', include('orders.urls')),
    path('users', include('users.urls')),
    path('products', include('products.urls')),
]
