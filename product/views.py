from django.db.models import Avg
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import Product, Category, Review
from .serializers import ProductSerializer, ProductDetailSerializer, CategorySerializer, ReviewSerializer
from .permissions import IsModerator

@api_view(['GET'])
def product_reviews_list_api_view(request):
    products = Product.objects.all()
    result = []
    for product in products:
        reviews = product.reviews.all()
        avg_rating = reviews.aggregate(rating=Avg('stars'))['rating']
        result.append({
            'id': product.id,
            'title': product.title,
            'description': product.description,
            'price': str(product.price),
            'category': CategorySerializer(product.category).data if product.category else None,
            'reviews': ReviewSerializer(reviews, many=True).data,
            'rating': avg_rating
        })
    return Response(result)

@api_view(['GET', 'POST'])
def category_list_api_view(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        data = CategorySerializer(categories, many=True).data
        return Response(data=data)
    elif request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@api_view(['GET', 'PUT', 'DELETE'])
def category_detail_api_view(request, id):
    try:
        category = Category.objects.get(id=id)
    except Category.DoesNotExist:
        return Response(data={'error': 'category not found!'}, status=404)
    if request.method == 'GET':
        data = CategorySerializer(category).data
        return Response(data=data)
    elif request.method == 'PUT':
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    elif request.method == 'DELETE':
        category.delete()
        return Response(status=204)

@api_view(['GET', 'POST'])
def review_list_api_view(request):
    if request.method == 'GET':
        reviews = Review.objects.all()
        data = ReviewSerializer(reviews, many=True).data
        return Response(data=data)
    elif request.method == 'POST':
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@api_view(['GET', 'PUT', 'DELETE'])
def review_detail_api_view(request, id):
    try:
        review = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response(data={'error': 'review not found!'}, status=404)
    if request.method == 'GET':
        data = ReviewSerializer(review).data
        return Response(data=data)
    elif request.method == 'PUT':
        serializer = ReviewSerializer(review, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    elif request.method == 'DELETE':
        review.delete()
        return Response(status=204)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsModerator])
def product_detail_api_view(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response(data={'error': 'product not found!'}, status=404)
    if request.method == 'GET':
        data = ProductDetailSerializer(product, many=False).data
        return Response(data=data)
    elif request.method == 'PUT':
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    elif request.method == 'DELETE':
        product.delete()
        return Response(status=204)


@api_view(['GET', 'POST'])
@permission_classes([IsModerator])
def product_list_api_view(request):
    if request.method == 'GET':
        product = Product.objects.all()
        data = ProductSerializer(instance=product, many=True).data
        return Response(status=status.HTTP_200_OK, data=data)
    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)