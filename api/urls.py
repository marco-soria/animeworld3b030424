from django.urls import path

from . import views

urlpatterns = [
    path('client', views.ClientView.as_view()),
    path('category',views.CategoryView.as_view()),
    path('product',views.ProductView.as_view()),
    path('category/<int:category_id>/products',views.CategoryProductView.as_view()),
    path('product/search',views.SearchProductView.as_view()),
    path('product/img/upload',views.UploadProductImgView.as_view()),
    path('order',views.OrderRegisterView.as_view())
]