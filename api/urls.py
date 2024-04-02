from django.urls import path
from . import views

urlpatterns = [
    # URLs para Categorías
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('categories/<int:pk>/', views.CategoryDetailView.as_view(), name='category-detail'),
    path('categories/<str:category_name>/products/', views.CategoryProductListView.as_view(), name='category-product-list'),

    # URLs para Productos
    path('products/', views.ProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('products/search/', views.search_product, name='product-search'),

    # URLs para Órdenes
    path('orders/', views.OrderListView.as_view(), name='order-list'),
    path('orders/<int:pk>/', views.OrderDetailView.as_view(), name='order-detail'),
    path('orders/create/', views.create_order, name='order-create'),

    # URLs para Reseñas
    path('products/<int:pk>/reviews/', views.create_review, name='review-create'),

    # URLs para Usuarios
    path('users/', views.UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', views.UserDetailView.as_view(), name='user-detail'),
    path('users/search/', views.search_user, name='user-search'),
    path('users/profile/', views.current_user_profile, name='user-profile'),

    # URL para Registro de Usuario
    path('register/', views.register_user, name='register'),
    
    path('login/', views.login, name='login')

    # Otras URLs
    # ...
]
