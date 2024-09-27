from django.urls import path
from .views import ProductCreateAPIView, ProductListAPIView, \
    ProductRetrieveUpdateDestroyAPIView, MaterialCreateAPIView, \
        MaterialListAPIView, MaterialRetrieveUpdateDestroyAPIView,\
            ProductMaterialListAPIView, ProductMaterialCreateAPIView,\
                ProductMaterialRetrieveUpdateDestroyAPIView, WarehouseCreateAPIView,\
                    WarehouseListAPIView, WaarehouseRetrieveUpdateDestroyAPIView
                


urlpatterns = [
    path('products/', ProductListAPIView.as_view()),
    path('product/create/', ProductCreateAPIView.as_view()),
    path('product/detail-update-delete/<uuid:id>/', ProductRetrieveUpdateDestroyAPIView.as_view()),
    path('materials/', MaterialListAPIView.as_view()),
    path('material/create/', MaterialCreateAPIView.as_view()),
    path('material/detail-update-delete/<int:pk>/', MaterialRetrieveUpdateDestroyAPIView.as_view()),
    path('product-materials/', ProductMaterialListAPIView.as_view()),
    path('product-material/create/', ProductMaterialCreateAPIView.as_view()),
    path('product-material/detail-update-delete/<int:pk>/', ProductMaterialRetrieveUpdateDestroyAPIView.as_view()),
    path('warehouses/', WarehouseListAPIView.as_view()),
    path('warehouse/create/', WarehouseCreateAPIView.as_view()),
    path('warehouse/detail-update-delete/<int:pk>/', WaarehouseRetrieveUpdateDestroyAPIView.as_view()),
]
