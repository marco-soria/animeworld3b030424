from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User, Category, Product, Review, Order, OrderItem, ShippingAddress
from .serializers import (CategorySerializer, ProductSerializer, ReviewSerializer,
                          OrderSerializer, ShippingAddressSerializer, UserSerializer)


# Vistas para Categorías
class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryDetailView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# Vistas para Productos
class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

@api_view(['GET'])
def search_product(request):
    query = request.query_params.get('query')
    if query:
        products = Product.objects.filter(name__icontains=query)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    else:
        return Response({'error': 'Please provide a search query'}, status=status.HTTP_400_BAD_REQUEST)


# Vistas para Órdenes
class OrderListView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

@api_view(['POST'])
def create_order(request):
    user = request.user
    data = request.data
    order_items = data.get('order_items', [])
    total_price = sum(item.get('price', 0) * item.get('quantity', 0) for item in order_items)

    if total_price > 0:
        order = Order.objects.create(user=user, total_price=total_price)
        for item_data in order_items:
            product_id = item_data.get('product')
            quantity = item_data.get('quantity', 0)
            price = item_data.get('price', 0)
            if product_id and quantity > 0:
                try:
                    product = Product.objects.get(pk=product_id)
                    OrderItem.objects.create(order=order, product=product, quantity=quantity, price=price)
                except Product.DoesNotExist:
                    pass  # Manejar el caso en el que el producto no exista
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response({'error': 'Invalid order data'}, status=status.HTTP_400_BAD_REQUEST)


# Vistas para Reseñas
@api_view(['POST'])
def create_review(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = ReviewSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user, product=product)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Vistas para Usuarios
class UserListView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

@api_view(['GET'])
def search_user(request):
    query = request.query_params.get('query')
    if query:
        users = User.objects.filter(email__icontains=query)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    else:
        return Response({'error': 'Please provide a search query'}, status=status.HTTP_400_BAD_REQUEST)


# Vista para el perfil del usuario actual
@api_view(['GET', 'PUT'])
def current_user_profile(request):
    user = request.user
    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Vistas de Autenticación
@api_view(['POST'])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login as django_login

@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    user = authenticate(request, email=email, password=password)
    if user is not None:
        django_login(request, user)
        return Response({'detail': 'Login successful'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)