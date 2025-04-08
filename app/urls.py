from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("productos/", views.productos_page, name="productos"),
    path("productos/<int:id>", views.producto_detalle, name="producto_detalle"),
    path("noticias/", views.noticias_page, name="noticias"),
    path("noticias/<int:id>", views.noticia_detalle, name="noticia_detalle"),
    path("contacto/", views.contacto_view, name="contacto"),
    path("carrito/", views.carrito, name="carrito"),
    path("carrito/agregar/<int:id>/", views.agregar_a_carrito, name="agregar_a_carrito"),
    path("politicas/", views.politicas, name="politicas"),
    path("carrito/quitar/<int:id>/", views.quitar_cantidad, name="quitar_cantidad"),
    path("carrito/agregar/<int:id>/", views.agregar_cantidad, name="agregar_cantidad"),
    path("carrito/eliminar/<int:id>/", views.eliminar_producto, name="eliminar_producto"),

]
