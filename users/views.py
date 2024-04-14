from django.conf import settings
from django.contrib import messages
from django.contrib.auth.views import LoginView as BaseLoginView
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, UpdateView

from config.settings import TWILIO_SECRET_SID, TWILIO_SECRET_TOKEN
from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm, PhoneAuthenticationForm
from users.models import User
from users.services import generate_verification_token
from twilio.rest import Client
import random
from django.contrib.auth import login, logout


class VerificationCodeSender:
    def __init__(self):
        self.account_sid = TWILIO_SECRET_SID
        self.auth_token = TWILIO_SECRET_TOKEN
        self.client = Client(self.account_sid, self.auth_token)

    def send_verification_code(self, phone_number):
        verification_code = ''.join([str(random.randint(0, 9)) for _ in range(4)])
        message = self.client.messages.create(
            body=f"Ваш код подтверждения: {verification_code}",
            from_='+12513206600',
            to=phone_number
        )
        return verification_code


class AuthenticatePhoneView(View):
    def get(self, request):
        form = PhoneAuthenticationForm()
        return render(request, 'users/authenticate_phone.html', {'form': form})

    def post(self, request):
        form = PhoneAuthenticationForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            verifier = VerificationCodeSender()
            verification_code = verifier.send_verification_code(phone_number)
            request.session['verification_code'] = verification_code
            request.session['phone_number'] = phone_number
            return redirect('/users/verifyphone')
        return render(request, 'users/authenticate_phone.html', {'form': form})


class VerifyPhoneView(View):
    def get(self, request):
        return render(request, 'users/verify_phone.html')

    def post(self, request):
        verification_code = request.POST.get('verification_code')
        stored_code = request.session.get('verification_code')
        phone_number = request.session.get('phone_number')
        if verification_code == stored_code:
            if User.objects.filter(phone=phone_number).exists():
                user = User.objects.get(phone=phone_number)
                login(request, user)
            return redirect('/users/profile/')  # Redirect to success page
        else:
            return redirect('/users/loginphone/')


class UserLoginView(BaseLoginView):
    model = User
    form_class = UserLoginForm
    template_name = 'users/login_form.html'
    success_url = reverse_lazy('home:index')

    def form_valid(self, form):
        user = form.get_user()

        if not user.is_active:
            messages.error(
                self.request,
                message='Ваша учетная запись не активирована. Пожалуйста, проверьте свою электронную почту.'
            )

        return super().form_valid(form)


class UserLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('/')


def user_registration_success(request):
    return render(request, template_name='users/registration_success.html')


def user_verification_view(request, pk, token):
    user = get_object_or_404(User, pk=pk, verification_token=token)
    user.is_active = True
    user.verification_token = None
    user.save()
    return redirect('users:login_phone')


class UserRegistrationCreateView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/registration_form.html'
    success_url = reverse_lazy('users:registration_success')

    def form_valid(self, form):
        new_user = form.save()
        verification_token = generate_verification_token()
        new_user.verification_token = verification_token
        new_user.is_active = True
        new_user.save()

        verification_url = self.request.build_absolute_uri(
            reverse(
                viewname='users:verification',
                args=[new_user.pk, verification_token])
        )

        send_mail(
            subject='Успешная регистрация на почтовом сервисе',
            message=f'Нажмите сюда, чтобы активировать свой профиль {verification_url}.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[new_user.email]
        )
        return super().form_valid(form)


class UserProfileUpdateView(UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile_form.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user
