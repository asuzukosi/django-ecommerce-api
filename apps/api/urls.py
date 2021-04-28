from django.urls import path, include

urlpatterns = [
    path('', include('djoser.urls')),  # Include the url patterns for djoser
    path('', include('djoser.urls.authtoken')),  # Include the url patterns for djoser authentication
    path('', include('rest_framework.urls')),  # Include the url patterns for django-rest-framework authentication
    path('products/', include('apps.product.api.router')),  # Include all the urls for the products endpoint
    path('order/', include('apps.orders.api.router'))  # Include all the urls for the orders endpoint
]
