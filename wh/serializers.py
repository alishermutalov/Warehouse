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
    

class ProductItemSerializer(serializers.Serializer):
    product_code = serializers.IntegerField()
    quantity = serializers.IntegerField()


class CheckAvailabilitySerializer(serializers.Serializer):
    products = serializers.ListField(child=ProductItemSerializer())
    
    def validate(self, attrs):
        if type(attrs.get('products'))!=list:
            raise ValidationError({
                'message':'Data should be list of products'
            })
    
        data = self.check_availability(attrs['products'])
        return data
    
    def check_availability(self, data):
        required_materials = []
        
        for item in data:
            if Product.objects.filter(product_code=item['product_code']).exists():
                product = Product.objects.get(product_code=item['product_code'])
            else:
                unmatched_product_code = item.get('product_code')
                required_materials.append({
                    'input_code': unmatched_product_code,
                    'message': 'Unmatched product code.'
                })
                continue
            
            if ProductMaterial.objects.filter(product=product).exists():
                product_materials = ProductMaterial.objects.filter(product=product)
                materials = []
                
                for product_material in product_materials:
                    warehouse_entries = Warehouse.objects.filter(material=product_material.material)
                    
                    total_available_quantity = sum(entry.remainder for entry in warehouse_entries)

                    required_quantity = product_material.quantity*item['quantity']
                    if total_available_quantity >= required_quantity:
                        status = 'Enough'
                        shortage = 0
                    else:
                        status = 'Not enough'
                        shortage = required_quantity - total_available_quantity
                    
                    materials.append({
                        'material_name': product_material.material.material_name,
                        'required_quantity': required_quantity,
                        'available_quantity': total_available_quantity,
                        'status': status,
                        'shortage': shortage if shortage > 0 else None
                    })
            
           
            required_materials.append({
                'product_name': product.product_name,
                'materials': materials
            })
        
        return required_materials

        
class MaterialBatchTrackingSerializer(serializers.Serializer):
    products = serializers.ListField(child=ProductItemSerializer())
    
    def validate(self, attrs):
        if type(attrs.get('products'))!=list:
            raise ValidationError({
                'message':'Data should be list of products'
            })
    
        data = self.check_availability(attrs['products'])
        return data
    
    def check_availability(self, data):
        required_materials = []
        warehouse_materials = Warehouse.objects.all()
        warehouse_materials_count = {}
        for warehouse_item in warehouse_materials:
            if warehouse_materials_count.get(warehouse_item.material.material_name) is not None:
                warehouse_materials_count[warehouse_item.material.material_name]+= warehouse_item.remainder
            else:
                warehouse_materials_count[warehouse_item.material.material_name] = warehouse_item.remainder
        
        
        for item in data:
            if Product.objects.filter(product_code=item['product_code']).exists():
                product = Product.objects.get(product_code=item['product_code'])
            else:
                unmatched_product_code = item.get('product_code')
                required_materials.append({
                    'input_code': unmatched_product_code,
                    'message': 'Unmatched product code.'
                })
                continue
            
            if ProductMaterial.objects.filter(product=product).exists():
                product_materials = ProductMaterial.objects.filter(product=product)
                materials = []
                for product_material in product_materials:
                    total_required_quantity = product_material.quantity*item['quantity']
                    
                    warehouse_entries = Warehouse.objects.filter(material=product_material.material)
                    
                    wh_material = []
                    wh_entire_sum=total_required_quantity
                    for wh_entire in warehouse_entries:
                        reminder = wh_entire.remainder
                        if total_required_quantity<= warehouse_materials_count[wh_entire.material.material_name]:
                            wh_material.append({   
                                                    'available_quantity':warehouse_materials_count[wh_entire.material.material_name],
                                                })
                        
                            warehouse_materials_count[wh_entire.material.material_name]-=total_required_quantity
                            print(wh_entire.material.material_name,' - ',warehouse_materials_count[wh_entire.material.material_name])
                            break
                        else:
                            missing_quantity = total_required_quantity-warehouse_materials_count[wh_entire.material.material_name]
                            wh_material.append({   
                                                    'available_quantity':warehouse_materials_count[wh_entire.material.material_name],
                                                    'missing_quantity':missing_quantity
                                                })

                            warehouse_materials_count[wh_entire.material.material_name]-=warehouse_materials_count[wh_entire.material.material_name]
                            break
                    materials.append({
                        'material_name':product_material.material.material_name,
                        'material_batches': wh_material,
                        'required_quantity':total_required_quantity,
                    })
                    
            required_materials.append({
                'product_name': product.product_name,
                'materials': materials
            })
        
        return required_materials
    
#  print(warehouse_materials_count)
#                         if warehouse_materials_count[wh_entire.material.material_name] >= total_required_quantity:
#                             if wh_entire.remainder <= wh_entire_sum:
                                
#                                 wh_material.append({   
#                                             'batch_id':wh_entire.id,
#                                             'available_quantity':warehouse_materials_count[wh_entire.material.material_name],
#                                             'batch_quantity':wh_entire.remainder,
#                                             'price':wh_entire.price,
#                                             'received':wh_entire.remainder
#                                         })
#                                 wh_entire_sum-=wh_entire.remainder
#                                 warehouse_materials_count[wh_entire.material.material_name]-=wh_entire.remainder
#                             elif wh_entire.remainder>=wh_entire_sum:
                                
#                                 wh_material.append({   
#                                             'batch_id':wh_entire.id,
#                                             'available_quantity':warehouse_materials_count[wh_entire.material.material_name],
#                                             'batch_quantity':wh_entire.remainder,
#                                             'price':wh_entire.price,
#                                             'received':wh_entire_sum
#                                         })
#                                 warehouse_materials_count[wh_entire.material.material_name]-=wh_entire.remainder
                            
#                         else:
#                             wh_material.append({   
#                                             'missing':total_required_quantity-warehouse_materials_count[wh_entire.material.material_name]
#                                         })
                    