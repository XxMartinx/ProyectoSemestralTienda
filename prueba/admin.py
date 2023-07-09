from django.contrib import admin
from .models import Marca, Producto, Contacto, Carrito, CarritoItem, MontoExtra
# Register your models here.

class ProductoAdmin(admin.ModelAdmin):
    list_display = ["nombre","precio","nuevo","marca"]
    list_editable =["precio"]
    search_fields =["nombre"]
    list_filter = ["marca", "nuevo", "precio"]

admin.site.register(Marca)
admin.site.register(Producto,ProductoAdmin)
admin.site.register(Contacto)
admin.site.register(Carrito)
admin.site.register(CarritoItem)
admin.site.register(MontoExtra)