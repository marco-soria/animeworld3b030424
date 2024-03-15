from django.urls import path

from . import views

urlpatterns = [
    path('client', views.ClientView.as_view()),
    path('category',views.CategoryView.as_view()),
    path('product',views.ProductView.as_view()),
    path('category/<int:category_id>/products',views.CategoryProductView.as_view()),
    path('product/search',views.SearchProductView.as_view()),
    path('product/img/upload',views.UploadProductImgView.as_view()),
    path('order',views.OrderRegisterView.as_view()),
    
    path('cart/', views.cart, name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/clear/', views.clear_cart, name='clear_cart'),
    
    path('client/register', views.register_client),
    path('client/login', views.login_client),
    path('client/logout', views.logout_client),
    path('client/update', views.update_client),
    path('client/thanks', views.thanks),
]