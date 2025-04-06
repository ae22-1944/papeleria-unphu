from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader


def home(request):
    template = loader.get_template("index.html")
    return HttpResponse(template.render())


def contacto(request):
    template = loader.get_template("contacto.html")
    return HttpResponse(template.render())


def politicas(request):
    template = loader.get_template("politicas.html")
    return HttpResponse(template.render())


def noticias(request):
    template = loader.get_template("noticias.html")
    return HttpResponse(template.render())


def carrito(request):
    template = loader.get_template("carrito.html")
    return HttpResponse(template.render())


def productos(request):
    template = loader.get_template("productos.html")
    return HttpResponse(template.render())
