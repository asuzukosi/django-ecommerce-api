from django.urls import path
from .viewsets import GetLatestProducts, GetProductDetails, GetCategoryProduct, CategoryDetail, search
urlpatterns = [
    path('get_latest_products/', GetLatestProducts.as_view(), name="Get the 4 latest products"),
    path('search/', search, name="Search for product based on query"),
    path('<str:category_slug>/products/', GetCategoryProduct.as_view(), name="Get all products of category"),
    path('<str:category_slug>/', CategoryDetail.as_view(), name="Get the details of specified category"),
    path('<str:category_slug>/<str:product_slug>/', GetProductDetails.as_view(), name="Get the product details"),

]