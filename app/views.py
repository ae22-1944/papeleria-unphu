from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Producto, Noticia, Categoria, CarritoItem
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from .forms import ContactoForm
from django.core.mail import EmailMessage
from django.conf import settings
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django import forms


def home(request):
    productos_list = Producto.objects.all().order_by('id')
    noticias_list = Noticia.objects.all().order_by('id')

    productos_paginator = Paginator(productos_list, 3)
    noticias_paginator = Paginator(noticias_list, 3)

    productos_page = request.GET.get("productos_page")
    noticias_page = request.GET.get("noticias_page")

    productos = productos_paginator.get_page(productos_page)
    noticias = noticias_paginator.get_page(noticias_page)

    template = loader.get_template("index.html")
    context = {
        "productos": productos,
        "noticias": noticias,
    }

    return HttpResponse(template.render(context, request))


def contacto(request):
    template = loader.get_template("contacto.html")
    return HttpResponse(template.render())


def politicas(request):
    template = loader.get_template("politicas.html")
    return HttpResponse(template.render())


def carrito(request):
    carrito = request.session.get('carrito', {})
    productos_en_carrito = []

    total = 0
    for producto_id, cantidad in carrito.items():
        producto = Producto.objects.get(id=producto_id)
        subtotal = producto.precio * cantidad
        productos_en_carrito.append({
            'producto': producto,
            'cantidad': cantidad,
            'subtotal': subtotal,
        })
        total += subtotal

    context = {
        'productos_en_carrito': productos_en_carrito,
        'total': total,
    }

    return render(request, 'carrito.html', context)


def producto_detalle(request, id):
    producto = Producto.objects.get(id=id)
    template = loader.get_template("producto_detalle.html")
    context = {
        "producto": producto,
    }

    return HttpResponse(template.render(context, request))


def productos_page(request):
    productos_list = Producto.objects.all().order_by('id')
    paginator = Paginator(productos_list, 3)
    page_number = request.GET.get("page")
    productos = paginator.get_page(page_number)

    template = loader.get_template("productos_page.html")
    context = {
        "productos": productos,
    }

    return HttpResponse(template.render(context, request))


def noticias(request):
    noticias_list = Noticia.objects.all().order_by('id')
    paginator = Paginator(noticias_list, 3)
    page_number = request.GET.get("page")
    noticias = paginator.get_page(page_number)

    template = loader.get_template("noticias.html")
    context = {
        "noticias": noticias,
    }

    return HttpResponse(template.render(context, request))


def noticia_detalle(request, id):
    noticia = Noticia.objects.get(id=id)
    template = loader.get_template("noticia_detalle.html")
    context = {
        "noticia": noticia,
    }

    return HttpResponse(template.render(context, request))


def noticias_page(request):
    noticias_list = Noticia.objects.all().order_by('id')
    paginator = Paginator(noticias_list, 3)
    page_number = request.GET.get("page")
    noticias = paginator.get_page(page_number)

    template = loader.get_template("noticias_page.html")
    context = {
        "noticias": noticias,
    }

    return HttpResponse(template.render(context, request))


def agregar_a_carrito(request, id):
    producto = get_object_or_404(Producto, id=id)
    carrito = request.session.get('carrito', {})

    if str(id) in carrito:
        carrito[str(id)] += 1
    else:
        carrito[str(id)] = 1

    request.session['carrito'] = carrito
    messages.success(request, f'“{producto.nombre}” fue agregado al carrito.')
    return redirect('carrito')


def quitar_cantidad(request, id):
    carrito = request.session.get('carrito', {})
    if str(id) in carrito:
        if carrito[str(id)] > 1:
            carrito[str(id)] -= 1
        else:
            del carrito[str(id)]

    request.session['carrito'] = carrito
    messages.success(request, "Cantidad reducida.")
    return redirect('carrito')


def agregar_cantidad(request, id):
    carrito = request.session.get('carrito', {})
    if str(id) in carrito:
        carrito[str(id)] += 1

    request.session['carrito'] = carrito
    messages.success(request, "Cantidad aumentada.")
    return redirect('carrito')


def eliminar_producto(request, id):
    carrito = request.session.get('carrito', {})
    if str(id) in carrito:
        del carrito[str(id)]

    request.session['carrito'] = carrito
    messages.success(request, "Producto eliminado.")
    return redirect('carrito')


def productos(request):
    categorias = Categoria.objects.all()
    productos_por_categoria = {}

    for categoria in categorias:
        productos_por_categoria[categoria] = Producto.objects.filter(categoria=categoria).order_by('id')

    paginator = Paginator(Producto.objects.all().order_by('id'), 3)
    page_number = request.GET.get("page")
    productos = paginator.get_page(page_number)

    template = loader.get_template("productos.html")
    context = {
        "productos_por_categoria": productos_por_categoria,
        "productos": productos,
    }

    return HttpResponse(template.render(context, request))


class ContactoForm(forms.Form):
    nombre = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Tu nombre completo'}))
    correo = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'nombre@ejemplo.com'}))
    asunto = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={'placeholder': 'Motivo del mensaje'}))
    mensaje = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Escribe tu mensaje aquí...'}), required=True)

    def enviar_correo(self):
        conexion = smtplib.SMTP(host='smtp.gmail.com', port=587)
        conexion.ehlo()
        conexion.starttls()
        conexion.login(user='usuario@gmail.com', password='Prueba')

        mensaje = MIMEMultipart()
        mensaje['Subject'] = 'LP1: Su mensaje ha sido recibido!'
        cuerpo_mensaje = """
            Hola,

            Gracias por solicitar información, les estaremos respondiendo a la mayor brevedad posible.

            Saludos,
            Equipo Ventas LP1
        """
        mensaje.attach(MIMEText(cuerpo_mensaje, 'plain'))
        mensaje['From'] = 'usuario@gmail.com'
        mensaje['To'] = 'usuario@gmail.com, usuario2@gmail.com'
        conexion.send_message(mensaje)
        conexion.quit()


def contacto_view(request):
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            try:
                form.enviar_correo()
                return render(request, 'contacto.html', {'form': form, 'success': True})
            except Exception as e:
                return render(request, 'contacto.html', {'form': form, 'success': False, 'error': str(e)})
        else:
            return render(request, 'contacto.html', {'form': form, 'success': False})
    else:
        form = ContactoForm()

    return render(request, 'contacto.html', {'form': form, 'success': False})
