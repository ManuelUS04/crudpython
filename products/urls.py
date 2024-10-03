from django.urls import path
from .views import ProductViewSet, product_index, product_create, product_edit, product_delete, product_show

urlpatterns = [
    path('', product_index, name='product_index'),
    path('create/', product_create, name='product_create'),
    path('edit/<int:pk>/', product_edit, name='product_edit'),
    path('show/<int:pk>/', product_show, name='product_show'),
    path('delete/<int:pk>/', product_delete, name='product_delete'),
    path('products/', ProductViewSet.as_view({'get': 'list', 'post': 'create'}), name='product-list'),
    path('products/<int:pk>/', ProductViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='product-detail'),
]
