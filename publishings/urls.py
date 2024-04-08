from django.urls import path, re_path, register_converter

from publishings.apps import PublishingsConfig

from . import views, converters
from .views import BaseView, CategoryListView, ConnectionView, ClientCreateView, ClientListView, ClientUpdateView, \
    ClientDeleteView

app_name = PublishingsConfig.name

register_converter(converters.FourDigitYearConverter, "year4")

urlpatterns = [
    path("", BaseView.as_view(), name="home"), # http://127.0.0.1:8000/publishings/
    path('categorys/', CategoryListView.as_view(), name='category_list'),
    path("connection/", ConnectionView.as_view(), name="connection_list"), # http://127.0.0.1:8000/publishings/

    # Client
    path('clients/create/', ClientCreateView.as_view(), name='clients_create'),
    path('clients/<int:pk>', ClientListView.as_view(), name='clients_list'),
    path('update/<int:pk>', ClientUpdateView.as_view(), name='clients_update'),
    path('delete/<int:pk>', ClientDeleteView.as_view(), name='clients_delete'),



    path("about/", views.about, name="about"),
    path("addpage/", views.addpage, name="add_page"), # http://127.0.0.1:8000/publishings/addpage/
    path("contact/", views.contact, name="contact"), # http://127.0.0.1:8000/publishings/contact/
    path("login/", views.login, name="login"), # http://127.0.0.1:8000/publishings/addpage/
    # path("categories/<slug:categories_slug>/", categories_bu_slug, name="categories_slug"), # http://127.0.0.1:8000/publishings/categories/music/
    path("post/<int:post_id>", views.show_post, name="post"),

]