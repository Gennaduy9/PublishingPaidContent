from django.urls import path
from publishings.apps import PublishingsConfig
from .views import BaseView, CategoryListView, ConnectionView, ClientCreateView, ClientUpdateView, \
    ClientDeleteView, ClientDetailView, PaymentStripeView, StripeWebhookView

app_name = PublishingsConfig.name

urlpatterns = [
    path("", BaseView.as_view(), name="home"),
    path('categorys/', CategoryListView.as_view(), name='category_list'),
    path("connection/", ConnectionView.as_view(), name="connection_list"),
    path("paymentstripe/", PaymentStripeView.as_view(), name="payment_stripe"),
    path("webhook", StripeWebhookView.as_view(), name="success_payment"),

    # Client
    path('clients/create/', ClientCreateView.as_view(), name='clients_create'),
    path('update/<int:pk>', ClientUpdateView.as_view(), name='clients_update'),
    path('delete/<int:pk>', ClientDeleteView.as_view(), name='clients_delete'),
    path('detail/<int:pk>', ClientDetailView.as_view(), name='detail'),

    # path("post/<int:post_id>", views.show_post, name="post"),

]
