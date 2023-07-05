from django.urls import path, include
from .views import home, contacto, galeria,agregar_producto,listar_producto,\
     modificar_producto,eliminar_producto, registro,ProductoViewset,MarcaViewset,detalle_productos,terminoycondiciones, carrito_index
from rest_framework import routers


router =  routers.DefaultRouter()
router.register('producto', ProductoViewset)
router.register('marca', MarcaViewset)


urlpatterns = [
    path('', home, name="home"),  
    path('contacto/', contacto, name="contacto"),
    path('galeria/', galeria, name="galeria"), 
    path('agregar-producto/', agregar_producto, name="agregar_producto"), 
    path('listar-producto/', listar_producto, name="listar_producto"),
    path('modificar-producto/<id>/', modificar_producto, name="modificar_producto"),
    path('eliminar-producto/<id>/', eliminar_producto, name="eliminar_producto"),
    path('registro/', registro, name="registro"),
    path('api/', include(router.urls)),
    path('detalles-productos/<int:producto_id>', detalle_productos, name="detalle_productos"),
    path('terminoy-condiciones/', terminoycondiciones, name="terminoycondiciones"),

    #CARRITO
    path('carrito/',carrito_index, name="carrito"),

]