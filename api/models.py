from django.db import models
from cloudinary.models import CloudinaryField

from django.db.models.signals import post_save
from django.dispatch import receiver

from django.core.validators import MinValueValidator

# MODELS FOR PRODUCT
class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=100,verbose_name='Name')
    category_registerdate = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tbl_category'

    def __str__(self):
        return self.category_name


class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=200,verbose_name='Name')
    product_description = models.TextField(null=True,verbose_name='Description')
    product_image = CloudinaryField('image',default='')
    product_price = models.DecimalField(max_digits=10,decimal_places=2,default=0,verbose_name='Price',validators=[MinValueValidator(0)])
    product_registerdate = models.DateTimeField(auto_now=True)
    category_id = models.ForeignKey(Category,related_name='Products',
                                    to_field='category_id',on_delete=models.RESTRICT,
                                    db_column='category_id',verbose_name='Category')
    

    class Meta:
        db_table = 'tbl_product'

    def __str__(self):
        return self.product_name

@receiver(post_save,sender=Product)
def generate_sku(sender,instance,created,**kwargs):
    if created:
        category_code = instance.category.name[:2].upper()
        correlative = str(Product.objects.count()).zfill(3)
        instance.sku = f'{category_code}{correlative}'
        instance.save()
######## MODELS FOR USER AND CLIENT #########
from django.contrib.auth.models import User

class Client(models.Model):
    client_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User,on_delete=models.RESTRICT)
    client_name = models.CharField(max_length=255)
    client_dni = models.CharField(max_length=8)
    client_genre = models.CharField(max_length=1)
    client_phone = models.CharField(max_length=20)
    client_birthdate = models.DateField(null=True)
    client_address= models.TextField()
    
    class Meta:
        db_table = 'tbl_client'
        
    def __str__(self):
        return self.client_name
    
######### MODELS FOR ORDERS ###############

class Order(models.Model):
    
    STATE_CHOICES = (
        ('0','Requested'),
        ('1','Payed')
    )
    
    order_id = models.AutoField(primary_key=True)
    order_registerdate = models.DateTimeField(auto_now=True)
    order_number = models.CharField(max_length=20,null=True)
    order_total = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    order_state = models.CharField(max_length=1,default='0',choices=STATE_CHOICES)
    client_id = models.ForeignKey(Client,on_delete=models.RESTRICT)
    
    
    class Meta:
        db_table = 'tbl_order'
        
    def __str__(self):
        return self.order_number
    
class OrderDetail(models.Model):
    orderdetail_id = models.AutoField(primary_key=True)
    orderdetail_quantity = models.IntegerField(default=1, validators=[MinValueValidator(0)])
    orderdetail_subtotal = models.DecimalField(max_digits=10,decimal_places=2)
    order_id = models.ForeignKey(Order,on_delete=models.RESTRICT)
    product_id = models.ForeignKey(Product,on_delete=models.RESTRICT)
    
    
    class Meta:
        db_table = 'tbl_orderdetail'
        
    def __str__(self):
        return self.orderdetail_product.name