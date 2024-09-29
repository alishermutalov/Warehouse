from django.shortcuts import render
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import ProductSerializer, MaterialSerializer,\
    ProductMaterialSerializer, WarehouseSerializer, CheckAvailabilitySerializer,\
        MaterialBatchTrackingSerializer
from .custom_permissions import IsAdminOrReadOnly
from .models import Product, ProductMaterial, Material, Warehouse

class ProductCreateAPIView(CreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly, ]
    
    
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        
        return Response({
            'success':True,
            'message':'Product Created!',
            'data':response.data
        })
        

class ProductListAPIView(ListAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    

class ProductRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly]
    queryset = Product.objects.all()
    lookup_field = 'id'
    
    
    
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs) 
        return Response({
            'message':'Product updated successfully',
            'data':response.data
        })
        
    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return Response({
            'success':True,
            'message':'Product deleted successfully'
        })
        
        
#Material CRUD
class MaterialCreateAPIView(CreateAPIView):
    serializer_class = MaterialSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly, ]
    
    
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        
        return Response({
            'success':True,
            'message':'Material Created!',
            'data':response.data
        })
        

class MaterialListAPIView(ListAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = MaterialSerializer
    queryset = Material.objects.all()
    

class MaterialRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = MaterialSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly]
    queryset = Material.objects.all()
    
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs) 
        return Response({
            'message':'Material updated successfully',
            'data':response.data
        })
        
    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return Response({
            'success':True,
            'message':'Material deleted successfully'
        })
        
        
#ProductMaterial CRUD
class ProductMaterialCreateAPIView(CreateAPIView):
    serializer_class = ProductMaterialSerializer
    permission_classes =[permissions.IsAuthenticated, IsAdminOrReadOnly, ]
    
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        product_material = serializer.save()
        
        return Response({
            'success':True,
            'message':'ProductMaterial Created!',
            'data': ProductMaterialSerializer(product_material).data
        })
        

class ProductMaterialListAPIView(ListAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = ProductMaterialSerializer
    queryset = ProductMaterial.objects.all()
    
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        return response
    

class ProductMaterialRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ProductMaterialSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly]
    queryset = ProductMaterial.objects.all()

    
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs) 
        return Response({
            'message':'Product Material updated successfully',
            'data':response.data
        })
        
    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return Response({
            'success':True,
            'message':'Product Material deleted successfully'
        })
        
#Warehouse CRUD
class WarehouseCreateAPIView(CreateAPIView):
    serializer_class = WarehouseSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly]
    
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({
            'success':True,
            'message':'Warehouse created successfully!',
            'data':response.data
        })
        
    
class WarehouseListAPIView(ListAPIView):
    serializer_class = WarehouseSerializer
    permission_classes = [permissions.IsAuthenticated,]
    queryset = Warehouse.objects.all()
    
    def get(self, request, *args, **kwargs):
        response = super().get(self, request, *args, **kwargs)
        return Response({
            'success':True,
            'message':'Warehous loaded successfully!',
            'data':response.data
        })
        

class WaarehouseRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = WarehouseSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly,]
    queryset = Warehouse.objects.all()
    
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response({
            'success':True,
            'message':'Warehouse item updated successfully!',
            'data':response.data
        })
        
    def delete(self, request, *args, **kwargs):
        return Response({
            'success':True,
            'message':'Warehouse item deleted successfully!'
        })
        

class CheckAvailibilityAPIView(APIView):
    permission_classes = [permissions.AllowAny,]
    def post(self, request, *args, **kwargs):
        serializer = CheckAvailabilitySerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            return Response({
                'data':validated_data
            })
        return Response(serializer.errors)
    

class MaterialBatchTrackingAPIView(APIView):
    permission_classes = [permissions.AllowAny,]
    def post(self, request, *args, **kwargs):
        serializer = MaterialBatchTrackingSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            return Response({
                'data':validated_data
            })
        return Response(serializer.errors)