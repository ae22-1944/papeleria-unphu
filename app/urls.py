from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("productos/", views.productos, name="productos"),
    path("noticias/", views.noticias, name="noticias"),
    path("contacto/", views.contacto, name="contacto"),
    path("carrito/", views.carrito, name="carrito"),
    path("politicas/", views.politicas, name="politicas"),
]
