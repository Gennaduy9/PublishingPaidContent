from django.urls import path

from users.apps import UsersConfig
from users.views import UserLoginView, UserLogoutView, UserRegistrationCreateView, user_registration_success, \
    user_verification_view, UserProfileUpdateView, AuthenticatePhoneView, VerifyPhoneView

app_name = UsersConfig.name

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('loginphone/', AuthenticatePhoneView.as_view(), name='login_phone'),
    path('verifyphone/', VerifyPhoneView.as_view(), name='verify_phone'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('registration/', UserRegistrationCreateView.as_view(), name='registration'),
    path('registration_success/', user_registration_success, name='registration_success'),
    path('verification/<int:pk>/<str:token>/', user_verification_view, name='verification'),
    path('profile/', UserProfileUpdateView.as_view(), name='profile'),
]
