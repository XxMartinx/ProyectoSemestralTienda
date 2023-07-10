from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto, Carrito, CarritoItem, MontoExtra  
from .forms import ContactoForm, ProductoForm, CustomUserCreationForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import Http404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required
from rest_framework import viewsets
from .serializers import ProductoSerializer, MarcaSerializer
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm


class MarcaViewset(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = MarcaSerializer

class ProductoViewset(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

    def get_queryset(self):
        productos = Producto.objects.all()
        nombre = self.request.GET.get('nombre')

        if nombre:
            productos = productos.filter(nombre__contains=nombre)

        return productos


def home(request):
    productos = Producto.objects.all()
    data = {
        'productos': productos
    }
    return render(request, 'tienda/home.html', data)

def contacto(request):
    data = {
        'form': ContactoForm()
    }

    if request.method == 'POST':
        formulario = ContactoForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            data["mensaje"] = "Contacto guardado"
        else:
            data["form"] = formulario

    return render(request, 'tienda/contacto.html', data)

def galeria(request):
    return render(request, 'tienda/galeria.html')

@permission_required('tienda.add_producto')
def agregar_producto(request):
    data = {
        'form': ProductoForm()
    }

    if request.method == 'POST':
        formulario = ProductoForm(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Producto registrado")
        else:
            data["form"] = formulario

    return render(request, 'tienda/producto/agregar.html', data)

@permission_required('tienda.view_producto')
def listar_producto(request):
    productos = Producto.objects.all()
    page = request.GET.get('page', 1)

    try:
        paginator = Paginator(productos, 2)
        productos = paginator.page(page)
    except:
        raise Http404

    data = {
        'entity': productos,
        'paginator': paginator,
    }

    return render(request, 'tienda/producto/listar.html', data)

@permission_required('tienda.change_producto')
def modificar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    data ={
        'form': ProductoForm(instance=producto)
    }

    if request.method == 'POST':
        formulario = ProductoForm(data=request.POST, instance=producto, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Modificado correctamente")
            return redirect(to="listar_producto")
        data["form"] = formulario

    return render(request, 'tienda/producto/modificar.html', data)

@permission_required('tienda.delete_producto')
def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    producto.delete()
    messages.success(request, "Eliminado correctamente")
    return redirect(to="listar_producto")

def registro(request):
    data = {
        'form': CustomUserCreationForm()
    }

    if request.method == 'POST':
        formulario = CustomUserCreationForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            user = authenticate(username=formulario.cleaned_data["username"], password=formulario.cleaned_data["password1"])
            usuario_logeado= User.objects.last()
            carrito = Carrito()
            carrito.usuario = usuario_logeado
            carrito.total = 0
            carrito.save()
            login(request, user)
            messages.success(request, "Te has registrado correctamente")
            return redirect(to="home")
        data["form"] = formulario

    return render(request, 'registration/registro.html', data)

def detalle_productos(request, id):
    producto = get_object_or_404(Producto, id=id)
    return render(request, 'tienda/detalleproducto.html', {'p': producto})

def terminoycondiciones(request):
    return render(request, 'tienda/terminoycondiciones.html')

@login_required
def carrito_index(request):
    usuario_logeado = request.user
    carrito = get_object_or_404(Carrito, usuario=usuario_logeado)
    productos = carrito.items.all()
    monto_extra = MontoExtra.objects.first().valor if MontoExtra.objects.exists() else None

    nuevo_precio_carrito = sum(item.producto.precio for item in productos)
    carrito.total = nuevo_precio_carrito
    carrito.save()

    nuevo_precio_carrito_impuesto = sum(item.producto.precio for item in productos) + (monto_extra or 0)
    carrito.total = nuevo_precio_carrito_impuesto
    carrito.save()

    contexto = {
        'usuario': usuario_logeado,
        'items_carrito': productos,
        'monto_extra': monto_extra,
        'total_carrito': nuevo_precio_carrito,
        'total_carrito_impuesto': nuevo_precio_carrito_impuesto,
    }

    return render(request, 'tienda/carrito/index.html', contexto)

@login_required
def carrito_save(request):
    if request.method == 'POST':
        producto = Producto.objects.get(id=request.POST['producto_id'])
        usuario_logeado = User.objects.get(username=request.user)

        carrito = Carrito.objects.get(usuario=usuario_logeado.id)
        item_carrito = CarritoItem()
        item_carrito.carrito = carrito
        item_carrito.producto = producto
        item_carrito.save()

        carrito.total = producto.precio + carrito.total
        carrito.save()
        messages.success(request, f"El producto {producto.nombre} fue agregado al carrito")

        return redirect("carrito")

    else:
        return redirect("carrito")

@login_required
def carrito_clean(request):
    usuario_logeado = User.objects.get(username=request.user)
    carrito = Carrito.objects.get(usuario=usuario_logeado.id)
    carrito.items.all().delete()
    carrito.total = 0
    carrito.save()
    return redirect('carrito')

@login_required
def item_carrito_delete(request, item_carrito_id):
    item_carrito = CarritoItem.objects.get(id=item_carrito_id)
    carrito = item_carrito.carrito
    
    # Vuelvo a calcular el precio del carrito
    nuevo_precio_carrito = 0 - item_carrito.producto.precio
    for item in carrito.items.all():
        nuevo_precio_carrito += item.producto.precio

    # Realizo los cambios en la base de datos
    carrito.total = nuevo_precio_carrito
    item_carrito.delete()
    carrito.save()
    return redirect("carrito")

@login_required
def finalizar_compra(request):
    if request.method == 'GET':
        usuario_logeado = request.user

        carrito = Carrito.objects.get(usuario=usuario_logeado)


        if carrito.items.exists():
            carrito.items.all().delete()
            carrito.total = 0
            carrito.save()

            messages.success(request, "¡Tu compra ha sido realizada con éxito!")
        else:
            messages.warning(request, "No tienes productos en tu carrito.")

        return redirect('carrito')  

@login_required
def ver_perfil(request):
    usuario = User.objects.get(username=request.user.username)
    data = {
        'usuario': usuario
    }
    return render(request, 'tienda/ver_perfil.html', data)


@login_required
def cambiar_contraseña(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Tu contraseña ha sido modificada.')
            return redirect('ver_perfil')
    else:
        form = PasswordChangeForm(user=request.user)
    
    return render(request, 'tienda/cambiar_contraseña.html', {'form': form})


