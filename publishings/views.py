import json

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from django.views.decorators.csrf import csrf_exempt

from config.settings import STRIPE_SECRET_API_KEY
from publishings.forms import ClientForm
from publishings.models import Profile, Subscription
from publishings.services import get_session
from users.models import User

# Устанавливаем секретный ключ Stripe API
endpoint_secret = STRIPE_SECRET_API_KEY


# Базовое представление, выводящее список статей авторов на главной странице
class BaseView(TemplateView):
    template_name = 'publishings/category_list.html'
    extra_context = {
        'title': 'Главная страница',
        'title_blog': 'Наш блок',
    }

    # делает выборку всех статей
    def get_context_data(self, **kwargs):
        # Получаем список всех статей
        context_data = super().get_context_data(**kwargs)
        context_data['object_list'] = Profile.objects.all()

        # Получаем подписки пользователя и формируем список идентификаторов
        subs = Subscription.objects.filter(user=self.request.user.id)
        id_sub = []
        for i in subs:
            id_sub.append(i.profile.id)
        context_data['id_sub'] = id_sub

        return context_data


# Представление для вывода списка статей авторов на странице профиля
class CategoryListView(LoginRequiredMixin, ListView):
    model = Subscription
    template_name = 'publishings/category_list.html'
    extra_context = {
        'title': 'Мои посты'
    }

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        # Получаем список статей автора
        context_data['object_list'] = Profile.objects.filter(user=self.request.user.id)

        return context_data


# Представление для обратной связи
class ConnectionView(TemplateView):
    # обратная связь
    template_name = 'publishings/connection_list.html'
    extra_context = {
        'title': 'Обратная связь',
    }

    def post(self, request):
        # Обрабатываем POST-запрос с данными формы обратной связи
        name = self.request.POST.get('name')
        email = self.request.POST.get('email')
        message = self.request.POST.get('message')
        send_mail(
            subject='Обратная связь',
            message=f'Имя {name} Email {email} Сообщение {message}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=settings.ADMIN_EMAIL
        )
        return redirect('/')


# Представление для детальной страницы статьи
class ClientDetailView(View):
    def get(self, request, pk):
        # Получаем и отображаем детальную информацию о статье
        profile = Profile.objects.get(id=pk)
        return render(request, 'publishings/detail.html', context={'profile': profile})


# Представление для создания новых статей
class ClientCreateView(LoginRequiredMixin, CreateView):
    # создание статей
    model = Profile
    form_class = ClientForm
    template_name = 'publishings/client_form.html'
    success_url = reverse_lazy('publishings:category_list')
    extra_context = {
        'title': 'Добавить статью',
    }

    def form_valid(self, form):
        # Сохраняем новую статью и привязываем её к текущему пользователю
        self.object = form.save()
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


# Представление для обновления существующих статей
class ClientUpdateView(UpdateView):
    # обновление статей
    model = Profile
    form_class = ClientForm
    template_name = 'publishings/client_form.html'
    success_url = reverse_lazy('publishings:category_list')
    permission_required = []

    def has_permission(self):
        # Проверяем разрешение на обновление статьи
        client = self.get_object()
        if self.request.user == client.user:
            return super().has_permission()


# Представление для удаления статей
class ClientDeleteView(DeleteView):
    model = Profile
    template_name = 'publishings/client_confirm_delete.html'
    success_url = reverse_lazy('publishings:category_list')
    permission_required = []

    def has_permission(self):
        # Проверяем разрешение на удаление статьи
        email = self.get_object()
        if self.request.user == email.user:
            return super().has_permission()


# Представление для обработки платежей через Stripe
class PaymentStripeView(View):
    def post(self, request):
        # Обрабатываем POST-запрос для создания сессии оплаты через Stripe
        id_profile = request.POST['id_profile']
        url_stripe = get_session(id_profile, request.user.id)
        return redirect(url_stripe)


# Представление для обработки событий от Stripe Webhook
class StripeWebhookView(View):
    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def handle_checkout_session_completed(self, session):
        # Обрабатываем событие завершения оплаты
        id_profile = session['metadata'].get('id_profile')
        id_user = session['metadata'].get('id_user')
        user_instance = User.objects.get(pk=id_user)
        profile_instance = Profile.objects.get(id=id_profile)
        s = Subscription()
        s.user = user_instance
        s.profile = profile_instance
        s.save()

    def post(self, request):
        # Обрабатываем POST-запрос от Stripe Webhook
        payload = request.body.decode('utf-8')
        event = None
        try:
            event = json.loads(payload)
        except ValueError as e:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        if event['type'] == 'checkout.session.completed':
            self.handle_checkout_session_completed(event['data']['object'])

        return JsonResponse({'status': 'success'})


class PageNotFoundView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponseNotFound("<h1>Страница не найдена</h1>")
