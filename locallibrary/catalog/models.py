from django.db import models
from django.urls import reverse # usa un genereador de URLS  para revertir los patrones de url
import uuid # requerida para las instancias de libros únicas
from datetime import date

class Genre(models.Model):
    """Modelo que representa genero literario (p. ej. ciencia ficcion)"""

    name = models.CharField(max_length=200,
                            help_text="ingrese el nombre del genero (p. ej. Ciencia Ficción, Poesía etc)" )

    def __str__(self):
        """
        Cadena que representa una instancia particular del modelo
        """
        return self.name

class Language(models.Model):
    name = models.CharField(max_length=200,
                            help_text='Ingrese el idioma del libro')

    def __str__(self):
        return self.name

class Book(models.Model):
    """
    modelo para representar un libro (pero no un ejemplar o copia específica)
    """
    title = models.CharField(max_length=200)

    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)

    summary = models.TextField(max_length=1000, help_text="ingrese breve descripción del libro")

    isbn = models.CharField('ISBN', max_length=13, help_text= '13 caracteres <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')

    genre = models.ManyToManyField(Genre, help_text="Seleccione un género para este libro")

    language = models.ForeignKey('Language',
                                 on_delete=models.SET_NULL, null=True)
    class Meta:
        ordering = ['title', 'author']

    # métodos

    def display_genre(self):
        return ', '.join([genre.name for genre in self.genre.all()[:3]])
    # añadir descripcion
    display_genre.short_description= 'Genre'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """
        Devuelve el url a una instancia particular de Book
        usado para ingresar al detalle de un registro
        """
        return reverse('book-detail', args=[str(self.id)])

class BookInstance(models.Model):
    """
     Modelo para representar una copia especifica de un libro
     """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Id único para este libro particular en toda la biblioteca")
    book = models.ForeignKey('Book',
                             on_delete=models.SET_NULL,
                             null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
     )
    status = models.CharField(max_length=1,
                              choices=LOAN_STATUS,
                              blank=True,
                              default='m',
                              help_text='disponibilidad del libro')
    class Meta:
         ordering = ["due_back"]

    def __str__(self):
        """string para representar el objetdo del modelo
         """
        return f'{self.id} ({self.book.title})'

class Author(models.Model):
    """
    Para representar el autor
    """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Die', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        """
        retorna url para acceder a una instancia particula de un autor
        """
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):

        return f'{self.last_name}, {self.first_name}'

