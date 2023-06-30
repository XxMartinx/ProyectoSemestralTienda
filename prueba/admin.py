from django.contrib import admin
from .models import Marca, Producto, Contacto
# Register your models here.

class ProductoAdmin(admin.ModelAdmin):
    list_display = ["nombre","precio","nuevo","marca"]
    list_editable =["precio"]
    search_fields =["nombre"]
    list_filter = ["marca", "nuevo", "precio"]

admin.site.register(Marca)
admin.site.register(Producto,ProductoAdmin)
admin.site.register(Contacto)