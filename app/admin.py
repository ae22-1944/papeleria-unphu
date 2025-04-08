from django.contrib import admin
from .models import Producto, Noticia, Categoria, CarritoItem

admin.site.register(Producto)
admin.site.register(Noticia)
admin.site.register(Categoria)
admin.site.register(CarritoItem)