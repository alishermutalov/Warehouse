from rest_framework import serializers
from .models import Product, ProductMaterial, Material, Warehouse
from rest_framework.exceptions import ValidationError, NotFound

class ProductSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(required=False, read_only=True)
    
    class Meta:
        model = Product
        fields = ['id','product_name', 'product_code']
        

class MaterialSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Material
        fields = ['id','material_name']
        

class ProductMaterialSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(required=False, read_only=True)
    product = ProductSerializer(read_only=True)  # Use the ProductSerializer for product details
    material = MaterialSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), source='product')
    material_id = serializers.PrimaryKeyRelatedField(queryset=Material.objects.all(), source='material')
    class Meta:
        model = ProductMaterial
        fields = ['id','product_id','material_id','product','material', 'quantity']
        
    def validate(self, attrs):
        product = attrs.get('product')
        material = attrs.get('material')
        
        if not product or not material:
            raise NotFound("Product or Material not found!")
        return attrs
    
    def update(self, instance, validated_data):
        instance.product = validated_data.get('product')
        instance.material = validated_data.get('material')
        instance.quantity = validated_data.get('quantity')
        return instance
    
    def create(self, validated_data):
        product = validated_data.get('product')
        material = validated_data.get('material')
        quantity = validated_data.get('quantity')
        if ProductMaterial.objects.filter(product=product, material=material).exists():
            raise serializers.ValidationError({
                'message': 'This product-material combination already exists.'
            })
        
        product_material = ProductMaterial.objects.create(
            product=product,
            material=material,
            quantity=quantity
        )
        return product_material
        
    
class WarehouseSerializer(serializers.ModelSerializer):
    material = MaterialSerializer(read_only=True)
    material_id = serializers.PrimaryKeyRelatedField(queryset=Material.objects.all(), source='material')
    
    class Meta:
        model = Warehouse
        fields = ['id','material_id', 'material','remainder','price']
        
    def validate(self, attrs):
        material = attrs.get('material')
        print(material)
        if not material:
            raise ValidationError("Material not found")
        return super().validate(attrs)