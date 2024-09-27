from django.contrib import admin
from .models import Product, Material, ProductMaterial, Warehouse


class MaterialAdmin(admin.ModelAdmin):
    list_display = ['material_name', 'id']


class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'id']

admin.site.register(Product, ProductAdmin)
admin.site.register(Material, MaterialAdmin)
admin.site.register(ProductMaterial)
admin.site.register(Warehouse)
