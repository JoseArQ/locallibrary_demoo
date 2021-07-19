from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^books/$', views.BookListView.as_view(), name = "books"), #llamamos una clase BookListView con el metodo as_view
    url(r'^book/(?P<pk>\d+)$', views.BookDetailView.as_view(), name= "book-detail"),
]