from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto
from .forms import ContactoForm, ProductoForm, CustomUserCreationForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import Http404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required
from rest_framework import viewsets
from .serializers import ProductoSerializer, MarcaSerializer
# Create your views here.

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
            data["mensaje"] = "contacto guardado"
        else:
            data["form"] = formulario

    return render(request, 'tienda/contacto.html', data)

def galeria(request):
    return render(request, 'tienda/galeria.html')

@permission_required('tienda.add_producto') #Este comando sirve para otorgar permisos y tenga mas seguridad.
def agregar_producto(request):
    
    data = {
        'form': ProductoForm()
    }
    if request.method == 'POST':
        formulario = ProductoForm(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Producto Registrado")
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
        if formulario.is_valid(): #Evalua si es valido el formulario
            formulario.save()#lo guarda cuando ya es valido
            messages.success(request, "Modificado Correctamente")
            return redirect(to="listar_producto") 
        data["form"] = formulario#si no se le muestran nuevamente los datos

    return render(request, 'tienda/producto/modificar.html', data)    

@permission_required('tienda.delate_producto')
def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    producto.delete()
    messages.success(request, "Eliminado Correctamente")
    return redirect(to="listar_producto")  

def registro(request):
    data= {
        'form': CustomUserCreationForm()
    }

    if request.method == 'POST':
        formulario = CustomUserCreationForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            user = authenticate(username=formulario.cleaned_data["username"], password=formulario.cleaned_data["password1"])
            login(request, user)
            messages.success(request, "Te has Registrado Correctamente")
            return redirect(to="home")
        data["form"] = formulario    

    return render(request, 'registration/registro.html', data)     

def detalle_productos(request):
    productos = Producto.objects.all()
    data = {
        'productos': productos
    }
    return render(request, 'tienda/detalleproducto.html', data) 