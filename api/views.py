from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import (
    Category, Product, Client, Order, OrderDetail
)

from .serializers import (
    CategorySerializer, ProductSerializer, ClientSerializer, OrderSerializerPOST, OrderSerializerGET, CategoryProductSerializer
)

class CategoryView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
class ClientView(generics.ListAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    
class ProductView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
class CategoryProductView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    lookup_url_kwarg = 'categoria_id'
    serializer_class = CategoryProductSerializer
    
class SearchProductView(APIView):
    
    def post(self,request):
        search = request.data['search']
        data = Product.objects.filter(product_name__contains=search)
        serializer = ProductSerializer(data,many=True)
        return Response(serializer.data)
    
#### upload product img
from rest_framework.parsers import MultiPartParser,JSONParser
import cloudinary.uploader


class UploadProductImgView(APIView):
    parser_classes = (
        MultiPartParser,
        JSONParser
    )
    
    @staticmethod
    def post(request):
        file = request.data.get('product_image')
        
        upload_data = cloudinary.uploader.upload(file)
        print(upload_data)
        context = {
            'url':upload_data['secure_url']
        }
        
        return Response(context)
    
class OrderRegisterView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    #serializer_class = PedidoSerializerPOST
    def get_serializer_class(self):
        if self.request.method == "GET":
            return OrderSerializerGET
        else:
            return OrderSerializerPOST
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data)

#cart
from rest_framework import status
from rest_framework.decorators import api_view
from .cart import Cart

@api_view(['GET'])
def cart(request):
    
    return Response({"message": "This view returns the content of the cart"}, status=status.HTTP_200_OK)

@api_view(['POST'])
def add_to_cart(request, product_id):
    try:
        product = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        return Response({"error": "Producto not found"}, status=status.HTTP_404_NOT_FOUND)
    
    quantity = int(request.data.get('quantity', 1))
    image_url = request.data.get('image_url')  # Si necesitas una imagen específica
    
    cart = Cart(request)
    cart.add(product, quantity, image_url)
    
    return Response({"message": "Product added to the cart"}, status=status.HTTP_200_OK)

@api_view(['DELETE'])
def remove_from_cart(request, product_id):
    try:
        product = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        return Response({"error": "Producto not found"}, status=status.HTTP_404_NOT_FOUND)
    
    cart = Cart(request)
    cart.delete(product)
    
    return Response({"message": "Product deleted from the cart"}, status=status.HTTP_204_NO_CONTENT)

@api_view(['DELETE'])
def clear_cart(request):
    cart = Cart(request)
    cart.clear()
    
    return Response({"message": "Cart cleaned"}, status=status.HTTP_204_NO_CONTENT)

##client
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import ClientForm
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm


@api_view(['POST'])
def register_client(request):
    username = request.data.get('username')
    password = request.data.get('password')
    first_name = request.data.get('first_name')
    last_name = request.data.get('last_name')

    if not username or not password or not first_name or not last_name:
        return Response({'error': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name)
    if user:
        login(request, user)
        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
    else:
        return Response({'error': 'Failed to create user'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login_client(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)
    if user:
        login(request, user)
        return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@login_required
def logout_client(request):
    logout(request)
    return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)

@login_required(login_url='/login')
def update_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            client = form.save(commit=False)
            client.user = request.user
            client.save()
            return redirect('/account')  # Redirigimos a la página de cuenta del usuario
    else:
        form = ClientForm(instance=request.user.client)
    
    return Response({'message': 'Please provide a valid request method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@login_required(login_url='/login')
def register_order(request):
    if request.method == "POST":
        form = ClientForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            
            obj_user = User.objects.get(pk=request.user.id)
            obj_user.first_name = data['first_name']
            obj_user.last_name = data['last_name']
            obj_user.email = data['email']
            obj_user.save()
            
            try:
                obj_client = obj_user.client  # Suponiendo que cada usuario tiene un perfil de cliente asociado
            except Client.DoesNotExist:
                obj_client = Client.objects.create(user=obj_user, client_name=data['client_name'], client_dni=data['client_dni'], client_genre=data['client_genre'], client_phone=data['client_phone'], client_birthdate=data['client_birthdate'], client_address=data['client_address'])
                
            total_amount = float(request.session.get('total_amount', 0))  # Aseguramos que el valor predeterminado sea 0 si no hay carrito
            order_obj = Order.objects.create(client_id=obj_client)
            order_number = 'ORD' + order_obj.order_registerdate.strftime('%Y') + str(order_obj.order_id)
            order_obj.order_number = order_number
            order_obj.save()
            
            cart = request.session.get('cart', {})  # Aseguramos que el carrito sea un diccionario vacío si no está definido
            for key, value in cart.items():
                product_obj = Product.objects.get(pk=value['product_id'])
                order_detail_obj = OrderDetail.objects.create(order_id=order_obj, product_id=product_obj, orderdetail_quantity=int(value['quantity']), orderdetail_subtotal=float(value['subtotal']))
                
            paypal_dict = {
                "business": "sb-0vpvr30010384@business.example.com",
                "amount": total_amount,
                "item_name": "ORDER NO : " + order_obj.order_number,
                "invoice": order_obj.order_id,
                "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
                "return": request.build_absolute_uri(reverse('web:thanks')),
                "cancel_return": request.build_absolute_uri(reverse('web:index')),
            }

            frm_paypal = PayPalPaymentsForm(initial=paypal_dict)
            context = {
                'order': order_obj,
                'frm_paypal': frm_paypal
            }
            
            request.session['order_id'] = order_obj.order_id
            
            return Response({'message': 'Order registered successfully'}, status=status.HTTP_201_CREATED)
    else:
        return Response({'error': 'Invalid request method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@login_required(login_url='/login')
def thanks(request):
    paypal_id = request.GET.get('PayerID', None)
    if paypal_id is not None:
        order_id = request.session.get('order_id')
        order = Order.objects.get(pk=order_id)
        order.status = '1'
        order.save()
        
        request.session['order_id'] = None
        cart = Cart(request)
        cart.clear()
    
    return Response({'message': 'Thank you for your purchase'}, status=status.HTTP_200_OK)

