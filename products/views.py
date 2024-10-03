from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Product
from .serializers import ProductSerializer
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from .serializers import ProductSerializer
from django.contrib import messages

class ProductViewSet(viewsets.ViewSet):
    
    def list(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        product = Product.objects.get(pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def update(self, request, pk=None):
        product = Product.objects.get(pk=pk)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        product = Product.objects.get(pk=pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
 
#***************** OJO: Esto es para las vistas HTML de aqui hacia abajo ***************************
def product_index(request):
    products = Product.objects.all()
    return render(request, 'products/index.html', {'products': products})


def product_create(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        description = request.POST.get('description', '').strip()
        price = request.POST.get('price', '').strip()
        stock = request.POST.get('stock', '').strip()       
        
        error_messages = []

        # Validaciones
        if not name:
            error_messages.append("El campo Nombre es obligatorio.")
        if not description:
            error_messages.append("El campo Descripción es obligatorio.")
        if not price:
            error_messages.append("El campo Precio es obligatorio.")
        if not stock:
            error_messages.append("El campo Stock es obligatorio.")

        
        try:
            if float(price) <= 0:
                error_messages.append("El campo Precio debe ser un número mayor que 0.")
        except ValueError:
            error_messages.append("El campo Precio debe ser un número válido.")

        try:
            if int(stock) <= 0:
                error_messages.append("El campo Stock debe ser un número mayor que 0.")
        except ValueError:
            error_messages.append("El campo Stock debe ser un número válido.")
       
        if error_messages:
            messages.error(request, " ".join(error_messages))
            return render(request, 'products/create.html')

        
        Product.objects.create(name=name, description=description, price=price, stock=stock)
        return redirect('product_index')

    return render(request, 'products/create.html')


def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        description = request.POST.get('description', '').strip()
        price = request.POST.get('price', '').strip()
        stock = request.POST.get('stock', '').strip()

        error_messages = []

        # Validaciones
        if not name:
            error_messages.append("El campo Nombre es obligatorio.")
        if not description:
            error_messages.append("El campo Descripción es obligatorio.")
        if not price:
            error_messages.append("El campo Precio es obligatorio.")
        if not stock:
            error_messages.append("El campo Stock es obligatorio.")

        try:
            if float(price) <= 0:
                error_messages.append("El campo Precio debe ser un número mayor que 0.")
        except ValueError:
            error_messages.append("El campo Precio debe ser un número válido.")

        try:
            if int(stock) <= 0:
                error_messages.append("El campo Stock debe ser un número mayor que 0.")
        except ValueError:
            error_messages.append("El campo Stock debe ser un número válido.")

        if error_messages:
            messages.error(request, " ".join(error_messages))
            return render(request, 'products/edit.html', {'product': product})

        product.name = name
        product.description = description
        product.price = price
        product.stock = stock
        product.save()
        return redirect('product_index')

    return render(request, 'products/edit.html', {'product': product})

def product_show(request, pk):
    product = Product.objects.get(pk=pk)
    if request.method == 'POST':
        product.name = request.POST['name']
        product.description = request.POST['description']
        product.price = request.POST['price']
        product.stock = request.POST['stock']
        product.save()
        return redirect('product_index')
    return render(request, 'products/show.html', {'product': product})

def product_delete(request, pk):
    product = Product.objects.get(pk=pk)
    product.delete()
    return redirect('product_index')
