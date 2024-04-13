from django.urls import path, re_path, register_converter

from publishings.apps import PublishingsConfig

from . import views, converters
from .views import BaseView, CategoryListView, ConnectionView, ClientCreateView, ClientListView, ClientUpdateView, \
    ClientDeleteView, ClientDetailView, PaymentStripeView, StripeWebhookView

app_name = PublishingsConfig.name

register_converter(converters.FourDigitYearConverter, "year4")

urlpatterns = [
    path("", BaseView.as_view(), name="home"), # http://127.0.0.1:8000/publishings/
    path('categorys/', CategoryListView.as_view(), name='category_list'),
    path("connection/", ConnectionView.as_view(), name="connection_list"), # http://127.0.0.1:8000/publishings/
    path("paymentstripe/", PaymentStripeView.as_view(), name="payment_stripe"),
    path("webhook", StripeWebhookView.as_view(), name="success_payment"),


    # Client
    path('clients/create/', ClientCreateView.as_view(), name='clients_create'),
    path('clients/<int:pk>', ClientListView.as_view(), name='clients_list'),
    path('update/<int:pk>', ClientUpdateView.as_view(), name='clients_update'),
    path('delete/<int:pk>', ClientDeleteView.as_view(), name='clients_delete'),
    path('detail/<int:pk>', ClientDetailView.as_view(), name='detail'),



    # path("post/<int:post_id>", views.show_post, name="post"),

]