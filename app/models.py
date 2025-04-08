from django.db import models
from django.contrib.auth.models import User

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    categoria = models.ForeignKey('Categoria', on_delete=models.CASCADE)
    imagen_url = models.URLField(blank=True)  # Campo para la URL de la imagen

    def __str__(self):
        return self.nombre


class Noticia(models.Model):
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    imagen_url = models.URLField(blank=True)  # Campo para la URL de la imagen

    def __str__(self):
        return self.titulo

class Categoria(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class CarritoItem(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    agregado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.agregado_en