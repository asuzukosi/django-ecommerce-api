from .serializers import ProductSerializer, CategorySerializer
from rest_framework.viewsets import ModelViewSet
from apps.product.models import Product, Category
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from django.db.models import Q
from rest_framework.decorators import api_view


class GetLatestProducts(APIView):
    def get(self, request):
        products = Product.objects.all()
        if len(products) > 4:
            products = products[:4]

        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetProductDetails(APIView):
    def get_object(self, category_slug, product_slug):
        try:
            product = Product.objects.filter(category__slug=category_slug, slug=product_slug)[0]
            # TODO: Should produce an error if two products bear the same category and slug
            return product
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, category_slug, product_slug):
        product = self.get_object(category_slug, product_slug)
        serializer = ProductSerializer(instance=product)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetCategoryProduct(APIView):
    """
    This endpoint returns a list of all the products that belong the
    specified category
    """

    def get(self, request, category_slug):
        """
        This is a get endpoint to get all the products of the
        category with the slug in the params
        :param request:
        :param category_slug:
        :return: All products from specified category
        """
        category = Category.objects.get(slug=category_slug)
        products = category.products

        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryDetail(APIView):
    def get_object(self, category_slug):
        try:
            category = Category.objects.get(slug=category_slug)
            return category
        except Category.DoesNotExist:
            return Http404

    def get(self, request, category_slug):
        category = self.get_object(category_slug)
        serializer = CategorySerializer(instance=category)

        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def search(request):
    query = request.data.get('query')
    if query:
        products = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    else:
        return Response([], status=status.HTTP_204_NO_CONTENT)
