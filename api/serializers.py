from rest_framework import serializers

from .models import (
    Category, Product, Client, Order, OrderDetail
)
class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
                
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        
    def to_representation(self,instance):
        representation = super().to_representation(instance)
        if instance.product_image:
            representation['product_image'] = instance.product_image.url
        else:
            representation['product_image'] = None
        representation['category_name'] = instance.category_id.category_name
        return representation
    
class CategoryProductSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True,read_only=True)
    class Meta:
        model = Category
        fields = ['category_id','category_name','products']
        
##### serializers  for orders
class OrderDetailSerializerPOST(serializers.ModelSerializer):
    class Meta:
        model = OrderDetail
        fields = ['product_id','orderdetail_quantity']
        
class OrderSerializerPOST(serializers.ModelSerializer):
    orderdetails = OrderDetailSerializerPOST(many=True)
    
    class Meta:
        model = Order
        fields = ['order_registerdate','order_state','client_id',
                  'orderdetails']
        
    def create(self,validated_data):
        list_order_detail = validated_data.pop('orderdetails')
        order = Order.objects.create(**validated_data)
        for obj_order_detail in list_order_detail:
            OrderDetail.objects.create(order_id=order,**obj_order_detail)
        return order
    
#### serializers for order GET
class OrderDetailSerializerGET(serializers.ModelSerializer):
    class Meta:
        model = OrderDetail
        fields = ['orderdetail_id','orderdetail_quantity','product_id']
        
    def to_representation(self,instance):
        representation = super().to_representation(instance)
        representation['product_name'] = instance.product_id.product_name
        representation['product_image'] = instance.product_id.product_image.url
        return representation
        
class OrderSerializerGET(serializers.ModelSerializer):
    orderdetails = OrderDetailSerializerGET(many=True,read_only=True)
    
    class Meta:
        model = Order
        fields = ['order_id','order_registerdate','order_state',
                  'client_id','orderdetails']
        
    def to_representation(self,instance):
        representation = super().to_representation(instance)
        representation['client_name'] = instance.client_id.client_name
        return representation
            
        