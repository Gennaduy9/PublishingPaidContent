import json

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.http import JsonResponse
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

endpoint_secret = STRIPE_SECRET_API_KEY


class BaseView(TemplateView):
    template_name = 'publishings/category_list.html'
    extra_context = {
        'title': 'Главная страница',
        'title_blog': 'Наш блок',
    }

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['object_list'] = Profile.objects.all()
        subs = Subscription.objects.filter(user=self.request.user.id)
        id_sub = []
        for i in subs:
            id_sub.append(i.profile.id)
        context_data['id_sub'] = id_sub

        return context_data


class CategoryListView(LoginRequiredMixin, ListView):
    model = Subscription
    template_name = 'publishings/category_list.html'
    extra_context = {
        'title': 'Мои посты'
    }

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['object_list'] = Profile.objects.filter(user=self.request.user.id)

        return context_data


class ConnectionView(TemplateView):
    template_name = 'publishings/connection_list.html'
    extra_context = {
        'title': 'Обратная связь',
    }

    def post(self, request):
        name = self.request.POST.get('name')
        email = self.request.POST.get('email')
        message = self.request.POST.get('message')
        send_mail(
            subject='Обратная связь',
            message=f'Имя {name} Email {email} Сообщение {message}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=['myparents2@yandex.ru']
        )
        return redirect('/')


class ClientListView(ListView):
    model = Profile
    template_name = 'publishings/client_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(id=self.kwargs.get('pk'))

        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        client_id = self.kwargs.get('pk')
        client_item = Profile.objects.get(id=client_id)

        context['client_pk'] = client_id
        context['title'] = f'Наш клиент {client_item.full_name}'

        return context


class ClientDetailView(View):
    def get(self, request, pk):
        profile = Profile.objects.get(id=pk)
        return render(request, 'publishings/detail.html', context={'profile': profile})


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Profile
    form_class = ClientForm
    template_name = 'publishings/client_form.html'
    success_url = reverse_lazy('publishings:category_list')
    extra_context = {
        'title': 'Добавить статью',
    }

    def form_valid(self, form):
        self.object = form.save()
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class ClientUpdateView(UpdateView):
    model = Profile
    form_class = ClientForm
    template_name = 'publishings/client_form.html'
    success_url = reverse_lazy('publishings:category_list')
    permission_required = []

    def has_permission(self):
        client = self.get_object()
        if self.request.user == client.user:
            return super().has_permission()


class ClientDeleteView(DeleteView):
    model = Profile
    template_name = 'publishings/client_confirm_delete.html'
    success_url = reverse_lazy('publishings:category_list')
    permission_required = []

    def has_permission(self):
        email = self.get_object()
        if self.request.user == email.user:
            return super().has_permission()


class PaymentStripeView(View):
    def post(self, request):
        id_profile = request.POST['id_profile']
        url_stripe = get_session(id_profile, request.user.id)
        return redirect(url_stripe)


class StripeWebhookView(View):
    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def handle_checkout_session_completed(self, session):
        id_profile = session['metadata'].get('id_profile')
        id_user = session['metadata'].get('id_user')
        user_instance = User.objects.get(pk=id_user)
        profile_instance = Profile.objects.get(id=id_profile)
        s = Subscription()
        s.user = user_instance
        s.profile = profile_instance
        s.save()

    def post(self, request):
        payload = request.body.decode('utf-8')
        event = None
        try:
            event = json.loads(payload)
        except ValueError as e:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        if event['type'] == 'checkout.session.completed':
            self.handle_checkout_session_completed(event['data']['object'])

        return JsonResponse({'status': 'success'})

# def page_not_found(request, exception):
#     return HttpResponseNotFound("<h1>Страница не найдена</h1>")

# class PageNotFoundView(View):
#     def get(self, request, *args, **kwargs):
#         return HttpResponseNotFound("<h1>Страница не найдена</h1>")
