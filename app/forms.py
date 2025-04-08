from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from django.contrib import messages
from django.conf import settings
from django import forms
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from .models import Producto, Noticia, Categoria

# --- VISTAS PRINCIPALES ---
def home(request):
    productos_list = Producto.objects.all()
    noticias_list = Noticia.objects.all()

    productos_paginator = Paginator(productos_list, 3)
    noticias_paginator = Paginator(noticias_list, 3)

    productos_page = request.GET.get("productos_page")
    noticias_page = request.GET.get("noticias_page")

    productos = productos_paginator.get_page(productos_page)
    noticias = noticias_paginator.get_page(noticias_page)

    return render(request, "index.html", {"productos": productos, "noticias": noticias})


def contacto(request):
    return render(request, "contacto.html")


def politicas(request):
    return render(request, "politicas.html")


# --- PRODUCTOS ---
def productos_page(request):
    productos_list = Producto.objects.all()
    paginator = Paginator(productos_list, 3)
    page_number = request.GET.get("page")
    productos = paginator.get_page(page_number)

    return render(request, "productos_page.html", {"productos": productos})


def producto_detalle(request, id):
    producto = get_object_or_404(Producto, id=id)
    return render(request, "producto_detalle.html", {"producto": producto})


def productos_por_categoria(request):
    categorias = Categoria.objects.all()
    productos_por_categoria = {}

    for categoria in categorias:
        productos_por_categoria[categoria] = Producto.objects.filter(categoria=categoria)

    paginator = Paginator(Producto.objects.all(), 3)
    page_number = request.GET.get("page")
    productos = paginator.get_page(page_number)

    context = {
        "productos_por_categoria": productos_por_categoria,
        "productos": productos,
    }

    return render(request, "productos.html", context)


# --- NOTICIAS ---
def noticias_page(request):
    noticias_list = Noticia.objects.all()
    paginator = Paginator(noticias_list, 3)
    page_number = request.GET.get("page")
    noticias = paginator.get_page(page_number)

    return render(request, "noticias_page.html", {"noticias": noticias})


def noticia_detalle(request, id):
    noticia = get_object_or_404(Noticia, id=id)
    return render(request, "noticia_detalle.html", {"noticia": noticia})


# --- CARRITO ---
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

    return render(request, 'carrito.html', {
        'productos_en_carrito': productos_en_carrito,
        'total': total
    })


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


# --- FORMULARIO DE CONTACTO ---
class ContactoForm(forms.Form):
    nombre = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Tu nombre completo'}))
    correo = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'nombre@ejemplo.com'}))
    asunto = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={'placeholder': 'Motivo del mensaje'}))
    mensaje = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Escribe tu mensaje aquí...'}), required=True)

    def enviar_correo(self):
        conexion = smtplib.SMTP(host='smtp.gmail.com', port=587)
        conexion.ehlo()
        conexion.starttls()
        conexion.login(user=settings.EMAIL_HOST_USER, password=settings.EMAIL_HOST_PASSWORD)

        mensaje = MIMEMultipart()
        mensaje['Subject'] = 'LP1: Su mensaje ha sido recibido!'
        mensaje.attach(MIMEText(
            """
            Hola,

            Gracias por solicitar información, les estaremos respondiendo a la mayor brevedad posible.

            Saludos,
            Equipo Ventas LP1
            """, 'plain'))

        mensaje['From'] = settings.EMAIL_HOST_USER
        mensaje['To'] = 'noelreyes426@gmail.com, usuario2@gmail.com'
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
