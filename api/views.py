from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import (
    Category, Product, Client, Order
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

    
    