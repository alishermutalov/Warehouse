from django.db import models
import uuid

class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product_name = models.CharField(max_length=255)
    product_code = models.IntegerField(unique=True)
    
    def __str__(self) -> str:
        return self.product_name
    

class Material(models.Model):
    material_name = models.CharField(max_length=255)
    
    def __str__(self) -> str:
        return self.material_name

class ProductMaterial(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    quantity = models.FloatField()
    
    def __str__(self) -> str:
        return f"{self.pk}) {self.quantity} pcs {self.material}(s) for make {self.product}"
    
class Warehouse(models.Model):
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    remainder = models.FloatField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    
    def __str__(self) -> str:
        return f"{self.material}-{self.remainder}"
