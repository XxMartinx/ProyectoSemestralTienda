from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Marca(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=50,unique=True)
    precio = models.IntegerField()
    descripcion = models.TextField()
    nuevo = models.BooleanField()
    marca = models.ForeignKey(Marca, on_delete=models.PROTECT)
    fecha_fabricacion = models.DateField()
    imagen = models.ImageField(upload_to="productos", null=True )
    def __str__(self) -> str:
        return f"Id: {self.pk} | Nombre: {self.nombre} | Imagen: {self.imagen} | Descripcion: {self.descripcion} | Precio: {self.precio} || Marca_id: {self.marca.id} "

class Carrito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="carrito")
    total = models.DecimalField(null=True, max_digits=10, decimal_places=2)
    
    def __str__(self) -> str:
        return f"Id: {self.pk} | Usuario_id: {self.usuario.id} | Usuario: {self.usuario.username} | Total: {self.total}"

class CarritoItem(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name="items")

    def __str__(self):
        return self.carrito
        
opciones_consultas = [
    [0, "consulta"],
    [1, "reclamo"],
    [2, "sugerencia"],
    [3, "felicitaciones"],

]


class Contacto(models.Model):
    nombre = models.CharField(max_length=50)
    correo = models.EmailField()
    tipo_consulta = models.IntegerField(choices=opciones_consultas)
    mensaje = models.TextField()
    avisos = models.BooleanField()

    def __str__(self):
        return self.nombre

        

